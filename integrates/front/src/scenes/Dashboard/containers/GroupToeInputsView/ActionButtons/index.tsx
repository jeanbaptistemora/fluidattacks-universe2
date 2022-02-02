import React from "react";

import { AddButton } from "./AddButton";
import type { IActionButtonsProps } from "./types";

const ActionButtons: React.FC<IActionButtonsProps> = ({
  isInternal,
  isAdding,
  onAdd,
}: IActionButtonsProps): JSX.Element | null => {
  return isInternal ? <AddButton isDisabled={isAdding} onAdd={onAdd} /> : null;
};

export { ActionButtons };
