import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
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
import {
  handleGroupCreateError,
  handleRootCreateError,
} from "scenes/Autoenrollment/helpers";
import {
  ADD_GIT_ROOT,
  ADD_GROUP_MUTATION,
  ADD_ORGANIZATION,
  GET_USER_WELCOME,
} from "scenes/Autoenrollment/queries";
import type {
  IAddOrganizationResult,
  IRootAttr,
} from "scenes/Autoenrollment/types";
import {
  FormikCheckbox,
  FormikDropdown,
  FormikText,
  FormikTextArea,
} from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
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
  repositoryValues: IRootAttr;
  setIsRepository: React.Dispatch<React.SetStateAction<boolean>>;
}

const AddOrganization: React.FC<IAddOrganizationProps> = ({
  repositoryValues,
  setIsRepository,
}: IAddOrganizationProps): JSX.Element => {
  const { t } = useTranslation();
  const { push, replace } = useHistory();

  const [orgMessages, setOrgMessages] = useState({
    message: "",
    type: "success",
  });
  const [organization, setOrganization] = useState("");
  const [group, setGroup] = useState("");
  const [showSubmitAlert, setShowSubmitAlert] = useState(false);
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

  const [addOrganization, { loading: submittingOrg }] =
    useMutation<IAddOrganizationResult>(ADD_ORGANIZATION, {
      awaitRefetchQueries: true,
      onCompleted: (result): void => {
        if (result.addOrganization.success) {
          mixpanel.track("NewOrganization", {
            OrganizationId: result.addOrganization.organization.id,
            OrganizationName: result.addOrganization.organization.name,
          });
        }
      },
      onError: (error): void => {
        error.graphQLErrors.forEach(({ message }): void => {
          if (message === "Access denied") {
            msgError(t("sidebar.newOrganization.modal.invalidName"));
          } else {
            Logger.error(
              "An error occurred creating new organization",
              message
            );
          }
        });
      },
      refetchQueries: [GET_USER_WELCOME],
    });

  const [addGroup, { loading: submittingGroup }] = useMutation(
    ADD_GROUP_MUTATION,
    {
      onCompleted: (result: { addGroup: { success: boolean } }): void => {
        if (result.addGroup.success) {
          msgSuccess(
            t("organization.tabs.groups.newGroup.success"),
            t("organization.tabs.groups.newGroup.titleSuccess")
          );
        }
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        handleGroupCreateError(graphQLErrors);
      },
    }
  );

  const [addGitRoot, { loading: submittingRoot }] = useMutation(ADD_GIT_ROOT, {
    onCompleted: (result: { addGitRoot: { success: boolean } }): void => {
      localStorage.clear();
      sessionStorage.clear();
      replace(
        `/orgs/${organization.toLowerCase()}/groups/${group.toLowerCase()}/scope`
      );
      if (result.addGitRoot.success) {
        msgSuccess(
          t("autoenrollment.addOrganization.messages.success.body"),
          t("autoenrollment.addOrganization.messages.success.title")
        );
      }
      setIsRepository(true);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleRootCreateError(graphQLErrors, setOrgMessages);
      setShowSubmitAlert(false);
    },
  });

  const handleSubmit = useCallback(
    async (values: {
      groupDescription: string;
      groupName: string;
      organizationName: string;
      reportLanguage: string;
      terms: string[];
    }): Promise<void> => {
      setIsRepository(false);
      mixpanel.track("AddOrganization");
      await addOrganization({
        variables: { name: values.organizationName.toUpperCase() },
      });
      mixpanel.track("AddGroup");
      await addGroup({
        variables: {
          description: values.groupDescription,
          groupName: values.groupName.toUpperCase(),
          hasMachine: true,
          hasSquad: false,
          language: values.reportLanguage,
          organizationName: values.organizationName,
          service: "WHITE",
          subscription: "CONTINUOUS",
        },
      });
      setGroup(values.groupName.toUpperCase());
      setOrganization(values.organizationName.toUpperCase());
      const { branch, credentials, env, exclusions, url } = repositoryValues;
      mixpanel.track("AddGitRoot");
      await addGitRoot({
        variables: {
          branch: branch.trim(),
          credentials: {
            id: "",
            key: credentials.key,
            name: credentials.name,
            password: credentials.password,
            token: credentials.token,
            type: credentials.type,
            user: credentials.user,
          },
          environment: env,
          gitignore: exclusions,
          groupName: values.groupName.toUpperCase(),
          includesHealthCheck: false,
          nickname: "",
          url: url.trim(),
          useVpn: false,
        },
      });
    },
    [
      addGitRoot,
      addGroup,
      addOrganization,
      repositoryValues,
      setGroup,
      setIsRepository,
      setOrganization,
    ]
  );

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
        initialValues={{
          groupDescription: "",
          groupName: "",
          organizationName: "",
          reportLanguage: "",
          terms: [],
        }}
        name={"newOrganization"}
        onSubmit={handleSubmit}
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
                </Col>
                <Col>
                  <TooltipWrapper
                    id={"addGroupTooltip"}
                    message={t("sidebar.newOrganization.modal.nameTooltip")}
                    placement={"top"}
                  >
                    <FontAwesomeIcon icon={faCircleInfo} />
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
                </Col>
                <Col>
                  <TooltipWrapper
                    id={"addGroupTooltip"}
                    message={t("sidebar.newOrganization.modal.nameTooltip")}
                    placement={"top"}
                  >
                    <FontAwesomeIcon icon={faCircleInfo} />
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
                disabled={submittingOrg || submittingGroup || submittingRoot}
                type={"submit"}
                variant={"primary"}
              >
                {t("autoenrollment.addOrganization.proceed")}
              </Button>
            </Col>
          </Row>
          <Row justify={"center"}>
            <Col>
              <Button onClick={cancelClick} variant={"secondary"}>
                {t("confirmmodal.cancel")}
              </Button>
              <Modal open={showCancelModal} size={"medium"} title={""}>
                <p>{t("autoenrollment.cancelModal.body")}</p>
                <ModalFooter>
                  <Button onClick={yesClick} variant={"primary"}>
                    {t("autoenrollment.cancelModal.yes")}
                  </Button>
                  <Button onClick={noClick} variant={"secondary"}>
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
