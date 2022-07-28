import type { ICredentialsData } from "../types";

interface IActionButtonsProps {
  isAdding: boolean;
  isEditing: boolean;
  isRemoving: boolean;
  onAdd: () => void;
  onEdit: () => void;
  onRemove: () => void;
  selectedCredentials: ICredentialsData | undefined;
}

export type { IActionButtonsProps };
