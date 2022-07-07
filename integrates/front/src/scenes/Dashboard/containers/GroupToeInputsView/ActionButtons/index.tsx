import React from "react";

import { AddButton } from "./AddButton";
import { AttackedButton } from "./AttackedButton";
import { EditButton } from "./EditButton";
import type { IActionButtonsProps } from "./types";

const ActionButtons: React.FC<IActionButtonsProps> = ({
  areInputsSelected,
  isAdding,
  isEditing,
  isInternal,
  isMarkingAsAttacked,
  onAdd,
  onMarkAsAttacked,
  onEdit,
}: IActionButtonsProps): JSX.Element | null => {
  return isInternal ? (
    <React.StrictMode>
      <AddButton isDisabled={isAdding} onAdd={onAdd} />
      <EditButton
        isDisabled={isEditing || !areInputsSelected}
        onEdit={onEdit}
      />
      <AttackedButton
        isDisabled={isMarkingAsAttacked || !areInputsSelected}
        onAttacked={onMarkAsAttacked}
      />
    </React.StrictMode>
  ) : null;
};

export { ActionButtons };
