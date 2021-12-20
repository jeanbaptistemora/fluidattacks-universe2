import React from "react";

import { EditButton } from "./EditButton";

interface IActionButtonsProps {
  areToeLinesDatasSelected: boolean;
  isInternal: boolean;
  isEditing: boolean;
  onEdit: () => void;
}

const ActionButtons: React.FC<IActionButtonsProps> = ({
  areToeLinesDatasSelected,
  isInternal,
  isEditing,
  onEdit,
}: IActionButtonsProps): JSX.Element | null => {
  return isInternal ? (
    <EditButton
      isDisabled={isEditing || !areToeLinesDatasSelected}
      onEdit={onEdit}
    />
  ) : null;
};

export { ActionButtons, IActionButtonsProps };
