# Vendor Incident Notification SLA Schedule

Doc ID: INCN-SLA
Version: 2.3
Owner: CISO Office — Third-Party Security
Effective: 1 April 2026
Status: Current

## 1. Purpose and Use

This schedule sets the maximum time a vendor has to notify Northwind of an incident. It is incorporated by reference into every vendor contract and every DPA (DPA-REQ clause 6). Legal must not agree longer deadlines without an approved exception under EXC-PRC. Shorter deadlines are always acceptable.

The clock starts when the vendor, or any of its subcontractors (FRTH-POL §7), becomes aware of the incident, not when its investigation concludes.

## 2. Notification Deadlines

| Incident type | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---|---|---|---|
| Outage of a service supporting a critical business service | 1 hour | 4 hours | Next business day | Not applicable |
| Ransomware or destructive malware on systems that store or process Northwind data | 4 hours | 8 hours | 24 hours | 48 hours |
| Confirmed personal-data breach involving Northwind data | 24 hours | 48 hours | 72 hours | 72 hours |
| Unauthorized access to Northwind data, not yet confirmed as a breach | 24 hours | 48 hours | 72 hours | 72 hours |
| Incident at a material subcontractor affecting Northwind data or services | 24 hours | 48 hours | 72 hours | Not applicable |
| Harmful or materially incorrect output from an AI service used by Northwind (AIV-STD) | 72 hours | 72 hours | 72 hours | 72 hours |
| Regulatory inquiry or enforcement action concerning the contracted services | 5 business days | 5 business days | 10 business days | Not applicable |
| Change of control, or financial distress event (FIN-STD §5) | 10 business days | 10 business days | 30 days | Not applicable |

"Hours" are clock hours, including weekends and public holidays.

## 3. Notification Content

The initial notification must include, to the extent known: a description of the incident; the time it occurred and the time it was discovered; the Northwind data and services affected; the containment actions taken; and a named vendor contact available around the clock. Missing information must not delay the initial notification.

## 4. Follow-Up Reporting

| Report | Deadline |
|---|---|
| Status updates during an active Tier 1 incident | Every 4 hours, or as agreed with the CISO office |
| Status updates during an active Tier 2 incident | Every 24 hours |
| Written root-cause analysis | 10 business days after containment |
| Remediation plan for root-cause findings | 20 business days after containment |

## 5. Notification Channels

Vendors notify through both channels:

- the vendor incident mailbox, vendor-incidents@northwindcg.example, and
- the TPRM Office incident hotline, staffed around the clock.

For Tier 1 outages, the vendor must also call the named Northwind service owner. Notification to a Vendor Manager's personal mailbox alone does not satisfy this schedule.

## 6. Northwind Actions on Receipt

The CISO office opens a third-party incident record within 1 hour of receiving a Tier 1 or Tier 2 notification. Where personal data is involved, the Privacy Office is engaged immediately to assess Northwind's own regulatory notification obligations. Missed vendor deadlines are recorded on the vendor's performance scorecard (PERF-STD) and considered at renewal (RNW-PRC Section 3).

## 7. Records

Incident records are retained under RET-SCH.
