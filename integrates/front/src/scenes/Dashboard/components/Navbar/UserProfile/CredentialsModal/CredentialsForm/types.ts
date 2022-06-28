import type { FormikHelpers } from "formik";

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
  areSelectedCredentials: boolean;
  initialValues?: IFormValues;
  isAdding: boolean;
  isEditing: boolean;
  isEditingSecrets: boolean;
  newSecrets: boolean;
  organizations: IOrganizationAttr[];
  onCancel: () => void;
  onSubmit: (
    values: IFormValues,
    formikHelpers: FormikHelpers<IFormValues>
  ) => void;
  setNewSecrets: (newSecrets: boolean) => void;
}

export type { IFormValues, ICredentialFormProps };
