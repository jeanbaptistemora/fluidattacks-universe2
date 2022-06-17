import { Field, Formik } from "formik";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import type { ICredentialFormProps, IFormValues } from "./types";

import type { IOrganizationAttr } from "../types";
import { disabled } from "styles/global.css";
import { Col100, Col50, ControlLabel, Row } from "styles/styledComponents";
import {
  FormikDropdown,
  FormikRadioGroup,
  FormikText,
  FormikTextArea,
} from "utils/forms/fields";
import { composeValidators, required } from "utils/validations";

const CredentialForm: React.FC<ICredentialFormProps> = (
  props: ICredentialFormProps
): JSX.Element => {
  const { organizations } = props;
  const { t } = useTranslation();

  function handleSubmit(values: IFormValues): void {
    // eslint-disable-next-line no-console
    console.log({ values });
  }
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

  return (
    <Formik
      initialValues={initialValues}
      name={"credential"}
      onSubmit={handleSubmit}
    >
      {({ values }): JSX.Element => {
        return (
          <div id={"stakeholder-credential"}>
            <Row>
              <Col50>
                <ControlLabel>
                  {t("profile.credentialModal.form.name.label")}
                </ControlLabel>
                <Field
                  component={FormikText}
                  disabled={disabled}
                  name={"name"}
                  placeholder={t(
                    "profile.credentialModal.form.name.placeholder"
                  )}
                  type={"text"}
                  validate={composeValidators([required])}
                />
              </Col50>
              <Col50>
                <ControlLabel>
                  {t("profile.credentialModal.form.organization")}
                </ControlLabel>
                <Field
                  component={FormikDropdown}
                  disabled={disabled}
                  name={"organization"}
                  validate={composeValidators([required])}
                >
                  <option value={""}>{""}</option>
                  {organizations.map(
                    (organization: IOrganizationAttr): JSX.Element => (
                      <option key={organization.id} value={organization.id}>
                        {_.capitalize(organization.name)}
                      </option>
                    )
                  )}
                </Field>
              </Col50>
            </Row>
            <br />
            <Row>
              <Col50>
                <Field
                  component={FormikRadioGroup}
                  initialState={
                    _.isUndefined(values.isHttpsType)
                      ? t("profile.credentialModal.form.ssh")
                      : values.isHttpsType
                      ? t("profile.credentialModal.form.https")
                      : t("profile.credentialModal.form.ssh")
                  }
                  labels={[
                    t("profile.credentialModal.form.https"),
                    t("profile.credentialModal.form.ssh"),
                  ]}
                  name={"isHttpsType"}
                  type={"Radio"}
                  validate={composeValidators([required])}
                />
              </Col50>
              {values.isHttpsType ? (
                <Col50>
                  <Field
                    component={FormikRadioGroup}
                    initialState={
                      _.isUndefined(values.isHttpsPasswordType)
                        ? t(
                            "profile.credentialModal.form.httpsType.accessToken"
                          )
                        : values.isHttpsPasswordType
                        ? t(
                            "profile.credentialModal.form.httpsType.userAndPassword"
                          )
                        : t(
                            "profile.credentialModal.form.httpsType.accessToken"
                          )
                    }
                    labels={[
                      t(
                        "profile.credentialModal.form.httpsType.userAndPassword"
                      ),
                      t("profile.credentialModal.form.httpsType.accessToken"),
                    ]}
                    name={"isHttpsPasswordType"}
                    type={"Radio"}
                    validate={composeValidators([required])}
                  />
                </Col50>
              ) : undefined}
            </Row>
            <br />
            {values.isHttpsType ? (
              values.isHttpsPasswordType ? (
                <Row>
                  <Col50>
                    <ControlLabel>
                      {t("profile.credentialModal.form.user")}
                    </ControlLabel>
                    <Field
                      component={FormikText}
                      disabled={disabled}
                      name={"user"}
                      type={"text"}
                      validate={composeValidators([required])}
                    />
                  </Col50>
                  <Col50>
                    <ControlLabel>
                      {t("profile.credentialModal.form.password")}
                    </ControlLabel>
                    <Field
                      component={FormikText}
                      disabled={disabled}
                      name={"password"}
                      type={"text"}
                      validate={composeValidators([required])}
                    />
                  </Col50>
                </Row>
              ) : (
                <Row>
                  <Col100>
                    <ControlLabel>
                      {t("profile.credentialModal.form.token")}
                    </ControlLabel>
                    <Field
                      component={FormikText}
                      disabled={disabled}
                      name={"accessToken"}
                      type={"text"}
                      validate={composeValidators([required])}
                    />
                  </Col100>
                </Row>
              )
            ) : (
              <Row>
                <Col100>
                  <ControlLabel>
                    {t("profile.credentialModal.form.sshKey.label")}
                  </ControlLabel>
                  <Field
                    component={FormikTextArea}
                    disabled={disabled}
                    name={"sshKey"}
                    placeholder={t(
                      "profile.credentialModal.form.sshKey.placeholder"
                    )}
                    type={"text"}
                    validate={composeValidators([required])}
                  />
                </Col100>
              </Row>
            )}
          </div>
        );
      }}
    </Formik>
  );
};

export { CredentialForm };
