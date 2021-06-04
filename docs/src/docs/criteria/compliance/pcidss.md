---
id: pcidss
title: PCI DSS
sidebar_label: PCI DSS
slug: /criteria/compliance/pcidss
---

The **`PCI Security Standards Council's`** mission
is to enhance global payment account data security
by developing standards
and supporting services
that drive education, awareness,
and effective implementation
by stakeholders.

## Correlation

### PCI DSS v3.2.1

- 6.5.10 *(v3.0)* - Broken authentication and session management

    - [023. Terminate inactive user sessions](/criteria/requirements/023)

    - [025. Manage concurrent sessions](/criteria/requirements/025)

    - [029. Cookies with security attributes](/criteria/requirements/029)

- [12.3.8 *(v3.0)* - Automatic disconnect of sessions for remote-access](/criteria/requirements/369)

- Appendix A1 A1.1 - A  hosting provider must fulfill these requirements

    - [096. Set users' required privileges](/criteria/requirements/096)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

- [Appendix A1 A1.2 - Restricteach entity’s access and privileges](/criteria/requirements/186)

- [Appendix A1 A1.3 - Ensure logging and audit trails](/criteria/requirements/075)

- [Appendix A2 A2.1 - Where POS  POI terminals use SSL or early TLS](/criteria/requirements/336)

- 1.2.1 - Restrict inbound and outbound traffic

    - [033. Restrict administrative access](/criteria/requirements/033)

    - [259. Segment the organization network](/criteria/requirements/259)

- 1.2.2 - Secure  and synchronize router configuration files

    - [033.  Restrict administrative access](/criteria/requirements/033)

    - [062. Define standard configurations](/criteria/requirements/062)

    - [176. Restrict system objects](/criteria/requirements/176)

- [1.2.3 - Install perimeter firewalls](/criteria/requirements/259)

- 1.3.1 - Implement a DMZ

    - [255. Allow access only to the necessary ports](/criteria/requirements/255)

    - [259. Segment the organization network](/criteria/requirements/259)

- 1.3.2 - Limit inbound Internet traffic

    - [255. Allow access only to the necessary ports](/criteria/requirements/255)

    - [259. Segment the organization network](/criteria/requirements/259)

- 1.3.3 - Implement anti-spoofing measures

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [259. Segment the organization network](/criteria/requirements/259)

- 1.3.4 - Do not allow unauthorized outbound traffic

    - [062. Define standard configurations](/criteria/requirements/062)

    - [259. Segment the organization network](/criteria/requirements/259)

- 1.3.5 - Permitonly “established” connections

    - [062. Define standard configurations](/criteria/requirements/062)

    - [255. Allow access only to the necessary ports](/criteria/requirements/255)

- 1.3.6 - Place system components that store cardholder data

    - [033. Restrict administrative access](/criteria/requirements/033)

    - [259. Segment the organization network](/criteria/requirements/259)

- 1.3.7 - Do not disclose private IP addresses and routing information

    - [077. Avoid disclosing technical information](/criteria/requirements/077)

    - [26- Avoid exposing sensitive information](/criteria/requirements/261)

- 2.1.1 - For wireless environments connected 

    - [142. Change system default credentials](/criteria/requirements/142)

    - [25- Change access point IP](/criteria/requirements/251)

- 2.2.2 - Enable only necessary services

    - [255. Allow access only to the necessary ports](/criteria/requirements/255)

    - [266. Disable insecure functionalities](/criteria/requirements/266)

    - [336. Disable insecure TLS versions](/criteria/requirements/336)

- [2.2.3 - Implement additional security features](/criteria/requirements/062)

- [2.2.4 - Configure system security parameters](/criteria/requirements/062)

- [2.2.5 - Remove all unnecessary functionality](/criteria/requirements/266)

- 2.3 - Encrypt all non-console administrative access

    - [18- Transmit data using secure protocols](/criteria/requirements/181)

    - [185. Encrypt sensitive information](/criteria/requirements/185)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

    - [302. Declare dependencies explicitly](/criteria/requirements/302)

- 3.1 - Keep cardholder data storage to a minimum

    - [183. Delete sensitive data securely](/criteria/requirements/183)

    - [360. Remove unnecessary sensitive information](/criteria/requirements/360)

- [3.2.1 - Do not store the full contents of any tracK](/criteria/requirements/360)

- [3.2.2 - Do not store the card verification code or value](/criteria/requirements/360)

- [3.2.3 - Do not store the personal identification number (PIN)](/criteria/requirements/360)

- [3.3 - Mask PAN  when displayed](/criteria/requirements/300)

- 3.4.1 - Disk encryption

    - [145. Protect system cryptographic keys](/criteria/requirements/145)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

- [3.4 - Render PAN  unreadable anywhere it is stored](/criteria/requirements/185)

- 3.5.2 - Restrict access to cryptographic keys

    - [145. Protect system cryptographic keys](/criteria/requirements/145)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

- 3.5.3 - Store secret and private keys used to encrypt or decrypt

    - [145. Protect system cryptographic keys](/criteria/requirements/145)

    - [185. Encrypt sensitive information](/criteria/requirements/185)

    - [333. Store salt values separately](/criteria/requirements/333)

- 3.5.4 - Store cryptographic keys

    - [145. Protect system cryptographic keys](/criteria/requirements/145)

    - [146. Remove cryptographic keys from RAM](/criteria/requirements/146)

- [3.6.1 - Generation of strong cryptographic keys](/criteria/requirements/224)

- [3.6.2 - Secure cryptographic key distributioN](/criteria/requirements/145)

- 3.6.3 - Secure  cryptographic key storage

    - [145.  Protect system cryptographic keys](/criteria/requirements/145)

    - [146. Remove cryptographic keys from RAM](/criteria/requirements/146)

- 3.6.4 - Cryptographic key changes for keys

    - [338. Implement perfect forward secrecy](/criteria/requirements/338)

    - [36- Replace cryptographic keys](/criteria/requirements/361)

- [3.6.5 - Retirement or replacement of keys](/criteria/requirements/361)

- 3.6.7 - Prevention of unauthorized substitution of cryptographic keys

    - [145.  Protect system cryptographic keys](/criteria/requirements/145)

    - [176. Restrict system objects](/criteria/requirements/176)

- 4.1 - Use strong cryptography and security protocols

    - [088. Request client certificates](/criteria/requirements/088)

    - [18- Transmit data using secure protocols](/criteria/requirements/181)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

    - [252. Configure key encryption](/criteria/requirements/252)

    - [336. Disable insecure TLS versions](/criteria/requirements/336)

- 4.1.1 - Ensure wireless networks transmitting cardholder data

    - [147. Use pre-existent mechanisms](/criteria/requirements/147)

    - [18- Transmit data using secure protocols](/criteria/requirements/181)

    - [252. Configure key encryption](/criteria/requirements/252)

- [4.2 - Never send unprotected PANs](/criteria/requirements/181)

- [5.1 - Deploy anti-virus software](/criteria/requirements/273)

- 5.1.1 - Ensure that anti-virus programs are capable of detecting

    - [04- Scan files for malicious code](/criteria/requirements/041)

    - [118. Inspect attachments](/criteria/requirements/118)

- [5.2 - Ensure anti-virus mechanisms maintainance](/criteria/requirements/262)

- [5.3 - Ensure that anti-virus mechanisms are actively running](/criteria/requirements/186)

- 6.2 - Ensure that all system components and softwareare protected

    - [062. Define standard configurations](/criteria/requirements/062)

    - [158. Use a secure programming language](/criteria/requirements/158)

    - [262. Verify third-party components](/criteria/requirements/262)

- [6.3 - Develop internal and external software applications securely](/criteria/requirements/062)

- [6.3.1 - Remove development, test or custom application accounts](/criteria/requirements/154)

- [6.4.1 - Separate  development or test environments from production environments](/criteria/requirements/180)

- [6.4.3 - Production data (live PANs) are  not used for testing or development](/criteria/requirements/180)

- [6.4.4 - Removal of test data and accounts from systemcomponents](/criteria/requirements/154)

- 6.5.1 - Injection flows

    - [037. Parameters without sensitive data](/criteria/requirements/037)

    - [050. Control calls to interpreted code](/criteria/requirements/050)

    - [117. Do not interpret HTML code](/criteria/requirements/117)

    - [160. Encode system outputs](/criteria/requirements/160)

    - [169. Use parameterized queries](/criteria/requirements/169)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [32- Avoid deserializing untrusted data](/criteria/requirements/321)

    - [344. Avoid dynamic code execution](/criteria/requirements/344)

- 6.5.2 - Buffer overflow

    - [157. Use the strict mode](/criteria/requirements/157)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [345. Establish protections against overflows](/criteria/requirements/345)

- 6.5.3 - Insecure cryptographic storage

    - [145. Protect system cryptographic keys](/criteria/requirements/145)

    - [185. Encrypt sensitive information](/criteria/requirements/185)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

- 6.5.4 - Insecure communications

    - [18- Transmit data using secure protocols](/criteria/requirements/181)

    - [336. Disable insecure TLS versions](/criteria/requirements/336)

- 6.5.5 - Improper error handling

    - [077. Avoid disclosing technical information](/criteria/requirements/077)

    - [078. Disable debugging events](/criteria/requirements/078)

    - [16- Define secure default options](/criteria/requirements/161)

- 6.5.7 - Cross-site scripting (XSS)

    - [029. Cookies with security attributes](/criteria/requirements/029)

    - [050. Control calls to interpreted code](/criteria/requirements/050)

    - [160. Encode system outputs](/criteria/requirements/160)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [340. Use octet stream downloads](/criteria/requirements/340)

    - [344. Avoid dynamic code execution](/criteria/requirements/344)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- 6.5.8 - Improper access control

    - [033. Restrict administrative access](/criteria/requirements/033)

    - [035. Manage privilege modifications](/criteria/requirements/035)

    - [080. Prevent log modification](/criteria/requirements/080)

    - [095. Define users with privileges](/criteria/requirements/095)

    - [096. Set users' required privileges](/criteria/requirements/096)

    - [176. Restrict system objects](/criteria/requirements/176)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

    - [265. Restrict access to critical processes](/criteria/requirements/265)

    - [266. Disable insecure functionalities](/criteria/requirements/266)

    - [320. Avoid client-side control enforcement](/criteria/requirements/320)

    - [34- Use the principle of deny by default](/criteria/requirements/341)

- 6.5.9 - Cross-site request forgery (CSRF)

    - [029. Cookies with security attributes](/criteria/requirements/029)

    - [174. Transactions without a distinguishable pattern](/criteria/requirements/174)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- 6.5.10 - Broken authenticationand session management

    - [023. Terminate inactive user sessions](/criteria/requirements/023)

    - [025. Manage concurrent sessions](/criteria/requirements/025)

    - [026. Encrypt client-side session information](/criteria/requirements/026)

    - [027. Allow session lockout](/criteria/requirements/027)

    - [028. Allow users to log out](/criteria/requirements/028)

    - [029. Cookies with security attributes](/criteria/requirements/029)

    - [030. Avoid object reutilization](/criteria/requirements/030)

    - [03- Discard user session data](/criteria/requirements/031)

    - [032. Avoid session ID leakages](/criteria/requirements/032)

    - [088. Request client certificates](/criteria/requirements/088)

    - [114. Deny access with inactive credentials](/criteria/requirements/114)

    - [13- Deny multiple password changing attempts](/criteria/requirements/131)

    - [139. Set minimum OTP length](/criteria/requirements/139)

    - [140. Define OTP lifespan](/criteria/requirements/140)

    - [14- Force re-authentication](/criteria/requirements/141)

    - [142. Change system default credentials](/criteria/requirements/142)

    - [143. Unique access credentials](/criteria/requirements/143)

    - [153. Out of band transactions](/criteria/requirements/153)

    - [209. Manage passwords in cache](/criteria/requirements/209)

    - [225. Proper authentication responses](/criteria/requirements/225)

    - [226. Avoid account lockouts](/criteria/requirements/226)

    - [228. Authenticate using standard protocols](/criteria/requirements/228)

    - [229. Request access credentials](/criteria/requirements/229)

    - [23- Implement a biometric verification component](/criteria/requirements/231)

    - [236. Establish authentication time](/criteria/requirements/236)

    - [237. Ascertain human interaction](/criteria/requirements/237)

    - [238. Establish safe recovery](/criteria/requirements/238)

    - [264. Request authentication](/criteria/requirements/264)

    - [319. Make authentication options equally secure](/criteria/requirements/319)

    - [320. Avoid client-side control enforcement](/criteria/requirements/320)

    - [328. Request MFA for critical systems](/criteria/requirements/328)

    - [332. Prevent the use of breached passwords](/criteria/requirements/332)

    - [334. Avoid knowledge-based authentication](/criteria/requirements/334)

    - [335. Define out of band token lifespan](/criteria/requirements/335)

    - [347. Invalidate previous OTPs](/criteria/requirements/347)

    - [357. Use stateless session tokens](/criteria/requirements/357)

    - [362. Assign MFA mechanisms to a single account](/criteria/requirements/362)

- 7.1.1 - Define access needs for each role

    - [095. Define users with privileges](/criteria/requirements/095)

    - [096. Set users' required privileges](/criteria/requirements/096)

    - [176. Restrict system objects](/criteria/requirements/176)

- 7.1.2 - Restrict access to privileged user IDs

    - [186. Use the principle of least privilege](/criteria/requirements/186)

    - [34- Use the principle of deny by default](/criteria/requirements/341)

- 7.1.3 - Assign access
        
    - [095. Define users with privileges](/criteria/requirements/095)

    - [096. Set users' required privileges](/criteria/requirements/096)

- 7.2.2 - Assignment of privileges

    - [095. Define users with privileges](/criteria/requirements/095)

    - [096. Set users' required privileges](/criteria/requirements/096)

    - [34- Use the principle of deny by default](/criteria/requirements/341)

- 8.1.1 - Assign all users a unique ID

    - [143. Unique access credentials](/criteria/requirements/143)

    - [229. Request access credentials](/criteria/requirements/229)

    - [264. Request authentication](/criteria/requirements/264)

- 8.1.2 - Control addition, deletion, and modification of user IDs

    - [034. Manage user accounts](/criteria/requirements/034)

    - [035. Manage privilege modifications](/criteria/requirements/035)

- [8.1.3 - Immediately revoke access for any terminated users](/criteria/requirements/114)

- [8.1.4 - Remove/disable inactive user accounts](/criteria/requirements/144)

- [8.1.8 - Require the user to re-authenticate (inactive)](/criteria/requirements/023)

- [8.2 - Ensure proper user-authentication management for non-consumer users](/criteria/requirements/229)

- 8.2.1 - Using strong cryptography

    - [127. Store hashed passwords](/criteria/requirements/127)

    - [18- Transmit data using secure protocols](/criteria/requirements/181)

    - [185. Encrypt sensitive information](/criteria/requirements/185)

- [8.2.2 - Verify user identity before modifying any authentication credential](/criteria/requirements/238)

- 8.2.3 - Passwords or passphrases must meet mininum requirements

    - [132. Passphrases with at least 4 words](/criteria/requirements/132)

    - [133. Passwords with at least 20 characters](/criteria/requirements/133)

- [8.2.4 - Change user passwords](/criteria/requirements/130)

- 8.2.5 - Passwords or passphrases

    - [126. Set a password regeneration mechanism](/criteria/requirements/126)

    - [129. Validate previous passwords](/criteria/requirements/129)

- 8.2.6 - Set  passwords or passphrases for first time use

    - [136. Force temporary password change](/criteria/requirements/136)

    - [137. Change temporary passwords of third parties](/criteria/requirements/137)

    - [367. Proper generation of temporary passwords](/criteria/requirements/367)

- 8.5 - Do not use group, shared, or generic IDs, passwords

    - [143. Unique access credentials](/criteria/requirements/143)

    - [362. Assign MFA mechanisms to a single account](/criteria/requirements/362)

- [8.6 - Proper use of authentication mechanisms](/criteria/requirements/362)

- 8.7 - Database containing cardholder data

    - [033. Restrict administrative access](/criteria/requirements/033)

    - [265. Restrict access to critical processes](/criteria/requirements/265)

- [9.8.2 - Render cardholder data on electronic media unrecoverable](/criteria/requirements/183)

- [10.2.1 - Individual user accesses to cardholder data](/criteria/requirements/075)

- 10.2.2 - Actions taken by anyindividual with root or administrative privileges

    - [046. Manage the integrity of critical files](/criteria/requirements/046)

    - [075. Record exceptional events in logs](/criteria/requirements/075)

- [10.2.3 - Access to all audit trails](/criteria/requirements/075)

- [10.2.4 - Invalid logical access attempts](/criteria/requirements/075)

- [10.2.5 - Use  of and changes to identification and authentication mechanisms](/criteria/requirements/075)

- 10.2.6 - Initialization, stopping,or pausing of the audit logs

    - [046. Manage the integrity of critical files](/criteria/requirements/046)

    - [075. Record exceptional events in logs](/criteria/requirements/075)

- [10.2.7 - Creation and deletion of system-level objects](/criteria/requirements/075)

- [10.3 - Record at least the following audit trail entries](/criteria/requirements/079)

- [10.4.1 - Critical systems have the correct and consistent time](/criteria/requirements/363)

- 10.4.2 - Time  data is protected

    - [046. Manage the integrity of critical files](/criteria/requirements/046)

    - [363. Synchronize system clocks](/criteria/requirements/363)

- [10.4.3 - Time settings are received from industry-accepted time source](/criteria/requirements/363)

- 10.5.1 - Limit viewing of audit trails

    - [096. Set users' required privileges](/criteria/requirements/096)

    - [176. Restrict system objects](/criteria/requirements/176)

- [10.5.2 - Protect audit trail files](/criteria/requirements/080)

- [10.5.3 - Promptly back up audit trail files](/criteria/requirements/080)

- [10.5.5 - Use  file-integrity monitoring or change-detection software](/criteria/requirements/046)
