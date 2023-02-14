import { Formik } from "formik";
import _ from "lodash";
import React from "react";

import type { ICredentialsFormProps, IFormValues } from "./types";
import { UpdateCredentials } from "./UpdateCredentials";
import { validateSchema } from "./utils";

const CredentialsForm: React.FC<ICredentialsFormProps> = (
  props: ICredentialsFormProps
): JSX.Element => {
  const { initialValues, isAdding, isEditing, onCancel, onSubmit } = props;

  const defaultInitialValues: IFormValues = {
    auth: "TOKEN",
    azureOrganization: undefined,
    isPat: false,
    key: undefined,
    name: undefined,
    newSecrets: true,
    password: undefined,
    token: undefined,
    type: "SSH",
    typeCredential: "SSH",
    user: undefined,
  };

  return (
    <Formik
      enableReinitialize={true}
      initialValues={
        _.isUndefined(initialValues) ? defaultInitialValues : initialValues
      }
      name={"credentials"}
      onSubmit={onSubmit}
      validationSchema={validateSchema()}
    >
      {({ values, isSubmitting, dirty, setFieldValue }): JSX.Element => {
        return (
          <UpdateCredentials
            dirty={dirty}
            isAdding={isAdding}
            isEditing={isEditing}
            isSubmitting={isSubmitting}
            onCancel={onCancel}
            setFieldValue={setFieldValue}
            values={values}
          />
        );
      }}
    </Formik>
  );
};

export { CredentialsForm };
