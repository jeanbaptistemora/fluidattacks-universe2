import React from "react";

import { AddButton } from "./AddButton";
import type { IActionButtonsProps } from "./types";

const ActionButtons: React.FC<IActionButtonsProps> = ({
  isAdding,
  isEditing,
  isInternal,
  onAdd,
}: IActionButtonsProps): JSX.Element | null => {
  return isInternal ? (
    <React.StrictMode>
      <AddButton isDisabled={isAdding} isEditing={isEditing} onAdd={onAdd} />
    </React.StrictMode>
  ) : null;
};

export { ActionButtons };
