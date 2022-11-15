/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IConfirmButtonsProps {
  deletingTag: boolean;
  handleCloseModal: () => void;
  isDescriptionPristine: boolean;
  isRunning: boolean;
  isTreatmentDescriptionPristine: boolean;
  isTreatmentPristine: boolean;
  requestingZeroRisk: boolean;
  updatingVulnerability: boolean;
}

export type { IConfirmButtonsProps };
