import React from "react";

import { AddButton } from "./AddButton";
import { EditButton } from "./EditButton";
import type { IActionButtonsProps } from "./types";

const ActionButtons: React.FC<IActionButtonsProps> = ({
  areInputsSelected,
  isAdding,
  isEditing,
  isInternal,
  onAdd,
  onEdit,
}: IActionButtonsProps): JSX.Element | null => {
  return isInternal ? (
    <React.StrictMode>
      <AddButton isDisabled={isAdding} onAdd={onAdd} />
      <EditButton
        isDisabled={isEditing || !areInputsSelected}
        onEdit={onEdit}
      />
    </React.StrictMode>
  ) : null;
};

export { ActionButtons };
