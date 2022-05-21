import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";
import { array, object, string } from "yup";

import { ADD_GIT_ROOT } from "../../queries";
import { Alert } from "components/Alert";
import type { IAlertProps } from "components/Alert";
import { Button } from "components/Button";
import { Col, Row } from "components/Layout";
import { TooltipWrapper } from "components/TooltipWrapper";
import { FormikDropdown, FormikText } from "utils/forms/fields";
import { Logger } from "utils/logger";

interface IAddRootProps {
  organizationName: string;
  group: string;
  setIsRepository: React.Dispatch<React.SetStateAction<boolean>>;
}

type modalMessages = React.Dispatch<
  React.SetStateAction<{
    message: string;
    type: string;
  }>
>;

const AddRoot: React.FC<IAddRootProps> = ({
  setIsRepository,
  organizationName,
  group,
}: IAddRootProps): JSX.Element => {
  const { t } = useTranslation();
  const { goBack, replace } = useHistory();

  const [rootMessages, setRootMessages] = useState({
    message: "",
    type: "success",
  });

  const [isGitAccessible, setIsGitAccessible] = useState(false);
  const [showSubmitAlert, setShowSubmitAlert] = useState(false);

  const handleCreationError = (
    graphQLErrors: readonly GraphQLError[],
    setMessages: modalMessages
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      switch (error.message) {
        case "Exception - Error empty value is not valid":
          setMessages({
            message: t("group.scope.git.errors.invalid"),
            type: "error",
          });
          break;
        case "Exception - Active root with the same Nickname already exists":
          setMessages({
            message: t("group.scope.common.errors.duplicateNickname"),
            type: "error",
          });
          break;
        case "Exception - Active root with the same URL/branch already exists":
          setMessages({
            message: t("group.scope.common.errors.duplicateUrl"),
            type: "error",
          });
          break;
        case "Exception - Root name should not be included in the exception pattern":
          setMessages({
            message: t("group.scope.git.errors.rootInGitignore"),
            type: "error",
          });
          break;
        case "Exception - Invalid characters":
          setMessages({
            message: t("validations.invalidChar"),
            type: "error",
          });
          break;
        default:
          setMessages({
            message: t("groupAlerts.errorTextsad"),
            type: "error",
          });
          Logger.error("Couldn't add git roots", error);
      }
    });
  };

  const [addGitRoot] = useMutation(ADD_GIT_ROOT, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleCreationError(graphQLErrors, setRootMessages);
    },
  });

  const handleAccess = useCallback((): void => {
    setIsGitAccessible(true);
    setRootMessages({
      message: t("group.scope.git.repo.credentials.checkAccess.success"),
      type: "success",
    });
  }, [setIsGitAccessible, t]);

  const handleSubmit = useCallback(
    async (values: {
      branch: string;
      credentialName: string;
      credentialType: string;
      environment: string;
      exclusions: string[];
      url: string;
    }): Promise<void> => {
      mixpanel.track("AddGitRoot");
      await addGitRoot({
        variables: {
          branch: values.branch.trim(),
          credentials: {
            id: undefined,
            key: undefined,
            name: values.credentialName,
            password: undefined,
            token: undefined,
            type: values.credentialType,
            user: undefined,
          },
          environment: values.environment,
          gitignore: values.exclusions,
          groupName: group,
          includesHealthCheck: false,
          nickname: false,
          url: values.url.trim(),
          useVpn: false,
        },
      });
      localStorage.clear();
      sessionStorage.clear();
      replace(`/orgs/${organizationName.toLowerCase()}/groups`);
      setIsRepository(true);
    },
    [addGitRoot, group, organizationName, replace, setIsRepository]
  );

  const validations = object().shape({
    branch: string().required(),
    credentialName: string().required(),
    credentialType: string().required(),
    environment: string().required(),
    exclusions: array().of(string()).required(),
    url: string().required(),
  });

  return (
    <div>
      <Formik
        enableReinitialize={true}
        initialValues={{
          branch: "",
          credentialName: "",
          credentialType: "",
          environment: "",
          exclusions: [],
          url: "",
        }}
        name={"newRoot"}
        onSubmit={handleSubmit}
        validationSchema={validations}
      >
        <Form>
          <Row justify={"flex-start"}>
            <Col large={"50"} medium={"50"} small={"50"}>
              <Row>
                <Col>
                  <strong>{t("autoenrollment.addRoot.url.label")}</strong>
                </Col>
                <Col>
                  <TooltipWrapper
                    id={"urlTooltip"}
                    message={t("autoenrollment.addRoot.url.tooltip")}
                    placement={"top"}
                  >
                    <FontAwesomeIcon icon={faCircleInfo} />
                  </TooltipWrapper>
                </Col>
              </Row>
              <Row>
                <Col>
                  <Field
                    component={FormikText}
                    name={"url"}
                    placeholder={t("autoenrollment.addRoot.url.placeholder")}
                    type={"text"}
                  />
                </Col>
              </Row>
            </Col>
            <Col large={"50"} medium={"50"} small={"50"}>
              <Row>
                <Col>
                  <strong>{t("autoenrollment.addRoot.branch.label")}</strong>
                </Col>
              </Row>
              <Row>
                <Col>
                  <Field
                    component={FormikText}
                    name={"branch"}
                    placeholder={t("autoenrollment.addRoot.branch.placeholder")}
                    type={"text"}
                  />
                </Col>
              </Row>
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col large={"50"} medium={"50"} small={"50"}>
              <Row>
                <Col>
                  <strong>{t("autoenrollment.addRoot.credentialType")}</strong>
                </Col>
              </Row>
              <Row>
                <Col>
                  <Field component={FormikDropdown} name={"credentialType"}>
                    <option value={""}>{""}</option>
                    <option value={"HTTPS"}>
                      {t("group.scope.git.repo.credentials.https")}
                    </option>
                    <option value={"SSH"}>
                      {t("group.scope.git.repo.credentials.ssh")}
                    </option>
                  </Field>
                </Col>
              </Row>
            </Col>
            <Col large={"50"} medium={"50"} small={"50"}>
              <Row>
                <Col>
                  <strong>
                    {t("autoenrollment.addRoot.credentialName.label")}
                  </strong>
                </Col>
              </Row>
              <Row>
                <Col>
                  <Field
                    component={FormikText}
                    name={"credentialName"}
                    placeholder={t(
                      "autoenrollment.addRoot.credentialName.placeholder"
                    )}
                    type={"text"}
                  />
                </Col>
              </Row>
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col large={"50"} medium={"50"} small={"50"}>
              <Row>
                <Col>
                  <strong>
                    {t("autoenrollment.addRoot.environment.label")}
                  </strong>
                </Col>
              </Row>
              <Row>
                <Col>
                  <Field
                    component={FormikText}
                    name={"environment"}
                    placeholder={t(
                      "autoenrollment.addRoot.environment.placeholder"
                    )}
                    type={"text"}
                  />
                </Col>
              </Row>
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col large={"50"} medium={"50"} small={"50"}>
              <Row>
                <Col>
                  <strong>
                    {t("autoenrollment.addRoot.exclusions.label")}
                  </strong>
                </Col>
                <Col>
                  <TooltipWrapper
                    id={"urlTooltip"}
                    message={t("autoenrollment.addRoot.exclusions.tooltip")}
                    placement={"top"}
                  >
                    <FontAwesomeIcon icon={faCircleInfo} />
                  </TooltipWrapper>
                </Col>
              </Row>
              <Row>
                <Col>
                  <Field
                    component={FormikText}
                    name={"exclusions"}
                    placeholder={t(
                      "autoenrollment.addRoot.exclusions.placeholder"
                    )}
                    type={"text"}
                  />
                </Col>
              </Row>
            </Col>
          </Row>
          {!showSubmitAlert && rootMessages.message !== "" && (
            <Alert
              icon={true}
              timer={setShowSubmitAlert}
              variant={rootMessages.type as IAlertProps["variant"]}
            >
              {rootMessages.message}
            </Alert>
          )}
          {isGitAccessible ? (
            <Row justify={"center"}>
              <Col>
                <Button disabled={false} type={"submit"} variant={"primary"}>
                  {t("autoenrollment.addRoot.proceed.next")}
                </Button>
              </Col>
            </Row>
          ) : (
            <Row justify={"center"}>
              <Col>
                <Button
                  disabled={false}
                  onClick={handleAccess}
                  variant={"primary"}
                >
                  {t("autoenrollment.addRoot.proceed.checkAccess")}
                </Button>
              </Col>
            </Row>
          )}
          <Row justify={"center"}>
            <Col>
              <Button onClick={goBack} variant={"secondary"}>
                {t("confirmmodal.cancel")}
              </Button>
            </Col>
          </Row>
        </Form>
      </Formik>
    </div>
  );
};

export { AddRoot };
