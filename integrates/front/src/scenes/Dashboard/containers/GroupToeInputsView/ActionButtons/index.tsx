import React from "react";

import { AddButton } from "./AddButton";
import { RemoveButton } from "./RemoveButton";
import type { IActionButtonsProps } from "./types";

const ActionButtons: React.FC<IActionButtonsProps> = ({
  areInputsSelected,
  isAdding,
  isEnumerating,
  isInternal,
  isRemoving,
  onAdd,
  onRemove,
  onRemoveMode,
}: IActionButtonsProps): JSX.Element | null => {
  return isInternal ? (
    <React.StrictMode>
      <AddButton
        isDisabled={isAdding}
        isEnumerating={isEnumerating}
        isRemoving={isRemoving}
        onAdd={onAdd}
      />
      <RemoveButton
        areInputsSelected={areInputsSelected}
        isEnumerating={isEnumerating}
        isRemoving={isRemoving}
        onRemove={onRemove}
        onRemoveMode={onRemoveMode}
      />
    </React.StrictMode>
  ) : null;
};

export { ActionButtons };
