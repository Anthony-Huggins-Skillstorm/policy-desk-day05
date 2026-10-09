// Target deployment for policy-desk: a container app that calls a Foundry project keylessly
// and writes audit records to blob storage. Describes the intended production shape.

@description('Short environment name, used as a suffix on every resource.')
@allowed(['dev', 'test', 'prod'])
param env string = 'dev'

param location string = resourceGroup().location

@description('Container image for the policy-desk API.')
param image string = 'northwindacr.azurecr.io/policy-desk:0.4.0'

var suffix = '${env}-${uniqueString(resourceGroup().id)}'
var openAiUserRole = '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd' // Cognitive Services OpenAI User
var blobContributorRole = 'ba92f5b4-2d11-453d-a403-e96b0029c9fe' // Storage Blob Data Contributor

resource foundry 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: 'nwc-foundry-${suffix}'
  location: location
  kind: 'AIServices'
  sku: { name: 'S0' }
  identity: { type: 'SystemAssigned' }
  properties: {
    customSubDomainName: 'nwc-foundry-${suffix}'
    allowProjectManagement: true
    disableLocalAuth: true
    publicNetworkAccess: 'Enabled'
  }
}

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = {
  parent: foundry
  name: 'policy-desk'
  location: location
  identity: { type: 'SystemAssigned' }
  properties: {}
}

resource chatModel 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: foundry
  name: 'gpt-5-mini'
  sku: { name: 'GlobalStandard', capacity: 50 }
  properties: {
    model: { format: 'OpenAI', name: 'gpt-5-mini', version: '2025-08-07' }
  }
}

resource embeddingModel 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: foundry
  name: 'text-embedding-3-small'
  sku: { name: 'Standard', capacity: 50 }
  properties: {
    model: { format: 'OpenAI', name: 'text-embedding-3-small', version: '1' }
  }
  dependsOn: [chatModel]
}

resource logs 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'nwc-logs-${suffix}'
  location: location
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 90
  }
}

resource auditStore 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: take('nwcaudit${uniqueString(resourceGroup().id, env)}', 24)
  location: location
  kind: 'StorageV2'
  sku: { name: 'Standard_ZRS' }
  properties: {
    allowSharedKeyAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

resource appEnv 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: 'nwc-cae-${suffix}'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logs.properties.customerId
        sharedKey: logs.listKeys().primarySharedKey
      }
    }
  }
}

resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'policy-desk-${env}'
  location: location
  identity: { type: 'SystemAssigned' }
  properties: {
    managedEnvironmentId: appEnv.id
    configuration: {
      ingress: { external: false, targetPort: 8000 }
    }
    template: {
      containers: [
        {
          name: 'policy-desk'
          image: image
          resources: { cpu: json('0.5'), memory: '1Gi' }
          env: [
            { name: 'PROJECT_ENDPOINT', value: '${foundry.properties.endpoint}api/projects/${project.name}' }
            { name: 'MODEL_DEPLOYMENT', value: chatModel.name }
            { name: 'AOAI_ENDPOINT', value: 'https://${foundry.properties.customSubDomainName}.openai.azure.com' }
            { name: 'EMBEDDING_DEPLOYMENT', value: embeddingModel.name }
            { name: 'AUDIT_BLOB_ENDPOINT', value: auditStore.properties.primaryEndpoints.blob }
          ]
        }
      ]
      scale: { minReplicas: 1, maxReplicas: 3 }
    }
  }
}

resource appCanCallModels 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(foundry.id, app.id, openAiUserRole)
  scope: foundry
  properties: {
    principalId: app.identity.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', openAiUserRole)
  }
}

resource appCanWriteAudit 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(auditStore.id, app.id, blobContributorRole)
  scope: auditStore
  properties: {
    principalId: app.identity.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', blobContributorRole)
  }
}

output appName string = app.name
output projectEndpoint string = '${foundry.properties.endpoint}api/projects/${project.name}'
