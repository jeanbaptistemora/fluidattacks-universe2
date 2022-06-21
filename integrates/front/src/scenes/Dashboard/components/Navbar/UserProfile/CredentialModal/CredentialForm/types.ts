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
  isAdding: boolean;
  isEditing: boolean;
  organizations: IOrganizationAttr[];
  onCancel: () => void;
  onSubmit: (
    values: IFormValues,
    formikHelpers: FormikHelpers<IFormValues>
  ) => void;
}

export type { IFormValues, ICredentialFormProps };
