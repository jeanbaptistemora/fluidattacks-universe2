import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";
import type { ConfigurableValidator } from "revalidate";
import { array, object, string } from "yup";

import { Alert } from "components/Alert";
import type { IAlertProps } from "components/Alert";
import { Button } from "components/Button";
import { ExternalLink } from "components/ExternalLink";
import { Col, Row } from "components/Layout";
import { Modal, ModalFooter } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import type { IOrgAttr } from "scenes/Autoenrollment/types";
import {
  FormikCheckbox,
  FormikDropdown,
  FormikText,
  FormikTextArea,
} from "utils/forms/fields";
import {
  alphaNumeric,
  composeValidators,
  maxLength,
  required,
  validTextField,
} from "utils/validations";

const MAX_DESCRIPTION_LENGTH: number = 200;
const MAX_GROUP_NAME_LENGTH: number = 20;

const maxDescriptionLength: ConfigurableValidator = maxLength(
  MAX_DESCRIPTION_LENGTH
);
const maxGroupNameLength: ConfigurableValidator = maxLength(
  MAX_GROUP_NAME_LENGTH
);

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
}

const AddOrganization: React.FC<IAddOrganizationProps> = ({
  isSubmitting,
  orgMessages,
  orgValues,
  onSubmit,
  setShowSubmitAlert,
  showSubmitAlert,
}: IAddOrganizationProps): JSX.Element => {
  const { t } = useTranslation();
  const { push } = useHistory();

  const [showCancelModal, setShowCancelModal] = useState(false);

  function cancelClick(): void {
    setShowCancelModal(true);
  }
  function yesClick(): void {
    push("/");
  }
  function noClick(): void {
    setShowCancelModal(false);
  }

  const minOrgLenth = 4;
  const maxOrgLength = 10;
  const validations = object().shape({
    groupDescription: string().required(),
    groupName: string().required(),
    organizationName: string()
      .required()
      .min(minOrgLenth)
      .max(maxOrgLength)
      .matches(/^[a-zA-Z]+$/u),
    reportLanguage: string().required(),
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
          <Row justify={"flex-start"}>
            <Col>
              <Row>
                <Col>
                  <strong>
                    {t("autoenrollment.addOrganization.organizationName.label")}
                  </strong>
                  <TooltipWrapper
                    displayClass={"dib"}
                    id={"addGroupTooltip"}
                    message={t("sidebar.newOrganization.modal.nameTooltip")}
                    placement={"top"}
                  >
                    <FontAwesomeIcon
                      color={"#b0b0bf"}
                      icon={faCircleInfo}
                      size={"sm"}
                    />
                  </TooltipWrapper>
                </Col>
              </Row>
              <Field
                component={FormikText}
                name={"organizationName"}
                placeholder={t(
                  "autoenrollment.addOrganization.organizationName.placeholder"
                )}
                type={"text"}
              />
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col>
              <Row>
                <Col>
                  <strong>
                    {t("autoenrollment.addOrganization.groupName.label")}
                  </strong>
                  <TooltipWrapper
                    displayClass={"dib"}
                    id={"addGroupTooltip"}
                    message={t("sidebar.newOrganization.modal.nameTooltip")}
                    placement={"top"}
                  >
                    <FontAwesomeIcon
                      color={"#b0b0bf"}
                      icon={faCircleInfo}
                      size={"sm"}
                    />
                  </TooltipWrapper>
                </Col>
              </Row>
              <Field
                component={FormikText}
                name={"groupName"}
                placeholder={t(
                  "autoenrollment.addOrganization.groupName.placeholder"
                )}
                type={"text"}
                validate={composeValidators([
                  alphaNumeric,
                  maxGroupNameLength,
                  required,
                  validTextField,
                ])}
              />
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col>
              <p>{t("autoenrollment.addOrganization.reportLanguageTip")}</p>
              <strong>
                {t("autoenrollment.addOrganization.reportLanguage")}
              </strong>
              <Field component={FormikDropdown} name={"reportLanguage"}>
                <option value={""}>{""}</option>
                <option value={"EN"}>
                  {t("organization.tabs.groups.newGroup.language.EN")}
                </option>
                <option value={"ES"}>
                  {t("organization.tabs.groups.newGroup.language.ES")}
                </option>
              </Field>
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col>
              <strong>
                {t("autoenrollment.addOrganization.groupDescription.label")}
              </strong>
              <Field
                component={FormikTextArea}
                name={"groupDescription"}
                placeholder={t(
                  "autoenrollment.addOrganization.groupDescription.placeholder"
                )}
                type={"text"}
                validate={composeValidators([
                  required,
                  maxDescriptionLength,
                  validTextField,
                ])}
              />
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col>
              <strong>{t("autoenrollment.addOrganization.roleTitle")}</strong>
              <p>{t("autoenrollment.addOrganization.role")}</p>
            </Col>
          </Row>
          <Row justify={"center"}>
            <Col>
              <Field
                component={FormikCheckbox}
                label={""}
                name={"terms"}
                type={"checkbox"}
                value={"accept"}
              >
                <ExternalLink href={"https://fluidattacks.com/terms-use/"}>
                  {t("autoenrollment.addOrganization.termsOfService")}
                </ExternalLink>
              </Field>
            </Col>
          </Row>
          <Row justify={"center"}>
            <Col>
              {!showSubmitAlert && orgMessages.message !== "" && (
                <Alert
                  icon={true}
                  timer={setShowSubmitAlert}
                  variant={orgMessages.type as IAlertProps["variant"]}
                >
                  {orgMessages.message}
                </Alert>
              )}
              <Button
                disabled={isSubmitting}
                type={"submit"}
                variant={"primary"}
              >
                {t("autoenrollment.addOrganization.proceed")}
              </Button>
            </Col>
          </Row>
          <Row justify={"center"}>
            <Col>
              <Button onClick={cancelClick} variant={"basic"}>
                {t("confirmmodal.cancel")}
              </Button>
              <Modal
                onClose={noClick}
                open={showCancelModal}
                size={"small"}
                title={t("autoenrollment.cancelModal.body")}
              >
                <ModalFooter>
                  <Button onClick={yesClick} variant={"primary"}>
                    {t("autoenrollment.cancelModal.yes")}
                  </Button>
                  <Button onClick={noClick} variant={"basic"}>
                    {t("autoenrollment.cancelModal.no")}
                  </Button>
                </ModalFooter>
              </Modal>
            </Col>
          </Row>
        </Form>
      </Formik>
    </div>
  );
};

export { AddOrganization };
