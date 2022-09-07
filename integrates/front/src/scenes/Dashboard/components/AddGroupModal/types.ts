/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IAddGroupModalProps {
  isOpen: boolean;
  organization: string;
  onClose: () => void;
  runTour: boolean;
}

export type { IAddGroupModalProps };
