# Fluid Attacks / Product repository

[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=fluidattacks_product&metric=alert_status)](https://sonarcloud.io/dashboard?id=fluidattacks_product)
[![Build](https://gitlab.com/fluidattacks/product/badges/master/pipeline.svg)](https://gitlab.com/fluidattacks/product/-/commits/master)

**Forces**

[![PyPI](https://img.shields.io/pypi/v/forces)](https://pypi.org/project/forces)
[![Downloads](https://img.shields.io/pypi/dm/forces)](https://pypi.org/project/forces)
[![License](https://img.shields.io/pypi/l/forces)](../LICENSE)
[![Docs](https://img.shields.io/badge/Docs-grey)](./forces/README.md)

**Integrates**

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/fluidattacks/integrates.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/fluidattacks/integrates/context:python)
[![Language grade: TypeScript](https://img.shields.io/lgtm/grade/javascript/g/fluidattacks/integrates.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/fluidattacks/integrates/context:python)
[![Coverage](https://codecov.io/gl/fluidattacks/integrates/branch/master/graph/badge.svg)](https://codecov.io/gl/fluidattacks/integrates)
[![Docs](https://img.shields.io/badge/Docs-grey)](./integrates/README.md)

**Reviews**

[![Docs](https://img.shields.io/badge/Docs-grey)](./reviews/README.md)

**Skims**

[![PyPI](https://img.shields.io/pypi/v/skims)](https://pypi.org/project/skims)
[![Status](https://img.shields.io/pypi/status/skims)](https://pypi.org/project/skims)
[![Downloads](https://img.shields.io/pypi/dm/skims)](https://pypi.org/project/skims)
[![License](https://img.shields.io/pypi/l/skims)](../LICENSE)
[![Docs](https://img.shields.io/badge/Docs-grey)](./skims/README.md)

# Installing

Most products are distributed as a standalone binary:

| Product  | Command            |
|--------- |------------------- |
| Asserts  |  $ asserts --help  |
| Forces   |  $ forces --help   |
| Melts    |  $ melts --help    |
| Reviews  |  $ reviews --help  |
| Skims    |  $ skims --help    |

Additional instructions may be available on the specific product documentation.

**From source**

Clone the repository and install with: `./install.sh`

Uninstall with: `./uninstall.sh`

**Nix**

Install with:

```sh
nix-env \
    -i product \
    -f 'https://gitlab.com/fluidattacks/product/-/archive/master/product-master.tar.gz'
```

Uninstall with: `nix-env -e product`

**Docker**

Launch an interactive container with:

```sh
docker run -it registry.gitlab.com/fluidattacks/product/bin
```

Uninstall by pruning your Docker daemon.
