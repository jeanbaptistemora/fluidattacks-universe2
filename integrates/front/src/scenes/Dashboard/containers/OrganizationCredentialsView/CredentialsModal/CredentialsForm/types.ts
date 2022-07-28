import type { FormikHelpers } from "formik";

interface IFormValues {
  auth: "TOKEN" | "USER";
  key: string | undefined;
  name: string | undefined;
  password: string | undefined;
  token: string | undefined;
  type: "HTTPS" | "SSH";
  user: string | undefined;
}

interface ICredentialsFormProps {
  initialValues?: IFormValues;
  isAdding: boolean;
  newSecrets: boolean;
  onCancel: () => void;
  onSubmit: (
    values: IFormValues,
    formikHelpers: FormikHelpers<IFormValues>
  ) => void;
  setNewSecrets: (newSecrets: boolean) => void;
}

export type { IFormValues, ICredentialsFormProps };
