import { Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import { HttpsTypeField } from "./HttpsTypeField";
import { NameField } from "./NameField";
import { OrganizationField } from "./OrganizationField";
import { PasswordField } from "./PasswordField";
import { SshKeyField } from "./SshKeyField";
import { TokenField } from "./TokenField";
import { TypeField } from "./TypeField";
import type { ICredentialFormProps, IFormValues } from "./types";
import { UserField } from "./UserField";

import { Button } from "components/Button";
import { Col100, Col50, Row } from "styles/styledComponents";

const CredentialForm: React.FC<ICredentialFormProps> = (
  props: ICredentialFormProps
): JSX.Element => {
  const { isAdding, isEditing, organizations, onCancel, onSubmit } = props;
  const { t } = useTranslation();

  const initialValues: IFormValues = {
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
      initialValues={initialValues}
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
                <OrganizationField organizations={organizations} />
              </Col50>
            </Row>
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
            <Row>
              <Col100>
                <Button onClick={onCancel} variant={"secondary"}>
                  {t("profile.credentialsModal.cancel")}
                </Button>
                <Button type={"submit"} variant={"primary"}>
                  {t("profile.credentialsModal.add")}
                </Button>
              </Col100>
            </Row>
          </Form>
        );
      }}
    </Formik>
  );
};

export { CredentialForm };
