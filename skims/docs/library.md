
# [Static Analysis](https://en.wikipedia.org/wiki/Static_application_security_testing)

Static Application Security Testing  or _SAST_ is used to secure software by reviewing the source code in order to identify vulnerabilities.

Below are the vulnerability types and their description that Skims report:

## [F060][F060] - [CWE-397][CWE-397]

### Java

Code examples:

```java
public class Test {
  // Vulnerable, Exception is generic
  public static void vulnerable() throws Exception {};

  // Safe, CustomException is not generic
  public static void safe() throws CustomException {};
}
```

The following exceptions are considered generic:

- Exception
- Throwable
- lang.Exception
- lang.Throwable
- java.lang.Exception
- java.lang.Throwable

---

[CWE-397]: https://cwe.mitre.org/data/definitions/397.html
[F060]: https://fluidattacks.com/products/rules/findings/060
