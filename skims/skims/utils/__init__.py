# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import sys

# Increase the level of recursion because some functions must iterate
# through very large trees
sys.setrecursionlimit(2147483647)
