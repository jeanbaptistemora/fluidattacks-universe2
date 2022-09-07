/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { AddButton } from "./AddButton";
import { AttackedButton } from "./AttackedButton";
import type { IActionButtonsProps } from "./types";

const ActionButtons: React.FC<IActionButtonsProps> = ({
  areInputsSelected,
  isAdding,
  isInternal,
  isMarkingAsAttacked,
  onAdd,
  onMarkAsAttacked,
}: IActionButtonsProps): JSX.Element | null => {
  return isInternal ? (
    <React.StrictMode>
      <AddButton isDisabled={isAdding} onAdd={onAdd} />
      <AttackedButton
        isDisabled={isMarkingAsAttacked || !areInputsSelected}
        onAttacked={onMarkAsAttacked}
      />
    </React.StrictMode>
  ) : null;
};

export { ActionButtons };
