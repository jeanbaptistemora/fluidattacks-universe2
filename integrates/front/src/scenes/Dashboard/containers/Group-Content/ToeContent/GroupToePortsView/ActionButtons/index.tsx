import React from "react";

import { AddButton } from "./AddButton";
import { AttackedButton } from "./AttackedButton";
import type { IActionButtonsProps } from "./types";

const ActionButtons: React.FC<IActionButtonsProps> = ({
  arePortsSelected,
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
        isDisabled={isMarkingAsAttacked || !arePortsSelected}
        onAttacked={onMarkAsAttacked}
      />
    </React.StrictMode>
  ) : null;
};

export { ActionButtons };
