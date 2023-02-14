---
id: config
title: Configuration
sidebar_label: Configuration
slug: /development/skims/guidelines/configuration
---

Skims uses a configuration file in
[YAML](https://yaml.org/) syntax.

The schema is described below:

```yaml
# Description:
#   Pick a name you like, normally the name of the repository.
# Example:
namespace: repository

# Description:
#   Omit if you want pretty-printed results,
#   Set to a path if you want CSV results.
# Optional:
#   Yes
# Example:
output:
  file_path: /path/to/results.csv
  format: CSV

# Description:
#   Working directory, normally used as the path to the repository.
# Example:
working_dir: /path/to/your/repository

# Description:
#   SAST for source code.
# Example:
path:
  # Description:
  #   Target files used in the analysis.
  # Example:
  include:
    # Absolute path
    - /path/to/file/or/dir
    # Relative path to `working_dir`
    - src/main/java/org/test/Test.java
    # Unix-style globs
    - glob(*)
    - glob(**.java)
    - glob(src/**/test*.py)

# Description:
#   DAST for HTTP.
http:
  # Description:
  #   Target HTTP urls used in the analysis.
  # Example:
  include:
    - http://example.com/

# Description:
#  Reversing checks for Android APKs.
apk:
  # Description:
  #   Target files used in the analysis.
  # Example:
  include:
    # Absolute path
    - /path/to/build/awesome-app-v1.0.apk
    # Relative path to `working_dir`
    - build/awesome-app-v1.0.apk

# Description:
#  DAST for SSL.
ssl:
  # Description:
  #   Target host and port used in the analysis.
  # Example:
  include:
    - host: example.com
      port: 443

# Description:
#  DAST for AWS cloud environments.
dast:
  # Description:
  #   Development credentials used to access the AWS console
  # Example:
  aws_credentials:
    - access_key_id: "000f"
      secret_access_key: "000f"

# Description:
#   Findings to analyze.
#   The complete list of findings can be found here:
#   https://gitlab.com/fluidattacks/universe/-/blob/trunk/skims/manifests/findings.lst
# Optional:
#   Yes, if not present all security findings will be analyzed.
# Example:
checks:
  - F052

# Description:
#   Language to use, valid values are: EN, ES.
# Optional:
#   Yes, defaults to: EN.
language: EN
```
