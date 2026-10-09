# Vendor Access Management Standard

Doc ID: ACC-STD
Version: 2.6
Owner: CISO Office — Identity and Access Management
Effective: 8 December 2025
Status: Current

## 1. Purpose

Vendor personnel with access to Northwind systems are a common route for attackers. This standard sets the rules for granting, using, reviewing, and removing vendor access.

## 2. Scope

All logical access by vendor personnel and vendor systems to Northwind networks, applications, data, and cloud tenants, and all physical access to Northwind premises by vendor personnel.

## 3. Preconditions

Access may be requested only for a vendor that is active under ONB-PRC Step 7, and only by the Vendor Manager or the Business Owner. Access for a vendor with an expired contract is refused.

## 4. Requirements

1. Every vendor user has a named account tied to one identified individual. Shared, generic, or team accounts are prohibited.
2. Vendor accounts use the "v-" prefix and are created in the dedicated vendor directory, separate from employee accounts.
3. Multi-factor authentication is required for all vendor access, without exception, including access from vendor premises.
4. Remote access is permitted only through the Northwind vendor access gateway. Direct VPN connections from vendor networks require CISO office approval.
5. Access is granted on least privilege, limited to the systems and data named in the access request.
6. Every vendor account has an expiry date no later than 12 months from creation or the contract end date, whichever is earlier.
7. Privileged access is granted only through the privileged access management (PAM) system, is time-limited to the approved change window, and is session-recorded.
8. Session recordings for privileged vendor sessions are retained for 12 months.
9. Service accounts used by vendor systems are owned by a named Northwind employee, use vaulted credentials, and have credentials rotated at least every 90 days.
10. API keys issued to vendors are scoped to the minimum required endpoints and rotated at least every 90 days.
11. Accounts inactive for 30 days are disabled automatically.
12. Vendor personnel must complete Northwind security awareness training before access is enabled and annually thereafter.
13. Vendor access to production data from outside the approved regions in CLD-STD §4.1 requires CISO office and Legal approval.
14. Physical badges for vendor personnel are issued for no more than 90 days at a time and are returned on the last day on site.

## 5. Quarterly Recertification

The Vendor Manager recertifies every vendor account quarterly. For each account, the Vendor Manager confirms the individual still works for the vendor, still needs the access, and that the access level remains appropriate. Accounts not recertified within 10 business days of the recertification deadline are disabled. Recertification evidence is retained under RET-SCH.

## 6. Revocation

6.1 The vendor must notify the Vendor Manager within 1 business day when any individual with Northwind access leaves the vendor or moves off the Northwind account. Northwind disables that individual's access within 24 hours of the notice.

6.2 On contract termination, all vendor accounts, tokens, keys, and badges are revoked within 24 hours of the termination effective date (EXIT-PLN §4.1).

6.3 On a security incident involving vendor credentials, the CISO office may suspend all of the vendor's access immediately without notice.

## 7. Monitoring

Vendor account activity is monitored by the Security Operations Center. Access outside the hours stated in the access request, or from unexpected locations, generates an alert reviewed within 1 business day.

## 8. Exceptions

Deviations require an exception under EXC-PRC. Shared accounts are not approved as exceptions unless the system technically cannot support named accounts, and then only with session recording as a compensating control.
