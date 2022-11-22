/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

interface IAttackedButtonProps {
  isDisabled: boolean;
  onAttacked: () => void;
}
export type { IAttackedButtonProps };