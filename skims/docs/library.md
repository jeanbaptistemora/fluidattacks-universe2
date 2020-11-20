
# [Static Analysis](https://en.wikipedia.org/wiki/Static_application_security_testing)

Static Application Security Testing  or _SAST_ is used to secure software by reviewing the source code in order to identify vulnerabilities.

Below are the vulnerability types and their description that Skims report:

## [F060. Insecure exceptions](https://fluidattacks.com/products/rules/findings/060)

### [CWE-397: Declaration of Throws for Generic Exception](https://cwe.mitre.org/data/definitions/397.html)

Vulnerable code examples:

```java
// Java
public class Test {
  public static void method() throws Exception {};
}
```
