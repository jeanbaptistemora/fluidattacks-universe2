import { Form, Formik } from "formik";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { HttpsTypeField } from "./HttpsTypeField";
import { NameField } from "./NameField";
import { OrganizationField } from "./OrganizationField";
import { PasswordField } from "./PasswordField";
import { SshKeyField } from "./SshKeyField";
import { TokenField } from "./TokenField";
import { TypeField } from "./TypeField";
import type {
  ICredentialFormProps as ICredentialsFormProps,
  IFormValues,
} from "./types";
import { UserField } from "./UserField";

import { Button } from "components/Button";
import { ModalFooter } from "components/Modal/Footer";
import { Switch } from "components/Switch";
import { Col100, Col50, Row } from "styles/styledComponents";

const CredentialsForm: React.FC<ICredentialsFormProps> = (
  props: ICredentialsFormProps
): JSX.Element => {
  const {
    initialValues,
    isAdding,
    isEditing,
    newSecrets,
    organizations,
    onCancel,
    onSubmit,
    setNewSecrets,
  } = props;
  const { t } = useTranslation();

  // Handle actions
  function toggleNewSecrets(): void {
    setNewSecrets(!newSecrets);
  }

  const defaultInitialValues: IFormValues = {
    accessToken: undefined,
    isHttpsPasswordType: true,
    isHttpsType: false,
    name: undefined,
    organization: undefined,
    password: undefined,
    sshKey: undefined,
    user: undefined,
  };

  if (!(isAdding || isEditing)) {
    return <div />;
  }

  return (
    <Formik
      enableReinitialize={true}
      initialValues={
        _.isUndefined(initialValues) ? defaultInitialValues : initialValues
      }
      name={"credentials"}
      onSubmit={onSubmit}
    >
      {({ values }): JSX.Element => {
        return (
          <Form id={"credentials"}>
            <Row>
              <Col50>
                <NameField />
              </Col50>
              <Col50>
                <OrganizationField
                  disabled={isEditing}
                  organizations={organizations}
                />
              </Col50>
            </Row>
            {newSecrets || !isEditing ? (
              <React.Fragment>
                <Row>
                  {values.isHttpsType ? (
                    <React.Fragment>
                      <Col50>
                        <TypeField />
                      </Col50>
                      <Col50>
                        <HttpsTypeField />
                      </Col50>
                    </React.Fragment>
                  ) : (
                    <Col100>
                      <TypeField />
                    </Col100>
                  )}
                </Row>
                {values.isHttpsType ? (
                  values.isHttpsPasswordType ? (
                    <Row>
                      <Col50>
                        <UserField />
                      </Col50>
                      <Col50>
                        <PasswordField />
                      </Col50>
                    </Row>
                  ) : (
                    <Row>
                      <Col100>
                        <TokenField />
                      </Col100>
                    </Row>
                  )
                ) : (
                  <Row>
                    <Col100>
                      <SshKeyField />
                    </Col100>
                  </Row>
                )}
              </React.Fragment>
            ) : undefined}
            {isEditing ? (
              <Row>
                <Col100>
                  {t("profile.credentialsModal.form.newSecrets")}
                  &nbsp;
                  <Switch
                    checked={newSecrets}
                    name={"newSecrets"}
                    onChange={toggleNewSecrets}
                  />
                </Col100>
              </Row>
            ) : undefined}
            <br />
            <ModalFooter>
              <Button onClick={onCancel} variant={"secondary"}>
                {t("profile.credentialsModal.cancel")}
              </Button>
              <Button type={"submit"} variant={"primary"}>
                {isAdding
                  ? t("profile.credentialsModal.form.add")
                  : t("profile.credentialsModal.form.edit")}
              </Button>
            </ModalFooter>
          </Form>
        );
      }}
    </Formik>
  );
};

export { CredentialsForm };
