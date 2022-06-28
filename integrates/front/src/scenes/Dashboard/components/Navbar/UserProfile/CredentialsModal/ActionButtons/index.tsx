import React from "react";

import { AddButton } from "./AddButton";
import { EditSecretsButton } from "./EditSecretsButton";
import type { IActionButtonsProps } from "./types";

const ActionButtons: React.FC<IActionButtonsProps> = ({
  isAdding,
  isEditingSecrets,
  onAdd,
  onEditSecrets,
}: IActionButtonsProps): JSX.Element | null => {
  const isHided = isAdding || isEditingSecrets;

  return (
    <React.StrictMode>
      <AddButton isHided={isHided} onAdd={onAdd} />
      <EditSecretsButton isHided={isHided} onEditSecrets={onEditSecrets} />
    </React.StrictMode>
  );
};

export { ActionButtons };
