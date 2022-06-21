import React from "react";

import { AddButton } from "./AddButton";
import type { IActionButtonsProps } from "./types";

const ActionButtons: React.FC<IActionButtonsProps> = ({
  isAdding,
  onAdd,
}: IActionButtonsProps): JSX.Element | null => {
  const isHided = isAdding;

  return (
    <React.StrictMode>
      <AddButton isHided={isHided} onAdd={onAdd} />
    </React.StrictMode>
  );
};

export { ActionButtons };
