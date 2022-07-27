import { Buffer } from "buffer";

import { useMutation } from "@apollo/client";
import type { ApolloError, FetchResult } from "@apollo/client";
import type { FormikProps } from "formik";
import { Field, Form, Formik } from "formik";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { Fragment, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import { Alert } from "components/Alert";
import type { IAlertProps } from "components/Alert";
import { Button } from "components/Button";
import { Input, Label, Select, TextArea } from "components/Input";
import { Col, Row } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { FormikArrayField } from "scenes/Autoenrollment/components/ArrayField";
import {
  handleValidationError,
  rootSchema,
} from "scenes/Autoenrollment/helpers";
import { VALIDATE_GIT_ACCESS } from "scenes/Autoenrollment/queries";
import type {
  ICheckGitAccessResult,
  IRootAttr,
} from "scenes/Autoenrollment/types";
import { FormikText } from "utils/forms/fields";

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

  const group = "UNITTESTING";

  const [isGitAccessible, setIsGitAccessible] = useState(false);
  const [isDirty, setIsDirty] = useState(false);
  const [showSubmitAlert, setShowSubmitAlert] = useState(false);
  const [showCancelModal, setShowCancelModal] = useState(false);

  function cancelClick(): void {
    setShowCancelModal(true);
  }
  function yesClick(): void {
    mixpanel.track("AutoenrollCancel");
    location.replace("/logout");
  }
  function noClick(): void {
    setShowCancelModal(false);
  }

  const formRef = useRef<FormikProps<IRootAttr>>(null);

  const [validateGitAccess] = useMutation(VALIDATE_GIT_ACCESS, {
    onCompleted: (): void => {
      setIsGitAccessible(true);
      setShowSubmitAlert(false);
      setRootMessages({
        message: t("group.scope.git.repo.credentials.checkAccess.success"),
        type: "success",
      });
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      setShowSubmitAlert(false);
      handleValidationError(graphQLErrors, setRootMessages);
      setIsGitAccessible(false);
    },
  });

  async function checkAccess(): Promise<void> {
    if (formRef.current !== null) {
      const response: FetchResult<ICheckGitAccessResult> =
        await validateGitAccess({
          variables: {
            branch: formRef.current.values.branch,
            credentials: {
              key: formRef.current.values.credentials.key
                ? Buffer.from(formRef.current.values.credentials.key).toString(
                    "base64"
                  )
                : undefined,
              name: formRef.current.values.credentials.name,
              password: formRef.current.values.credentials.password,
              token: formRef.current.values.credentials.token,
              type: formRef.current.values.credentials.type,
              user: formRef.current.values.credentials.user,
            },
            groupName: group,
            url: formRef.current.values.url,
          },
        });
      setRepositoryValues(formRef.current.values);
      const validateSuccess =
        response.data === null || response.data === undefined
          ? false
          : response.data.validateGitAccess.success;
      mixpanel.track("AutoenrollCheckAccess", {
        credentialType: formRef.current.values.credentials.type,
        formErrors: 0,
        success: validateSuccess,
        url: formRef.current.values.url,
      });
    }
  }

  function handleSubmit(): void {
    setRootMessages({
      message: t("group.scope.git.repo.credentials.checkAccess.success"),
      type: "success",
    });
    onCompleted();
  }

  return (
    <div>
      <Formik
        enableReinitialize={true}
        initialValues={initialValues}
        innerRef={formRef}
        name={"newRoot"}
        onSubmit={handleSubmit}
        validationSchema={rootSchema(isGitAccessible, isDirty)}
      >
        {({
          dirty,
          isSubmitting,
          setFieldTouched,
          validateForm,
          values,
        }): JSX.Element => {
          if (isSubmitting) {
            setShowSubmitAlert(false);
          }

          setIsDirty(dirty);

          async function handleAccess(): Promise<void> {
            const validateErrors = await validateForm();
            const errorsLength = Object.keys(validateErrors).length;
            const exclusionsError =
              validateErrors.exclusions === undefined
                ? false
                : errorsLength === 1 && validateErrors.exclusions.length > 0;
            if (errorsLength === 0 || exclusionsError) {
              await checkAccess();
            } else {
              mixpanel.track("AutoenrollCheckAccess", {
                credentialType: values.credentials.type,
                formErrors: errorsLength,
                success: false,
                url: values.url,
              });
              setFieldTouched("branch", true);
              setFieldTouched("credentials.key", true);
              setFieldTouched("credentials.name", true);
              setFieldTouched("credentials.password", true);
              setFieldTouched("credentials.token", true);
              setFieldTouched("credentials.type", true);
              setFieldTouched("credentials.user", true);
              setFieldTouched("env", true);
              setFieldTouched("exclusions", true);
              setFieldTouched("url", true);
            }
          }

          return (
            <Form>
              <Row justify={"flex-start"}>
                <Col large={"50"} medium={"50"} small={"100"}>
                  <Input
                    label={t("autoenrollment.addRoot.url.label")}
                    name={"url"}
                    placeholder={t("autoenrollment.addRoot.url.placeholder")}
                    tooltip={t("autoenrollment.addRoot.url.tooltip")}
                    type={"text"}
                  />
                </Col>
                <Col large={"50"} medium={"50"} small={"100"}>
                  <Input
                    label={t("autoenrollment.addRoot.branch.label")}
                    name={"branch"}
                    placeholder={t("autoenrollment.addRoot.branch.placeholder")}
                    type={"text"}
                  />
                </Col>
                <Col large={"50"} medium={"50"} small={"100"}>
                  <Select
                    label={t("autoenrollment.addRoot.credentials.type.label")}
                    name={"credentials.type"}
                  >
                    <option value={""}>{""}</option>
                    <option value={"HTTPS"}>
                      {t("autoenrollment.addRoot.credentials.type.https")}
                    </option>
                    <option value={"SSH"}>
                      {t("autoenrollment.addRoot.credentials.type.ssh")}
                    </option>
                  </Select>
                </Col>
                <Col large={"50"} medium={"50"} small={"100"}>
                  <Input
                    disabled={values.credentials.type === ""}
                    label={t("autoenrollment.addRoot.credentials.name.label")}
                    name={"credentials.name"}
                    placeholder={t(
                      "autoenrollment.addRoot.credentials.name.placeholder"
                    )}
                  />
                </Col>
                {values.credentials.type === "SSH" && (
                  <Col large={"100"} medium={"100"} small={"100"}>
                    <TextArea
                      label={t("group.scope.git.repo.credentials.sshKey")}
                      name={"credentials.key"}
                      placeholder={t(
                        "group.scope.git.repo.credentials.sshHint"
                      )}
                    />
                  </Col>
                )}
                {values.credentials.type === "HTTPS" && (
                  <Col large={"100"} medium={"100"} small={"100"}>
                    <Select name={"credentials.auth"}>
                      <option value={"TOKEN"}>
                        {t("autoenrollment.addRoot.credentials.auth.token")}
                      </option>
                      <option value={"USER"}>
                        {t("autoenrollment.addRoot.credentials.auth.user")}
                      </option>
                    </Select>
                  </Col>
                )}
                {values.credentials.type === "HTTPS" &&
                  values.credentials.auth === "TOKEN" && (
                    <Col large={"100"} medium={"100"} small={"100"}>
                      <Input
                        label={t("autoenrollment.addRoot.credentials.token")}
                        name={"credentials.token"}
                      />
                    </Col>
                  )}
                {values.credentials.type === "HTTPS" &&
                  values.credentials.auth === "USER" && (
                    <Fragment>
                      <Col large={"50"} medium={"50"} small={"100"}>
                        <Input
                          label={t("autoenrollment.addRoot.credentials.user")}
                          name={"credentials.user"}
                        />
                      </Col>
                      <Col large={"50"} medium={"50"} small={"100"}>
                        <Input
                          label={t(
                            "autoenrollment.addRoot.credentials.password"
                          )}
                          name={"credentials.password"}
                          type={"password"}
                        />
                      </Col>
                    </Fragment>
                  )}
                <Col large={"100"} medium={"100"} small={"100"}>
                  <Input
                    label={t("autoenrollment.addRoot.environment.label")}
                    name={"env"}
                    placeholder={t(
                      "autoenrollment.addRoot.environment.placeholder"
                    )}
                  />
                </Col>
                <Col>
                  <Label
                    tooltip={t("autoenrollment.addRoot.exclusions.tooltip")}
                  >
                    {t("autoenrollment.addRoot.exclusions.label")}
                  </Label>
                </Col>
                <Col large={"100"} medium={"100"} small={"100"}>
                  <FormikArrayField
                    allowEmpty={true}
                    initialValue={""}
                    name={"exclusions"}
                  >
                    {(fieldName: string): JSX.Element => (
                      <Field
                        component={FormikText}
                        name={fieldName}
                        placeholder={t(
                          "autoenrollment.addRoot.exclusions.placeholder"
                        )}
                        type={"text"}
                      />
                    )}
                  </FormikArrayField>
                </Col>
              </Row>
              {!showSubmitAlert && rootMessages.message !== "" && (
                <Alert
                  icon={true}
                  onTimeOut={setShowSubmitAlert}
                  variant={rootMessages.type as IAlertProps["variant"]}
                >
                  {rootMessages.message}
                </Alert>
              )}
              <Row justify={"center"}>
                <Col>
                  {isGitAccessible && !dirty ? (
                    <Button
                      disabled={isSubmitting}
                      type={"submit"}
                      variant={"primary"}
                    >
                      {t("autoenrollment.addRoot.proceed.next")}
                    </Button>
                  ) : (
                    <Button onClick={handleAccess} variant={"primary"}>
                      {t("autoenrollment.addRoot.proceed.checkAccess")}
                    </Button>
                  )}
                </Col>
              </Row>
              <Row justify={"center"}>
                <Col>
                  <Button onClick={cancelClick}>
                    {t("components.modal.cancel")}
                  </Button>
                  <Modal
                    onClose={noClick}
                    open={showCancelModal}
                    title={t("autoenrollment.cancelModal.body")}
                  >
                    <ModalConfirm
                      onCancel={noClick}
                      onConfirm={yesClick}
                      txtCancel={t("autoenrollment.cancelModal.no")}
                      txtConfirm={t("autoenrollment.cancelModal.yes")}
                    />
                  </Modal>
                </Col>
              </Row>
            </Form>
          );
        }}
      </Formik>
    </div>
  );
};

export { AddRoot };
