/* eslint-disable complexity, react/forbid-component-props */
import { Buffer } from "buffer";

import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import {
  faQuestionCircle,
  faTrashAlt,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FormikProps } from "formik";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import { GET_GROUP_CREDENTIALS, VALIDATE_GIT_ACCESS } from "../../queries";
import type { ICredentials, IGitRootAttr } from "../../types";
import { GitIgnoreAlert, gitModalSchema } from "../helpers";
import { Alert } from "components/Alert";
import type { IAlertProps } from "components/Alert";
import { Button } from "components/Button";
import { ModalFooter } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import { BaseStep, Tour } from "components/Tour";
import {
  ControlLabel,
  QuestionButton,
  RequiredField,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { Have } from "utils/authz/Have";
import {
  FormikArrayField,
  FormikCheckbox,
  FormikDropdown,
  FormikRadioGroup,
  FormikText,
  FormikTextArea,
} from "utils/forms/fields";
import { Logger } from "utils/logger";
import { openUrl } from "utils/resourceHelpers";
import {
  composeValidators,
  hasSshFormat,
  required,
  validEnvironment,
} from "utils/validations";

interface IRepositoryProps {
  groupName: string;
  initialValues: IGitRootAttr;
  isEditing: boolean;
  modalMessages: { message: string; type: string };
  nicknames: string[];
  onClose: () => void;
  onSubmit: (values: IGitRootAttr) => Promise<void>;
  runTour: boolean;
  finishTour: () => void;
}

const Repository: React.FC<IRepositoryProps> = ({
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

  // GraphQL operations
  const { data } = useQuery<{
    group: { credentials: ICredentials[] };
  }>(GET_GROUP_CREDENTIALS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load roots", error);
      });
    },
    variables: { groupName },
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
    initialValues.credentials.id !== ""
  );
  const [disabledCredsEdit, setDisabledCredsEdit] = useState(false);

  const deleteCredential: () => void = useCallback((): void => {
    setCredExists(false);
  }, []);

  const [hasSquad, setHasSquad] = useState(false);
  function setSquad(): void {
    setHasSquad(true);
  }
  const [confirmHealthCheck, setConfirmHealthCheck] = useState(
    isEditing ? initialValues.includesHealthCheck : undefined
  );
  const [isHttpsCredentialsTypeUser, setIsHttpsCredentialsTypeUser] =
    useState(false);

  const [isCheckedHealthCheck, setIsCheckedHealthCheck] = useState(isEditing);
  const [isRootChange, setIsRootChange] = useState(
    [initialValues.url, initialValues.branch].join("")
  );

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
        if (
          error.message ===
          "Exception - Git repository was not accessible with given credentials"
        ) {
          setValidateGitMsg({
            message: t("group.scope.git.errors.invalidGitCredentials"),
            type: "error",
          });
        } else {
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

  const formRef = useRef<FormikProps<IGitRootAttr>>(null);
  const groupedExistingCreds =
    !_.isUndefined(data) && data.group.credentials.length > 0
      ? Object.fromEntries(
          data.group.credentials.map((cred): [string, ICredentials] => [
            cred.id,
            cred,
          ])
        )
      : {};

  function handleCheckAccessClick(): void {
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
          groupName,
          url: formRef.current.values.url,
        },
      });
    }
  }

  function rootChanged(values: IGitRootAttr): null {
    setIsRootChange([values.url, values.branch].join(""));
    if (
      [values.url, values.branch].join("") !==
      [initialValues.url, initialValues.branch].join("")
    ) {
      setIsCheckedHealthCheck(false);
    }

    return null;
  }

  const submittableCredentials = (values: IGitRootAttr): boolean => {
    return values.credentials.type === "SSH"
      ? !values.credentials.name ||
          !values.credentials.key ||
          hasSshFormat(values.credentials.key) !== undefined
      : !values.credentials.name ||
          (isHttpsCredentialsTypeUser
            ? !values.credentials.user || !values.credentials.password
            : !values.credentials.token);
  };

  function onChangeExits(event: React.ChangeEvent<HTMLInputElement>): void {
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
    <div>
      <Formik
        initialValues={initialValues}
        innerRef={formRef}
        name={"gitRoot"}
        onSubmit={onSubmit}
        validationSchema={gitModalSchema(
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
            <React.Fragment>
              <Form>
                <React.Fragment>
                  <fieldset className={"bn"}>
                    <legend className={"f3 b"}>
                      {t("group.scope.git.repo.title")}
                    </legend>
                    <div className={"flex"}>
                      <div className={"w-60 mr3"} id={"git-root-add-repo-url"}>
                        <ControlLabel>
                          <RequiredField>{"*"}&nbsp;</RequiredField>
                          {t("group.scope.git.repo.url")}
                        </ControlLabel>
                        <Field
                          component={FormikText}
                          name={"url"}
                          type={"text"}
                        />
                      </div>
                      <div className={"w-30"} id={"git-root-add-repo-branch"}>
                        <ControlLabel>
                          <RequiredField>{"*"}&nbsp;</RequiredField>
                          {t("group.scope.git.repo.branch")}
                        </ControlLabel>
                        <Field
                          component={FormikText}
                          name={"branch"}
                          type={"text"}
                        />
                      </div>
                      <div
                        className={"w-10 ml3 mt4"}
                        id={"git-root-add-use-vpn"}
                      >
                        <Field
                          component={FormikCheckbox}
                          label={""}
                          name={"useVpn"}
                          type={"checkbox"}
                        >
                          {t("group.scope.git.repo.useVpn")}
                        </Field>
                      </div>
                    </div>
                    {isEditing && values.branch !== initialValues.branch ? (
                      <Alert variant={"error"}>
                        {t("group.scope.common.changeWarning")}
                      </Alert>
                    ) : undefined}
                    <br />
                    {isDuplicated(values.url) || isEditing ? (
                      <React.Fragment>
                        <div className={"flex"}>
                          <div className={"w-100"} id={"git-root-add-nickname"}>
                            <ControlLabel>
                              <RequiredField>{"*"}&nbsp;</RequiredField>
                              {t("group.scope.git.repo.nickname")}
                            </ControlLabel>
                            <Field
                              component={FormikText}
                              name={"nickname"}
                              placeholder={t(
                                "group.scope.git.repo.nicknameHint"
                              )}
                              type={"text"}
                            />
                          </div>
                        </div>
                        <br />
                      </React.Fragment>
                    ) : undefined}
                    <div id={"git-root-add-credentials"}>
                      <div className={"flex"}>
                        {!_.isUndefined(data) &&
                        data.group.credentials.length > 0 ? (
                          <div className={"w-30 mr3"}>
                            <ControlLabel>
                              {"Existing credentials"}
                            </ControlLabel>
                            <Field
                              component={FormikDropdown}
                              customChange={onChangeExits}
                              name={"credentials.id"}
                            >
                              <option value={""}>{""}</option>
                              {data.group.credentials.map(
                                (cred): JSX.Element => {
                                  return (
                                    <option key={cred.id} value={cred.id}>
                                      {cred.name}
                                    </option>
                                  );
                                }
                              )}
                            </Field>
                          </div>
                        ) : null}
                        <div className={"w-20 mr3"}>
                          <ControlLabel>
                            {t("group.scope.git.repo.credentials.type")}
                          </ControlLabel>
                          <Field
                            component={FormikDropdown}
                            disabled={disabledCredsEdit}
                            name={"credentials.type"}
                          >
                            <option value={""}>{""}</option>
                            <option value={"HTTPS"}>
                              {t("group.scope.git.repo.credentials.https")}
                            </option>
                            <option value={"SSH"}>
                              {t("group.scope.git.repo.credentials.ssh")}
                            </option>
                          </Field>
                        </div>
                        <div className={"w-40"}>
                          <ControlLabel>
                            {t("group.scope.git.repo.credentials.name")}
                          </ControlLabel>
                          <div className={"flex"}>
                            <Field
                              component={FormikText}
                              disabled={disabledCredsEdit}
                              name={"credentials.name"}
                              placeholder={t(
                                "group.scope.git.repo.credentials.nameHint"
                              )}
                              type={"text"}
                            />
                            {credExists ? (
                              <Button
                                id={"git-root-add"}
                                onClick={deleteCredential}
                                variant={"secondary"}
                              >
                                <FontAwesomeIcon icon={faTrashAlt} />
                              </Button>
                            ) : undefined}
                          </div>
                        </div>
                      </div>
                      <br />
                      {values.credentials.type === "SSH" && !credExists ? (
                        <div className={"flex"}>
                          <div className={"w-100"}>
                            <ControlLabel>
                              {t("group.scope.git.repo.credentials.sshKey")}
                            </ControlLabel>
                            <Field
                              component={FormikTextArea}
                              name={"credentials.key"}
                              placeholder={t(
                                "group.scope.git.repo.credentials.sshHint"
                              )}
                              type={"text"}
                            />
                          </div>
                        </div>
                      ) : values.credentials.type === "HTTPS" && !credExists ? (
                        <React.Fragment>
                          <Field
                            component={FormikRadioGroup}
                            initialState={"Access Token"}
                            labels={["User and Password", "Access Token"]}
                            name={"httpsCredentialsType"}
                            onSelect={setIsHttpsCredentialsTypeUser}
                            type={"Radio"}
                          />
                          {isHttpsCredentialsTypeUser && (
                            <div className={"flex"}>
                              <div className={"w-30 mr3"}>
                                <ControlLabel>
                                  {t("group.scope.git.repo.credentials.user")}
                                </ControlLabel>
                                <Field
                                  component={FormikText}
                                  name={"credentials.user"}
                                  type={"text"}
                                />
                              </div>
                              <div className={"w-70"}>
                                <ControlLabel>
                                  {t(
                                    "group.scope.git.repo.credentials.password"
                                  )}
                                </ControlLabel>
                                <Field
                                  component={FormikText}
                                  name={"credentials.password"}
                                  type={"text"}
                                />
                              </div>
                            </div>
                          )}
                          {!isHttpsCredentialsTypeUser && (
                            <div className={"flex"}>
                              <div className={"w-30 mr3"}>
                                <ControlLabel>
                                  {t("group.scope.git.repo.credentials.token")}
                                </ControlLabel>
                                <Field
                                  component={FormikText}
                                  name={"credentials.token"}
                                  type={"text"}
                                />
                              </div>
                            </div>
                          )}
                        </React.Fragment>
                      ) : undefined}
                      {!showGitAlert && validateGitMsg.message !== "" && (
                        <Alert
                          icon={true}
                          timer={setShowGitAlert}
                          variant={
                            validateGitMsg.type as IAlertProps["variant"]
                          }
                        >
                          {validateGitMsg.message}
                        </Alert>
                      )}
                      {
                        <div className={"mt2 tr"}>
                          <Button
                            disabled={submittableCredentials(values)}
                            id={"checkAccessBtn"}
                            onClick={handleCheckAccessClick}
                            variant={"secondary"}
                          >
                            {t(
                              "group.scope.git.repo.credentials.checkAccess.text"
                            )}
                          </Button>
                        </div>
                      }
                    </div>
                    <div className={"flex mt3"}>
                      <div className={"w-100"} id={"git-root-add-env"}>
                        <ControlLabel>
                          <RequiredField>{"*"}&nbsp;</RequiredField>
                          {t("group.scope.git.repo.environment")}
                        </ControlLabel>
                        <Field
                          component={FormikText}
                          name={"environment"}
                          placeholder={t(
                            "group.scope.git.repo.environmentHint"
                          )}
                          type={"text"}
                          validate={composeValidators([
                            required,
                            validEnvironment,
                          ])}
                        />
                      </div>
                    </div>
                    <br />
                  </fieldset>
                  <Have I={"has_squad"}>
                    <fieldset className={"bn"}>
                      <div
                        id={"git-root-add-health-check"}
                        onMouseMove={setSquad}
                        role={"none"}
                      >
                        <legend className={"f3 b"}>
                          {t("group.scope.git.healthCheck.title")}
                        </legend>
                        <div className={"flex"}>
                          <div className={"w-100"}>
                            <ControlLabel>
                              {t("group.scope.git.healthCheck.confirm")}
                            </ControlLabel>
                            <Field
                              component={FormikRadioGroup}
                              initialState={
                                isEditing
                                  ? confirmHealthCheck ?? false
                                    ? "Yes"
                                    : "No"
                                  : null
                              }
                              labels={["Yes", "No"]}
                              name={"includesHealthCheck"}
                              onSelect={setConfirmHealthCheck}
                              type={"Radio"}
                              uncheck={setIsCheckedHealthCheck}
                            />
                          </div>
                        </div>
                        <div>
                          <div className={"flex"}>
                            <div className={"w-100"}>
                              {[values.url, values.branch].join("") ===
                              isRootChange
                                ? undefined
                                : rootChanged(values)}
                              {values.includesHealthCheck ?? false ? (
                                <Alert variant={"error"}>
                                  <Field
                                    component={FormikCheckbox}
                                    isChecked={isCheckedHealthCheck}
                                    label={""}
                                    name={"healthCheckConfirm"}
                                    type={"checkbox"}
                                    value={"includeA"}
                                  >
                                    {t("group.scope.git.healthCheck.accept")}
                                    <RequiredField>{"*"}&nbsp;</RequiredField>
                                  </Field>
                                </Alert>
                              ) : undefined}
                              {values.includesHealthCheck ??
                              true ? undefined : (
                                <Alert variant={"error"}>
                                  <Field
                                    component={FormikCheckbox}
                                    isChecked={isCheckedHealthCheck}
                                    label={""}
                                    name={"healthCheckConfirm"}
                                    type={"checkbox"}
                                    value={"rejectA"}
                                  >
                                    {t("group.scope.git.healthCheck.rejectA")}
                                    <RequiredField>{"*"}&nbsp;</RequiredField>
                                  </Field>
                                  <Field
                                    component={FormikCheckbox}
                                    isChecked={isCheckedHealthCheck}
                                    label={""}
                                    name={"healthCheckConfirm"}
                                    type={"checkbox"}
                                    value={"rejectB"}
                                  >
                                    {t("group.scope.git.healthCheck.rejectB")}
                                    <RequiredField>{"*"}&nbsp;</RequiredField>
                                  </Field>
                                  <Field
                                    component={FormikCheckbox}
                                    isChecked={isCheckedHealthCheck}
                                    label={""}
                                    name={"healthCheckConfirm"}
                                    type={"checkbox"}
                                    value={"rejectC"}
                                  >
                                    {t("group.scope.git.healthCheck.rejectC")}
                                    <RequiredField>{"*"}&nbsp;</RequiredField>
                                  </Field>
                                </Alert>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    </fieldset>
                  </Have>
                  <Can do={"update_git_root_filter"}>
                    <fieldset className={"bn"}>
                      <TooltipWrapper
                        displayClass={"dib"}
                        hide={runTour}
                        id={"group.scope.git.filter.tooltip.info"}
                        message={t("group.scope.git.filter.tooltip")}
                      >
                        <ControlLabel>
                          {t("group.scope.git.filter.exclude")}
                        </ControlLabel>
                      </TooltipWrapper>
                      <QuestionButton onClick={goToDocumentation}>
                        <FontAwesomeIcon icon={faQuestionCircle} />
                      </QuestionButton>
                      <GitIgnoreAlert gitignore={values.gitignore} />
                      <FormikArrayField
                        allowEmpty={true}
                        initialValue={""}
                        name={"gitignore"}
                      >
                        {(fieldName: string): JSX.Element => (
                          <Field
                            component={FormikText}
                            name={fieldName}
                            placeholder={t(
                              "group.scope.git.filter.placeholder"
                            )}
                            type={"text"}
                          />
                        )}
                      </FormikArrayField>
                    </fieldset>
                  </Can>
                </React.Fragment>
                {!showSubmitAlert && modalMessages.message !== "" && (
                  <Alert
                    icon={true}
                    timer={setShowSubmitAlert}
                    variant={modalMessages.type as IAlertProps["variant"]}
                  >
                    {modalMessages.message}
                  </Alert>
                )}
                <ModalFooter>
                  <Button onClick={onClose} variant={"secondary"}>
                    {t("confirmmodal.cancel")}
                  </Button>
                  <Button
                    disabled={!isGitAccessible || !dirty || isSubmitting}
                    id={"git-root-add-proceed"}
                    type={"submit"}
                    variant={"primary"}
                  >
                    {t("confirmmodal.proceed")}
                  </Button>
                </ModalFooter>
              </Form>
              {runTour ? (
                <Tour
                  onFinish={finishTour}
                  run={runTour}
                  steps={[
                    {
                      ...BaseStep,
                      content: t("tours.addGitRoot.intro"),
                      placement: "center",
                      target: "#git-root-add-use-vpn",
                      title: t("group.scope.common.add"),
                    },
                    {
                      ...BaseStep,
                      content: t("tours.addGitRoot.rootUrl"),
                      hideBackButton: true,
                      hideFooter: values.url.length === 0,
                      target: "#git-root-add-repo-url",
                    },
                    {
                      ...BaseStep,
                      content: t("tours.addGitRoot.rootBranch"),
                      hideFooter: values.branch.length === 0,
                      target: "#git-root-add-repo-branch",
                    },
                    {
                      ...BaseStep,
                      content: t("tours.addGitRoot.vpn"),
                      target: "#git-root-add-use-vpn",
                    },
                    {
                      ...BaseStep,
                      content: t("tours.addGitRoot.nickname"),
                      hideFooter: values.nickname.length === 0,
                      target: "#git-root-add-nickname",
                    },
                    {
                      ...BaseStep,
                      content: (
                        <React.Fragment>
                          {t("tours.addGitRoot.rootCredentials.content")}
                          <ul>
                            {values.credentials.type === "" && (
                              <li>
                                {t("tours.addGitRoot.rootCredentials.type")}
                              </li>
                            )}
                            {values.credentials.name === "" && (
                              <li>
                                {t("tours.addGitRoot.rootCredentials.name")}
                              </li>
                            )}
                            {values.credentials.type === "HTTPS" &&
                              isHttpsCredentialsTypeUser &&
                              (values.credentials.user === "" ||
                                values.credentials.password === "") && (
                                <li>
                                  {t("tours.addGitRoot.rootCredentials.user")}
                                </li>
                              )}
                            {values.credentials.type === "HTTPS" &&
                              !isHttpsCredentialsTypeUser &&
                              values.credentials.token === "" && (
                                <li>
                                  {t("tours.addGitRoot.rootCredentials.token")}
                                </li>
                              )}
                            {values.credentials.type === "SSH" &&
                              values.credentials.key === "" && (
                                <li>
                                  {t("tours.addGitRoot.rootCredentials.key")}
                                </li>
                              )}
                            {!isGitAccessible && (
                              <li>
                                {t("tours.addGitRoot.rootCredentials.invalid")}
                              </li>
                            )}
                          </ul>
                        </React.Fragment>
                      ),
                      hideFooter:
                        values.credentials.type === "" ||
                        values.credentials.name.length === 0 ||
                        (!_.isUndefined(values.credentials.key) &&
                          !_.isUndefined(values.credentials.token) &&
                          values.credentials.key.length === 0 &&
                          ((!isHttpsCredentialsTypeUser &&
                            values.credentials.token.length === 0) ||
                            (isHttpsCredentialsTypeUser &&
                              (values.credentials.user.length === 0 ||
                                values.credentials.password.length === 0)))),
                      placement: "left",
                      target: "#git-root-add-credentials",
                    },
                    {
                      ...BaseStep,
                      content: t("tours.addGitRoot.rootEnvironment"),
                      hideFooter: values.environment.length === 0,
                      target: "#git-root-add-env",
                    },
                    {
                      ...BaseStep,
                      content: (
                        <React.Fragment>
                          {t("tours.addGitRoot.rootHasHealthCheck")}
                          <ul>
                            {values.includesHealthCheck !== null &&
                              errors.healthCheckConfirm !== undefined && (
                                <li>
                                  {t("tours.addGitRoot.healthCheckConditions")}
                                </li>
                              )}
                          </ul>
                        </React.Fragment>
                      ),
                      hideFooter:
                        values.includesHealthCheck === null ||
                        errors.healthCheckConfirm !== undefined,
                      placement: "left",
                      target: "#git-root-add-health-check",
                    },
                    {
                      ...BaseStep,
                      content:
                        !isGitAccessible || !dirty
                          ? t("tours.addGitRoot.proceedButton.invalidForm")
                          : t("tours.addGitRoot.proceedButton.validForm"),
                      target: "#git-root-add-proceed",
                    },
                  ]}
                />
              ) : undefined}
            </React.Fragment>
          );
        }}
      </Formik>
    </div>
  );
};

export { Repository };
