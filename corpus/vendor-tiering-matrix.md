# Vendor Risk Tiering Matrix

Doc ID: TIER-MTX
Version: 3.2
Owner: TPRM Office
Effective: 1 February 2026
Status: Current

## Section 1 — Purpose

The tier drives everything downstream: diligence depth, contract clauses, reassessment frequency, incident deadlines, and continuity targets. The TPRM Office assigns the tier at intake (TPR-POL §4.1) and confirms it after due diligence. A vendor takes the highest tier triggered by any single criterion.

## Section 2 — Tier Criteria

| Criterion | Tier 1 (Critical) | Tier 2 (High) | Tier 3 (Moderate) | Tier 4 (Low) |
|---|---|---|---|---|
| Data access | Restricted data, or personal data on more than 100,000 individuals | Confidential data, or personal data on 100,000 individuals or fewer | Internal data only | No Northwind data |
| Service criticality | Supports a critical business service | Supports an important business service | Supports a non-critical internal function | Commodity goods or services |
| Annual spend | More than $1,000,000 | $250,000 to $1,000,000 | $50,000 to $249,999 | Under $50,000 |
| System connectivity | Persistent connection or privileged access | Named-user access to production | Named-user access to non-production | None |

Critical business services are those listed in the Northwind Business Impact Register, including payments processing, trade settlement, client onboarding, and regulatory reporting.

## Section 3 — Reassessment Frequency

| Tier | Full reassessment | Sanctions rescreening | Financial review | Performance review |
|---|---|---|---|---|
| Tier 1 | Every 12 months | Daily (automated) | Annually | Quarterly business review |
| Tier 2 | Every 24 months | Daily (automated) | Every 24 months | Semi-annual |
| Tier 3 | Every 36 months | Daily (automated) | Not required | Annual |
| Tier 4 | At renewal only | Daily (automated) | Not required | Not required |

A reassessment is also triggered early by a material change: a security incident, a change of control, a new data type, or a new material subcontractor (FRTH-POL).

## Section 4 — Required Assessments by Tier

| Assessment | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---|---|---|---|
| Northwind Security Questionnaire (NSQ) | Full | Full | Lite | Not required |
| SOC 2 Type II or approved equivalent | Required | Required | Not required | Not required |
| Financial health review (FIN-STD) | Required | Required | Not required | Not required |
| Business continuity evidence (BCP-REQ) | Required, tested annually | Required, tested every 24 months | Self-attestation | Not required |
| Exit plan (EXIT-PLN) | Required | Required | Not required | Not required |
| Right-to-audit clause (AUDT-GDE) | Required | Required | Recommended | Not required |
| Onsite or virtual assessment | At CISO discretion | Not required | Not required | Not required |
| Sanctions and adverse media (SANC-PRC) | Required | Required | Sanctions only | Sanctions only |

## Section 5 — Overrides

The TPRM Office may raise a tier on judgment but may not lower a tier below what the criteria produce. A request to lower a tier is an exception under EXC-PRC. Vendors supplying AI or machine-learning services are subject to the minimum tier rules in AIV-STD, and cloud service providers to CLD-STD.
