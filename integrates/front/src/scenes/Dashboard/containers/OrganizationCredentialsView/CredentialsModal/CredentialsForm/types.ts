/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { FormikHelpers } from "formik";

interface IFormValues {
  auth: "TOKEN" | "USER";
  azureOrganization: string | undefined;
  isPat: boolean | undefined;
  key: string | undefined;
  name: string | undefined;
  newSecrets: boolean;
  password: string | undefined;
  token: string | undefined;
  type: "HTTPS" | "SSH";
  typeCredential: "SSH" | "TOKEN" | "USER";
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
