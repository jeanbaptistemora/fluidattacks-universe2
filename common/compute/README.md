<!--
SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>

SPDX-License-Identifier: MPL-2.0
-->

# Computes

A processing pool micro-service that receives tasks definitions and ensure
they are executed successfully in the cloud.

Currently you can execute any build job here.

It's guaranteed that if the job runs locally, it'll run on the cloud (thanks to Nix).

Just make sure you propagate the required secrets as environment variables as that is the only impurity.
