# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
let
  m = import (import ./makes.lock.nix).makesSrc;
in {inherit m;}
