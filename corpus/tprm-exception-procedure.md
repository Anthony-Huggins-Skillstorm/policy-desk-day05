# Third-Party Risk Exception Procedure

Doc ID: EXC-PRC
Version: 2.1
Owner: TPRM Office
Effective: 20 February 2026
Status: Current

## 1. Purpose

Sometimes a requirement cannot be met on time: a vendor's SOC 2 Type II report is three months late, or a contract cannot be renegotiated before a critical go-live. An exception is a time-bound, approved acceptance of that gap with compensating controls. It is not a waiver, and it is never permanent.

## 2. What Can and Cannot Be Excepted

Any requirement in a TPRM standard or procedure may be excepted except:

- proceeding with a vendor that is a confirmed sanctions true match (SANC-PRC §6.5);
- sharing personal data without an executed DPA (DPA-REQ §1);
- removing regulator access rights from a contract (AUDT-GDE §3.3);
- retroactive approval of a gap that already caused a policy breach. A retroactive request is recorded as a breach under TPR-POL §6 and may then be excepted going forward.

## 3. Requesting an Exception

The Business Owner submits an exception request in ProcureNet. The request must include:

1. the requirement not met, with the doc_id and section reference;
2. the reason it cannot be met;
3. the risk created, assessed by the TPRM Office as Critical, High, Medium, or Low;
4. compensating controls, with owners and dates;
5. the remediation plan that will close the gap;
6. the requested duration.

Requests without compensating controls are returned unreviewed.

## 4. Approval Authority

| Vendor tier | Approver |
|---|---|
| Tier 3 and Tier 4 | Head of Third-Party Risk Management |
| Tier 2 | Head of Third-Party Risk Management, plus the CISO for any security-related exception |
| Tier 1 | Chief Risk Officer, after recommendation by the Head of Third-Party Risk Management |

Any exception rated Critical risk requires Chief Risk Officer approval regardless of tier. The approver may not be in the reporting line of the Business Owner requesting the exception.

## 5. Duration

5.1 The maximum duration of an exception is 180 days.

5.2 An exception may be extended once, for up to 90 days, by the original approval authority, only if the remediation plan has made documented progress.

5.3 A need beyond 270 days in total must be escalated to the TPRC, which may require the Business Owner to exit the vendor (EXIT-PLN) or formally accept the risk on behalf of the business unit.

## 6. Compensating Controls

Compensating controls must reduce the specific risk the gap creates. Examples:

- a late SOC 2 Type II report covered by a bridge letter plus a CISO office review of the vendor's key controls;
- a missing right-to-audit clause covered by quarterly attestation and an on-site visit before renewal;
- a lapsed reassessment covered by a focused review of changes since the last assessment.

Monitoring that only means "the Vendor Manager will keep an eye on it" is not a compensating control.

## 7. Register and Reporting

The TPRM Office maintains the exceptions register. Open exceptions are reported monthly to the TPRC, with any exception due to expire within 30 days highlighted. On expiry, the exception closes automatically; if the gap remains, the TPRM Office records a breach. Exception records are retained under RET-SCH.
