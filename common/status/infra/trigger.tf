# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "checkly_trigger_group" "main" {
  group_id = checkly_check_group.fluidattacks.id
}
