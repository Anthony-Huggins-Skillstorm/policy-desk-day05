# Cloud Service Provider Assessment Standard

Doc ID: CLD-STD
Version: 2.0
Owner: CISO Office — Cloud Security
Effective: 12 January 2026
Status: Current

## 1. Purpose

Cloud service providers (CSPs) change the shape of third-party risk. Northwind shares responsibility for security with the provider, data may move across regions, and many vendors depend on the same few platforms. This standard adds cloud-specific requirements on top of DUE-STD. It applies to infrastructure, platform, and software-as-a-service providers that store or process Northwind data.

## 2. Tiering

A CSP that hosts Restricted data or supports a critical business service is Tier 1 under TIER-MTX regardless of spend. A SaaS provider hosted on a CSP is assessed as a vendor in its own right; its CSP is a fourth party (FRTH-POL).

## 3. Assurance

3.1 Tier 1 and Tier 2 CSPs provide a SOC 2 Type II report meeting DUE-STD §4.2. CSA STAR Level 2 certification is accepted as an alternative for Tier 2 CSPs with CISO office approval.

3.2 The CSP must publish, or provide under NDA, a shared responsibility matrix. The CISO office maps every control in the matrix marked as a customer responsibility to a Northwind control owner before go-live.

## 4. Data Location

4.1 Northwind data may be stored only in the approved regions: United States, European Union, and United Kingdom.

4.2 Storing data, or replicating backups, in any other region requires approval from the CISO office and Legal, and a DPA amendment where personal data is involved (DPA-REQ §3).

4.3 The CSP contract must require at least 90 days' notice of any change to the regions in which Northwind data is stored.

## 5. Encryption and Keys

5.1 All Northwind data must be encrypted in transit with TLS 1.2 or higher and at rest with AES-256 or equivalent.

5.2 Restricted data must be encrypted with customer-managed keys held in a Northwind-controlled key management service or hardware security module. The CSP must not have the ability to access customer-managed keys in plaintext.

5.3 Customer-managed keys are rotated at least every 12 months.

## 6. Identity and Logging

Administrative access to Northwind tenants uses Northwind's identity provider with MFA (ACC-STD). The CSP must make audit logs for Northwind tenants available for export to Northwind's security monitoring platform, with at least 12 months of log history retrievable.

## 7. Resilience and Portability

7.1 Tier 1 workloads must be deployed across at least two availability zones, and the design must meet the RTO and RPO for the vendor's tier in BCP-REQ.

7.2 The exit plan (EXIT-PLN) must show that data can be exported in a non-proprietary format and describe how workloads would be rebuilt on an alternative platform.

## 8. Concentration

Every new Tier 1 CSP engagement and every new workload on an existing CSP that supports a critical business service is checked against CONC-STD thresholds, in particular threshold 4 (a single fourth party supporting more than 5 Tier 1 vendors).

## 9. Reassessment

CSPs are reassessed on their tier's frequency under TIER-MTX §3. The CISO office also reviews the CSP's published security bulletins monthly and records any that affect Northwind services.
