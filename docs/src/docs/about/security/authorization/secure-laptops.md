---
id: secure-laptops
title: Requirements for corporative laptops
sidebar_label: Requirements for corporative laptops
slug: /about/security/authorization/secure-laptops
---

## Device Management

At `Fluid Attacks`,
in order to protect our clients data
we administer our devices with a centralized
device management tool.

This tool enables us to control
how our devices are being used
and improving the devices' security
by installing pre-configured profiles.

Said profiles are configured with different
configurations following our criteria.

## Devices policy

Since we use different configuration
profiles for our laptops for users and admins,
said profiles are configured with different policies:

- Authorization: How the devices can be accessed
  only by its intended users and how permissions
  over said device are managed. We comply with
  the following criteria:

  - Laptops' passwords and data are only
    visible by its user, the use of
    [KeyChain](https://es.wikipedia.org/wiki/Keychain_(software))
    is mandatory for all users for security purposes,
    also to protect passwords saved on the KeyChain
    it automatically gets locked
    when the computer is locked or suspended.
  - Only administrators have access to administration
    data, also admin users permissions are limited for their
    tasks, meaning there's no root users nor root accounts
    enabled.
  - Automatic login is disabled to prevent data leaks,
    password is required for any system configuration and
    to access data.
  - A minimum set of requirements must be followed for passwords:
    a minimum set of 16 characters including at least two
    non alphanumeric, not to have two consecutive nor three
    sequential characters, at least one number and one alphabetic,
    not to be the same as the previous 50 passwords.
  - Passwords have an age limit established, and a history of
    passwords is saved for future passwords checking.

  Requirements:
  [300](/criteria/requirements/300), [185](/criteria/requirements/185),
  [375](/criteria/requirements/375), [096](/criteria/requirements/096),
  [033](/criteria/requirements/033), [341](/criteria/requirements/341),
  [095](/criteria/requirements/095), [341](/criteria/requirements/341),
  [257](/criteria/requirements/257), [186](/criteria/requirements/186),
  [229](/criteria/requirements/229), [227](/criteria/requirements/227),
  [380](/criteria/requirements/380), [300](/criteria/requirements/300),
  [310](/criteria/requirements/310), [133](/criteria/requirements/133),
  [130](/criteria/requirements/130), [129](/criteria/requirements/129),
  [141](/criteria/requirements/141), [369](/criteria/requirements/369).

- Updates: Keep devices and Apps updated
  with its latest and secure versions.

- Users: Control about how login is made on the device and
  local accounts are created improving the security:

  - The guest account allows users access to the system
    without having to create an account or password.
    Guest users are unable to make setting changes,
    cannot remotely login to the system and all created
    files, caches, and passwords are deleted upon logging out.
  - The login window prompts a user for his/her credentials,
    verifies their authorization level and then allows or
    denies the user access to the system.
  - The presence of the Guest home folder can cause
    automated audits to fail when looking for
    compliant settings within all User folders as well.
    Rather than ignoring the folders continued existence
    it is best removed.

  Requirements:
  [142](/criteria/requirements/142), [264](/criteria/requirements/264),
  [265](/criteria/requirements/265), [266](/criteria/requirements/266),
  [319](/criteria/requirements/319).

- Preferences: What the user can accomplish
  with manual configurations on the devices,
  restrict access to unnecessary system configurations
  to devices depending on its use for the different roles.
  Requirements:
  [265](/criteria/requirements/265), [261](/criteria/requirements/261),
  [266](/criteria/requirements/266), [177](/criteria/requirements/177),
  [045](/criteria/requirements/045), [046](/criteria/requirements/046),
  [339](/criteria/requirements/339), [185](/criteria/requirements/185),
  [273](/criteria/requirements/273), [141](/criteria/requirements/141),
  [173](/criteria/requirements/173).

- Networking: How we handle insecure
  protocols and services which can
  compromise the data stored on the devices:

  - HTTP Apache server and NFSD is part of the Operating System
    and can be easily turned on to share files and
    provide remote connectivity to an end user computer.
    Web sharing should only be done through hardened
    web servers and appropriate cloud services.

  Requirements:
  [265](/criteria/requirements/265), [266](/criteria/requirements/266).

- Auditing: How we handle logs and monitor
  our devices for auditing purposes:

  - The audit system writes important operational
    and security information that can be both
    useful for an attacker and a place for an
    attacker to attempt to obfuscate unwanted
    changes that were recorded. As part of
    defense-in-depth the `/etc/security/audit_control`
    configuration and the files in /var/audit should
    be owned only by root with group wheel with read
    only rights and no other access allowed.
    ACLs should not be used for these files.
  - The socketfilter firewall is what is used
    when the firewall is turned on in the Security
    PreferencePane. In order to appropriately monitor
    what access is allowed and denied logging must be enabled.

  Requirements:
  [080](/criteria/requirements/080), [377](/criteria/requirements/377),
  [378](/criteria/requirements/378), [079](/criteria/requirements/079),
  [075](/criteria/requirements/075).

## Requirements

- [033. Restrict administrative access](/criteria/requirements/033)
- [045. Remove metadata when sharing files](/criteria/requirements/045)
- [046. Manage the integrity of critical files](/criteria/requirements/046)
- [075. Record exceptional events in logs](/criteria/requirements/075)
- [079. Record exact occurrence time of events](/criteria/requirements/079)
- [080. Prevent log modification](/criteria/requirements/080)
- [095. Define users with privilege](/criteria/requirements/095)
- [096. Set user's required privileges](/criteria/requirements/096)
- [129. Validate previous passwords](/criteria/requirements/129)
- [130. Limit password lifespan](/criteria/requirements/130)
- [133. Password with at least 20 characters](/criteria/requirements/133)
- [141. Force re-authentication](/criteria/requirements/141)
- [142. Change system default credentials](/criteria/requirements/142)
- [173. Discard unsafe inputs](/criteria/requirements/173)
- [177. Avoid caching and temporary files](/criteria/requirements/177)
- [185. Encrypt sensitive information](/criteria/requirements/185)
- [186. Use the principle of less privilege](/criteria/requirements/186)
- [227. Display access notification](/criteria/requirements/227)
- [229. Request access credentials](/criteria/requirements/229)
- [257. Access based on user credentials](/criteria/requirements/257)
- [261. Avoid exposing sensitive information](/criteria/requirements/261)
- [264. Request authentication](/criteria/requirements/264)
- [265. Restrict access to critical processes](/criteria/requirements/265)
- [266. Disable insecure functionalities](/criteria/requirements/266)
- [273. Define a fixed security suite](/criteria/requirements/273)
- [300. Mask sensitive data](/criteria/requirements/300)
- [310. Request user consent](/criteria/requirements/310)
- [319. Make authentication options equally secure](/criteria/requirements/319)
- [339. Avoid storing sensitive files in the web root](/criteria/requirements/339)
- [341. Use the principle of deny by default](/criteria/requirements/341)
- [369. Set a maximum lifetime in sessions](/criteria/requirements/369)
- [375. Remove sensitive data from client-side applications](/criteria/requirements/375)
- [377. Store logs based on valid regulation](/criteria/requirements/377)
- [378. Use of log management system](/criteria/requirements/378)
- [380. Define a password management tool](/criteria/requirements/380)
