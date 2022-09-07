# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0


class BatchSucceededJob(Exception):
    pass


class BatchFailedJob(Exception):
    pass


class BatchUnknownExitCode(Exception):
    pass


class BatchCancelledJob(Exception):
    pass


class BatchUnstartedJob(Exception):
    pass
