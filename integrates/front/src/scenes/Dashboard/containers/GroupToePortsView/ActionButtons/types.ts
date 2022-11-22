/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IActionButtonsProps {
  arePortsSelected: boolean;
  isAdding: boolean;
  isMarkingAsAttacked: boolean;
  isInternal: boolean;
  onAdd: () => void;
  onMarkAsAttacked: () => void;
}

export type { IActionButtonsProps };
