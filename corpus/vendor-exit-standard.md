# Vendor Exit and Offboarding Standard

Doc ID: EXIT-PLN
Version: 2.0
Owner: TPRM Office
Effective: 2026-02-01
Status: Current

## 1. Purpose

Every relationship ends. This standard ensures that when one does, whether planned or forced, Northwind gets its data back, removes the vendor's access promptly, and keeps its services running. It implements TPR-POL §4.5.

## 2. Exit Plans

2.1 An exit plan is required for every Tier 1 and Tier 2 vendor. It is drafted by the Vendor Manager during onboarding and attached to the contract as a schedule before signature (ONB-PRC Step 5).

2.2 The exit plan must cover two scenarios:

- **Planned exit** — non-renewal or termination for convenience, with a transition period agreed in the contract.
- **Stressed exit** — the vendor fails suddenly through insolvency, a sanctions designation, a severe security incident, or a regulatory order. The plan must state how the service is maintained with no transition assistance from the vendor.

2.3 Each plan names the replacement option (alternate vendor, in-house capability, or orderly service discontinuation), the data to be returned and its format, the estimated transition time, and the cost estimate.

2.4 Tier 1 exit plans are tested by tabletop exercise every 24 months and reviewed at each annual reassessment. Tier 2 exit plans are reviewed at each reassessment.

## 3. Contract Requirements

Tier 1 and Tier 2 contracts must require the vendor to:

- provide transition assistance for at least 6 months after notice of termination, at the rates in force;
- return Northwind data in an agreed, non-proprietary, machine-readable format;
- securely destroy all remaining copies after return, including backups, and certify destruction;
- continue to meet INCN-SLA and BCP-REQ obligations during the transition period.

## 4. Offboarding Steps

Once a termination or non-renewal date is set, the Vendor Manager opens an offboarding case in ProcureNet and completes the following.

### 4.1 Access Revocation

All vendor accounts, VPN tokens, API keys, and physical badges are revoked within 24 hours of the termination effective date. Revocation follows ACC-STD §6. Shared secrets known to the vendor are rotated within the same 24 hours.

### 4.2 Data Return and Destruction

The vendor must return Northwind data and deliver a signed certificate of data destruction within 30 days of the termination effective date. The certificate must identify the data sets, the destruction method, the date, and the vendor officer signing. Where the vendor used subcontractors, the certificate must cover subcontractor copies too (FRTH-POL). The TPRM Office escalates any certificate not received within 30 days to Legal.

### 4.3 Financial Close

Accounts Payable settles the final invoice only after the destruction certificate is received for Tier 1 and Tier 2 vendors. Procurement deactivates the vendor master record after final payment.

### 4.4 Records

The exit file, including the destruction certificate, is retained under RET-SCH.

## 5. Stressed Exit Triggers

The TPRM Office must assess whether to invoke the stressed exit plan when any of these occur: a confirmed sanctions match (SANC-PRC), a financial watch-list rating of Red (FIN-STD), a breach of a Tier 1 RTO during a real incident (BCP-REQ), or a regulator instruction. The decision is made by the Business Owner and the Head of Third-Party Risk Management within 5 business days and reported to the TPRC.
