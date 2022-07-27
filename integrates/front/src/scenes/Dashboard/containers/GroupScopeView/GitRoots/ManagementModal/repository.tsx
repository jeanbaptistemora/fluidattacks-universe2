/* eslint-disable complexity, react/forbid-component-props */
import { Buffer } from "buffer";

import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faQuestionCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FormikProps } from "formik";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import type { ChangeEvent, FC } from "react";
import React, {
  Fragment,
  useCallback,
  useContext,
  useRef,
  useState,
} from "react";
import { useTranslation } from "react-i18next";

import { HealthCheck } from "./HealthCheck";
import { RepositoryTour } from "./RepositoryTour";

import {
  GET_ORGANIZATION_CREDENTIALS,
  VALIDATE_GIT_ACCESS,
} from "../../queries";
import type { ICredentialsAttr, IFormValues } from "../../types";
import { GitIgnoreAlert, gitModalSchema } from "../helpers";
import { Alert } from "components/Alert";
import type { IAlertProps } from "components/Alert";
import { Button } from "components/Button";
import { Input, Label, Select, TextArea } from "components/Input";
import { Col, Row } from "components/Layout";
import { ModalConfirm } from "components/Modal";
import { Text } from "components/Text";
import { groupContext } from "scenes/Dashboard/containers/GroupContent/context";
import type { IGroupContext } from "scenes/Dashboard/containers/GroupContent/types";
import { QuestionButton } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import {
  FormikArrayField,
  FormikCheckbox,
  FormikDropdown,
  FormikRadioGroup,
  FormikText,
} from "utils/forms/fields";
import { Logger } from "utils/logger";
import { openUrl } from "utils/resourceHelpers";
import {
  composeValidators,
  hasSshFormat,
  validTextField,
} from "utils/validations";

interface IRepositoryProps {
  groupName: string;
  initialValues: IFormValues;
  isEditing: boolean;
  modalMessages: { message: string; type: string };
  nicknames: string[];
  onClose: () => void;
  onSubmit: (values: IFormValues) => Promise<void>;
  runTour: boolean;
  finishTour: () => void;
}

