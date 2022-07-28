import type { ICredentialsData } from "../types";

interface ICredentialsModalProps {
  isAdding: boolean;
  isEditing: boolean;
  organizationId: string;
  onClose: () => void;
  selectedCredentials: ICredentialsData | undefined;
  setSelectedCredentials: (
    selectedCredentials: ICredentialsData | undefined
  ) => void;
}

export type { ICredentialsModalProps };
