---
id: capec
title: CAPEC™
sidebar_label: CAPEC™
slug: /criteria/compliance/capec
---

**`Common Attack Pattern Enumeration and Classification`**
helps by providing a comprehensive dictionary
of known patterns of attack
employed by adversaries to exploit
known weaknesses in cyber-enabled capabilities.
It can be used by analysts,
developers, testers,
and educators to advance community understanding
and enhance defenses.
The version used in this section is
[CAPEC List v3.4](https://capec.mitre.org/data/index.html).

### Correlation

- 1: Accessing Functionality Not Properly Constrained by ACLs

    - [096. Set users' required privileges](/criteria/requirements/096)

    - [264. Request authentication](/criteria/requirements/264)

- [2: Inducing Account Lockout](/criteria/requirements/226)

- [3: Using Leading 'Ghost' Character Sequences to Bypass Input Filters](/criteria/requirements/173)

- [4: Using Alternative IP Address Encodings](/criteria/requirements/173)

- 6: Argument Injection

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [342. Validate request parameters](/criteria/requirements/342)

- 7: Blind SQL Injection

    - [169. Use parameterized queries](/criteria/requirements/169)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- 11: Cause Web Server Misclassification

    - [037. Parameters without sensitive data](/criteria/requirements/037)

    - [040. Compare file format and extension](/criteria/requirements/040)

    - [320. Avoid client-side control enforcement](/criteria/requirements/320)

- [12: Choosing Message Identifier](/criteria/requirements/181)

- 13: Subverting Environment Variable Values

    - [046. Manage the integrity of critical files](/criteria/requirements/046)

    - [265. Restrict access to critical processes](/criteria/requirements/265)

- [15: Command Delimiters](/criteria/requirements/173)

- [16: Dictionary-based Password Attack](/criteria/requirements/332)

- 17: Using Malicious Files

    - [041. Scan files for malicious code](/criteria/requirements/041)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

- 18: XSS Targeting Non-Script Elements

    - [160. Encode system outputs](/criteria/requirements/160)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- 19: Embedding Scripts within Scripts

    - [050. Control calls to interpreted code](/criteria/requirements/050)

    - [160. Encode system outputs](/criteria/requirements/160)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [340. Use octet stream downloads](/criteria/requirements/340)

    - [344. Avoid dynamic code execution](/criteria/requirements/344)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- 20: Encryption Brute Forcing

    - [147. Use pre-existent mechanisms](/criteria/requirements/147)

    - [148. Set minimum size of asymmetric encryption](/criteria/requirements/148)

    - [149. Set minimum size of symmetric encryption](/criteria/requirements/149)

    - [150. Set minimum size for hash functions](/criteria/requirements/150)

    - [223. Uniform distribution in random numbers](/criteria/requirements/223)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

    - [370. Use OAEP padding with RSA](/criteria/requirements/370)

    - [371. Use GCM Padding with AES](/criteria/requirements/371)

- 21: Exploitation of Trusted Identifiers

    - [174. Transactions without a distinguishable pattern](/criteria/requirements/174)

    - [178. Use digital signatures](/criteria/requirements/178)

- 22: Exploiting Trust in Client

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [178. Use digital signatures](/criteria/requirements/178)

    - [320. Avoid client-side control enforcement](/criteria/requirements/320)

- 23: File Content Injection

    - [041. Scan files for malicious code](/criteria/requirements/041)

    - [046. Manage the integrity of critical files](/criteria/requirements/046)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

- [24: Filter Failure through Buffer Overflow](/criteria/requirements/161)

- [25: Forced Deadlock](/criteria/requirements/337)

- [26: Leveraging Race Conditions](/criteria/requirements/337)

- 27: Leveraging Race Conditions via Symbolic Links

    - [186. Use the principle of least privilege](/criteria/requirements/186)

    - [337. Make critical logic flows thread safe](/criteria/requirements/337)

- 28: Fuzzing

    - [161. Define secure default options](/criteria/requirements/161)

    - [320. Avoid client-side control enforcement](/criteria/requirements/320)

- [29: Leveraging Time-of-Check and Time-of-Use (TOCTOU) Race Conditions](/criteria/requirements/337)

- [30: Hijacking a Privileged Thread of Execution](/criteria/requirements/337)

- 31: Accessing/Intercepting/Modifying HTTP Cookies

    - [029. Cookies with security attributes](/criteria/requirements/029)

    - [174. Transactions without a distinguishable pattern](/criteria/requirements/174)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

    - [342. Validate request parameters](/criteria/requirements/342)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- 32: XSS Through HTTP Query Strings

    - [160. Encode system outputs](/criteria/requirements/160)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [342. Validate request parameters](/criteria/requirements/342)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- [33: HTTP Request Smuggling](/criteria/requirements/348)

- 34: HTTP Response Splitting

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [320. Avoid client-side control enforcement](/criteria/requirements/320)

- 35: Leverage Executable Code in Non-Executable Files

    - [046. Manage the integrity of critical files](/criteria/requirements/046)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

- [36: Using Unpublished Interfaces](/criteria/requirements/264)

- [38: Leveraging/Manipulating Configuration File Search Paths](/criteria/requirements/046)

- 39: Manipulating Opaque Client-based Data Tokens

    - [026. Encrypt client-side session information](/criteria/requirements/026)

    - [320. Avoid client-side control enforcement](/criteria/requirements/320)

    - [328. Request MFA for critical systems](/criteria/requirements/328)

- 41: Using Meta-characters in E-mail Headers to Inject Malicious Payloads

    - [115. Filter malicious emails](/criteria/requirements/115)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- [42: MIME Conversion](/criteria/requirements/262)

- [43: Exploiting Multiple Input Interpretation Layers](/criteria/requirements/348)

- 48: Passing Local Filenames to Functions That Expect a URL

    - [160. Encode system outputs](/criteria/requirements/160)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- 49: Password Brute Forcing

    - [130. Limit password lifespan](/criteria/requirements/130)

    - [132. Passphrases with at least 4 words](/criteria/requirements/132)

    - [133. Passwords with at least 20 characters](/criteria/requirements/133)

    - [237. Ascertain human interaction](/criteria/requirements/237)

    - [327. Set a rate limit](/criteria/requirements/327)

- [60: Reusing Session IDs (aka Session Replay)](/criteria/requirements/030)

- [70: Try Common Usernames and Passwords](/criteria/requirements/142)

- 74: Manipulating State

    - [026. Encrypt client-side session information](/criteria/requirements/026)

    - [328. Request MFA for critical systems](/criteria/requirements/328)

    - [329. Keep client-side storage without sensitive data](/criteria/requirements/329)

- 94: Man in the Middle Attack

    - [092. Use externally signed certificates](/criteria/requirements/092)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

    - [336. Disable insecure TLS versions](/criteria/requirements/336)

    - [373. Use certificate pinning](/criteria/requirements/373)

- 113: API Manipulation

    - [078. Disable debugging events](/criteria/requirements/078)

    - [154. Eliminate backdoors](/criteria/requirements/154)

- [114: Authentication Abuse](/criteria/requirements/319)

- 115: Authentication Bypass

    - [154. Eliminate backdoors](/criteria/requirements/154)

    - [222. Deny access to the host machine](/criteria/requirements/222)

    - [228. Authenticate using standard protocols](/criteria/requirements/228)

    - [264. Request authentication](/criteria/requirements/264)

    - [319. Make authentication options equally secure](/criteria/requirements/319)

- 116: Excavation

    - [077. Avoid disclosing technical information](/criteria/requirements/077)

    - [078. Disable debugging events](/criteria/requirements/078)

    - [261. Avoid exposing sensitive information](/criteria/requirements/261)

    - [325. Protect WSDL files](/criteria/requirements/325)

    - [339. Avoid storing sensitive files in the web root](/criteria/requirements/339)

    - [365. Avoid exposing technical information](/criteria/requirements/365)

- 117: Interception

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

    - [336. Disable insecure TLS versions](/criteria/requirements/336)

    - [338. Implement perfect forward secrecy](/criteria/requirements/338)

- 122: Privilege Abuse
 
    - [095. Define users with privileges](/criteria/requirements/095)

    - [096. Set users' required privileges](/criteria/requirements/096)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

    - [265. Restrict access to critical processes](/criteria/requirements/265)

    - [280. Restrict service root directory](/criteria/requirements/280)

    - [341. Use the principle of deny by default](/criteria/requirements/341)

- 123: Buffer Manipulation

    - [157. Use the strict mode](/criteria/requirements/157)

    - [158. Use a secure programming language](/criteria/requirements/158)

    - [345. Establish protections against overflows](/criteria/requirements/345)

- 124: Shared Resource Manipulation

    - [337. Make critical logic flows thread safe](/criteria/requirements/337)

    - [374. Use of isolation methods in running applications](/criteria/requirements/374)

- 125: Flooding

    - [062. Define standard configurations](/criteria/requirements/062)

    - [072. Set maximum response time](/criteria/requirements/072)

    - [327. Set a rate limit](/criteria/requirements/327)

- 129: Pointer Manipulation

    - [157. Use the strict mode](/criteria/requirements/157)

    - [158. Use a secure programming language](/criteria/requirements/158)

- 130: Excessive Allocation

    - [062. Define standard configurations](/criteria/requirements/062)

    - [072. Set maximum response time](/criteria/requirements/072)

    - [157. Use the strict mode](/criteria/requirements/157)

    - [160. Encode system outputs](/criteria/requirements/160)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [321. Avoid deserializing untrusted data](/criteria/requirements/321)

    - [327. Set a rate limit](/criteria/requirements/327)

- [131: Resource Leak Exposure](/criteria/requirements/158)

- 137: Parameter Injection

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [342. Validate request parameters](/criteria/requirements/342)

- 148: Content Spoofing

    - [178. Use digital signatures](/criteria/requirements/178)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

    - [330. Verify Subresource Integrity](/criteria/requirements/330)

- 151: Identity Spoofing

    - [062. Define standard configurations](/criteria/requirements/062)

    - [224. Separate keys for encryption and signatures](/criteria/requirements/224)

    - [319. Make authentication options equally secure](/criteria/requirements/319)

- 153: Input Data Manipulation

    - [037. Parameters without sensitive data](/criteria/requirements/037)

    - [160. Encode system outputs](/criteria/requirements/160)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

    - [320. Avoid client-side control enforcement](/criteria/requirements/320)

    - [321. Avoid deserializing untrusted data](/criteria/requirements/321)

    - [342. Validate request parameters](/criteria/requirements/342)

    - [345. Establish protections against overflows](/criteria/requirements/345)

    - [348. Use consistent encoding](/criteria/requirements/348)

- 154: Resource Location Spoofing

    - [046. Manage the integrity of critical files](/criteria/requirements/046)

    - [154: Resource Location Spoofing](/criteria/requirements/050)

    - [154: Resource Location Spoofing](/criteria/requirements/330)

- 161: Infrastructure Manipulation

    - [062. Define standard configurations](/criteria/requirements/062)

    - [080. Prevent log modification](/criteria/requirements/080)

    - [266. Disable insecure functionalities](/criteria/requirements/266)

    - [324. Control redirects](/criteria/requirements/324)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- 165: File Manipulation

    - [037. Parameters without sensitive data](/criteria/requirements/037)

    - [040. Compare file format and extension](/criteria/requirements/040)

    - [041. Scan files for malicious code](/criteria/requirements/041)

    - [042. Validate file format](/criteria/requirements/042)

    - [330. Verify Subresource Integrity](/criteria/requirements/330)

    - [340. Use octet stream downloads](/criteria/requirements/340)

- [169: Footprinting](/criteria/requirements/273)

- [173: Action Spoofing](/criteria/requirements/349)

- 175: Code Inclusion

    - [037. Parameters without sensitive data](/criteria/requirements/037)

    - [050. Control calls to interpreted code](/criteria/requirements/050)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

- 176: Configuration/Environment Manipulation

    - [046. Manage the integrity of critical files](/criteria/requirements/046)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

- [188: Reverse Engineering](/criteria/requirements/159)

- [212: Functionality Misuse](/criteria/requirements/226)

    - [212: Functionality Misuse](/criteria/requirements/266)

    - [212: Functionality Misuse](/criteria/requirements/336)

- [216: Communication Channel Manipulation](/criteria/requirements/181)

    - [216: Communication Channel Manipulation](/criteria/requirements/224)

    - [216: Communication Channel Manipulation](/criteria/requirements/336)

- 224: Fingerprinting

    - [077. Avoid disclosing technical information](/criteria/requirements/077)

    - [325. Protect WSDL files](/criteria/requirements/325)

    - [365. Avoid exposing technical information](/criteria/requirements/365)

- 227: Sustained Client Engagement

    - [023. Terminate inactive user sessions](/criteria/requirements/023)

    - [025. Manage concurrent sessions](/criteria/requirements/025)

- 233: Privilege Escalation

    - [035. Manage privilege modifications](/criteria/requirements/035)

    - [095. Define users with privileges](/criteria/requirements/095)

    - [186. Use the principle of least privilege](/criteria/requirements/186)

    - [337. Make critical logic flows thread safe](/criteria/requirements/337)

    - [341. Use the principle of deny by default](/criteria/requirements/341)

- 240: Resource Injection

    - [160. Encode system outputs](/criteria/requirements/160)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [262. Verify third-party components](/criteria/requirements/262)

- 242: Code Injection

    - [043. Define an explicit content type](/criteria/requirements/043)

    - [044. Define an explicit charset](/criteria/requirements/044)

    - [050. Control calls to interpreted code](/criteria/requirements/050)

    - [117. Do not interpret HTML code](/criteria/requirements/117)

    - [160. Encode system outputs](/criteria/requirements/160)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [262. Verify third-party components](/criteria/requirements/262)

    - [344. Avoid dynamic code execution](/criteria/requirements/344)

- 248: Command Injection

    - [160. Encode system outputs](/criteria/requirements/160)

    - [169. Use parameterized queries](/criteria/requirements/169)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [321. Avoid deserializing untrusted data](/criteria/requirements/321)

    - [344. Avoid dynamic code execution](/criteria/requirements/344)

- 272: Protocol Manipulation

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

    - [336. Disable insecure TLS versions](/criteria/requirements/336)

- 438: Modification During Manufacture

    - [154. Eliminate backdoors](/criteria/requirements/154)

    - [155. Application free of malicious code](/criteria/requirements/155)

    - [273. Define a fixed security suite](/criteria/requirements/273)

- 549: Local Execution of Code

    - [041. Scan files for malicious code](/criteria/requirements/041)

    - [273. Define a fixed security suite](/criteria/requirements/273)

- [554: Functionality Bypass](/criteria/requirements/154)

- 560: Use of Known Domain Credentials

    - [132. Passphrases with at least 4 words](/criteria/requirements/132)

    - [133. Passwords with at least 20 characters](/criteria/requirements/133)

    - [142. Change system default credentials](/criteria/requirements/142)

    - [332. Prevent the use of breached passwords](/criteria/requirements/332)

- [586: Object Injection](/criteria/requirements/321)

- 594: Traffic Injection

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

    - [224. Use secure cryptographic mechanisms](/criteria/requirements/224)

    - [336. Disable insecure TLS versions](/criteria/requirements/336)
