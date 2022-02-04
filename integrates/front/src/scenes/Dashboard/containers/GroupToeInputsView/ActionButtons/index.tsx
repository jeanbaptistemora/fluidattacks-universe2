import React from "react";

import { AddButton } from "./AddButton";
import { RemoveButton } from "./RemoveButton";
import type { IActionButtonsProps } from "./types";

const ActionButtons: React.FC<IActionButtonsProps> = ({
  areInputsSelected,
  isAdding,
  isEnumeratingMode,
  isInternal,
  isRemovingMode,
  onAdd,
  onRemove,
  onRemoveMode,
}: IActionButtonsProps): JSX.Element | null => {
  return isInternal ? (
    <React.StrictMode>
      <AddButton
        isDisabled={isAdding}
        isEnumeratingMode={isEnumeratingMode}
        isRemovingMode={isRemovingMode}
        onAdd={onAdd}
      />
      <RemoveButton
        areInputsSelected={areInputsSelected}
        isEnumeratingMode={isEnumeratingMode}
        isRemovingMode={isRemovingMode}
        onRemove={onRemove}
        onRemoveMode={onRemoveMode}
      />
    </React.StrictMode>
  ) : null;
};

export { ActionButtons };
