/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

export interface IHandleAcceptanceButtonProps {
  areVulnerabilitiesPendingToAcceptance: boolean;
  isEditing: boolean;
  isRequestingReattack: boolean;
  isVerifying: boolean;
  openHandleAcceptance: () => void;
}
