/* eslint-disable complexity */
import { Buffer } from "buffer";

import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import {
  faQuestionCircle,
  faTrashAlt,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FieldValidator, FormikProps } from "formik";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import React, { useCallback, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import { VALIDATE_GIT_ACCESS } from "../../queries";
import type { IGitRootAttr } from "../../types";
import { GitIgnoreAlert, gitModalSchema } from "../helpers";
import { Button } from "components/Button";
import { ModalFooter } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import { BaseStep, Tour } from "components/Tour";
import {
  Alert,
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
import { msgError, msgSuccess } from "utils/notifications";
import { openUrl } from "utils/resourceHelpers";
import {
  checked,
  composeValidators,
  hasSshFormat,
  required,
  selected,
} from "utils/validations";

interface IRepositoryProps {
  groupName: string;
  initialValues: IGitRootAttr;
  isEditing: boolean;
  nicknames: string[];
  onClose: () => void;
  onSubmit: (values: IGitRootAttr) => Promise<void>;
  runTour: boolean;
}

const Repository: React.FC<IRepositoryProps> = ({
  groupName,
  initialValues,
  isEditing,
  nicknames,
  onClose,
  onSubmit,
  runTour,
}: IRepositoryProps): JSX.Element => {
  const { t } = useTranslation();

  const isDuplicated = (field: string): boolean => {
    const repoName: string = field
      ? field.split("/").slice(-1)[0].replace(".git", "")
      : "";
    const { nickname: initialNickname } = initialValues;

    return nicknames.includes(repoName) && initialNickname !== repoName;
  };

  const [isGitAccessible, changeGitAccessibility] = useState(true);
  const [credExists, deleteExistingCred] = useState(
    initialValues.credentials.id !== ""
  );

  const deleteCredential: () => void = useCallback((): void => {
    deleteExistingCred(false);
  }, []);

  const requireNickname: FieldValidator = useCallback(
    (field: string): string | undefined => {
      const { nickname: initialNickname } = initialValues;
      if (nicknames.includes(field) && initialNickname !== field) {
        return t("validations.requireNickname");
      }

      return required(field) as string | undefined;
    },
    [initialValues, nicknames, t]
  );

  const requireGitAccessibility: FieldValidator = (): string | undefined => {
    if (!isGitAccessible) {
      return t("group.scope.git.repo.credentials.checkAccess.noAccess");
    }

    return undefined;
  };

  const [confirmHealthCheck, setConfirmHealthCheck] = useState(
    isEditing ? initialValues.includesHealthCheck : null
  );
  const [isHttpsCredentialsTypeUser, setHttpsCredentialsTypeUser] =
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

  const [validateGitAccess] = useMutation(VALIDATE_GIT_ACCESS, {
    onCompleted: (): void => {
      changeGitAccessibility(true);
      msgSuccess(
        t("group.scope.git.repo.credentials.checkAccess.success"),
        t("group.scope.git.repo.credentials.checkAccess.successTitle")
      );
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        if (
          error.message ===
          "Exception - Git repository was not accessible with given credentials"
        ) {
          msgError(t("group.scope.git.errors.invalidGitCredentials"));
        } else {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.error("Couldn't activate root", error);
        }
      });
      changeGitAccessibility(false);
    },
  });

  const formRef = useRef<FormikProps<IGitRootAttr>>(null);

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

  const checkedValidation = isCheckedHealthCheck ? undefined : checked;
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

  return (
    <div>
      <Formik
        initialValues={initialValues}
        innerRef={formRef}
        name={"gitRoot"}
        onSubmit={onSubmit}
        validationSchema={gitModalSchema}
      >
        {({ dirty, isSubmitting, values }): JSX.Element => (
          <React.Fragment>
            <Form>
              <React.Fragment>
                <fieldset className={"bn"}>
                  <legend className={"f3 b"}>
                    {t("group.scope.git.repo.title")}
                  </legend>
                  <div className={"flex"} id={"git-root-add-repo"}>
                    <div className={"w-70 mr3"}>
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
                    <div className={"w-30"}>
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
                  </div>
                  {isEditing && values.branch !== initialValues.branch ? (
                    <Alert>{t("group.scope.common.changeWarning")}</Alert>
                  ) : undefined}
                  <br />
                  {isDuplicated(values.url) ? (
                    <React.Fragment>
                      <div className={"flex"}>
                        <div className={"w-100"}>
                          <ControlLabel>
                            <RequiredField>{"*"}&nbsp;</RequiredField>
                            {t("group.scope.git.repo.nickname")}
                          </ControlLabel>
                          <Field
                            component={FormikText}
                            name={"nickname"}
                            placeholder={t("group.scope.git.repo.nicknameHint")}
                            type={"text"}
                            validate={requireNickname}
                          />
                        </div>
                      </div>
                      <br />
                    </React.Fragment>
                  ) : undefined}
                  <div id={"git-root-add-credentials"}>
                    <div className={"flex"}>
                      <div className={"w-30 mr3"}>
                        <ControlLabel>
                          {t("group.scope.git.repo.credentials.type")}
                        </ControlLabel>
                        {credExists ? (
                          <Field
                            component={FormikText}
                            disabled={true}
                            name={"credentials.type"}
                            value={values.credentials.type}
                          />
                        ) : (
                          <Field
                            component={FormikDropdown}
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
                        )}
                      </div>
                      <div className={"w-70"}>
                        <ControlLabel>
                          {t("group.scope.git.repo.credentials.name")}
                        </ControlLabel>
                        <div className={"flex"}>
                          <Field
                            component={FormikText}
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
                            validate={composeValidators([
                              hasSshFormat,
                              required,
                              requireGitAccessibility,
                            ])}
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
                          onSelect={setHttpsCredentialsTypeUser}
                          type={"Radio"}
                          validate={selected}
                        />
                        {isHttpsCredentialsTypeUser ? (
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
                                {t("group.scope.git.repo.credentials.password")}
                              </ControlLabel>
                              <Field
                                component={FormikText}
                                name={"credentials.password"}
                                type={"text"}
                              />
                            </div>
                          </div>
                        ) : (
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
                  </div>
                  {
                    <div className={"mt2 tr"}>
                      <Button
                        disabled={submittableCredentials(values)}
                        id={"checkAccessBtn"}
                        onClick={handleCheckAccessClick}
                        variant={"secondary"}
                      >
                        {t("group.scope.git.repo.credentials.checkAccess.text")}
                      </Button>
                    </div>
                  }
                  <div className={"flex mt3"}>
                    <div className={"w-100"}>
                      <ControlLabel>
                        <RequiredField>{"*"}&nbsp;</RequiredField>
                        {t("group.scope.git.repo.environment")}
                      </ControlLabel>
                      <Field
                        component={FormikText}
                        id={"git-root-add-env"}
                        name={"environment"}
                        placeholder={t("group.scope.git.repo.environmentHint")}
                        type={"text"}
                        validate={required}
                      />
                    </div>
                  </div>
                  <br />
                </fieldset>
                <Have I={"is_continuous"}>
                  <div id={"git-root-add-healthcheck"}>
                    <fieldset className={"bn"}>
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
                            validate={selected}
                          />
                          {[values.url, values.branch].join("") === isRootChange
                            ? undefined
                            : rootChanged(values)}
                          {confirmHealthCheck ?? false ? (
                            <Alert>
                              <Field
                                component={FormikCheckbox}
                                isChecked={isCheckedHealthCheck}
                                label={""}
                                name={"includesHealthCheckA"}
                                type={"checkbox"}
                                validate={checkedValidation}
                              >
                                {t("group.scope.git.healthCheck.accept")}
                                <RequiredField>{"*"}&nbsp;</RequiredField>
                              </Field>
                            </Alert>
                          ) : undefined}
                          {confirmHealthCheck ?? true ? undefined : (
                            <Alert>
                              <Field
                                component={FormikCheckbox}
                                isChecked={isCheckedHealthCheck}
                                label={""}
                                name={"rejectHealthCheckA"}
                                type={"checkbox"}
                                validate={checkedValidation}
                              >
                                {t("group.scope.git.healthCheck.rejectA")}
                                <RequiredField>{"*"}&nbsp;</RequiredField>
                              </Field>
                              <Field
                                component={FormikCheckbox}
                                isChecked={isCheckedHealthCheck}
                                label={""}
                                name={"rejectHealthCheckB"}
                                type={"checkbox"}
                                validate={checkedValidation}
                              >
                                {t("group.scope.git.healthCheck.rejectB")}
                                <RequiredField>{"*"}&nbsp;</RequiredField>
                              </Field>
                              <Field
                                component={FormikCheckbox}
                                isChecked={isCheckedHealthCheck}
                                label={""}
                                name={"rejectHealthCheckC"}
                                type={"checkbox"}
                                validate={checkedValidation}
                              >
                                {t("group.scope.git.healthCheck.rejectC")}
                                <RequiredField>{"*"}&nbsp;</RequiredField>
                              </Field>
                            </Alert>
                          )}
                        </div>
                      </div>
                    </fieldset>
                  </div>
                </Have>
                <Can do={"update_git_root_filter"}>
                  <fieldset className={"bn"}>
                    <TooltipWrapper
                      displayClass={"dib"}
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
                          placeholder={t("group.scope.git.filter.placeholder")}
                          type={"text"}
                        />
                      )}
                    </FormikArrayField>
                  </fieldset>
                </Can>
              </React.Fragment>
              <ModalFooter>
                <Button onClick={onClose} variant={"secondary"}>
                  {t("confirmmodal.cancel")}
                </Button>
                <Button
                  disabled={!dirty || isSubmitting}
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
                run={runTour}
                steps={[
                  {
                    ...BaseStep,
                    content: t("tours.addGitRoot.rootInfo"),
                    hideFooter:
                      values.url.length === 0 || values.branch.length === 0,
                    target: "#git-root-add-repo",
                  },
                  {
                    ...BaseStep,
                    content: t("tours.addGitRoot.rootCredentials"),
                    hideFooter:
                      values.credentials.type === "" ||
                      values.credentials.name.length === 0 ||
                      (values.credentials.key.length === 0 &&
                        values.credentials.token.length === 0 &&
                        (values.credentials.user.length === 0 ||
                          values.credentials.password.length === 0)),
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
                    content: t("tours.addGitRoot.rootHasHealthcheck"),
                    hideFooter: values.includesHealthCheck === null,
                    placement: "left",
                    target: "#git-root-add-healthcheck",
                  },
                  {
                    ...BaseStep,
                    content: t("tours.addGitRoot.proceedButton"),
                    target: "#git-root-add-proceed",
                  },
                ]}
              />
            ) : undefined}
          </React.Fragment>
        )}
      </Formik>
    </div>
  );
};

export { Repository };
