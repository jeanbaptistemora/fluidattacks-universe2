import type { ICredentialsData } from "../types";

interface IActionButtonsProps {
  isAdding: boolean;
  isRemoving: boolean;
  onAdd: () => void;
  onRemove: () => void;
  selectedCredentials: ICredentialsData | undefined;
}

export type { IActionButtonsProps };
