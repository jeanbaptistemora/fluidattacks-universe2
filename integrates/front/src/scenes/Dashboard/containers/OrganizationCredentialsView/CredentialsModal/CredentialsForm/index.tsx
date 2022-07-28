import { Form, Formik } from "formik";
import _ from "lodash";
import React, { Fragment } from "react";
import { useTranslation } from "react-i18next";

import type { ICredentialsFormProps, IFormValues } from "./types";
import { validateSchema } from "./utils";

import { Input, TextArea } from "components/Input/Fields";
import { Select } from "components/Input/Fields/Select";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { ModalConfirm } from "components/Modal";

const CredentialsForm: React.FC<ICredentialsFormProps> = (
  props: ICredentialsFormProps
): JSX.Element => {
  const { initialValues, isAdding, onCancel, onSubmit } = props;
  const { t } = useTranslation();

  const defaultInitialValues: IFormValues = {
    auth: "TOKEN",
    key: undefined,
    name: undefined,
    password: undefined,
    token: undefined,
    type: "SSH",
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
      {({ values, isValid, dirty }): JSX.Element => {
        return (
          <Form id={"credentials"}>
            <Row justify={"flex-start"}>
              <Col large={"50"} medium={"50"} small={"100"}>
                <Select
                  label={t(
                    "organization.tabs.credentials.credentialsModal.form.type.label"
                  )}
                  name={"type"}
                >
                  <option value={"HTTPS"}>
                    {t(
                      "organization.tabs.credentials.credentialsModal.form.type.https"
                    )}
                  </option>
                  <option value={"SSH"}>
                    {t(
                      "organization.tabs.credentials.credentialsModal.form.type.ssh"
                    )}
                  </option>
                </Select>
              </Col>
              <Col large={"50"} medium={"50"} small={"100"}>
                <Input
                  label={t(
                    "organization.tabs.credentials.credentialsModal.form.name.label"
                  )}
                  name={"name"}
                  placeholder={t(
                    "organization.tabs.credentials.credentialsModal.form.name.placeholder"
                  )}
                />
              </Col>
              {values.type === "SSH" && (
                <Col large={"100"} medium={"100"} small={"100"}>
                  <TextArea
                    label={t("group.scope.git.repo.credentials.sshKey")}
                    name={"key"}
                    placeholder={t("group.scope.git.repo.credentials.sshHint")}
                  />
                </Col>
              )}
              {values.type === "HTTPS" && (
                <Col large={"100"} medium={"100"} small={"100"}>
                  <Select name={"auth"}>
                    <option value={"TOKEN"}>
                      {t(
                        "organization.tabs.credentials.credentialsModal.form.auth.token"
                      )}
                    </option>
                    <option value={"USER"}>
                      {t(
                        "organization.tabs.credentials.credentialsModal.form.auth.user"
                      )}
                    </option>
                  </Select>
                </Col>
              )}
              {values.type === "HTTPS" && values.auth === "TOKEN" && (
                <Col large={"100"} medium={"100"} small={"100"}>
                  <Input
                    label={t(
                      "organization.tabs.credentials.credentialsModal.form.token"
                    )}
                    name={"token"}
                  />
                </Col>
              )}
              {values.type === "HTTPS" && values.auth === "USER" && (
                <Fragment>
                  <Col large={"50"} medium={"50"} small={"100"}>
                    <Input
                      label={t(
                        "organization.tabs.credentials.credentialsModal.form.user"
                      )}
                      name={"user"}
                    />
                  </Col>
                  <Col large={"50"} medium={"50"} small={"100"}>
                    <Input
                      label={t(
                        "organization.tabs.credentials.credentialsModal.form.password"
                      )}
                      name={"password"}
                      type={"password"}
                    />
                  </Col>
                </Fragment>
              )}
            </Row>
            <br />
            <ModalConfirm
              disabled={!isValid || !dirty}
              onCancel={onCancel}
              txtConfirm={t(
                `organization.tabs.credentials.credentialsModal.form.${
                  isAdding ? "add" : "edit"
                }`
              )}
            />
          </Form>
        );
      }}
    </Formik>
  );
};

export { CredentialsForm };