const Repository: FC<IRepositoryProps> = ({
  groupName,
  initialValues,
  isEditing,
  nicknames,
  modalMessages,
  onClose,
  onSubmit,
  runTour,
  finishTour,
}: IRepositoryProps): JSX.Element => {
  const { t } = useTranslation();
  const { organizationId }: IGroupContext = useContext(groupContext);

  // GraphQL operations
  const { data: organizationCredentialsData } = useQuery<{
    organization: { credentials: ICredentialsAttr[] };
  }>(GET_ORGANIZATION_CREDENTIALS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load organization credentials", error);
      });
    },
    variables: {
      organizationId,
    },
  });

  const isDuplicated = (field: string): boolean => {
    const repoName: string = field
      ? field.split("/").slice(-1)[0].replace(".git", "")
      : "";
    const { nickname: initialNickname } = initialValues;

    return nicknames.includes(repoName) && initialNickname !== repoName;
  };

  const [isGitAccessible, setIsGitAccessible] = useState(true);
  const [credExists, setCredExists] = useState(
    !_.isNull(initialValues.credentials) && initialValues.credentials.id !== ""
  );
  const [disabledCredsEdit, setDisabledCredsEdit] = useState(
    !_.isNull(initialValues.credentials) && initialValues.credentials.id !== ""
  );
  const [hasSquad, setHasSquad] = useState(false);
  const [isHttpsCredentialsTypeUser, setIsHttpsCredentialsTypeUser] =
    useState(false);
  const [isCheckedHealthCheck, setIsCheckedHealthCheck] = useState(isEditing);

  const goToDocumentation = useCallback((): void => {
    openUrl(
      "https://mirrors.edge.kernel.org/pub/software/scm/git/docs/gitignore.html#_pattern_format"
    );
  }, []);

  const [showGitAlert, setShowGitAlert] = useState(false);
  const [showSubmitAlert, setShowSubmitAlert] = useState(false);

  const [validateGitMsg, setValidateGitMsg] = useState({
    message: "",
    type: "success",
  });
  const [validateGitAccess] = useMutation(VALIDATE_GIT_ACCESS, {
    onCompleted: (): void => {
      setShowGitAlert(false);
      setIsGitAccessible(true);
      setValidateGitMsg({
        message: t("group.scope.git.repo.credentials.checkAccess.success"),
        type: "success",
      });
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      setShowGitAlert(false);
      graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Exception - Git repository was not accessible with given credentials":
            setValidateGitMsg({
              message: t("group.scope.git.errors.invalidGitCredentials"),
              type: "error",
            });
            break;
          case "Exception - Branch not found":
            setValidateGitMsg({
              message: t("group.scope.git.errors.invalidBranch"),
              type: "error",
            });
            break;
          default:
            setValidateGitMsg({
              message: t("groupAlerts.errorTextsad"),
              type: "error",
            });
            Logger.error("Couldn't activate root", error);
        }
      });
      setIsGitAccessible(false);
    },
  });

  const formRef = useRef<FormikProps<IFormValues>>(null);

  const organizationCredentials = _.isUndefined(organizationCredentialsData)
    ? []
    : organizationCredentialsData.organization.credentials;
  const groupedExistingCreds =
    organizationCredentials.length > 0
      ? Object.fromEntries(
          organizationCredentials.map((cred): [string, ICredentialsAttr] => [
            cred.id,
            cred,
          ])
        )
      : {};

  function handleCheckAccessClick(): void {
    if (formRef.current !== null) {
      void validateGitAccess({
        variables: {
          branch: formRef.current.values.branch,
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
          groupName,
          url: formRef.current.values.url,
        },
      });
    }
  }

  const submittableCredentials = (values: IFormValues): boolean => {
    return values.credentials.type === "SSH"
      ? !values.credentials.name ||
          !values.credentials.key ||
          hasSshFormat(values.credentials.key) !== undefined
      : !values.credentials.name ||
          (isHttpsCredentialsTypeUser
            ? !values.credentials.user || !values.credentials.password
            : !values.credentials.token);
  };

  function onChangeExits(event: ChangeEvent<HTMLInputElement>): void {
    if (event.target.value === "") {
      formRef.current?.setFieldValue("credentials.type", "");
      formRef.current?.setFieldValue("credentials.name", "");
      formRef.current?.setFieldValue("credentials.id", "");
      setCredExists(false);
      setDisabledCredsEdit(false);
    } else {
      const currentCred = groupedExistingCreds[event.target.value];
      formRef.current?.setFieldValue("credentials.type", currentCred.type);
      formRef.current?.setFieldValue("credentials.name", currentCred.name);
      formRef.current?.setFieldValue("credentials.id", currentCred.id);
      setCredExists(true);
      setDisabledCredsEdit(true);
    }
  }

  return (
    <Formik
      initialValues={initialValues}
      innerRef={formRef}
      name={"gitRoot"}
      onSubmit={onSubmit}
      validationSchema={gitModalSchema(
        isEditing,
        credExists,
        hasSquad,
        initialValues,
        isCheckedHealthCheck,
        isDuplicated,
        isGitAccessible,
        isHttpsCredentialsTypeUser,
        nicknames
      )}
    >
      {({ dirty, errors, isSubmitting, values }): JSX.Element => {
        if (isSubmitting) {
          setShowSubmitAlert(false);
        }

        return (
          <Fragment>
            <Form>
              <fieldset className={"bn"}>
                <Text fw={7} mb={2} size={4}>
                  {t("group.scope.git.repo.title")}
                </Text>
                <Row align={"center"}>
                  <div>
                    <Label required={true}>
                      {t("group.scope.git.repo.url")}
                    </Label>
                    <Field
                      component={FormikText}
                      id={"git-root-add-repo-url"}
                      name={"url"}
                      type={"text"}
                      validate={composeValidators([validTextField])}
                    />
                  </div>
                  <Col id={"git-root-add-repo-branch"}>
                    <Input
                      label={t("group.scope.git.repo.branch")}
                      name={"branch"}
                      required={true}
                    />
                  </Col>
                  <Col id={"git-root-add-use-vpn"}>
                    <Field
                      component={FormikCheckbox}
                      label={""}
                      name={"useVpn"}
                      type={"checkbox"}
                    >
                      {t("group.scope.git.repo.useVpn")}
                    </Field>
                  </Col>
                  {isEditing && values.branch !== initialValues.branch ? (
                    <Alert>{t("group.scope.common.changeWarning")}</Alert>
                  ) : undefined}
                  {isDuplicated(values.url) || isEditing ? (
                    <Input
                      id={"git-root-add-nickname"}
                      label={t("group.scope.git.repo.nickname")}
                      name={"nickname"}
                      placeholder={t("group.scope.git.repo.nicknameHint")}
                      required={true}
                    />
                  ) : undefined}
                </Row>
                <Row id={"git-root-add-credentials"}>
                  {_.isEmpty(groupedExistingCreds) ? null : (
                    <div>
                      <Label>{"Existing credentials"}</Label>
                      <Field
                        component={FormikDropdown}
                        customChange={onChangeExits}
                        label={"Existing credentials"}
                        name={"credentials.id"}
                      >
                        <option value={""}>{""}</option>
                        {Object.values(groupedExistingCreds).map(
                          (cred): JSX.Element => (
                            <option key={cred.id} value={cred.id}>
                              {cred.name}
                            </option>
                          )
                        )}
                      </Field>
                    </div>
                  )}
                  <Col>
                    <Select
                      disabled={disabledCredsEdit}
                      label={t("group.scope.git.repo.credentials.type")}
                      name={"credentials.type"}
                      required={!isEditing}
                    >
                      <option value={""}>{""}</option>
                      <option value={"HTTPS"}>
                        {t("group.scope.git.repo.credentials.https")}
                      </option>
                      <option value={"SSH"}>
                        {t("group.scope.git.repo.credentials.ssh")}
                      </option>
                    </Select>
                  </Col>
                  <Col>
                    <Input
                      disabled={disabledCredsEdit}
                      label={t("group.scope.git.repo.credentials.name")}
                      name={"credentials.name"}
                      placeholder={t(
                        "group.scope.git.repo.credentials.nameHint"
                      )}
                      required={!isEditing}
                    />
                  </Col>
                  {values.credentials.type === "SSH" && !credExists ? (
                    <TextArea
                      label={t("group.scope.git.repo.credentials.sshKey")}
                      name={"credentials.key"}
                      placeholder={t(
                        "group.scope.git.repo.credentials.sshHint"
                      )}
                    />
                  ) : values.credentials.type === "HTTPS" && !credExists ? (
                    <Fragment>
                      <Field
                        component={FormikRadioGroup}
                        initialState={"Access Token"}
                        labels={["User and Password", "Access Token"]}
                        name={"httpsCredentialsType"}
                        onSelect={setIsHttpsCredentialsTypeUser}
                        type={"Radio"}
                      />
                      {isHttpsCredentialsTypeUser ? (
                        <Fragment>
                          <Col>
                            <Input
                              label={t("group.scope.git.repo.credentials.user")}
                              name={"credentials.user"}
                            />
                          </Col>
                          <Col>
                            <Input
                              label={t(
                                "group.scope.git.repo.credentials.password"
                              )}
                              name={"credentials.password"}
                            />
                          </Col>
                        </Fragment>
                      ) : undefined}
                      {isHttpsCredentialsTypeUser ? undefined : (
                        <Input
                          label={t("group.scope.git.repo.credentials.token")}
                          name={"credentials.token"}
                        />
                      )}
                    </Fragment>
                  ) : undefined}
                  {!showGitAlert && validateGitMsg.message !== "" ? (
                    <Alert
                      icon={true}
                      onTimeOut={setShowGitAlert}
                      variant={validateGitMsg.type as IAlertProps["variant"]}
                    >
                      {validateGitMsg.message}
                    </Alert>
                  ) : undefined}
                  <Button
                    disabled={submittableCredentials(values)}
                    id={"checkAccessBtn"}
                    onClick={handleCheckAccessClick}
                    variant={"secondary"}
                  >
                    {t("group.scope.git.repo.credentials.checkAccess.text")}
                  </Button>
                  <Input
                    id={"git-root-add-env"}
                    label={t("group.scope.git.repo.environment")}
                    name={"environment"}
                    placeholder={t("group.scope.git.repo.environmentHint")}
                    required={true}
                  />
                </Row>
              </fieldset>
              <HealthCheck
                initValues={initialValues}
                isEditing={isEditing}
                isHealthChecked={isCheckedHealthCheck}
                setHasSquad={setHasSquad}
                setIsHealthChecked={setIsCheckedHealthCheck}
                values={values}
              />
              <Can do={"update_git_root_filter"}>
                <fieldset className={"bn"}>
                  <Label
                    htmlFor={"group.scope.git.filter"}
                    tooltip={
                      runTour ? undefined : t("group.scope.git.filter.tooltip")
                    }
                  >
                    <QuestionButton onClick={goToDocumentation}>
                      <FontAwesomeIcon icon={faQuestionCircle} />
                    </QuestionButton>
                    &nbsp;
                    {t("group.scope.git.filter.exclude")}
                  </Label>
                  <GitIgnoreAlert gitignore={values.gitignore} />
                  <FormikArrayField
                    allowEmpty={true}
                    initialValue={""}
                    name={"gitignore"}
                  >
                    {(fieldName: string): JSX.Element => (
                      <Input
                        name={fieldName}
                        placeholder={t("group.scope.git.filter.placeholder")}
                      />
                    )}
                  </FormikArrayField>
                </fieldset>
              </Can>
              {!showSubmitAlert && modalMessages.message !== "" ? (
                <Alert
                  icon={true}
                  onTimeOut={setShowSubmitAlert}
                  variant={modalMessages.type as IAlertProps["variant"]}
                >
                  {modalMessages.message}
                </Alert>
              ) : undefined}
              <ModalConfirm
                disabled={!isGitAccessible || !dirty || isSubmitting}
                id={"git-root-add-confirm"}
                onCancel={onClose}
              />
            </Form>
            {runTour ? (
              <RepositoryTour
                dirty={dirty}
                errors={errors}
                finishTour={finishTour}
                isGitAccessible={isGitAccessible}
                isHttpsCredentialsTypeUser={isHttpsCredentialsTypeUser}
                runTour={runTour}
                values={values}
              />
            ) : undefined}
          </Fragment>
        );
      }}
    </Formik>
  );
};

export { Repository };
