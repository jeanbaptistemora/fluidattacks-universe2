import { Form, Formik } from "formik";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { array, object, string } from "yup";

import { Alert } from "components/Alert";
import type { IAlertProps } from "components/Alert";
import { Button } from "components/Button";
import { Checkbox } from "components/Checkbox";
import { ExternalLink } from "components/ExternalLink";
import { Input, Select, TextArea } from "components/Input";
import { Col, Gap, Row } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Text } from "components/Text";
import type { IOrgAttr } from "scenes/Autoenrollment/types";
import { regExps } from "utils/validations";

const MAX_DESCRIPTION_LENGTH = 200;
const MAX_GROUP_LENGTH = 20;
const MAX_ORG_LENGTH = 10;
const MIN_ORG_LENGTH = 4;

interface IAddOrganizationProps {
  isSubmitting: boolean;
  orgMessages: {
    message: string;
    type: string;
  };
  orgValues: IOrgAttr;
  onSubmit: (values: {
    groupDescription: string;
    groupName: string;
    organizationName: string;
    reportLanguage: string;
    terms: string[];
  }) => Promise<void>;
  setShowSubmitAlert: React.Dispatch<React.SetStateAction<boolean>>;
  showSubmitAlert: boolean;
  successMutation: {
    group: boolean;
    organization: boolean;
    repository: boolean;
  };
}

const AddOrganization: React.FC<IAddOrganizationProps> = ({
  isSubmitting,
  orgMessages,
  orgValues,
  onSubmit,
  setShowSubmitAlert,
  showSubmitAlert,
  successMutation,
}: IAddOrganizationProps): JSX.Element => {
  const { t } = useTranslation();

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
      .max(
        MAX_GROUP_LENGTH,
        t("validations.maxLength", { count: MAX_GROUP_LENGTH })
      )
      .matches(regExps.alphanumeric, t("validations.alphanumeric")),
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
    terms: array().of(string()).required().length(1, t("validations.required")),
  });

  return (
    <div>
      <Formik
        initialValues={orgValues}
        name={"newOrganization"}
        onSubmit={onSubmit}
        validationSchema={validations}
      >
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
            <Col lg={100} md={100} sm={100}>
              <Checkbox
                label={
                  <ExternalLink href={"https://fluidattacks.com/terms-use/"}>
                    <Text>{t("autoenrollment.termsOfService")}</Text>
                  </ExternalLink>
                }
                name={"terms"}
                value={"accept"}
              />
            </Col>
            <Text fw={7} mb={1} mt={2}>
              {t("autoenrollment.roleTitle")}
            </Text>
            <Text mb={2}>{t("autoenrollment.role")}</Text>
            {!showSubmitAlert && orgMessages.message !== "" ? (
              <Alert
                icon={true}
                onTimeOut={setShowSubmitAlert}
                variant={orgMessages.type as IAlertProps["variant"]}
              >
                {orgMessages.message}
              </Alert>
            ) : undefined}
          </Row>
          <Gap>
            <Button disabled={isSubmitting} type={"submit"} variant={"primary"}>
              {t("autoenrollment.proceed")}
            </Button>
            <Button onClick={cancelClick}>
              {t("components.modal.cancel")}
            </Button>
          </Gap>
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
        </Form>
      </Formik>
    </div>
  );
};

export { AddOrganization };
