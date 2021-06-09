---
id: cwe
title: CWE™
sidebar_label: CWE™
slug: /criteria/compliance/cwe
---

**`Common Weakness Enumeration`** is a community-developed list
of software and hardware weakness types.
It serves as a common language,
a measuring stick for security tools,
and as a baseline for weakness identification,
mitigation, and prevention efforts.

## Correlation

- CWE-20: Improper Input Validation

    - [160. Encode system outputs](/criteria/requirements/160)

    - [164. Use optimized structures](/criteria/requirements/164)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [342. Validate request parameters](/criteria/requirements/342)

    - [344. Avoid dynamic code execution](/criteria/requirements/344)

- [CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path traversal')](/criteria/requirements/037)

- [CWE-23: Relative Path Traversal](/criteria/requirements/037)

- [CWE-36: Absolute Path Traversal](/criteria/requirements/037)

- CWE-73: External Control of File Name or Path

    - [037. Parameters without sensitive data](/criteria/requirements/037)

    - [381. Use of absolute paths](/criteria/requirements/381)

- [CWE-74: Injection](/criteria/requirements/173)

- [CWE-78: OS Command Injection](/criteria/requirements/173)

- [CWE-79: Cross-site Scripting](/criteria/requirements/160)

- CWE-80: Improper Neutralization of Script-Related HTML Tags in a Web Page

    - [117. Do not interpret HTML code](/criteria/requirements/117)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- CWE-89: SQL Injection

    - [169. Use parameterized queries](/criteria/requirements/169)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- CWE-94: Code Injection

    - [321. Avoid deserializing untrusted data](/criteria/requirements/321)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [344. Avoid dynamic code execution](/criteria/requirements/344)

- CWE-95: Eval Injection

    - [321. Avoid deserializing untrusted data](/criteria/requirements/321)

    - [344. Avoid dynamic code execution](/criteria/requirements/344)

- [CWE-98: PHP Remote File Inclusion](/criteria/requirements/037)

- CWE-116: Improper Encoding or Escaping of Output

    - [043. Define an explicit content type](/criteria/requirements/043)

    - [044. Define an explicit charset](/criteria/requirements/044)

    - [160. Encode system outputs](/criteria/requirements/160)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [348. Use consistent encoding](/criteria/requirements/348)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- [CWE-117: Improper Output Neutralization for Logs](/criteria/requirements/160)

- CWE-120: Classic Buffer Overflow

    - [157. Use the strict mode](/criteria/requirements/157)

    - [158. Use a secure programming language](/criteria/requirements/158)

    - [345. Establish protections against overflows](/criteria/requirements/345)

- [CWE-134: Use of Externally-Controlled Format String](/criteria/requirements/345)

- [CWE-138: Improper Neutralization of Special Elements](/criteria/requirements/173)

- [CWE-147: Improper Neutralization of Input Terminators](/criteria/requirements/173)

- [CWE-159: Improper Handling of Invalid Use of Special Elements](/criteria/requirements/173)

- CWE-173: Improper Handling of Alternate Encoding

    - [044. Define an explicit charset](/criteria/requirements/044)

    - [160. Encode system outputs](/criteria/requirements/160)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- [CWE-176: Improper Handling of Unicode Encoding](/criteria/requirements/160)

- [CWE-190: Integer Overflow or Wraparound](/criteria/requirements/345)

- CWE-200: Exposure of Sensitive Information to an Unauthorized Actor

    - [032. Avoid session ID leakages](/criteria/requirements/032)

    - [080. Prevent log modification](/criteria/requirements/080)
       
    - [180. Use mock data](/criteria/requirements/180)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

    - [184. Obfuscate application data](/criteria/requirements/184)
 
    - [261. Avoid exposing sensitive information](/criteria/requirements/261)

    - [355. Serve files with specific extensions](/criteria/requirements/355)

    - [375. Remove sensitive data from client-side applications](/criteria/requirements/375)

- CWE-203: Observable Differences in Behavior to Error Inputs

    - [225. Proper authentication responses](/criteria/requirements/225)

    - [368. Use of indistinguishable response time](/criteria/requirements/368)

- CWE-204: Observable Response Discrepancy

    - [225. Proper authentication responses](/criteria/requirements/225)

    - [368. Use of indistinguishable response time](/criteria/requirements/368)

- [CWE-208: Observable Timing Discrepancy](/criteria/requirements/368)

- CWE-209: Generation of Error Message Containing Sensitive Information

    - [Avoid disclosing technical information](/criteria/requirements/077)

    - [078. Disable debugging events](/criteria/requirements/078)

- CWE-210: Self-generated Error Message Containing Sensitive Information

    - [077. Avoid disclosing technical information](/criteria/requirements/077)

    - [078. Disable debugging events](/criteria/requirements/078)

- [CWE-212: Improper Removal of Sensitive Information Before Storage or Transfer](/criteria/requirements/317)

- [CWE-213: Exposure of Sensitive Information Due to Incompatible Policies](/criteria/requirements/355)

- [CWE-219: Storage of File with Sensitive Data Under Web Root](/criteria/requirements/339)

- [CWE-223: Omission of Security-relevant Information](/criteria/requirements/376)

- CWE-226: Sensitive Information Uncleared in Resource Before Release for Reuse

    - [146. Remove cryptographic keys from RAM](/criteria/requirements/146)

    - [183. Delete sensitive data securely](/criteria/requirements/183)

- [CWE-233: Improper Handling of Parameters](/criteria/requirements/342)

- [CWE-235: Improper Handling of Extra Parameters](/criteria/requirements/342)

- CWE-250: Execution with Unnecessary Privileges

    - [095. Define users with privileges](/criteria/requirements/095)

    - [096. Set users' required privileges](/criteria/requirements/096)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

    - [326. Detect rooted devices](/criteria/requirements/326)

- [CWE-256: Unprotected Storage of Credentials](/criteria/requirements/380)

- CWE-259: Use of Hard-coded Password

    - [172. Encrypt connection strings](/criteria/requirements/172) 

    - [176. Restrict system objects](/criteria/requirements/156)  

- CWE-263: Password Aging with Long Expiration

    - [130. Limit password lifespan](/criteria/requirements/130)

    - [136. Force temporary password change](/criteria/requirements/136)

    - [137. Change temporary passwords of third parties](/criteria/requirements/137)

    - [138. Define lifespan for temporary passwords](/criteria/requirements/138)

    - [358. Notify upcoming expiration dates](/criteria/requirements/358)

    - [367. Proper generation of temporary passwords](/criteria/requirements/367)

- [CWE-267: Privilege Defined With Unsafe Actions](/criteria/requirements/035)

- CWE-269: Improper Privilege Management

    - [035. Manage privilege modifications](/criteria/requirements/035)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

    - [265. Restrict access to critical processes](/criteria/requirements/265)

- [CWE-272: Least Privilege Violation](/criteria/requirements/186)

- CWE-276: Incorrect Default Permissions

    - [095. Define users with privileges](/criteria/requirements/095)

    - [096. Set users' required privileges](/criteria/requirements/096)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

    - [341. Use the principle of deny by default](/criteria/requirements/341)

- CWE-284: Improper Access Control

    - [176. Restrict system objects](/criteria/requirements/176)

    - [265. Restrict access to critical processes](/criteria/requirements/265)
    
    - [266. Disable insecure functionalities](/criteria/requirements/266)

    - [320. Avoid client-side control enforcement](/criteria/requirements/320)  

- CWE-285: Improper Authorization

    - [035. Manage privilege modifications](/criteria/requirements/035)

    - [080. Prevent log modification](/criteria/requirements/080)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

    - [265. Restrict access to critical processes](/criteria/requirements/265)

    - [320. Avoid client-side control enforcement](/criteria/requirements/320)

- CWE-287: Improper Authentication

    - [030. Avoid object reutilization](/criteria/requirements/030)

    - [096. Set users' required privileges](/criteria/requirements/096)

    - [140. Define OTP lifespan](/criteria/requirements/140)

    - [153. Out of band transactions](/criteria/requirements/153)

    - [176. Restrict system objects](/criteria/requirements/176)

    - [227. Display access notification](/criteria/requirements/227)

    - [237. Ascertain human interaction](/criteria/requirements/237)

    - [264. Request authentication](/criteria/requirements/264)

    - [265. Restrict access to critical processes](/criteria/requirements/265)

    - [319. Make authentication options equally secure](/criteria/requirements/319)

    - [335. Define out of band token lifespan](/criteria/requirements/335)

    - [347. Invalidate previous OTPs](/criteria/requirements/347)

    - [362. Assign MFA mechanisms to a single account](/criteria/requirements/362)    

- [CWE-290: Authentication Bypass by Spoofing](/criteria/requirements/357)

- CWE-294: Authentication Bypass by Capture-replay

    - [030. Avoid object reutilization](/criteria/requirements/030)

    - [335. Define out of band token lifespan](/criteria/requirements/335)

- CWE-295: Improper Certificate Validation

    - [091. Use internally signed certificates](/criteria/requirements/091)

    - [373. Use certificate pinning](/criteria/requirements/373)

- [CWE-297: Improper Validation of Certificate with Host Mismatch](/criteria/requirements/373)

- CWE-299: Improper Check for Certificate Revocation

    - [088. Request client certificates](/criteria/requirements/088)

    - [090. Use valid certificates](/criteria/requirements/090)

- CWE-300: Channel Accessible by Non-Endpoint

    - [092. Use externally signed certificates](/criteria/requirements/092)

    - [373. Use certificate pinning](/criteria/requirements/373)

- CWE-306: Missing Authentication for Critical Function

    - [227. Display access notification](/criteria/requirements/227)

    - [229. Request access credentials](/criteria/requirements/229)

    - [096. Set users' required privileges](/criteria/requirements/096)

    - [176. Restrict system objects](/criteria/requirements/176)
    
    - [264. Request authentication](/criteria/requirements/264)

    - [265. Restrict access to critical processes](/criteria/requirements/265)

    - [319. Make authentication options equally secure](/criteria/requirements/319)

- CWE-307: Improper Restriction of Excessive Authentication Attempts

    - [226. Avoid account lockouts](/criteria/requirements/226)

    - [237. Ascertain human interaction](/criteria/requirements/237)

    - [347. Invalidate previous OTPs](/criteria/requirements/347)

- CWE-308: Use of Single-factor Authentication

    - [030. Avoid object reutilization](/criteria/requirements/030)

    - [231. Implement a biometric verification component](/criteria/requirements/231)

- CWE-311: Missing Encryption of Sensitive Data

    - [172. Encrypt connection strings](/criteria/requirements/172)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

    - [185. Encrypt sensitive information](/criteria/requirements/185)

- CWE-319: Cleartext Transmission of Sensitive Information

    - [032. Avoid session ID leakages](/criteria/requirements/032)

    - [153. Out of band transactions](/criteria/requirements/153)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

    - [336. Disable insecure TLS versions](/criteria/requirements/336)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- CWE-321: Use of Hard-coded Cryptographic Key

    - [145. Protect system cryptographic keys](/criteria/requirements/145)

    - [156. Source code without sensitive information](/criteria/requirements/156)

- [CWE-322: Key Exchange without Entity Authentication](/criteria/requirements/145)

- [CWE-323: Reusing a Nonce, Key Pair in Encryption](/criteria/requirements/145)

- [CWE-324: Use of a Key Past its Expiration Date](/criteria/requirements/361)

- CWE-326: Inadequate Encryption Strength

    - [140. Define OTP lifespan](/criteria/requirements/140)

    - [147. Use pre-existent mechanisms](/criteria/requirements/147)

    - [178. Use digital signatures](/criteria/requirements/178)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

    - [336. Disable insecure TLS versions](/criteria/requirements/336)

    - [338. Implement perfect forward secrecy](/criteria/requirements/338)

    - [346. Use initialization vectors once](/criteria/requirements/346)

    - [351. Assign unique keys to each device](/criteria/requirements/351)

    - [361. Replace cryptographic keys](/criteria/requirements/361)   

- CWE-327: Use of a Broken or Risky Cryptographic Algorithm

    - [147. Use pre-existent mechanisms](/criteria/requirements/147)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

- CWE-330: Use of Insufficiently Random Values

    - [139. Set minimum OTP length](/criteria/requirements/139)

    - [223. Uniform distribution in random numbers](/criteria/requirements/223)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

    - [346. Use initialization vectors once](/criteria/requirements/346)

    - [351. Assign unique keys to each device](/criteria/requirements/351)

    - [372. Proper Use of Initialization Vector (IV)](/criteria/requirements/372)

- CWE-331: Insufficient Entropy

    - [223. Uniform distribution in random numbers](/criteria/requirements/223)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

- CWE-332: Insufficient Entropy in PRNG

    - [223. Uniform distribution in random numbers](/criteria/requirements/223)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

- [CWE-333: Improper Handling of Insufficient Entropy in TRNG](/criteria/requirements/224)

- [CWE-334: Small Space of Random Values](/criteria/requirements/224)

- CWE-335: Incorrect Usage of Seeds in Pseudo-Random Number Generator (PRNG)

    - [223. Uniform distribution in random numbers](/criteria/requirements/223)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

- CWE-338: Use of Cryptographically Weak Pseudo-Random Number Generator (PRNG)

    - [223. Uniform distribution in random numbers](/criteria/requirements/223)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

- CWE-340: Generation of Predictable Numbers or Identifiers

    - [223. Uniform distribution in random numbers](/criteria/requirements/223)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

- CWE-345: Insufficient Verification of Data Authenticity

    - [030. Avoid object reutilization](/criteria/requirements/030)

    - [122. Validate credential ownership](/criteria/requirements/122)

    - [178. Use digital signatures](/criteria/requirements/178)

    - [238. Establish safe recovery](/criteria/requirements/238)
    
    - [357. Use stateless session tokens](/criteria/requirements/357)

- CWE-346: Origin Validation Error

    - [029. Cookies with security attributes](/criteria/requirements/029)

    - [175. Protect pages from clickjacking](/criteria/requirements/175)

- [CWE-347: Improper Verification of Cryptographic Signature](/criteria/requirements/178)

- [CWE-350: Reliance on Reverse DNS Resolution for a Security-Critical Action](/criteria/requirements/356)

- CWE-352: Cross-Site Request Forgery (CSRF)

    - [029. Cookies with security attributes](/criteria/requirements/029)

    - [174. Transactions without a distinguishable pattern](/criteria/requirements/174)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- [CWE-353: Missing Support for Integrity Check](/criteria/requirements/330)

- CWE-359: Exposure of Private Personal Information to an Unauthorized Actor

    - [176. Restrict system objects](/criteria/requirements/176)

    - [180. Use mock data](/criteria/requirements/180)

    - [184. Obfuscate application data](/criteria/requirements/184)

    - [261. Avoid exposing sensitive information](/criteria/requirements/261)

    - [300. Mask sensitive data](/criteria/requirements/300)

    - [375. Remove sensitive data from client-side applications](/criteria/requirements/375)

- [CWE-362: Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition')](/criteria/requirements/337)

- CWE-367: Time-of-check Time-of-use (TOCTOU) Race Condition

    - [337. Make critical logic flows thread safe](/criteria/requirements/337)

    - [353. Schedule firmware updates](/criteria/requirements/353)

- [CWE-384: Session Fixation](/criteria/requirements/025)

- [CWE-390: Detection of Error Condition Without Action](/criteria/requirements/075)

- CWE-396: Declaration of Catch for Generic Exception

    - [161. Define secure default options](/criteria/requirements/161)

    - [359. Avoid using generic exceptions](/criteria/requirements/359)

- CWE-397: Declaration of Throws for Generic Exception

    - [161. Define secure default options](/criteria/requirements/161)

    - [359. Avoid using generic exceptions](/criteria/requirements/359)

- CWE-400: Uncontrolled Resource Consumption

    - [039. Define maximum file size](/criteria/requirements/039)
    
    - [072. Set maximum response time](/criteria/requirements/072)

- CWE-404: Improper Resource Shutdown or Release

    - [023. Terminate inactive user sessions](/criteria/requirements/023)

    - [167. Close unused resources](/criteria/requirements/167)

- [CWE-409: Improper Handling of Highly Compressed Data (Data Amplification)](/criteria/requirements/039)

- [CWE-419: Unprotected Primary Channel](/criteria/requirements/033)

- [CWE-434: Unrestricted Upload of File with Dangerous Type](/criteria/requirements/040)

- [CWE-444: HTTP Request Smuggling](/criteria/requirements/348)

- CWE-451: User Interface (UI) Misrepresentation of Critical Information

    - [175. Protect pages from clickjacking](/criteria/requirements/175)
    
    - [349. Include HTTP security headers](/criteria/requirements/349)

- CWE-459: Incomplete Cleanup

    - [146. Remove cryptographic keys from RAM](/criteria/requirements/146)

    - [183. Delete sensitive data securely](/criteria/requirements/183)

    - [210. Delete information from mobile devices](/criteria/requirements/210)

- [CWE-474: Use of Function with Inconsistent Implementations](/criteria/requirements/162)

- [CWE-478: Missing Default Case in Switch Statement](/criteria/requirements/161)

- CWE-494: Download of Code Without Integrity Check

    - [178. Use digital signatures](/criteria/requirements/178)

    - [330. Verify Subresource Integrity](/criteria/requirements/330)

- [CWE-497: Exposure of Sensitive System Information to an Unauthorized Control Sphere](/criteria/requirements/078)

- [CWE-502: Deserialization of Untrusted Data](/criteria/requirements/321)

- CWE-507: Trojan Horse

    - [155. Application free of malicious code](/criteria/requirements/155)
    
    - [262. Verify third-party components](/criteria/requirements/262)

- CWE-509: Replicating Malicious Code (Virus or Worm)

    - [041. Scan files for malicious code](/criteria/requirements/041)
    
    - [118. Inspect attachments](/criteria/requirements/118)

- CWE-510: Trapdoor

    - [154. Eliminate backdoors](/criteria/requirements/154)

    - [155. Application free of malicious code](/criteria/requirements/155)

    - [323. Exclude unverifiable files](/criteria/requirements/323)

- [CWE-511: Logic or Time Bomb](/criteria/requirements/155)

- CWE-521: Weak Password Requirements

    - [088. Request client certificates](/criteria/requirements/088)

    - [126. Set a password regeneration mechanism](/criteria/requirements/126)

    - [132. Passphrases with at least 4 words](/criteria/requirements/132)

    - [133. Passwords with at least 20 characters](/criteria/requirements/133)

    - [332. Prevent the use of breached passwords](/criteria/requirements/332)

- CWE-522: Insufficiently Protected Credentials

    - [128. Define unique data source](/criteria/requirements/128)

    - [145. Protect system cryptographic keys](/criteria/requirements/145)

    - [156. Source code without sensitive information](/criteria/requirements/156)

    - [375. Remove sensitive data from client-side applications](/criteria/requirements/375)

    - [380. Define a password management tool](/criteria/requirements/380)

- CWE-523: Unprotected Transport of Credentials

    - [153. Out of band transactions](/criteria/requirements/153)
    
    - [349. Include HTTP security headers](/criteria/requirements/349)

- [CWE-524: Use of Cache Containing Sensitive Information](/criteria/requirements/177)

- CWE-525: Use of Web Browser Cache Containing Sensitive Information

    - [177. Avoid caching and temporary files](/criteria/requirements/177)
    
    - [349. Include HTTP security headers](/criteria/requirements/349)

- CWE-532: Insertion of Sensitive Information into Log File

    - [083. Avoid logging sensitive data](/criteria/requirements/083)

    - [376. Register severity level](/criteria/requirements/376)

- CWE-540: Inclusion of Sensitive Information in Source Code

    - [156. Source code without sensitive information](/criteria/requirements/156)
    
    - [375. Remove sensitive data from client-side applications](/criteria/requirements/375)

- CWE-544: Missing Standardized Error Handling Mechanism

    - [075. Record exceptional events in logs](/criteria/requirements/075)

    - [161. Define secure default options](/criteria/requirements/161)

- CWE-548: Exposure of Information Through Directory Listing

    - [339. Avoid storing sensitive files in the web root](/criteria/requirements/339)

    - [261. Avoid exposing sensitive information](/criteria/requirements/261)

- [CWE-552: Files or Directories Accessible to External Parties](/criteria/requirements/339)

- [CWE-561: Dead Code](/criteria/requirements/162)

- CWE-598: Use of GET Request Method With Sensitive Query Strings

    - [032. Avoid session ID leakages](/criteria/requirements/032)
    
    - [181. Transmit data using secure protocols](/criteria/requirements/181)

- [CWE-601: URL Redirection to Untrusted Site ('Open Redirect')](/criteria/requirements/324)

- CWE-602: Client-Side Enforcement of Server-Side Security

    - [122. Validate credential ownership](/criteria/requirements/122)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [238. Establish safe recovery](/criteria/requirements/238)
    
    - [266. Disable insecure functionalities](/criteria/requirements/266)

    - [320. Avoid client-side control enforcement](/criteria/requirements/320)

    - [324. Control redirects](/criteria/requirements/324)

- [CWE-611: Improper Restriction of XML External Entity Reference](/criteria/requirements/157)

- CWE-613: Insufficient Session Expiration

    - [023. Terminate inactive user sessions](/criteria/requirements/023)

    - [028. Allow users to log out](/criteria/requirements/028)

    - [031. Discard user session data](/criteria/requirements/031)

    - [140. Define OTP lifespan](/criteria/requirements/140)

    - [141. Force re-authentication](/criteria/requirements/141)

    - [335. Define out of band token lifespan](/criteria/requirements/335)

    - [369. Set a maximum lifetime in sessions](/criteria/requirements/369)

- [CWE-614: Sensitive Cookie in HTTPS Session Without 'Secure' Attribute](/criteria/requirements/029)

- [CWE-615: Inclusion of Sensitive Information in Source Code Comments](/criteria/requirements/156)

- CWE-620: Unverified Password Change

    - [131. Deny multiple password changing attempts](/criteria/requirements/131)
    
    - [238. Establish safe recovery](/criteria/requirements/238)

    - [301. Notify configuration changes](/criteria/requirements/301)

- CWE-639: Authorization Bypass Through User-Controlled Key

    - [035. Manage privilege modifications](/criteria/requirements/035)

    - [176. Restrict system objects](/criteria/requirements/176)
    
    - [320. Avoid client-side control enforcement](/criteria/requirements/320)

- CWE-640: Weak Password Recovery Mechanism for Forgotten Password

    - [126. Set a password regeneration mechanism](/criteria/requirements/126)

    - [131. Deny multiple password changing attempts](/criteria/requirements/131)
    
    - [238. Establish safe recovery](/criteria/requirements/238)

    - [334. Avoid knowledge-based authentication](/criteria/requirements/334)

    - [367. Proper generation of temporary passwords](/criteria/requirements/367)

- [CWE-641: Improper Restriction of Names for Files and Other Resources](/criteria/requirements/037)

- CWE-642: External Control of Critical State Data

    - [026. Encrypt client-side session information](/criteria/requirements/026)
    
    - [328. Request MFA for critical systems](/criteria/requirements/328)

- [CWE-643: XPath Injection](/criteria/requirements/173)

- [CWE-644: Improper Neutralization of HTTP Headers for Scripting Syntax](/criteria/requirements/349)

- [CWE-645: Overly Restrictive Account Lockout Mechanism](/criteria/requirements/226)

- CWE-646: Reliance on File Name or Extension of Externally-Supplied File

    - [040. Compare file format and extension](/criteria/requirements/040)

    - [042. Validate file format](/criteria/requirements/042)

    - [340. Use octet stream downloads](/criteria/requirements/340)

- [CWE-651: Exposure of WSDL File Containing Sensitive Information](/criteria/requirements/325)

- CWE-693: Protection Mechanism Failure

    - [326. Detect rooted devices](/criteria/requirements/326)

    - [350. Enable memory protection mechanisms](/criteria/requirements/350)

    - [352. Enable trusted execution](/criteria/requirements/352)

    - [354. Prevent firmware downgrades](/criteria/requirements/354)

- CWE-710: Improper Adherence to Coding Standards

    - [366. Associate type to variables](/criteria/requirements/366)

    - [381. Use of absolute paths](/criteria/requirements/381)

- CWE-732: Incorrect Permission Assignment for Critical Resource

    - [186. Use the principle of least privilege](/criteria/requirements/186)
    
    - [341. Use the principle of deny by default](/criteria/requirements/341)    

- CWE-749: Exposed Dangerous Method or Function

    - [041. Scan files for malicious code](/criteria/requirements/041)
    
    - [266. Disable insecure functionalities](/criteria/requirements/266)

- CWE-759: Use of a One-Way Hash without a Salt

    - [134. Store passwords with salt](/criteria/requirements/134)

    - [135. Passwords with random salt](/criteria/requirements/135)

- CWE-760: Use of a One-Way Hash with a Predictable Salt

    - [134. Store passwords with salt](/criteria/requirements/134)

    - [135. Passwords with random salt](/criteria/requirements/135)

- CWE-770: Allocation of Resources Without Limits or Throttling

    - [039. Define maximum file size](/criteria/requirements/039)
    
    - [072. Set maximum response time](/criteria/requirements/072)

    - [327. Set a rate limit](/criteria/requirements/327)

- CWE-778: Insufficient Logging

    - [046. Manage the integrity of critical files](/criteria/requirements/046)

    - [075. Record exceptional events in logs](/criteria/requirements/075)

    - [079. Record exact occurrence time of events](/criteria/requirements/079)

    - [376. Register severity level](/criteria/requirements/376)

    - [377. Store logs based on valid regulation](/criteria/requirements/377)

    - [378. Use of log management system](/criteria/requirements/378)

- [CWE-779: Logging of Excessive Data](/criteria/requirements/322)

- CWE-798: Use of Hard-coded Credentials

    - [156. Source code without sensitive information](/criteria/requirements/156)

    - [172. Encrypt connection strings](/criteria/requirements/172)

    - [357. Use stateless session tokens](/criteria/requirements/357)

- CWE-799: Improper Control of Interaction Frequency

    - [237. Ascertain human interaction](/criteria/requirements/237)
    
    - [327. Set a rate limit](/criteria/requirements/327)

- [CWE-804: Guessable CAPTCHA](/criteria/requirements/237)

- CWE-829: Inclusion of Functionality from Untrusted Control Sphere

    - [050. Control calls to interpreted code](/criteria/requirements/050)

    - [302. Declare dependencies explicitly](/criteria/requirements/302)

- [CWE-830: Inclusion of Web Functionality from an Untrusted Source](/criteria/requirements/050)

- [CWE-915: Improperly Controlled Modification of Dynamically-Determined Object Attributes](/criteria/requirements/342)

- CWE-916: Use of Password Hash With Insufficient Computational Effort

    - [127. Store hashed passwords](/criteria/requirements/127)

    - [134. Store passwords with salt](/criteria/requirements/134)

    - [135. Passwords with random salt](/criteria/requirements/135)

    - [333. Store salt values separately](/criteria/requirements/333)

- [CWE-918: Server-Side Request Forgery (SSRF)](/criteria/requirements/324)

- CWE-922: Insecure Storage of Sensitive Information

    - [329. Keep client-side storage without sensitive data](/criteria/requirements/329)

    - [339. Avoid storing sensitive files in the web root](/criteria/requirements/339)

- CWE-923: Improper Restriction of Communication Channel to Intended Endpoints

    - [259. Segment the organization network](/criteria/requirements/259)

    - [273. Define a fixed security suite](/criteria/requirements/273)

- [CWE-943: Improper Neutralization of Special Elements in Data Query Logic](/criteria/requirements/173)

- [CWE-1004: Sensitive Cookie Without 'HttpOnly' Flag](/criteria/requirements/029)

- CWE-1021: Improper Restriction of Rendered UI Layers or Frames

    - [324. Control redirects](/criteria/requirements/324)

    - [340. Use octet stream downloads](/criteria/requirements/340)
    
    - [349. Include HTTP security headers](/criteria/requirements/349)

- [CWE-1085: Invokable Control Element with Excessive Volume of Commented-out Code](/criteria/requirements/171)

- [CWE-1120: Excessive Code Complexity](/criteria/requirements/379)

- [CWE-1121: Excessive McCabe Cyclomatic Complexity](/criteria/requirements/379)

- [CWE-1204: Generation of Weak Initialization Vector (IV)](/criteria/requirements/372)

- [CWE-1230: Exposure of Sensitive Information Through Metadata](/criteria/requirements/045)

- CWE-1233: Improper Hardware Lock Protection for Security Sensitive Controls

    - [350. Enable memory protection mechanisms](/criteria/requirements/350)

    - [352. Enable trusted execution](/criteria/requirements/352)

- CWE-1269: Product Released in Non-Release Configuration

    - [078. Disable debugging events](/criteria/requirements/078)

    - [154. Eliminate backdoors](/criteria/requirements/154)

    - [159. Obfuscate code](/criteria/requirements/159)
