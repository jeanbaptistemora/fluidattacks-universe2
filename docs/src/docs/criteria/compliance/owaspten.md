---
id: owaspten
title: OWASP TOP 10
sidebar_label: OWASP TOP 10
slug: /criteria/compliance/owaspten
---

The **`OWASP Top 10`**
is a standard awareness document
for developers and web application security.
It represents a broad consensus
about the most critical security risks
to web applications.
The version used in this section is
[OWASP Top 10:2017](https://owasp.org/www-pdf-archive/OWASP_Top_10-2017_%28en%29.pdf.pdf).

### Correlation

- A1-Injection

    - [037. Parameters without sensitive data](/criteria/requirements/037)

    - [043. Define an explicit content type](/criteria/requirements/043)

    - [050. Control calls to interpreted code](/criteria/requirements/050)

    - [117. Do not interpret HTML code](/criteria/requirements/117)

    - [160. Encode system outputs](/criteria/requirements/160)

    - [169. Use parameterized queries](/criteria/requirements/169)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [321. Avoid deserializing untrusted data](/criteria/requirements/321)

    - [340. Use octet stream downloads](/criteria/requirements/340)

    - [342. Validate request parameters](/criteria/requirements/342)

    - [344. Avoid dynamic code execution](/criteria/requirements/344)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- A2-Broken Authentication

    - [023. Terminate inactive user sessions](/criteria/requirements/023)

    - [025. Manage concurrent sessions](/criteria/requirements/025)

    - [026. Encrypt client-side session information](/criteria/requirements/026)

    - [027. Allow session lockout](/criteria/requirements/027)

    - [028. Allow users to log out](/criteria/requirements/028)

    - [029. Cookies with security attributes](/criteria/requirements/029)

    - [030. Avoid object reutilization](/criteria/requirements/030)

    - [031. Discard user session data](/criteria/requirements/031)

    - [032. Avoid session ID leakages](/criteria/requirements/032)

    - [088. Request client certificates](/criteria/requirements/088)

    - [114. Deny access with inactive credentials](/criteria/requirements/114)

    - [131. Deny multiple password changing attempts](/criteria/requirements/131)

    - [139. Set minimum OTP length](/criteria/requirements/139)

    - [140. Define OTP lifespan](/criteria/requirements/140)

    - [141. Force re-authentication](/criteria/requirements/141)

    - [142. Change system default credentials](/criteria/requirements/142)

    - [143. Unique access credentials](/criteria/requirements/143)

    - [153. Out of band transactions](/criteria/requirements/153)

    - [209. Manage passwords in cache](/criteria/requirements/209)

    - [225. Proper authentication responses](/criteria/requirements/225)

    - [226. Avoid account lockouts](/criteria/requirements/226)

    - [228. Authenticate using standard protocols](/criteria/requirements/228)

    - [229. Request access credentials](/criteria/requirements/229)

    - [231. Implement a biometric verification component](/criteria/requirements/231)

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

- A3-Sensitive Data Exposure

    - [024. Transfer information using session objects](/criteria/requirements/024)

    - [029. Cookies with security attributes](/criteria/requirements/029)

    - [032. Avoid session ID leakages](/criteria/requirements/032)

    - [037. Parameters without sensitive data](/criteria/requirements/037)

    - [045. Remove metadata when sharing files](/criteria/requirements/045)

    - [083. Avoid logging sensitive data](/criteria/requirements/083)

    - [145. Protect system cryptographic keys](/criteria/requirements/145)

    - [156. Source code without sensitive information](/criteria/requirements/156)

    - [176. Restrict system objects](/criteria/requirements/176)

    - [177. Avoid caching and temporary files](/criteria/requirements/177)

    - [180. Use mock data](/criteria/requirements/180)

    - [181. Transmit data using secure protocols](/criteria/requirements/181)

    - [183. Delete sensitive data securely](/criteria/requirements/183)

    - [184. Obfuscate application data](/criteria/requirements/184)

    - [185. Encrypt sensitive information](/criteria/requirements/185)

    - [261. Avoid exposing sensitive information](/criteria/requirements/261)

    - [264. Request authentication](/criteria/requirements/264)

    - [300. Mask sensitive data](/criteria/requirements/300)

    - [329. Keep client-side storage without sensitive data](/criteria/requirements/329)

    - [336. Disable insecure TLS versions](/criteria/requirements/336)

    - [338. Implement perfect forward secrecy](/criteria/requirements/338)

    - [339. Avoid storing sensitive files in the web root](/criteria/requirements/339)

    - [349. Include HTTP security headers](/criteria/requirements/349)

    - [375. Remove sensitive data from client-side applications](/criteria/requirements/375)

- A4-XML External Entities (XXE)

    - [062. Define standard configurations](/criteria/requirements/062)

    - [157. Use the strict mode](/criteria/requirements/157)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [321. Avoid deserializing untrusted data](/criteria/requirements/321)

- A5-Broken Access Control

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

    - [341. Use the principle of deny by default](/criteria/requirements/341)

- A6-Security Misconfiguration

    - [043. Define an explicit content type](/criteria/requirements/043)

    - [050. Control calls to interpreted code](/criteria/requirements/050)

    - [062. Define standard configurations](/criteria/requirements/062)

    - [078. Disable debugging events](/criteria/requirements/078)

    - [157. Use the strict mode](/criteria/requirements/157)

    - [205. Configure PIN](/criteria/requirements/205)

    - [206. Configure communication protocols](/criteria/requirements/206)

    - [252. Configure key encryption](/criteria/requirements/252)

    - [259. Segment the organization network](/criteria/requirements/259)

    - [266. Disable insecure functionalities](/criteria/requirements/266)

    - [349. Include HTTP security headers](/criteria/requirements/349)

    - [350. Enable memory protection mechanisms](/criteria/requirements/350)

    - [352. Enable trusted execution](/criteria/requirements/352)

    - [353. Schedule firmware updates](/criteria/requirements/353)

    - [355. Serve files with specific extensions](/criteria/requirements/355)

    - [356. Verify sub-domain names](/criteria/requirements/356)

- A7-Cross-Site Scripting (XSS)

    - [029. Cookies with security attributes](/criteria/requirements/029)

    - [050. Control calls to interpreted code](/criteria/requirements/050)

    - [160. Encode system outputs](/criteria/requirements/160)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [340. Use octet stream downloads](/criteria/requirements/340)

    - [344. Avoid dynamic code execution](/criteria/requirements/344)

    - [349. Include HTTP security headers](/criteria/requirements/349)

- A8-Insecure Deserialization

    - [157. Use the strict mode](/criteria/requirements/157)

    - [173. Discard unsafe inputs](/criteria/requirements/173)

    - [321. Avoid deserializing untrusted data](/criteria/requirements/321)

- A9-Using Components with Known Vulnerabilities

    - [158. Use a secure programming language](/criteria/requirements/158)

    - [262. Verify third-party components](/criteria/requirements/262)

    - [353. Schedule firmware updates](/criteria/requirements/353)

- A10-Insufficient Logging & Monitoring

    - [075. Record exceptional events in logs](/criteria/requirements/075)

    - [079. Record exact occurrence time of events](/criteria/requirements/079)

    - [376. Register severity level](/criteria/requirements/376)

    - [377. Store logs based on valid regulation](/criteria/requirements/377)

    - [378. Use of log management system](/criteria/requirements/378)
