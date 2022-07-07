import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Form, Formik } from "formik";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { Fragment, useState } from "react";
import { useTranslation } from "react-i18next";
import { array, object, string } from "yup";

import { Alert } from "components/Alert";
import type { IAlertProps } from "components/Alert";
import { Button } from "components/Button";
import { Checkbox } from "components/Checkbox";
import { ExternalLink } from "components/ExternalLink";
import { Input } from "components/Input";
import { Col, Gap, Row } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Text } from "components/Text";
import { TooltipWrapper } from "components/TooltipWrapper";
import type { IOrgAttr } from "scenes/Autoenrollment/types";

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
      .required()
      .max(MAX_DESCRIPTION_LENGTH)
      .matches(/^[\w\-\s,;.¿?¡!]+$/u, t("validations.text")),
    groupName: string()
      .required()
      .max(MAX_GROUP_LENGTH)
      .matches(/^[a-zA-Z0-9]+$/u, t("validations.alphanumeric")),
    organizationName: string()
      .required()
      .min(MIN_ORG_LENGTH)
      .max(MAX_ORG_LENGTH)
      .matches(/^[a-zA-Z]+$/u, t("validations.alphabetic")),
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
            <Col large={"100"} medium={"100"} small={"100"}>
              <Input
                disabled={successMutation.organization}
                label={
                  <Fragment>
                    {t("autoenrollment.addOrganization.organizationName.label")}
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
                  </Fragment>
                }
                name={"organizationName"}
                placeholder={t(
                  "autoenrollment.addOrganization.organizationName.placeholder"
                )}
              />
            </Col>
            <Col large={"100"} medium={"100"} small={"100"}>
              <Input
                disabled={successMutation.group}
                label={
                  <Fragment>
                    {t("autoenrollment.addOrganization.groupName.label")}
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
                  </Fragment>
                }
                name={"groupName"}
                placeholder={t(
                  "autoenrollment.addOrganization.groupName.placeholder"
                )}
              />
            </Col>
            <Col large={"100"} medium={"100"} small={"100"}>
              <Input
                label={
                  <Fragment>
                    {t("autoenrollment.addOrganization.reportLanguage")}
                    <TooltipWrapper
                      displayClass={"dib"}
                      id={"addGroupTooltip"}
                      message={t(
                        "autoenrollment.addOrganization.reportLanguageTip"
                      )}
                      placement={"top"}
                    >
                      <FontAwesomeIcon
                        color={"#b0b0bf"}
                        icon={faCircleInfo}
                        size={"sm"}
                      />
                    </TooltipWrapper>
                  </Fragment>
                }
                name={"reportLanguage"}
                type={"select"}
              >
                <option value={""}>{""}</option>
                <option value={"EN"}>
                  {t("organization.tabs.groups.newGroup.language.EN")}
                </option>
                <option value={"ES"}>
                  {t("organization.tabs.groups.newGroup.language.ES")}
                </option>
              </Input>
            </Col>
            <Col large={"100"} medium={"100"} small={"100"}>
              <Input
                label={t(
                  "autoenrollment.addOrganization.groupDescription.label"
                )}
                name={"groupDescription"}
                placeholder={t(
                  "autoenrollment.addOrganization.groupDescription.placeholder"
                )}
                type={"textarea"}
              />
            </Col>
            <Col large={"100"} medium={"100"} small={"100"}>
              <Checkbox
                label={
                  <ExternalLink href={"https://fluidattacks.com/terms-use/"}>
                    <Text>
                      {t("autoenrollment.addOrganization.termsOfService")}
                    </Text>
                  </ExternalLink>
                }
                name={"terms"}
                value={"accept"}
              />
            </Col>
            <Text fw={7} mb={1} mt={2}>
              {t("autoenrollment.addOrganization.roleTitle")}
            </Text>
            <Text mb={2}>{t("autoenrollment.addOrganization.role")}</Text>
            {!showSubmitAlert && orgMessages.message !== "" && (
              <Alert
                icon={true}
                timer={setShowSubmitAlert}
                variant={orgMessages.type as IAlertProps["variant"]}
              >
                {orgMessages.message}
              </Alert>
            )}
            <Gap>
              <Button
                disabled={isSubmitting}
                type={"submit"}
                variant={"primary"}
              >
                {t("autoenrollment.addOrganization.proceed")}
              </Button>
              <Button onClick={cancelClick}>
                {t("components.modal.cancel")}
              </Button>
            </Gap>
            <Modal onClose={noClick} open={showCancelModal} title={""}>
              <Text>{t("autoenrollment.cancelModal.body")}</Text>
              <ModalConfirm
                onCancel={noClick}
                onConfirm={yesClick}
                txtCancel={t("autoenrollment.cancelModal.no")}
                txtConfirm={t("autoenrollment.cancelModal.yes")}
              />
            </Modal>
          </Row>
        </Form>
      </Formik>
    </div>
  );
};

export { AddOrganization };
