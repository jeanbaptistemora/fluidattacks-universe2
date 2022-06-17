import type { IOrganizationAttr } from "../types";

interface IFormValues {
  accessToken: string | undefined;
  isHttpsPasswordType: boolean;
  isHttpsType: boolean;
  name: string | undefined;
  organization: string | undefined;
  password: string | undefined;
  sshKey: string | undefined;
  user: string | undefined;
}

interface ICredentialFormProps {
  organizations: IOrganizationAttr[];
}

export type { IFormValues, ICredentialFormProps };
