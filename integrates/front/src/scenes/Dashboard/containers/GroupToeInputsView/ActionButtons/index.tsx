import React from "react";

import { AddButton } from "./AddButton";
import type { IActionButtonsProps } from "./types";

const ActionButtons: React.FC<IActionButtonsProps> = ({
  isAdding,
  isEnumeratingMode,
  isInternal,
  onAdd,
}: IActionButtonsProps): JSX.Element | null => {
  return isInternal ? (
    <React.StrictMode>
      <AddButton
        isDisabled={isAdding}
        isEnumeratingMode={isEnumeratingMode}
        onAdd={onAdd}
      />
    </React.StrictMode>
  ) : null;
};

export { ActionButtons };
