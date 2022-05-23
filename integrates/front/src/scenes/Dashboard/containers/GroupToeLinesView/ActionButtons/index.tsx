import React from "react";

import { AddButton } from "./AddButton";
import { EditButton } from "./EditButton";

interface IActionButtonsProps {
  areToeLinesDatasSelected: boolean;
  isAdding: boolean;
  isInternal: boolean;
  isEditing: boolean;
  onAdd: () => void;
  onEdit: () => void;
}

const ActionButtons: React.FC<IActionButtonsProps> = ({
  areToeLinesDatasSelected,
  isAdding,
  isInternal,
  isEditing,
  onAdd,
  onEdit,
}: IActionButtonsProps): JSX.Element | null => {
  return isInternal ? (
    <React.StrictMode>
      <AddButton isDisabled={isAdding} onAdd={onAdd} />
      <EditButton
        isDisabled={isEditing || !areToeLinesDatasSelected}
        onEdit={onEdit}
      />
    </React.StrictMode>
  ) : null;
};

export type { IActionButtonsProps };
export { ActionButtons };
