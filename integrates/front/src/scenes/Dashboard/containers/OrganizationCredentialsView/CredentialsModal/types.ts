import type { ICredentialsData } from "../types";

interface ICredentialsModalProps {
  isAdding: boolean;
  isEditing: boolean;
  organizationId: string;
  onClose: () => void;
  selectedCredentials: ICredentialsData[];
  setSelectedCredentials: (selectedCredentials: ICredentialsData[]) => void;
}

export type { ICredentialsModalProps };
