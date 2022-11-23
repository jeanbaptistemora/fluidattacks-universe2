# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import os

CI_COMMIT_REF_NAME = os.environ["CI_COMMIT_REF_NAME"]
CI_COMMIT_SHA = os.environ["CI_COMMIT_SHA"]
JWT_ENCRYPTION_KEY = os.environ["JWT_ENCRYPTION_KEY"]
JWT_SECRET = os.environ["JWT_SECRET"]
TEST_E2E_USER_1 = os.environ["TEST_E2E_USER_1"]
TESTRIGOR_AUTH_TOKEN = os.environ["TESTRIGOR_AUTH_TOKEN"]
TESTRIGOR_SUITE_ID = os.environ["TESTRIGOR_SUITE_ID"]
