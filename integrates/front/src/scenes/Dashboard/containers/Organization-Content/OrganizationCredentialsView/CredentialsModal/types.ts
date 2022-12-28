import type { ICredentialsData } from "../types";

interface ICredentialsModalProps {
  isAdding: boolean;
  isEditing: boolean;
  organizationId: string;
  onClose: () => void;
  selectedCredentials: ICredentialsData[];
  setSelectedCredentials: (selectedCredentials: ICredentialsData[]) => void;
}

interface ISecretsHttpsCredentials {
  password: string | undefined;
  type: string;
  user: string | undefined;
}

interface ISecretsTokenCredentials {
  azureOrganization: string | undefined;
  isPat: boolean;
  token: string | undefined;
  type: string;
}

interface ISecretsSshCredentials {
  key: string;
  type: string;
}
type ISecretsCredentials =
  | ISecretsHttpsCredentials
  | ISecretsSshCredentials
  | ISecretsTokenCredentials;

export type { ICredentialsModalProps, ISecretsCredentials };
