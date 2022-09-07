# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

"""
Stream consumers for AWS

While the most common approach is to use stream triggers and lambdas on AWS,
we decided to look for an alternative that would reuse pieces of the stack
we already have, such as AWS batch jobs. This, aiming to circumvent the
complexities and disparities between environments inherent to using lambdas.

https://gitlab.com/fluidattacks/universe/-/issues/7049
"""
