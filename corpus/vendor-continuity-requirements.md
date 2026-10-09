# Vendor Business Continuity and Resilience Requirements

Doc ID: BCP-REQ
Version: 3.0
Owner: Operational Resilience Office
Effective: 03/01/2026
Status: Current

## Section 1 — Purpose

Northwind's own recovery commitments to clients and regulators are only as strong as the vendors behind them. This document sets the minimum business continuity and disaster recovery requirements vendors must meet, by tier.

## Section 2 — Recovery Objectives

The recovery time objective (RTO) is the maximum time from service disruption to restoration. The recovery point objective (RPO) is the maximum period of data loss measured back from the moment of disruption.

| Tier | RTO | RPO | Plan testing | Test results to Northwind |
|---|---|---|---|---|
| Tier 1 | 4 hours | 15 minutes | Annually, full failover test | Within 30 days of the test |
| Tier 2 | 24 hours | 4 hours | Every 24 months | Within 30 days of the test |
| Tier 3 | 72 hours | 24 hours | Self-attestation at reassessment | On request |
| Tier 4 | Best effort | Best effort | Not required | Not required |

Where a vendor supports a critical business service with a stricter impact tolerance in the Business Impact Register, the stricter value applies and must be written into the contract.

## Section 3 — Plan Content

Tier 1 and Tier 2 vendors must maintain a documented business continuity plan and disaster recovery plan that address, at minimum:

- loss of a primary facility;
- loss of a primary data center or cloud region;
- loss of key personnel, including pandemic-level absence of up to 40% of staff;
- loss of a material subcontractor (FRTH-POL);
- a cyberattack, including ransomware, that renders production systems unavailable.

## Section 4 — Recovery Sites

Tier 1 vendors must operate a recovery site, or a cloud region, at least 100 miles from the primary site and not dependent on the same power grid. Cloud-hosted Tier 1 services must also meet the multi-availability-zone requirement in CLD-STD §7.1.

## Section 5 — Testing

5.1 Tier 1 vendors perform a full failover test annually. Tabletop exercises do not satisfy this requirement.

5.2 Test reports must show the RTO and RPO actually achieved, issues found, and remediation dates.

5.3 Northwind may participate in or observe any test. For Tier 1 vendors supporting a critical business service, the Operational Resilience Office joins at least one test every 24 months.

5.4 A test that fails to meet the RTO or RPO is treated as a High finding under DUE-STD §6.

## Section 6 — Real Incidents

Service disruptions must be notified under INCN-SLA. A Tier 1 vendor that exceeds its RTO during a real incident triggers a stressed exit assessment under EXIT-PLN §5 and a review by the TPRC.

## Section 7 — Ransomware Resilience

Tier 1 and Tier 2 vendors must keep immutable or offline backups of Northwind data, isolated from production credentials, and must test restoration from those backups at least annually.

## Section 8 — Evidence at Reassessment

At each reassessment the vendor provides its current plans, the latest test report, and confirmation that remediation items from the prior test are closed.
