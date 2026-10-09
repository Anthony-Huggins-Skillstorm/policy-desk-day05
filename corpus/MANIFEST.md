# Policy Desk Corpus Manifest

This corpus is synthetic. Northwind Capital Group is a fictional financial-services firm, and every policy, threshold, role, system name (such as ProcureNet), and email address in these documents was invented for training. The 23 documents model the Third-Party Risk Management (TPRM) and Procurement policy set an employee who engages vendors would search. The corpus exists to exercise retrieval, grounding, and citation behaviour in a policy question-answering assistant, and it is paired with `../eval/golden-questions.json`. Do not treat any requirement here as real guidance.

| Doc ID | File | Title | Status | Words |
|---|---|---|---|---|
| TPR-POL | third-party-risk-policy.md | Third-Party Risk Management Policy | Current | 581 |
| TIER-MTX | vendor-tiering-matrix.md | Vendor Risk Tiering Matrix | Current | 550 |
| DUE-STD | due-diligence-standard.md | Vendor Due Diligence Standard | Current | 486 |
| DUE-OLD | due-diligence-standard-v2.md | Vendor Due Diligence Standard | SUPERSEDED by DUE-STD | 389 |
| ONB-PRC | vendor-onboarding-procedure.md | Vendor Onboarding Procedure | Current | 490 |
| RNW-PRC | contract-renewal-procedure.md | Contract Renewal Procedure | Current | 527 |
| EXIT-PLN | vendor-exit-standard.md | Vendor Exit and Offboarding Standard | Current | 541 |
| DPA-REQ | data-processing-agreement-requirements.md | Data Processing Agreement Requirements | Current | 526 |
| SANC-PRC | sanctions-screening-procedure.md | Sanctions and Adverse Media Screening Procedure | Current | 481 |
| CONC-STD | concentration-risk-standard.md | Concentration Risk Standard | Current | 471 |
| AUDT-GDE | right-to-audit-guide.md | Right-to-Audit Clause Guide | Current | 481 |
| FRTH-POL | fourth-party-policy.md | Fourth-Party (Subcontractor) Policy | Current | 482 |
| INCN-SLA | vendor-incident-notification-sla.md | Vendor Incident Notification SLA Schedule | Current | 573 |
| RET-SCH | tprm-records-retention-schedule.md | TPRM Records Retention Schedule | Current | 609 |
| CLD-STD | cloud-provider-assessment-standard.md | Cloud Service Provider Assessment Standard | Current | 519 |
| FIN-STD | vendor-financial-health-standard.md | Vendor Financial Health Review Standard | Current | 508 |
| BCP-REQ | vendor-continuity-requirements.md | Vendor Business Continuity and Resilience Requirements | Current | 532 |
| PRC-POL | procurement-policy.md | Procurement Policy | Current | 497 |
| EXC-PRC | tprm-exception-procedure.md | Third-Party Risk Exception Procedure | Current | 536 |
| PERF-STD | vendor-performance-monitoring-standard.md | Vendor Performance Monitoring Standard | Current | 498 |
| ACC-STD | vendor-access-standard.md | Vendor Access Management Standard | Current | 603 |
| GIFT-POL | vendor-gifts-conflicts-policy.md | Gifts, Entertainment and Vendor Conflicts of Interest Policy | Current | 544 |
| AIV-STD | ai-vendor-assessment-addendum.md | AI Vendor Assessment Addendum | Current | 592 |

Total: 23 documents, 12016 words. Word counts are whitespace-delimited tokens over the full file, including the metadata block.

## Retrieval properties

The corpus contains deliberate traps. Each one is there to catch a specific retrieval or grounding failure.

- **Superseded document.** DUE-OLD (Vendor Due Diligence Standard v2.1) is marked `Status: SUPERSEDED by DUE-STD` and contradicts the current standard: Tier 1 reassessment every 24 months instead of 12, SOC 2 Type I accepted, SOC 2 reports up to 18 months old, diligence valid for 180 days instead of 90, and contracts allowed to be signed before diligence completes. It shares a title with DUE-STD and is lexically very similar, so naive similarity search will often rank it highly. An assistant should cite DUE-STD unless the user explicitly asks about v2.1.
- **Table-heavy documents.** TIER-MTX, INCN-SLA, RET-SCH, and BCP-REQ carry their key facts in markdown tables. Chunkers that split tables mid-row or drop the header row lose the meaning of a cell such as `24 hours`. RNW-PRC, ONB-PRC, PRC-POL, PERF-STD, EXC-PRC, and DUE-OLD also contain smaller tables.
- **Cross-references.** Most documents cite others by doc_id and section (for example `DUE-STD §4.2`, `EXIT-PLN §4.1`, `TIER-MTX §3`). Multi-hop questions need both the citing and the cited document.
- **Missing owner.** FRTH-POL omits the `Owner:` line from its metadata block. Parsers must not assume every field is present.
- **Mixed date formats.** `Effective:` dates appear as ISO (`2026-03-01`), day-month-year (`1 February 2026`), US numeric (`03/15/2026`), and month-day-year (`September 1, 2025`). US numeric dates are ambiguous with day-first formats.
- **Mixed 3- and 4-letter doc_id prefixes.** IDs such as `DUE-STD` and `PRC-POL` sit alongside `TIER-MTX`, `EXIT-PLN`, `SANC-PRC`, `CONC-STD`, `AUDT-GDE`, `FRTH-POL`, `INCN-SLA`, `PERF-STD`, and `GIFT-POL`. Anything that parses doc ids must not assume a fixed segment length.
- **Inconsistent heading styles.** Documents use `## 1. Purpose`, `## Section 1 — Purpose`, `## 1 Purpose`, `## Step 1: Intake`, and unnumbered headings. GIFT-POL uses bold pseudo-headings (`**Purpose.**`) and no markdown headings below the title, so heading-based chunking produces a single chunk.
- **Long numbered list.** ACC-STD section 4 is a 14-item numbered requirements list, which tests whether a chunker keeps list items with their section context.
- **Near-duplicate numbers.** Several figures recur with different meanings: `24 hours` (breach notice, access revocation, Tier 2 RTO), `30 days` (destruction certificate, sub-processor notice, raw AI log retention), and `12 months` (Tier 1 reassessment, report age, key rotation). Grounding checks must verify the figure's context and not just its presence.
