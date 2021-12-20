import React from "react";

import { EditButton } from "./EditButton";

interface IActionButtonsProps {
  isInternal: boolean;
  isEditing: boolean;
  onEdit: () => void;
}

const ActionButtons: React.FC<IActionButtonsProps> = ({
  isInternal,
  isEditing,
  onEdit,
}: IActionButtonsProps): JSX.Element | null => {
  return isInternal ? (
    <EditButton isEditing={isEditing} onEdit={onEdit} />
  ) : null;
};

export { ActionButtons, IActionButtonsProps };
