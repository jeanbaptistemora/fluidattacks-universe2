---
id: owaspasvs
title: OWASP ASVS
sidebar_label: OWASP ASVS
slug: /criteria/compliance/owaspasvs
---

The **`OWASP Application Security Verification Standard`** project
provides a basis for testing
web application technical security controls
and also provides developers
with a list of requirements
for secure development.
The version used in this section is
[OWASP-ASVS v4.0.1](https://github.com/OWASP/ASVS/blob/v4.0.1/4.0/OWASP%20Application%20Security%20Verification%20Standard%204.0-en.pdf).

## Correlation

### Appendix C: Internet of Things Verification Requirements

- C.1 - Application layer debugging interfaces are disabled or protected

    - [078. Disable debugging events](/criteria/requirements/078)

    - [266. Disable insecure functionalities](/criteria/requirements/266)

- [C.2 - Cryptographic keys and certificates](/criteria/requirements/351)

- [C.3 - Memory protection controls (ASLR and DEP)](/criteria/requirements/350)

- C.4 - On-chip debugging interfaces such as JTAG and SWD

    - [078. Disable debugging events](/criteria/requirements/078)

    - [266. Disable insecure functionalities](/criteria/requirements/266)

- [C.5 - Trusted execution is implemented and enabled](/criteria/requirements/352)

- C.6 - Private keys and certificates are store securely

    - [145. Protect system cryptographic keys](/criteria/requirements/145)

    - [185. Encrypt sensitive information](/criteria/requirements/185)

- [C.7 - Transport layer security](/criteria/requirements/181)

- C.8 - Firmware apps validate the digital signature (server)

    - [178. Use digital signatures](/criteria/requirements/178)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

- C.9 - Wireless connection are mutually authenticated

    - [088. Request client certificates](/criteria/requirements/088)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

    - [264. Request authentication](/criteria/requirements/264)

- [C.10 - Wireless communication over an encrypted channel](/criteria/requirements/181)

- C.11 - Replace banned C functions

    - [158. Use a secure programming language](/criteria/requirements/158)

    - [266. Disable insecure functionalities](/criteria/requirements/266)

- [C.12 - Firmware maintains a software bill of materials](/criteria/requirements/302)

- C.13 - Hardcoded credentials reviewed in code with third party libraries

    - [154. Eliminate backdoors](/criteria/requirements/154)

    - [155. Application free of malicious code](/criteria/requirements/155)

    - [156. Source code without sensitive information](/criteria/requirements/156)

    - [262. Verify third-party components](/criteria/requirements/262)

- [C.14 - Components are not susceptible to OS Command Injection](/criteria/requirements/344)

- [C.15 - Pin the digital signature to a trusted server](/criteria/requirements/178)

- C.16 - Use of tamper resistance or detection

    - [178. Use digital signatures](/criteria/requirements/178)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

- [C.17 - Intellectual Property protection](/criteria/requirements/062)

- C.18 - Security controls against firmware reverse engineering

    - [078. Disable debugging events](/criteria/requirements/078)

    - [159. Obfuscate code](/criteria/requirements/159)

- [C.19 - Boot image signature](/criteria/requirements/178)

- C.20 - Time-of-checks vs time-of-use attacks

    - [337. Make critical logic flows thread safe](/criteria/requirements/337)

    - [353. Schedule firmware updates](/criteria/requirements/353)

- [C.21 - Validate firmware upgrade and use code signing](/criteria/requirements/178)

- C.22 - Device cannot be downgraded

    - [336. Disable insecure TLS versions](/criteria/requirements/336)

    - [354. Prevent firmware downgrades](/criteria/requirements/354)

- C.23 - Cryptographically secure pseudo-random number generator

    - [147. Use pre-existent mechanisms](/criteria/requirements/147)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

- [C.24 - Predefined schedule for firmware updates](/criteria/requirements/353)

- C.25 - Wipe of firmware and sensitive data

    - [183. Delete sensitive data securely](/criteria/requirements/183)

    - [210. Delete information from mobile devices](/criteria/requirements/210)

    - [214. Allow data destruction](/criteria/requirements/214)

- C.26 - Disabling debugging interfaces 

    - [078. Disable debugging events](/criteria/requirements/078)

    - [262. Verify third-party components](/criteria/requirements/262)

- [C.27 - Substantial protection from decapping and side channel attacks](/criteria/requirements/262)

- [C.29 - Interchip communication is encrypted](/criteria/requirements/181)

- [C.30 - Code validation before execution](/criteria/requirements/178)

- C.31 - Sensitive information in memory is overwritten with zeros

    - [146. Remove cryptographic keys from RAM](/criteria/requirements/146)

    - [183. Delete sensitive data securely](/criteria/requirements/183)

    - [214. Allow data destruction](/criteria/requirements/214)

- [C.32 - Kernel containers for isolation](/criteria/requirements/062)

- C.33 - Secure compiler flags configured for firmware builts

    - [062. Define standard configurations](/criteria/requirements/062)

    - [157. Use the strict mode](/criteria/requirements/157)

- C.34 - Micro controllers configured with code protection

    - [062. Define standard configurations](/criteria/requirements/062)

    - [159. Obfuscate code](/criteria/requirements/159)

### General Requirements

- V1.2 Authentication Architectural Requirements.(1.2.1)

    - [096. Set users' required privileges](/criteria/requirements/096)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

- V1.2 Authentication Architectural Requirements.(1.2.2)

    - [176. Restrict system objects](/criteria/requirements/176)

    - [227. Display access notification](/criteria/requirements/227)

    - [229. Request access credentials](/criteria/requirements/229)

    - [264. Request authentication](/criteria/requirements/264)

- V1.2 Authentication Architectural Requirements.(1.2.3)

    - [227. Display access notification](/criteria/requirements/227)

    - [229. Request access credentials](/criteria/requirements/229)

    - [264. Request authentication](/criteria/requirements/264)

- V1.2 Authentication Architectural Requirements.(1.2.4)

    - [237. Ascertain human interaction](/criteria/requirements/237)

    - [319. Make authentication options equally secure](/criteria/requirements/319)

    - [362. Assign MFA mechanisms to a single account](/criteria/requirements/362)

- [V1.10 Malicious Software Architectural Requirements.(1.10.1)](/criteria/requirements/051)

- [V1.11 Business Logic Architectural Requirements.(1.11.2)](/criteria/requirements/337)

- V1.11 Business Logic Architectural Requirements.(1.11.3)

    - [337. Make critical logic flows thread safe](/criteria/requirements/337)

    - [353. Schedule firmware updates](/criteria/requirements/353)

- [V1.12 Secure File Upload Architectural Requirements.(1.12.1)](/criteria/requirements/339)

- [V1.12 Secure File Upload Architectural Requirements.(1.12.2)](/criteria/requirements/340)

- V1.14 Configuration Architectural Requirements.(1.14.1)

    - [262. Verify third-party components](/criteria/requirements/262)

    - [273. Define a fixed security suite](/criteria/requirements/273)

- [V1.14 Configuration Architectural Requirements.(1.14.2)](/criteria/requirements/178)

- V10.1 Code Integrity Controls.(10.1.1)

    - [041. Scan files for malicious code](/criteria/requirements/041)

    - [118. Inspect attachments](/criteria/requirements/118)

- V10.2 Malicious Code Search.(10.2.1)

    - [155. Application free of malicious code](/criteria/requirements/155)

    - [262. Verify third-party components](/criteria/requirements/262)

- [V10.2 Malicious Code Search.(10.2.1)](/criteria/requirements/310)

- V10.2 Malicious Code Search.(10.2.2)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

    - [341. Use the principle of deny by default](/criteria/requirements/341)

- V10.2 Malicious Code Search.(10.2.3)

    - [154. Eliminate backdoors](/criteria/requirements/154)

    - [155. Application free of malicious code](/criteria/requirements/155)

    - [262. Verify third-party components](/criteria/requirements/262)

    - [323. Exclude unverifiable files](/criteria/requirements/323)

- V10.2 Malicious Code Search.(10.2.4)

    - [155. Application free of malicious code](/criteria/requirements/155)

    - [262. Verify third-party components](/criteria/requirements/262)

- V10.2 Malicious Code Search.(10.2.5)

    - [155. Application free of malicious code](/criteria/requirements/155)

    - [262. Verify third-party components](/criteria/requirements/262)

- V10.2 Malicious Code Search.(10.2.6)

    - [155. Application free of malicious code](/criteria/requirements/155)

    - [262. Verify third-party components](/criteria/requirements/262)

- V10.3 Deployed Application Integrity Controls.(10.3.1)

    - [178. Use digital signatures](/criteria/requirements/178)

    - [330. Verify Subresource Integrity](/criteria/requirements/330)

- V10.3 Deployed Application Integrity Controls.(10.3.2)

    - [050. Control calls to interpreted code](/criteria/requirements/050)

    - [062. Define standard configurations](/criteria/requirements/062)

    - [178. Use digital signatures](/criteria/requirements/178)

    - [330. Verify Subresource Integrity](/criteria/requirements/330)

- V10.3 Deployed Application Integrity Controls.(10.3.3)

    - [050. Control calls to interpreted code](/criteria/requirements/050)

    - [356. Verify sub-domain names](/criteria/requirements/356)

- [V11.1 Business Logic Security Requirements.(11.1.1)](/criteria/requirements/319)

- V11.1 Business Logic Security Requirements.(11.1.2)

    - [237. Ascertain human interaction](/criteria/requirements/237)

    - [327. Set a rate limit](/criteria/requirements/327)

- V11.1 Business Logic Security Requirements.(11.1.3)

    - [039. Define maximum file size](/criteria/requirements/039)

    - [327. Set a rate limit](/criteria/requirements/327)

- V11.1 Business Logic Security Requirements.(11.1.4)

    - [039. Define maximum file size](/criteria/requirements/039)

    - [072. Set maximum response time](/criteria/requirements/072)

    - [123. Restrict the reading of emails](/criteria/requirements/123)

    - [327. Set a rate limit](/criteria/requirements/327)

- [V11.1 Business Logic Security Requirements.(11.1.5)](/criteria/requirements/327)

- V11.1 Business Logic Security Requirements.(11.1.6)

    - [337. Make critical logic flows thread safe](/criteria/requirements/337)

    - [353. Schedule firmware updates](/criteria/requirements/353)

- [V11.1 Business Logic Security Requirements.(11.1.7)](/criteria/requirements/075)

- [V11.1 Business Logic Security Requirements.(11.1.8)](/criteria/requirements/237)

- [V12.1 File Upload Requirements.(12.1.1)](/criteria/requirements/039)

- V12.1 File Upload Requirements.(12.1.2)

    - [039. Define maximum file size](/criteria/requirements/039)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- V12.1 File Upload Requirements.(12.1.3)

    - [039. Define maximum file size](/criteria/requirements/039)

    - [327. Set a rate limit](/criteria/requirements/327)

- V12.2 File Integrity Requirements.(12.2.1)

    - [040. Compare file format and extension](/criteria/requirements/040)

    - [042. Validate file format](/criteria/requirements/042)

- [V12.3 File execution Requirements.(12.3.1)](/criteria/requirements/037)

- [V12.3 File execution Requirements.(12.3.2)](/criteria/requirements/037)

- [V12.3 File execution Requirements.(12.3.3)](/criteria/requirements/037)

- V12.3 File execution Requirements.(12.3.4)

    - [037. Parameters without sensitive data](/criteria/requirements/037)

    - [043. Define an explicit content type](/criteria/requirements/043)

    - [349. Include HTTP security headers](/criteria/requirements/349)

    - [355. Serve files with specific extensions](/criteria/requirements/355)

- V12.3 File execution Requirements.(12.3.5)

    - [037. Parameters without sensitive data](/criteria/requirements/037)

    - [050. Control calls to interpreted code](/criteria/requirements/050)

- V12.4 File Storage Requirements.(12.4.1)

    - [041. Scan files for malicious code](/criteria/requirements/041)

    - [118. Inspect attachments](/criteria/requirements/118)

    - [273. Define a fixed security suite](/criteria/requirements/273)

    - [339. Avoid storing sensitive files in the web root](/criteria/requirements/339)

- V12.5 File Download Requirements.(12.5.1)

    - [043. Define an explicit content type](/criteria/requirements/043)

    - [355. Serve files with specific extensions](/criteria/requirements/355)

- V12.5 File Download Requirements.(12.5.2)

    - [043. Define an explicit content type](/criteria/requirements/043)

    - [340. Use octet stream downloads](/criteria/requirements/340)

- [V12.6 SSRF Protection Requirements.(12.6.1)](/criteria/requirements/324)

- [V13.1: Generic Web Service Security Verification Requirements.(13.1.1)](/criteria/requirements/348)

- V13.1 Generic Web Service Security Verification Requirements.(13.1.2)

    - [033. Restrict administrative access](/criteria/requirements/033)

    - [035. Manage privilege modifications](/criteria/requirements/035)

- [V13.1 Generic Web Service Security Verification Requirements.(13.1.3)](/criteria/requirements/032)

- [V13.1 Generic Web Service Security Verification Requirements.(13.1.4)](/criteria/requirements/320)

- V13.1 Generic Web Service Security Verification Requirements.(13.1.5)

    - [043. Define an explicit content type](/criteria/requirements/043)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- V13.2 RESTful Web Service Verification Requirements.(13.2.1)

    - [096. Set users' required privileges](/criteria/requirements/096)

    - [176. Restrict system objects](/criteria/requirements/176)

- V13.2 RESTful Web Service Verification Requirements.(13.2.2)

    - [062. Define standard configurations](/criteria/requirements/062)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [321. Avoid deserializing untrusted data](/criteria/requirements/321)

- V13.2 RESTful Web Service Verification Requirements.(13.2.3)

    - [029. Cookies with security attributes](/criteria/requirements/029)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- V13.2 RESTful Web Service Verification Requirements.(13.2.4)

    - [237. Ascertain human interaction](/criteria/requirements/237)

    - [327. Set a rate limit](/criteria/requirements/327)

- V13.2 RESTful Web Service Verification Requirements.(13.2.5)

    - [043. Define an explicit content type](/criteria/requirements/043)

    - [178. Use digital signatures](/criteria/requirements/178)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

- V13.3 SOAP Web Service Verification Requirements.(13.3.1)

    - [062. Define standard configurations](/criteria/requirements/062)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [321. Avoid deserializing untrusted data](/criteria/requirements/321)

- V13.3 SOAP Web Service Verification Requirements.(13.3.2)

    - [178. Use digital signatures](/criteria/requirements/178)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

- V13.4 GraphQL and other Web Service Data Layer Security Requirements.(13.4.1)

    - [072. Set maximum response time](/criteria/requirements/072)

    - [327. Set a rate limit](/criteria/requirements/327)

- [V13.4 GraphQL and other Web Service Data Layer Security Requirements.(13.4.2)](/criteria/requirements/320)

- [V14.1 Build.(14.1.1)](/criteria/requirements/062)

- V14.1 Build.(14.1.2)

    - [062. Define standard configurations](/criteria/requirements/062)

    - [157. Use the strict mode](/criteria/requirements/157)

- [V14.1 Build.(14.1.3)](/criteria/requirements/062)

- [V14.1 Build.(14.1.4)](/criteria/requirements/302)

- [V14.1 Build.(14.1.5)](/criteria/requirements/046)

- V14.2 Dependency.(14.2.1)

    - [158. Use a secure programming language](/criteria/requirements/158)

    - [262. Verify third-party components](/criteria/requirements/262)

    - [302. Declare dependencies explicitly](/criteria/requirements/302)

- V14.2 Dependency.(14.2.2)

    - [142. Change system default credentials](/criteria/requirements/142)

    - [171. Remove commented-out code](/criteria/requirements/171)

    - [251. Change access point IP](/criteria/requirements/251)

    - [266. Disable insecure functionalities](/criteria/requirements/266)

- [V14.2 Dependency.(14.2.3)](/criteria/requirements/330)

- V14.2 Dependency.(14.2.4)

    - [158. Use a secure programming language](/criteria/requirements/158)

    - [262. Verify third-party components](/criteria/requirements/262)

- [V14.2 Dependency.(14.2.5)](/criteria/requirements/302)

- V14.2 Dependency.(14.2.6)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

    - [341. Use the principle of deny by default](/criteria/requirements/341)

- [V14.3 Unintended Security Disclosure Requirements.(14.3.1)](/criteria/requirements/077)

- V14.3 Unintended Security Disclosure Requirements.(14.3.2)

    - [077. Avoid disclosing technical information](/criteria/requirements/077)

    - [078. Disable debugging events](/criteria/requirements/078)

- [V14.3 Unintended Security Disclosure Requirements.(14.3.3)](/criteria/requirements/077)

- V14.4 HTTP Security Headers Requirements.(14.4.1)

    - [043. Define an explicit content type](/criteria/requirements/043)

    - [044. Define an explicit charset](/criteria/requirements/044)

    - [349. Include HTTP security headers](/criteria/requirements/349)

    - [355. Serve files with specific extensions](/criteria/requirements/355)

- V14.4 HTTP Security Headers Requirements.(14.4.2)

    - [043. Define an explicit content type](/criteria/requirements/043)

    - [349. Include HTTP security headers](/criteria/requirements/349)

    - [355. Serve files with specific extensions](/criteria/requirements/355)

- V14.4 HTTP Security Headers Requirements.(14.4.3)

    - [340. Use octet stream downloads](/criteria/requirements/340)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- [V14.4 HTTP Security Headers Requirements.(14.4.4)](/criteria/requirements/349)

- [V14.4 HTTP Security Headers Requirements.(14.4.5)](/criteria/requirements/349)

- V14.4 HTTP Security Headers Requirements.(14.4.6)

    - [324. Control redirects](/criteria/requirements/324)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- V14.4 HTTP Security Headers Requirements.(14.4.7)

    - [175. Protect pages from clickjacking](/criteria/requirements/175)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- V14.5 Validate HTTP Request Header Requirements.(14.5.1)

    - [266. Disable insecure functionalities](/criteria/requirements/266)

- [V14.5 Validate HTTP Request Header Requirements.(14.5.1)](/criteria/requirements/341)

- [V14.5 Validate HTTP Request Header Requirements.(14.5.2)](/criteria/requirements/320)

- V14.5 Validate HTTP Request Header Requirements.(14.5.3)

    - [029. Cookies with security attributes](/criteria/requirements/029)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- V14.5 Validate HTTP Request Header Requirements.(14.5.4)

    - [264. Request authentication](/criteria/requirements/264)

    - [319. Make authentication options equally secure](/criteria/requirements/319)

- V1.4 Access Control Architectural Requirements.(1.4.1)

    - [122. Validate credential ownership](/criteria/requirements/122)

    - [131. Deny multiple password changing attempts](/criteria/requirements/131)

    - [238. Establish safe recovery](/criteria/requirements/238)

    - [266. Disable insecure functionalities](/criteria/requirements/266)

    - [320. Avoid client-side control enforcement](/criteria/requirements/320)

    - [324. Control redirects](/criteria/requirements/324)

- V1.4 Access Control Architectural Requirements.(1.4.3)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

    - [265. Restrict access to critical processes](/criteria/requirements/265)

- V1.4 Access Control Architectural Requirements.(1.4.4)

    - [265. Restrict access to critical processes](/criteria/requirements/265)

    - [320. Avoid client-side control enforcement](/criteria/requirements/320)

- V1.4 Access Control Architectural Requirements.(1.4.5)

    - [176. Restrict system objects](/criteria/requirements/176)

    - [265. Restrict access to critical processes](/criteria/requirements/265)

- [V1.5 Input and Output Architectural Requirements.(1.5.1)](/criteria/requirements/331)

- [V1.5 Input and Output Architectural Requirements.(1.5.2)](/criteria/requirements/321)

- V1.5 Input and Output Architectural Requirements.(1.5.3)

    - [160. Encode system outputs](/criteria/requirements/160)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [320. Avoid client-side control enforcement](/criteria/requirements/320)

    - [324. Control redirects](/criteria/requirements/324)

- V1.5 Input and Output Architectural Requirements.(1.5.4)

    - [160. Encode system outputs](/criteria/requirements/160)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- V1.6 Cryptographic Architectural Requirements.(1.6.1)

    - [145. Protect system cryptographic keys](/criteria/requirements/145)

    - [146. Remove cryptographic keys from RAM](/criteria/requirements/146)

    - [147. Use pre-existent mechanisms](/criteria/requirements/147)

    - [148. Set minimum size of asymmetric encryption](/criteria/requirements/148)

    - [149. Set minimum size of symmetric encryption](/criteria/requirements/149)

    - [150. Set minimum size for hash functions](/criteria/requirements/150)

    - [151. Separate keys for encryption and signatures](/criteria/requirements/151)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

    - [370. Use OAEP padding with RSA](/criteria/requirements/370)

    - [371. Use GCM Padding with AES](/criteria/requirements/371)

    - [372. Proper Use of Initialization Vector (IV)](/criteria/requirements/372)

- V1.6 Cryptographic Architectural Requirements.(1.6.2)

    - [145. Protect system cryptographic keys](/criteria/requirements/145)

    - [147. Use pre-existent mechanisms](/criteria/requirements/147)

- V1.6 Cryptographic Architectural Requirements.(1.6.3)

    - [145. Protect system cryptographic keys](/criteria/requirements/145)

    - [147. Use pre-existent mechanisms](/criteria/requirements/147)

    - [361. Replace cryptographic keys](/criteria/requirements/361)

- [V1.6 Cryptographic Architectural Requirements.(1.6.4)](/criteria/requirements/145)

- V1.7 Errors, Logging and Auditing Architectural Requirements.(1.7.1)

    - [075. Record exceptional events in logs](/criteria/requirements/075)

    - [079. Record exact occurrence time of events](/criteria/requirements/079)

    - [083. Avoid logging sensitive data](/criteria/requirements/083)

    - [322. Avoid excessive logging](/criteria/requirements/322)

    - [376. Register severity level](/criteria/requirements/376)

    - [377. Store logs based on valid regulation](/criteria/requirements/377)

    - [378. Use of log management system](/criteria/requirements/378)

- [V1.9 Client-side Data Protection.(1.9.1)](/criteria/requirements/181)

- [V2.1 Password Security Requirements.(2.1.1)](/criteria/requirements/133)

- [V2.1 Password Security Requirements.(2.1.2)](/criteria/requirements/132)

- [V2.1 Password Security Requirements.(2.1.5)](/criteria/requirements/126)

- [V2.1 Password Security Requirements.(2.1.6)](/criteria/requirements/238)

- [V2.1 Password Security Requirements.(2.1.7)](/criteria/requirements/332)

- V2.2 General Authenticator Requirements.(2.2.1)

    - [226. Avoid account lockouts](/criteria/requirements/226)

    - [237. Ascertain human interaction](/criteria/requirements/237)

    - [327. Set a rate limit](/criteria/requirements/327)

    - [332. Prevent the use of breached passwords](/criteria/requirements/332)

    - [347. Invalidate previous OTPs](/criteria/requirements/347)

- V2.2 General Authenticator Requirements.(2.2.3)

    - [025. Manage concurrent sessions](/criteria/requirements/025)

    - [301. Notify configuration changes](/criteria/requirements/301)

- [V2.2 General Authenticator Requirements.(2.2.4)](/criteria/requirements/088)

- [V2.2 General Authenticator Requirements.(2.2.5)](/criteria/requirements/181)

- [V2.2 General Authenticator Requirements.(2.2.6)](/criteria/requirements/030)

- V2.3 Authenticator Lifecycle Requirements.(2.3.1)

    - [136. Force temporary password change](/criteria/requirements/136)

    - [137. Change temporary passwords of third parties](/criteria/requirements/137)

    - [138. Define lifespan for temporary passwords](/criteria/requirements/138)

    - [139. Set minimum OTP length](/criteria/requirements/139)

    - [367. Proper generation of temporary passwords](/criteria/requirements/367)

- [V2.3 Authenticator Lifecycle Requirements.(2.3.3)](/criteria/requirements/358)

- V2.4 Credential Storage Requirements.(2.4.1)

    - [127. Store hashed passwords](/criteria/requirements/127)

    - [134. Store passwords with salt](/criteria/requirements/134)

    - [135. Passwords with random salt](/criteria/requirements/135)

- [V2.4 Credential Storage Requirements.(2.4.2)](/criteria/requirements/135)

- [V2.4 Credential Storage Requirements.(2.4.3)](/criteria/requirements/127)

- [V2.4 Credential Storage Requirements.(2.4.4)](/criteria/requirements/127)

- [V2.4 Credential Storage Requirements.(2.4.5)](/criteria/requirements/333)

- V2.5 Credential Recovery Requirements.(2.5.1)

    - [126. Set a password regeneration mechanism](/criteria/requirements/126)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

- [V2.5 Credential Recovery Requirements.(2.5.2)](/criteria/requirements/334)

- [V2.5 Credential Recovery Requirements.(2.5.3)](/criteria/requirements/126)

- V2.5 Credential Recovery Requirements.(2.5.4)

    - [142. Change system default credentials](/criteria/requirements/142)

    - [251. Change access point IP](/criteria/requirements/251)

- V2.5 Credential Recovery Requirements.(2.5.6)

    - [126. Set a password regeneration mechanism](/criteria/requirements/126)

    - [131. Deny multiple password changing attempts](/criteria/requirements/131)

    - [238. Establish safe recovery](/criteria/requirements/238)

- V2.5 Credential Recovery Requirements.(2.5.7)

    - [122. Validate credential ownership](/criteria/requirements/122)

    - [319. Make authentication options equally secure](/criteria/requirements/319)

- [V2.6 Look-up Secret Verifier Requirements.(2.6.1)](/criteria/requirements/347)

- [V2.6 Look-up Secret Verifier Requirements.(2.6.2)](/criteria/requirements/224)

- V2.6 Look-up Secret Verifier Requirements.(2.6.3)

    - [223. Uniform distribution in random numbers](/criteria/requirements/223)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

- [V2.7 Out of Band Verifier Requirements.(2.7.1)](/criteria/requirements/153)

- [V2.7 Out of Band Verifier Requirements.(2.7.2)](/criteria/requirements/335)

- [V2.7 Out of Band Verifier Requirements.(2.7.3)](/criteria/requirements/335)

- [V2.7 Out of Band Verifier Requirements.(2.7.4)](/criteria/requirements/153)

- [V2.7 Out of Band Verifier Requirements.(2.7.6)](/criteria/requirements/224)

- [V2.8 Single or Multi Factor One Time Verifier Requirements.(2.8.1)](/criteria/requirements/140)

- [V2.8 Single or Multi Factor One Time Verifier Requirements.(2.8.2)](/criteria/requirements/145)

- V2.8 Single or Multi Factor One Time Verifier Requirements.(2.8.3)

    - [140. Define OTP lifespan](/criteria/requirements/140)

    - [147. Use pre-existent mechanisms](/criteria/requirements/147)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

- V2.8 Single or Multi Factor One Time Verifier Requirements.(2.8.4)

    - [140. Define OTP lifespan](/criteria/requirements/140)

    - [347. Invalidate previous OTPs](/criteria/requirements/347)

- [V2.8 Single or Multi Factor One Time Verifier Requirements.(2.8.7)](/criteria/requirements/231)

- [V2.9 Cryptographic Software and Devices Verifier Requirements.(2.9.1)](/criteria/requirements/145)

- V2.9 Cryptographic Software and Devices Verifier Requirements.(2.9.2)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

    - [351. Assign unique keys to each device](/criteria/requirements/351)

    - [361. Replace cryptographic keys](/criteria/requirements/361)

- V2.9 Cryptographic Software and Devices Verifier Requirements.(2.9.3)

    - [147. Use pre-existent mechanisms](/criteria/requirements/147)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

- V2.10 Service Authentication Requirements.(2.10.2)

    - [142. Change system default credentials](/criteria/requirements/142)

    - [251. Change access point IP](/criteria/requirements/251)

- V2.10 Service Authentication Requirements.(2.10.3)

    - [156. Source code without sensitive information](/criteria/requirements/156)

    - [375. Remove sensitive data from client-side applications](/criteria/requirements/375)

- V2.10 Service Authentication Requirements.(2.10.4)

    - [156. Source code without sensitive information](/criteria/requirements/156)

    - [172. Encrypt connection strings](/criteria/requirements/172)

- V3.1 Client-side Data Protection.(3.1.1)

    - [032. Avoid session ID leakages](/criteria/requirements/032)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

- V3.2 Session Binding Requirements.(3.2.1)

    - [025. Manage concurrent sessions](/criteria/requirements/025)

    - [030. Avoid object reutilization](/criteria/requirements/030)

    - [347. Invalidate previous OTPs](/criteria/requirements/347)

- [V3.2 Session Binding Requirements.(3.2.2)](/criteria/requirements/357)

- [V3.2 Session Binding Requirements.(3.2.3)](/criteria/requirements/029)

- [V3.2 Session Binding Requirements.(3.2.4)](/criteria/requirements/224)

- [V3.3 Session Logout and Timeout Requirements.(3.3.1)](/criteria/requirements/031)

- V3.3 Session Logout and Timeout Requirements.(3.3.2)

    - [023. Terminate inactive user sessions](/criteria/requirements/023)

    - [369. Set a maximum lifetime in sessions](/criteria/requirements/369)

- [V3.3 Session Logout and Timeout Requirements.(3.3.3)](/criteria/requirements/141)

- [V3.3 Session Logout and Timeout Requirements.(3.3.4)](/criteria/requirements/028)

- [V3.4 Cookie-based Session Management.(3.4.1)](/criteria/requirements/029)

- [V3.4 Cookie-based Session Management.(3.4.2)](/criteria/requirements/029)

- [V3.4 Cookie-based Session Management.(3.4.3)](/criteria/requirements/029)

- [V3.4 Cookie-based Session Management.(3.4.4)](/criteria/requirements/029)

- [V3.4 Cookie-based Session Management.(3.4.5)](/criteria/requirements/029)

- V3.5 Token-based Session Management.(3.5.1)

    - [028. Allow users to log out](/criteria/requirements/028)

    - [357. Use stateless session tokens](/criteria/requirements/357)

- [V3.5 Token-based Session Management.(3.5.2)](/criteria/requirements/357)

- V3.5 Token-based Session Management.(3.5.3)

    - [178. Use digital signatures](/criteria/requirements/178)

    - [357. Use stateless session tokens](/criteria/requirements/357)

- V3.6 Re-authentication from a Federation or Assertion.(3.6.1)

    - [023. Terminate inactive user sessions](/criteria/requirements/023)

    - [236. Establish authentication time](/criteria/requirements/236)

- [V3.6 Re-authentication from a Federation or Assertion.(3.6.2)](/criteria/requirements/023)

- V3.7 Defenses Against Session Management Exploits.(3.7.1)

    - [141. Force re-authentication](/criteria/requirements/141)

    - [264. Request authentication](/criteria/requirements/264)

- V4.1 General Access Control Design.(4.1.1)

    - [238. Establish safe recovery](/criteria/requirements/238)

    - [266. Disable insecure functionalities](/criteria/requirements/266)

    - [320. Avoid client-side control enforcement](/criteria/requirements/320)

    - [324. Control redirects](/criteria/requirements/324)

- V4.1 General Access Control Design.(4.1.2)

    - [035. Manage privilege modifications](/criteria/requirements/035)

    - [320. Avoid client-side control enforcement](/criteria/requirements/320)

- V4.1 General Access Control Design.(4.1.3)

    - [035. Manage privilege modifications](/criteria/requirements/035)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

- V4.1 General Access Control Design.(4.1.4)

    - [095. Define users with privileges](/criteria/requirements/095)

    - [096. Set users' required privileges](/criteria/requirements/096)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

    - [341. Use the principle of deny by default](/criteria/requirements/341)

- V4.1 General Access Control Design.(4.1.5)

    - [161. Define secure default options](/criteria/requirements/161)

    - [359. Avoid using generic exceptions](/criteria/requirements/359)

- V4.2 Operation Level Access Control.(4.2.1)

    - [176. Restrict system objects](/criteria/requirements/176)

    - [320. Avoid client-side control enforcement](/criteria/requirements/320)

- V4.2 Operation Level Access Control.(4.2.2)

    - [029. Cookies with security attributes](/criteria/requirements/029)

    - [174. Transactions without a distinguishable pattern](/criteria/requirements/174)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- V4.3 Other Access Control Considerations.(4.3.2)

    - [045. Remove metadata when sharing files](/criteria/requirements/045)

    - [261. Avoid exposing sensitive information](/criteria/requirements/261)

    - [339. Avoid storing sensitive files in the web root](/criteria/requirements/339)

- V5.1 Input Validation Requirements.(5.1.1)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [342. Validate request parameters](/criteria/requirements/342)

- [V5.1 Input Validation Requirements.(5.1.2)](/criteria/requirements/342)

- V5.1 Input Validation Requirements.(5.1.3)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [342. Validate request parameters](/criteria/requirements/342)

- V5.1 Input Validation Requirements.(5.1.4)

    - [164. Use optimized structures](/criteria/requirements/164)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- [V5.1 Input Validation Requirements.(5.1.5)](/criteria/requirements/324)

- [V5.1 Input Validation Requirements.(5.2.4)](/criteria/requirements/344)

- [V5.2 Sanitization and Sandboxing Requirements.(5.2.1)](/criteria/requirements/173)

- [V5.2 Sanitization and Sandboxing Requirements.(5.2.2)](/criteria/requirements/173)

- [V5.2 Sanitization and Sandboxing Requirements.(5.2.3)](/criteria/requirements/173)

- [V5.2 Sanitization and Sandboxing Requirements.(5.2.4)](/criteria/requirements/173)

- [V5.2 Sanitization and Sandboxing Requirements.(5.2.5)](/criteria/requirements/173)

- V5.2 Sanitization and Sandboxing Requirements.(5.2.6)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [324. Control redirects](/criteria/requirements/324)

- V5.2 Sanitization and Sandboxing Requirements.(5.2.7)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [344. Avoid dynamic code execution](/criteria/requirements/344)

- V5.2 Sanitization and Sandboxing Requirements.(5.2.8)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [344. Avoid dynamic code execution](/criteria/requirements/344)

- V5.3 Output encoding and Injection Prevention Requirements.(5.3.1)

    - [043. Define an explicit content type](/criteria/requirements/043)

    - [044. Define an explicit charset](/criteria/requirements/044)

    - [160. Encode system outputs](/criteria/requirements/160)

- [V5.3 Output encoding and Injection Prevention Requirements.(5.3.2)](/criteria/requirements/160)

- [V5.3 Output encoding and Injection Prevention Requirements.(5.3.3)](/criteria/requirements/160)

- V5.3 Output encoding and Injection Prevention Requirements.(5.3.4)

    - [169. Use parameterized queries](/criteria/requirements/169)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- V5.3 Output encoding and Injection Prevention Requirements.(5.3.5)

    - [160. Encode system outputs](/criteria/requirements/160)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- V5.3 Output encoding and Injection Prevention Requirements.(5.3.6)

    - [050. Control calls to interpreted code](/criteria/requirements/050)

    - [160. Encode system outputs](/criteria/requirements/160)

- [V5.3 Output encoding and Injection Prevention Requirements.(5.3.7)](/criteria/requirements/173)

- V5.3 Output encoding and Injection Prevention Requirements.(5.3.8)

    - [160. Encode system outputs](/criteria/requirements/160)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- V5.3 Output encoding and Injection Prevention Requirements.(5.3.9)

    - [037. Parameters without sensitive data](/criteria/requirements/037)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- V5.3 Output encoding and Injection Prevention Requirements.(5.3.10)

    - [037. Parameters without sensitive data](/criteria/requirements/037)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- V5.4 Memory, String, and Unmanaged Code Requirements.(5.4.1)

    - [158. Use a secure programming language](/criteria/requirements/158)

    - [345. Establish protections against overflows](/criteria/requirements/345)

- V5.4 Memory, String, and Unmanaged Code Requirements.(5.4.2)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [345. Establish protections against overflows](/criteria/requirements/345)

- V5.4 Memory, String, and Unmanaged Code Requirements.(5.4.3)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [345. Establish protections against overflows](/criteria/requirements/345)

- [V5.5 Deserialization Prevention Requirements.(5.5.1)](/criteria/requirements/321)

- V5.5 Deserialization Prevention Requirements.(5.5.2)

    - [062. Define standard configurations](/criteria/requirements/062)

    - [157. Use the strict mode](/criteria/requirements/157)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- [V5.5 Deserialization Prevention Requirements.(5.5.3)](/criteria/requirements/321)

- [V5.5 Deserialization Prevention Requirements.(5.5.4)](/criteria/requirements/321)

- V6.1 Data Classification.(6.1.1)

    - [185. Encrypt sensitive information](/criteria/requirements/185)

    - [331. Guarantee legal compliance](/criteria/requirements/331)

- [V6.1 Data Classification.(6.1.2)](/criteria/requirements/185)

- [V6.1 Data Classification.(6.1.3)](/criteria/requirements/185)

- [V6.2 Algorithms.(6.2.1)](/criteria/requirements/161)

- V6.2 Algorithms.(6.2.2)

    - [062. Define standard configurations](/criteria/requirements/062)

    - [147. Use pre-existent mechanisms](/criteria/requirements/147)

- V6.2 Algorithms.(6.2.3)

    - [062. Define standard configurations](/criteria/requirements/062)

    - [147. Use pre-existent mechanisms](/criteria/requirements/147)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

- V6.2 Algorithms.(6.2.5)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

    - [266. Disable insecure functionalities](/criteria/requirements/266)

- V6.2 Algorithms.(6.2.6)

    - [346. Use initialization vectors once](/criteria/requirements/346)

    - [351. Assign unique keys to each device](/criteria/requirements/351)

- [V6.2 Algorithms.(6.2.6)](/criteria/requirements/361)

- [V6.2 Algorithms.(6.2.7)](/criteria/requirements/178)

- V6.3 Random Values.(6.3.1)

    - [223. Uniform distribution in random numbers](/criteria/requirements/223)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

    - [346. Use initialization vectors once](/criteria/requirements/346)

- [V6.3 Random Values.(6.3.2)](/criteria/requirements/223)

- [V6.3 Random Values.(6.3.3)](/criteria/requirements/223)

- V6.4 Secret Management.(6.4.1)

    - [128. Define unique data source](/criteria/requirements/128)

    - [145. Protect system cryptographic keys](/criteria/requirements/145)

    - [156. Source code without sensitive information](/criteria/requirements/156)

- [V6.4 Secret Management.(6.4.1)](/criteria/requirements/259)

- V6.4 Secret Management.(6.4.2)

    - [128. Define unique data source](/criteria/requirements/128)

    - [145. Protect system cryptographic keys](/criteria/requirements/145)

- V6.4 Secret Management.(6.4.2)

    - [156. Source code without sensitive information](/criteria/requirements/156)

    - [333. Store salt values separately](/criteria/requirements/333)

- [V7.1 Log Content Requirements.(1.7.2)](/criteria/requirements/331)

- [V7.1 Log Content Requirements.(7.1.1)](/criteria/requirements/083)

- [V7.1 Log Content Requirements.(7.1.2)](/criteria/requirements/083)

- [V7.1 Log Content Requirements.(7.1.3)](/criteria/requirements/075)

- V7.1 Log Content Requirements.(7.1.4)

    - [075. Record exceptional events in logs](/criteria/requirements/075)

    - [079. Record exact occurrence time of events](/criteria/requirements/079)

    - [376. Register severity level](/criteria/requirements/376)

    - [377. Store logs based on valid regulation](/criteria/requirements/377)

    - [378. Use of log management system](/criteria/requirements/378)

- V7.2 Log Processing Requirements.(7.2.1)

    - [075. Record exceptional events in logs](/criteria/requirements/075)

    - [083. Avoid logging sensitive data](/criteria/requirements/083)

    - [085. Allow session history queries](/criteria/requirements/085)

- [V7.2 Log Processing Requirements.(7.2.2)](/criteria/requirements/075)

- V7.3 Log Protection Requirements.(7.3.1)

    - [160. Encode system outputs](/criteria/requirements/160)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- [V7.3 Log Protection Requirements.(7.3.2)](/criteria/requirements/160)

- [V7.3 Log Protection Requirements.(7.3.3)](/criteria/requirements/080)

- [V7.3 Log Protection Requirements.(7.3.4)](/criteria/requirements/079)

- V7.4 Error Handling.(7.4.1)

    - [077. Avoid disclosing technical information](/criteria/requirements/077)

    - [078. Disable debugging events](/criteria/requirements/078)

- V7.4 Error Handling.(7.4.2)

    - [161. Define secure default options](/criteria/requirements/161)

    - [359. Avoid using generic exceptions](/criteria/requirements/359)

- [V7.4 Error Handling.(7.4.3)](/criteria/requirements/161)

- [V8.1 General Data Protection.(8.1.1)](/criteria/requirements/177)

- V8.1 General Data Protection.(8.1.2)

    - [177. Avoid caching and temporary files](/criteria/requirements/177)

    - [183. Delete sensitive data securely](/criteria/requirements/183)

- [V8.1 General Data Protection.(8.1.3)](/criteria/requirements/342)

- V8.1 General Data Protection.(8.1.4)

    - [237. Ascertain human interaction](/criteria/requirements/237)

    - [327. Set a rate limit](/criteria/requirements/327)

- V8.2 Client-side Data Protection.(8.2.1)

    - [177. Avoid caching and temporary files](/criteria/requirements/177)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- V8.2 Client-side Data Protection.(8.2.2)

    - [177. Avoid caching and temporary files](/criteria/requirements/177)

    - [329. Keep client-side storage without sensitive data](/criteria/requirements/329)

- V8.2 Client-side Data Protection.(8.2.3)

    - [031. Discard user session data](/criteria/requirements/031)

    - [146. Remove cryptographic keys from RAM](/criteria/requirements/146)

    - [183. Delete sensitive data securely](/criteria/requirements/183)

- V8.3 Sensitive Private Data.(8.3.1)

    - [032. Avoid session ID leakages](/criteria/requirements/032)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

- [V8.3 Sensitive Private Data.(8.3.2)](/criteria/requirements/317)

- V8.3 Sensitive Private Data.(8.3.3)

    - [189. Specify the purpose of data collection](/criteria/requirements/189)

    - [310. Request user consent](/criteria/requirements/310)

- V8.3 Sensitive Private Data.(8.3.4)

    - [180. Use mock data](/criteria/requirements/180)

    - [184. Obfuscate application data](/criteria/requirements/184)

    - [313. Inform inability to identify users](/criteria/requirements/313)

    - [315. Provide processed data information](/criteria/requirements/315)

    - [331. Guarantee legal compliance](/criteria/requirements/331)

- V8.3 Sensitive Private Data.(8.3.5)

    - [075. Record exceptional events in logs](/criteria/requirements/075)

    - [083. Avoid logging sensitive data](/criteria/requirements/083)

- V8.3 Sensitive Private Data.(8.3.6)

    - [146. Remove cryptographic keys from RAM](/criteria/requirements/146)

    - [183. Delete sensitive data securely](/criteria/requirements/183)

    - [214. Allow data destruction](/criteria/requirements/214)

- V8.3 Sensitive Private Data.(8.3.7)

    - [185. Encrypt sensitive information](/criteria/requirements/185)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

- V8.3 Sensitive Private Data.(8.3.8)

    - [183. Delete sensitive data securely](/criteria/requirements/183)

    - [210. Delete information from mobile devices](/criteria/requirements/210)

    - [360. Remove unnecessary sensitive information](/criteria/requirements/360)

- V9.1 Communications Security Requirements.(9.1.1)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

    - [336. Disable insecure TLS versions](/criteria/requirements/336)

    - [338. Implement perfect forward secrecy](/criteria/requirements/338)

- V9.1 Communications Security Requirements.(9.1.2)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

    - [336. Disable insecure TLS versions](/criteria/requirements/336)

    - [338. Implement perfect forward secrecy](/criteria/requirements/338)

- V9.1 Communications Security Requirements.(9.1.3)

    - [266. Disable insecure functionalities](/criteria/requirements/266)

    - [336. Disable insecure TLS versions](/criteria/requirements/336)

- [V9.2 Server Communications Security Requirements.(9.2.1)](/criteria/requirements/091)

- V9.2 Server Communications Security Requirements.(9.2.2)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

    - [336. Disable insecure TLS versions](/criteria/requirements/336)

- V9.2 Server Communications Security Requirements.(9.2.3)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

    - [264. Request authentication](/criteria/requirements/264)

- V9.2 Server Communications Security Requirements.(9.2.4)

    - [062. Define standard configurations](/criteria/requirements/062)

    - [088. Request client certificates](/criteria/requirements/088)

    - [090. Use valid certificates](/criteria/requirements/090)

- [V9.2 Server Communications Security Requirements.(9.2.5)](/criteria/requirements/075)
