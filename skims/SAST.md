# Most used languages

Despite what intuition or news may tell,
this are the most used languages.

`Implemented` column means we are able to load a parse tree of the language with
line and column numbers in a sufficiently accurate way
(close to what an official compiler understands) in a sufficiently high number
of random files (>90% of files can be parsed)
and thus we are able to perform taint analysis,
symbolic evaluation, tokens lookup, code-as-data and execution flow, etc.

| Weight | Language         | Implemented |
| :----- | :--------------- | :---------- |
| 9234   | Java             | yes         |
| 8638   | C#               | yes         |
| 3072   | JavaScript       | yes         |
| 2100   | TypeScript       | yes         |
| 1152   | YAML, AWS CFN    | yes         |
| 453    | JSON, NPM FILE   | yes         |
| 415    | Java.properties  | yes         |
| 397    | Python           | yes         |
| 271    | Scala            | yes         |
| 259    | HTML             |             |
| 254    | XML              |             |
| 317    | Jasper           |             |
| 128    | XSD              |             |
| 128    | JKS              |             |
| 112    | VB               |             |
| 218    | CSS              |             |
| 79     | JMX              |             |
| 77     | TXT              |             |
| 76     | ZIP              |             |
| 75     | PDB              |             |
| 60     | SQL              |             |
| 60     | JSP              |             |
| 60     | Conf             |             |
| 57     | Terraform        | yes         |

Weights are proportional to the impact that writing a method for such language
would make to increasing the total number of vulns Skims have found over time.
