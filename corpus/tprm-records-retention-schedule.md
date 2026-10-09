# TPRM Records Retention Schedule

Doc ID: RET-SCH
Version: 1.8
Owner: Records Management Office
Effective: 2026-04-01
Status: Current

## 1. Purpose

This schedule sets how long Third-Party Risk Management and Procurement records are kept and when they must be destroyed. Keeping records too short a time breaches regulatory record-keeping rules; keeping them too long breaches data minimization obligations and increases breach exposure. Both are violations.

## 2. Retention Periods

| Record type | Retention period | Trigger | Disposal |
|---|---|---|---|
| Due diligence files (DUE-STD), including questionnaires and assurance reports | 7 years | End of the vendor relationship | Secure deletion |
| Executed contracts, amendments, and DPAs | 7 years | Contract termination or expiry | Secure deletion |
| Renewal risk reviews (RNW-PRC) | 7 years | Contract termination or expiry | Secure deletion |
| Sanctions and adverse media screening results and alert dispositions (SANC-PRC) | 5 years | End of the vendor relationship | Secure deletion |
| Vendor incident records (INCN-SLA) | 7 years | Incident closure | Secure deletion |
| Data destruction and exit certificates (EXIT-PLN) | 10 years | Date of certificate | Secure deletion |
| Exception records (EXC-PRC) | 7 years | Exception expiry or closure | Secure deletion |
| Performance scorecards and QBR minutes (PERF-STD) | 3 years | Date of scorecard | Secure deletion |
| Gifts and entertainment register entries (GIFT-POL) | 5 years | Date of entry | Secure deletion |
| Vendor access recertification evidence (ACC-STD) | 3 years | Date of recertification | Secure deletion |
| Internal AI assistant interaction logs | 13 months | Date of interaction | Automatic deletion |
| Unsuccessful bid submissions (PRC-POL) | 3 years | Award date | Secure deletion |

## 3. Internal AI Assistant Interaction Logs

Northwind employees use internal AI assistants to search and summarize TPRM policies and vendor files. Logs of these interactions are records under this schedule and are subject to the following rules:

3.1 Raw user prompts and raw assistant responses that contain personal data must not be stored for more than 30 days. The 30-day limit applies to all storage locations, including application logs, observability and tracing platforms, and debugging exports.

3.2 After 30 days, interaction logs may be kept only in summarized or hashed form. Summarized form means a record of the interaction metadata (timestamp, user identifier, documents retrieved, response latency, and evaluation scores) with personal data removed. Hashed form means prompts replaced by a one-way hash sufficient to detect duplicates but not to reconstruct the text.

3.3 Summarized or hashed logs are retained for up to 13 months from the date of interaction and then deleted automatically.

3.4 Logs subject to a legal hold are exempt from 3.1 to 3.3 for the duration of the hold, under the control of Legal.

3.5 System owners must document how their assistant meets 3.1 to 3.3 before production launch. The Records Management Office reviews this documentation annually.

## 4. Legal Holds

A legal hold issued by Legal suspends destruction of any affected record, regardless of the periods above. Records under hold are released for disposal only on written notice from Legal.

## 5. Format and Location

Records are held in the ProcureNet document repository or another system approved by the Records Management Office. Records held in personal drives, email folders, or chat channels do not satisfy this schedule and must be moved to an approved system within 30 days of creation.

## 6. Disposal Evidence

Each quarterly disposal run produces a disposal log listing record types and counts destroyed. Disposal logs are themselves retained for 7 years.
