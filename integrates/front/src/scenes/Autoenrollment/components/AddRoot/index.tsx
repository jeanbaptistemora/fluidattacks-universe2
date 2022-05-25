import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FormikProps } from "formik";
import { Field, Form, Formik } from "formik";
import React, { useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

import { Alert } from "components/Alert";
import type { IAlertProps } from "components/Alert";
import { Button } from "components/Button";
import { Col, Row } from "components/Layout";
import { TooltipWrapper } from "components/TooltipWrapper";
import type { IRootAttr } from "scenes/Autoenrollment/helpers";
import {
  handleCreationError,
  handleValidationError,
  rootSchema,
  useRootSubmit,
} from "scenes/Autoenrollment/helpers";
import {
  ADD_GIT_ROOT,
  VALIDATE_GIT_ACCESS,
} from "scenes/Autoenrollment/queries";
import { FormikDropdown, FormikText, FormikTextArea } from "utils/forms/fields";

interface IAddRootProps {
  organization: string;
  group: string;
  setIsRepository: React.Dispatch<React.SetStateAction<boolean>>;
}

const AddRoot: React.FC<IAddRootProps> = ({
  setIsRepository,
  organization,
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

  const [addGitRoot] = useMutation(ADD_GIT_ROOT, {
    onCompleted: (): void => {
      localStorage.clear();
      sessionStorage.clear();
      replace(`/orgs/${organization.toLowerCase()}/groups`);
      setIsRepository(true);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleCreationError(graphQLErrors, setRootMessages);
    },
  });

  const formRef = useRef<FormikProps<IRootAttr>>(null);

  const [validateGitAccess] = useMutation(VALIDATE_GIT_ACCESS, {
    onCompleted: (): void => {
      setShowSubmitAlert(false);
      setIsGitAccessible(true);
      setRootMessages({
        message: t("group.scope.git.repo.credentials.checkAccess.success"),
        type: "success",
      });
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      setShowSubmitAlert(false);
      handleValidationError(graphQLErrors, setRootMessages);
      setIsGitAccessible(false);
    },
  });

  function checkAccess(): void {
    if (formRef.current !== null) {
      void validateGitAccess({
        variables: {
          credentials: {
            key: formRef.current.values.credentials.key
              ? Buffer.from(formRef.current.values.credentials.key).toString(
                  "base64"
                )
              : undefined,
            name: formRef.current.values.credentials.name,
            password: formRef.current.values.credentials.password,
            token: formRef.current.values.credentials.token,
            type: formRef.current.values.credentials.type,
            user: formRef.current.values.credentials.user,
          },
          groupName: group,
          url: formRef.current.values.url,
        },
      });
    }
  }

  return (
    <div>
      <Formik
        enableReinitialize={true}
        initialValues={{
          branch: "",
          credentials: {
            auth: "TOKEN",
            id: "",
            key: "",
            name: "",
            password: "",
            token: "",
            type: "",
            user: "",
          },
          env: "",
          exclusions: [],
          url: "",
        }}
        innerRef={formRef}
        name={"newRoot"}
        onSubmit={useRootSubmit(addGitRoot, group)}
        validationSchema={rootSchema(isGitAccessible)}
      >
        {({ isSubmitting, values, setFieldTouched }): JSX.Element => {
          if (isSubmitting) {
            setShowSubmitAlert(false);
          }

          function handleAccess(): void {
            checkAccess();
            setFieldTouched("branch", true);
            setFieldTouched("credentials.key", true);
            setFieldTouched("credentials.name", true);
            setFieldTouched("credentials.password", true);
            setFieldTouched("credentials.token", true);
            setFieldTouched("credentials.type", true);
            setFieldTouched("credentials.user", true);
            setFieldTouched("env", true);
            setFieldTouched("exclusions", true);
            setFieldTouched("url", true);
          }

          return (
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
                        placeholder={t(
                          "autoenrollment.addRoot.url.placeholder"
                        )}
                        type={"text"}
                      />
                    </Col>
                  </Row>
                </Col>
                <Col large={"50"} medium={"50"} small={"50"}>
                  <Row>
                    <Col>
                      <strong>
                        {t("autoenrollment.addRoot.branch.label")}
                      </strong>
                    </Col>
                  </Row>
                  <Row>
                    <Col>
                      <Field
                        component={FormikText}
                        name={"branch"}
                        placeholder={t(
                          "autoenrollment.addRoot.branch.placeholder"
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
                        {t("autoenrollment.addRoot.credentials.type.label")}
                      </strong>
                    </Col>
                  </Row>
                  <Row>
                    <Col>
                      <Field
                        component={FormikDropdown}
                        name={"credentials.type"}
                      >
                        <option value={""}>{""}</option>
                        <option value={"HTTPS"}>
                          {t("autoenrollment.addRoot.credentials.type.https")}
                        </option>
                        <option value={"SSH"}>
                          {t("autoenrollment.addRoot.credentials.type.ssh")}
                        </option>
                      </Field>
                    </Col>
                  </Row>
                </Col>
                <Col large={"50"} medium={"50"} small={"50"}>
                  <Row>
                    <Col>
                      <strong>
                        {t("autoenrollment.addRoot.credentials.name.label")}
                      </strong>
                    </Col>
                  </Row>
                  <Row>
                    <Col>
                      <Field
                        component={FormikText}
                        disabled={values.credentials.type === ""}
                        name={"credentials.name"}
                        placeholder={t(
                          "autoenrollment.addRoot.credentials.name.placeholder"
                        )}
                        type={"text"}
                      />
                    </Col>
                  </Row>
                </Col>
              </Row>
              {values.credentials.type === "SSH" && (
                <React.Fragment>
                  <Row justify={"center"}>
                    <Col>
                      <strong>
                        {t("group.scope.git.repo.credentials.sshKey")}
                      </strong>
                    </Col>
                  </Row>
                  <Row>
                    <Col>
                      <Field
                        component={FormikTextArea}
                        name={"credentials.key"}
                        placeholder={t(
                          "group.scope.git.repo.credentials.sshHint"
                        )}
                        type={"text"}
                      />
                    </Col>
                  </Row>
                </React.Fragment>
              )}
              {values.credentials.type === "HTTPS" && (
                <Row>
                  <Col>
                    <Field component={FormikDropdown} name={"credentials.auth"}>
                      <option value={"TOKEN"}>
                        {t("autoenrollment.addRoot.credentials.auth.token")}
                      </option>
                      <option value={"USER"}>
                        {t("autoenrollment.addRoot.credentials.auth.user")}
                      </option>
                    </Field>
                  </Col>
                </Row>
              )}
              {values.credentials.type === "HTTPS" &&
                values.credentials.auth === "TOKEN" && (
                  <Row>
                    <Col large={"50"} medium={"50"} small={"50"}>
                      <Row>
                        <Col>
                          <strong>
                            {t("autoenrollment.addRoot.credentials.token")}
                          </strong>
                        </Col>
                      </Row>
                      <Row>
                        <Col>
                          <Field
                            component={FormikText}
                            name={"credentials.token"}
                            type={"text"}
                          />
                        </Col>
                      </Row>
                    </Col>
                  </Row>
                )}
              {values.credentials.type === "HTTPS" &&
                values.credentials.auth === "USER" && (
                  <Row>
                    <Col large={"50"} medium={"50"} small={"50"}>
                      <Row>
                        <Col>
                          <strong>
                            {t("autoenrollment.addRoot.credentials.user")}
                          </strong>
                        </Col>
                      </Row>
                      <Row>
                        <Col>
                          <Field
                            component={FormikText}
                            name={"credentials.user"}
                            type={"text"}
                          />
                        </Col>
                      </Row>
                    </Col>
                    <Col large={"50"} medium={"50"} small={"50"}>
                      <Row>
                        <Col>
                          <strong>
                            {t("autoenrollment.addRoot.credentials.password")}
                          </strong>
                        </Col>
                      </Row>
                      <Row>
                        <Col>
                          <Field
                            component={FormikText}
                            name={"credentials.password"}
                            type={"password"}
                          />
                        </Col>
                      </Row>
                    </Col>
                  </Row>
                )}
              <Row justify={"flex-start"}>
                <Col>
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
                        name={"env"}
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
                    <Button type={"submit"} variant={"primary"}>
                      {t("autoenrollment.addRoot.proceed.next")}
                    </Button>
                  </Col>
                </Row>
              ) : (
                <Row justify={"center"}>
                  <Col>
                    <Button onClick={handleAccess} variant={"primary"}>
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
          );
        }}
      </Formik>
    </div>
  );
};

export { AddRoot };
