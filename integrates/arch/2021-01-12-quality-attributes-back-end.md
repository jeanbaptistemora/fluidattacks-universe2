# Quality Attributes, Back-end

We should worry about bold fields

[ISO/IEC 25010](https://iso25000.com/index.php/normas-iso-25000/iso-25010)

- Functional suitability: Overall feature requests are low
- Performance Efficiency
  - Time behavior:
    - Around 1 second response time between 400-600 rpm
    - with some (rare) peaks at 2 seconds between 800-100rpm
  - Resource utilization:
    - 10 machines x 1/2 vcpus (soft/hard) cpus
    - 10 machines x 4/7 GB (soft/hard) ram
  - **Capacity: 50% average, 110% on peaks**
  - **Active users: Can't be measured**
- Compatibility
  - **Co-existence: ports collide with other applications**
  - Interoperability:
    - Cache: Complete interface
    - DB: Partial interface
    - Logging: Complete interface
    - Third party software: Complete interface
- Usability
  - **Appropriateness recognizability: poor, a human has to explain the user**
  - **Learnability: poor, there is no guide/docs besides the API schema**
  - Operability: good, there is an API
  - **User error protection: partial, most operations are validated, some are not**
  - **User interfaces aesthetics: poor**, on most error conditions only a boolean is displayed, the error message is not known to the user
  - Accessibility: good, there is an API
- Reliability
  - Availability: 99.388% (last 7 days)
  - **Fault tolerance: bad, reports being processed are dropped if a fault occurs**
  - Recoverability: ok, we have data backups, we can rollback in 30 minutes
  - Maturity: High under normal operation
- Security
  - Confidentiality: ok
  - Integrity: ok
  - **Non-repudiation: partial, we have no structured system to deal with this**
  - **Authenticity: partial, not all operations record data for this**
  - **Accountability: same as non-repudiation**
- Maintainability
  - **Modularity: null, we have 1 monolith package**
  - **Reusability: null across systems, low within integrates**
  - **Analysability: low, changes have unknown impacts**
  - **Modifiability: low, require experts in order to avoid bugs (still happens sometimes)**
  - Testability, good, although they should be split-able across machines
- Portability
  - Adaptability: Excellent (nix)
  - Installability: Excellent (nix)
  - Replaceability: No other product allows Fluid Attacks to do the same,
    Other products may partially allow the customers to do the same

[Domain Driven Design](https://www.dddcommunity.org/learning-ddd/what_is_ddd/)

- Focus: good, our primary focus is visible in the code
- **Model: poor**
  - concepts are not coherent (project, group, system, namespace)
  - no data-model (NamedTuple)
  - no schema (NamedTuple)
  - fields are optional (dict.get(key) instead of dict[key])
  - types are missing (cast)
- Creative collaboration: poor, only tech people collaborate in the project
