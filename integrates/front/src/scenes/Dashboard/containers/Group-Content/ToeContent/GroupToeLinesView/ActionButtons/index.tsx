import React, { useCallback } from "react";

import { AddButton } from "./AddButton";
import { EditButton } from "./EditButton";
import { ExportButton } from "./ExportButton";
import { VerifyButton } from "./VerifyButton";

interface IActionButtonsProps {
  areToeLinesDatasSelected: boolean;
  isAdding: boolean;
  isInternal: boolean;
  isEditing: boolean;
  isVerifying: boolean;
  onAdd: () => void;
  onEdit: () => void;
  onVerify: () => void;
}

const ActionButtons: React.FC<IActionButtonsProps> = ({
  areToeLinesDatasSelected,
  isAdding,
  isInternal,
  isEditing,
  isVerifying,
  onAdd,
  onEdit,
  onVerify,
}: IActionButtonsProps): JSX.Element | null => {
  const isActiveAction = isAdding || isVerifying || isEditing;

  const Internal = useCallback(
    (): JSX.Element | null =>
      isInternal ? (
        <React.StrictMode>
          <AddButton isDisabled={isActiveAction} onAdd={onAdd} />
          <VerifyButton
            isDisabled={isActiveAction || !areToeLinesDatasSelected}
            onVerify={onVerify}
          />
          <EditButton
            isDisabled={isActiveAction || !areToeLinesDatasSelected}
            onEdit={onEdit}
          />
        </React.StrictMode>
      ) : null,
    [
      areToeLinesDatasSelected,
      isActiveAction,
      isInternal,
      onAdd,
      onEdit,
      onVerify,
    ]
  );

  return (
    <React.Fragment>
      <Internal />
      <ExportButton />
    </React.Fragment>
  );
};

export type { IActionButtonsProps };
export { ActionButtons };
