---
id: forces
title: Forces
sidebar_label: Forces
slug: /development/forces
---

Forces is the product responsible
for the client-side part of the [DevSecOps agent](/machine/agent).
On the other hand, [Integrates](/development/products/integrates)
is responsible for the back-end
and the web interface.

## Public Oath

1. A container image with the tag `new` is available in Docker Hub
   under the `fluidattacks/forces` identifier.
1. A customer can follow the
   [Agent Installation Steps](/machine/agent/installation)
   to run Forces successfully.
1. The container image, the CLI,
   and the Agent installation steps are backwards compatible.
1. In the event that backward incompatible changes are needed,
   a proper notification
   and sufficient time is given to the End Users
   to adopt the new changes.

## Architecture

1. Forces is a CLI application written in Python.

   It reports/logs debugging information to
   [Bugsnag](https://www.bugsnag.com/),
   where developers can consume it to improve exception handling
   and improve the program's logic to protect against crashes,
   and communicates with the [ARM (Integrates)](/development/products/integrates)
   through the API
   in order to fetch the End User information,
   and to upload execution logs that the End User
   can inspect through the web interface.

1. The CLI application is packaged into a container image
   that is deployed to Docker Hub
   using two tags:

   - `new`, for production use, deployed from the `trunk` branch.
   - `<name>atfluid`, for development use and testing purposes,
     deployed from the developer branch.

1. Forces is also tested in a schedule using the
   [Compute component of Common](/development/common/compute).

:::tip
You can right-click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Forces](./forces-arch.dot.svg)

## Contributing

Please read the
[contributing](/development/contributing) page first.

### Development Environment

Follow the steps
in the [Development Environment](/development/setup/environment) section of our documentation.

When prompted for an AWS role, choose `dev`,
and when prompted for a Development Environment, pick `forces`.

### Local Environment

#### CLI Application

Just run:

```sh
universe $ m . /integrates/forces
```

This will build and run the Forces CLI application,
including the changes you've made to the source code.

#### Container

Just run:

```bash
# Build the container image (a tarball):
universe $ m . /integrates/forces/container

# Load the tarball into the local Docker repository:
universe $ docker load < ~/.makes/out-forces-container

# Run the container image:
universe $ docker run container-image:latest forces
```

This will build and run the Forces container image,
including the changes you've made to the source code.
