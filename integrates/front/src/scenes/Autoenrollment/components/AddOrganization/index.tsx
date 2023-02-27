import { Form, Formik } from "formik";
import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { Alert } from "components/Alert";
import type { IAlertProps } from "components/Alert";
import { Button } from "components/Button";
import { ExternalLink } from "components/ExternalLink";
import { Input, Select, TextArea } from "components/Input";
import { Col, Hr, Row } from "components/Layout";
import { Text } from "components/Text";
import type { IOrgAttr } from "scenes/Autoenrollment/types";
import type { ICountry } from "utils/countries";
import { getCountries } from "utils/countries";
import { regExps } from "utils/validations";

const MAX_DESCRIPTION_LENGTH = 200;
const MAX_GROUP_LENGTH = 20;
const MAX_ORG_LENGTH = 10;
const MIN_ORG_LENGTH = 4;

interface IAddOrganizationProps {
  orgMessages: {
    message: string;
    type: string;
  };
  orgValues: IOrgAttr;
  onSubmit: (values: {
    groupDescription: string;
    groupName: string;
    organizationCountry: string;
    organizationName: string;
    reportLanguage: string;
    terms: string[];
  }) => Promise<void>;
  setShowSubmitAlert: React.Dispatch<React.SetStateAction<boolean>>;
  showSubmitAlert: boolean;
  successMutation: {
    group: boolean;
    organization: boolean;
  };
}

const AddOrganization: React.FC<IAddOrganizationProps> = ({
  orgMessages,
  orgValues,
  onSubmit,
  setShowSubmitAlert,
  showSubmitAlert,
  successMutation,
}: IAddOrganizationProps): JSX.Element => {
  const { t } = useTranslation();
  const [countries, setCountries] = useState<ICountry[]>([]);

  useEffect((): void => {
    const loadCountries = async (): Promise<void> => {
      setCountries(await getCountries());
    };
    void loadCountries();
  }, [setCountries]);

  const validations = object().shape({
    groupDescription: string()
      .required(t("validations.required"))
      .max(
        MAX_DESCRIPTION_LENGTH,
        t("validations.maxLength", { count: MAX_DESCRIPTION_LENGTH })
      )
      .matches(regExps.text, t("validations.text")),
    groupName: string()
      .required(t("validations.required"))
      .min(
        MIN_ORG_LENGTH,
        t("validations.minLength", { count: MIN_ORG_LENGTH })
      )
      .max(
        MAX_GROUP_LENGTH,
        t("validations.maxLength", { count: MAX_GROUP_LENGTH })
      )
      .matches(regExps.alphanumeric, t("validations.alphanumeric")),
    organizationCountry: string().required(t("validations.required")),
    organizationName: string()
      .required(t("validations.required"))
      .min(
        MIN_ORG_LENGTH,
        t("validations.minLength", { count: MIN_ORG_LENGTH })
      )
      .max(
        MAX_ORG_LENGTH,
        t("validations.maxLength", { count: MAX_ORG_LENGTH })
      )
      .matches(/^[a-zA-Z]+$/u, t("validations.alphabetic")),
    reportLanguage: string().required(t("validations.required")),
  });

  return (
    <Formik
      initialValues={orgValues}
      name={"newOrganization"}
      onSubmit={onSubmit}
      validationSchema={validations}
    >
      {({ isSubmitting }): JSX.Element => (
        <Form>
          <Row justify={"start"}>
            <Col lg={100} md={100} sm={100}>
              <Input
                disabled={successMutation.organization}
                label={t("autoenrollment.organizationName.label")}
                name={"organizationName"}
                placeholder={t("autoenrollment.organizationName.placeholder")}
                tooltip={t("autoenrollment.organizationName.tooltip")}
              />
            </Col>
            <Col lg={100} md={100} sm={100}>
              <Select
                disabled={successMutation.organization}
                label={t("autoenrollment.organizationCountry.label")}
                name={"organizationCountry"}
                tooltip={t("autoenrollment.organizationCountry.tooltip")}
              >
                <option value={""}>{""}</option>
                {countries.map(
                  (country): JSX.Element => (
                    <option key={country.id} value={country.name}>
                      {country.name}
                    </option>
                  )
                )}
              </Select>
            </Col>
            <Col lg={100} md={100} sm={100}>
              <Input
                disabled={successMutation.group}
                label={t("autoenrollment.groupName.label")}
                name={"groupName"}
                placeholder={t("autoenrollment.groupName.placeholder")}
                tooltip={t("autoenrollment.groupName.tooltip")}
              />
            </Col>
            <Col lg={100} md={100} sm={100}>
              <Select
                id={"reportLanguage"}
                label={t("autoenrollment.reportLanguage")}
                name={"reportLanguage"}
                tooltip={t("autoenrollment.reportLanguageTip")}
              >
                <option value={""}>{""}</option>
                <option value={"EN"}>
                  {t("organization.tabs.groups.newGroup.language.EN")}
                </option>
                <option value={"ES"}>
                  {t("organization.tabs.groups.newGroup.language.ES")}
                </option>
              </Select>
            </Col>
            <Col lg={100} md={100} sm={100}>
              <TextArea
                label={t("autoenrollment.groupDescription.label")}
                name={"groupDescription"}
                placeholder={t("autoenrollment.groupDescription.placeholder")}
              />
            </Col>
            {!showSubmitAlert && orgMessages.message !== "" ? (
              <Alert
                onTimeOut={setShowSubmitAlert}
                variant={orgMessages.type as IAlertProps["variant"]}
              >
                {orgMessages.message}
              </Alert>
            ) : undefined}
          </Row>
          <div className={"flex justify-start mv3"}>
            <Button disabled={isSubmitting} type={"submit"} variant={"primary"}>
              {t("autoenrollment.proceed")}
            </Button>
          </div>
          <Hr mv={16} />
          <Text bright={9}>
            {t("autoenrollment.acceptTerms")}
            <ExternalLink href={"https://fluidattacks.com/terms-use/"}>
              {t("autoenrollment.termsOfService")}
            </ExternalLink>
            {t("autoenrollment.and")}
            <ExternalLink href={"https://fluidattacks.com/privacy/"}>
              {t("autoenrollment.privacyPolicy")}
            </ExternalLink>
          </Text>
        </Form>
      )}
    </Formik>
  );
};

export { AddOrganization };
