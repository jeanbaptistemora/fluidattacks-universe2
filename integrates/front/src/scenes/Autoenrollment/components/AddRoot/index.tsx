import { Buffer } from "buffer";

import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Formik } from "formik";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { AddRootForm } from "./form";

import {
  handleValidationError,
  rootSchema,
} from "scenes/Autoenrollment/helpers";
import { VALIDATE_GIT_ACCESS } from "scenes/Autoenrollment/queries";
import type {
  ICheckGitAccessResult,
  IRootAttr,
} from "scenes/Autoenrollment/types";

interface IAddRootProps {
  initialValues: IRootAttr;
  onCompleted: () => void;
  rootMessages: {
    message: string;
    type: string;
  };
  setRepositoryValues: React.Dispatch<React.SetStateAction<IRootAttr>>;
  setRootMessages: React.Dispatch<
    React.SetStateAction<{
      message: string;
      type: string;
    }>
  >;
}

const AddRoot: React.FC<IAddRootProps> = ({
  initialValues,
  onCompleted,
  rootMessages,
  setRepositoryValues,
  setRootMessages,
}: IAddRootProps): JSX.Element => {
  const { t } = useTranslation();

  const [showSubmitAlert, setShowSubmitAlert] = useState(false);

  const [validateGitAccess] =
    useMutation<ICheckGitAccessResult>(VALIDATE_GIT_ACCESS);

  const validateAndSubmit = useCallback(
    async (values: IRootAttr): Promise<void> => {
      try {
        await validateGitAccess({
          variables: {
            branch: values.branch,
            credentials: {
              key: values.credentials.key
                ? Buffer.from(values.credentials.key).toString("base64")
                : undefined,
              name: values.credentials.name,
              password: values.credentials.password,
              token: values.credentials.token,
              type: values.credentials.type,
              user: values.credentials.user,
            },
            url: values.url,
          },
        });
        setShowSubmitAlert(false);
        setRepositoryValues(values);
        setRootMessages({
          message: t("group.scope.git.repo.credentials.checkAccess.success"),
          type: "success",
        });
        onCompleted();
      } catch (error) {
        setShowSubmitAlert(false);
        const { graphQLErrors } = error as ApolloError;
        handleValidationError(graphQLErrors, setRootMessages);
      }
    },
    [onCompleted, setRootMessages, setRepositoryValues, t, validateGitAccess]
  );

  return (
    <div>
      <Formik
        enableReinitialize={true}
        initialValues={initialValues}
        name={"newRoot"}
        onSubmit={validateAndSubmit}
        validationSchema={rootSchema}
      >
        {({ isSubmitting, values, setFieldValue }): JSX.Element => {
          return (
            <AddRootForm
              isSubmitting={isSubmitting}
              rootMessages={rootMessages}
              setFieldValue={setFieldValue}
              setShowSubmitAlert={setShowSubmitAlert}
              showSubmitAlert={showSubmitAlert}
              values={values}
            />
          );
        }}
      </Formik>
    </div>
  );
};

export { AddRoot };
