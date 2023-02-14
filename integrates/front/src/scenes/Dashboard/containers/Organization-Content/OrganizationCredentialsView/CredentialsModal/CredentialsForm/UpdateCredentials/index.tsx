import { Form } from "formik";
import React, { Fragment, useCallback, useMemo } from "react";
import { useTranslation } from "react-i18next";

import type { IFormValues } from "../types";
import { Input, Select, TextArea } from "components/Input";
import { Col, Row } from "components/Layout";
import { ModalConfirm } from "components/Modal";
import { Switch } from "components/Switch";

interface IUpdateCredentialsProps {
  values: IFormValues;
  isSubmitting: boolean;
  isEditing: boolean;
  dirty: boolean;
  onCancel: () => void;
  isAdding: boolean;
  setFieldValue: (
    field: string,
    value: unknown,
    shouldValidate?: boolean | undefined
  ) => void;
}

export const UpdateCredentials: React.FC<IUpdateCredentialsProps> = ({
  values,
  isSubmitting,
  isEditing,
  dirty,
  setFieldValue,
  onCancel,
  isAdding,
}): JSX.Element => {
  const buttonMessage = useMemo(
    (): string => (isAdding ? "add" : "edit"),
    [isAdding]
  );
  const { t } = useTranslation();

  // Handle actions
  const toggleNewSecrets = useCallback((): void => {
    setFieldValue("newSecrets", !values.newSecrets);
  }, [setFieldValue, values.newSecrets]);

  const onTypeChange = useCallback(
    (event: React.ChangeEvent<HTMLSelectElement>): void => {
      event.preventDefault();
      if (event.target.value === "SSH") {
        setFieldValue("type", "SSH");
        setFieldValue("auth", "");
        setFieldValue("isPat", false);
      }
      if (event.target.value === "USER") {
        setFieldValue("type", "HTTPS");
        setFieldValue("auth", "USER");
        setFieldValue("isPat", false);
      }
      if (event.target.value === "TOKEN") {
        setFieldValue("type", "HTTPS");
        setFieldValue("auth", "TOKEN");
        setFieldValue("isPat", true);
      }
    },
    [setFieldValue]
  );

  return (
    <Form id={"credentials"}>
      <div style={{ maxWidth: "97%", width: "1100px" }} />
      <Row justify={"start"}>
        <Col lg={100} md={100} sm={100}>
          <Input
            label={t(
              "organization.tabs.credentials.credentialsModal.form.name.label"
            )}
            name={"name"}
            placeholder={t(
              "organization.tabs.credentials.credentialsModal.form.name.placeholder"
            )}
            required={true}
          />
        </Col>
        {isAdding || values.newSecrets ? (
          <Fragment>
            <Col lg={100} md={100} sm={100}>
              <Select
                label={t(
                  "organization.tabs.credentials.credentialsModal.form.type.label"
                )}
                name={"typeCredential"}
                onChange={onTypeChange}
              >
                <option value={"SSH"}>
                  {t(
                    "organization.tabs.credentials.credentialsModal.form.type.ssh"
                  )}
                </option>
                <option value={"TOKEN"}>
                  {t(
                    "organization.tabs.credentials.credentialsModal.form.auth.azureToken"
                  )}
                </option>
                <option value={"USER"}>
                  {t(
                    "organization.tabs.credentials.credentialsModal.form.auth.user"
                  )}
                </option>
              </Select>
            </Col>
            {values.type === "SSH" && (
              <Col lg={100} md={100} sm={100}>
                <TextArea
                  label={t("group.scope.git.repo.credentials.sshKey")}
                  name={"key"}
                  placeholder={t("group.scope.git.repo.credentials.sshHint")}
                  required={true}
                />
              </Col>
            )}
            {values.type === "HTTPS" && values.auth === "TOKEN" && (
              <React.Fragment>
                <Col lg={100} md={100} sm={100}>
                  <Input
                    label={t(
                      "organization.tabs.credentials.credentialsModal.form.token"
                    )}
                    name={"token"}
                    required={true}
                  />
                </Col>
                <Col lg={100} md={100} sm={100}>
                  {values.isPat === true ? (
                    <Input
                      label={t(
                        "organization.tabs.credentials.credentialsModal.form.azureOrganization.text"
                      )}
                      name={"azureOrganization"}
                      required={true}
                      tooltip={t(
                        "organization.tabs.credentials.credentialsModal.form.azureOrganization.tooltip"
                      )}
                    />
                  ) : undefined}
                </Col>
              </React.Fragment>
            )}
            {values.type === "HTTPS" && values.auth === "USER" && (
              <Fragment>
                <Col lg={50} md={50} sm={100}>
                  <Input
                    label={t(
                      "organization.tabs.credentials.credentialsModal.form.user"
                    )}
                    name={"user"}
                    required={true}
                  />
                </Col>
                <Col lg={50} md={50} sm={100}>
                  <Input
                    label={t(
                      "organization.tabs.credentials.credentialsModal.form.password"
                    )}
                    name={"password"}
                    required={true}
                  />
                </Col>
              </Fragment>
            )}
          </Fragment>
        ) : undefined}
      </Row>
      {isEditing ? (
        <Row>
          <Col lg={100} md={100} sm={100}>
            {t("profile.credentialsModal.form.newSecrets")}
            &nbsp;
            <Switch
              checked={values.newSecrets}
              name={"newSecrets"}
              onChange={toggleNewSecrets}
            />
          </Col>
        </Row>
      ) : undefined}
      <br />
      <ModalConfirm
        disabled={isSubmitting || !dirty}
        onCancel={onCancel}
        txtConfirm={t(
          `organization.tabs.credentials.credentialsModal.form.${buttonMessage}`
        )}
      />
    </Form>
  );
};
