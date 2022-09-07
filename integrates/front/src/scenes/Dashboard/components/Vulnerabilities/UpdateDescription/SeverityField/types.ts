/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface ISeverityFieldProps {
  hasNewVulnSelected: boolean;
  isAcceptedSelected: boolean;
  isAcceptedUndefinedSelected: boolean;
  isInProgressSelected: boolean;
  level: string;
}

export type { ISeverityFieldProps };
