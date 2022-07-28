import type { FormikHelpers } from "formik";

interface IFormValues {
  auth: "TOKEN" | "USER";
  key: string | undefined;
  name: string | undefined;
  newSecrets: boolean;
  password: string | undefined;
  token: string | undefined;
  type: "HTTPS" | "SSH";
  user: string | undefined;
}

interface ICredentialsFormProps {
  initialValues?: IFormValues;
  isAdding: boolean;
  isEditing: boolean;
  onCancel: () => void;
  onSubmit: (
    values: IFormValues,
    formikHelpers: FormikHelpers<IFormValues>
  ) => void;
}

export type { IFormValues, ICredentialsFormProps };
