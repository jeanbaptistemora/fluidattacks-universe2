import { faQuestionCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import type { Validator as ValidatorField } from "redux-form";
import type { BaseSchema } from "yup";
import { array, lazy, object, string } from "yup";

import type { IGitRootAttr } from "../types";
import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { SwitchButton } from "components/SwitchButton";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  Alert,
  ButtonToolbar,
  Col100,
  ControlLabel,
  QuestionButton,
  RequiredField,
  Row,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import {
  FormikArrayField,
  FormikCheckbox,
  FormikText,
} from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { checked, required } from "utils/validations";

interface IGitModalProps {
  initialValues: IGitRootAttr | undefined;
  nicknames: string[];
  onClose: () => void;
  onSubmit: (values: IGitRootAttr) => Promise<void>;
}

const GitModal: React.FC<IGitModalProps> = ({
  initialValues = {
    __typename: "GitRoot",
    branch: "",
    cloningStatus: {
      message: "",
      status: "UNKNOWN",
    },
    environment: "",
    environmentUrls: [],
    gitignore: [],
    id: "",
    includesHealthCheck: false,
    nickname: "",
    state: "ACTIVE",
    url: "",
  },
  nicknames,
  onClose,
  onSubmit,
}: IGitModalProps): JSX.Element => {
  const isEditing: boolean = initialValues.url !== "";

  const [isDuplicated, setIsDuplicated] = useState(false);

  const { t } = useTranslation();

  const duplicated: (field: string) => ValidatorField = useCallback(
    (field: string): ValidatorField => {
      const repoName: string = field
        ? field.split("/").slice(-1)[0].replace(".git", "")
        : "";
      const { nickname: initialNickname } = initialValues;
      if (nicknames.includes(repoName) && initialNickname !== repoName) {
        setIsDuplicated(true);
      } else {
        setIsDuplicated(false);
      }

      return required(field) as ValidatorField;
    },
    [initialValues, nicknames]
  );

  const requireNickname: (field: string) => ValidatorField = useCallback(
    (field: string): ValidatorField => {
      const { nickname: initialNickname } = initialValues;
      if (nicknames.includes(field) && initialNickname !== field) {
        return t("validations.requireNickname");
      }

      return required(field) as ValidatorField;
    },
    [initialValues, nicknames, t]
  );

  const [confirmHealthCheck, setConfirmHealthCheck] = useState(
    initialValues.includesHealthCheck
  );

  function goToDocumentation(): void {
    window.open(t("group.scope.git.filter.documentation"));
  }

  return (
    <Modal
      headerTitle={t(`group.scope.common.${isEditing ? "edit" : "add"}`)}
      open={true}
    >
      <Formik
        initialValues={initialValues}
        name={"gitRoot"}
        onSubmit={onSubmit}
        validationSchema={lazy(
          (values: IGitRootAttr): BaseSchema =>
            object().shape({
              gitignore: array().of(
                string()
                  .required(translate.t("validations.required"))
                  .test(
                    "excludeFormat",
                    translate.t("validations.excludeFormat"),
                    (value): boolean => {
                      const repoUrl = values.url;

                      if (!_.isUndefined(repoUrl) && !_.isUndefined(value)) {
                        const [urlBasename] = repoUrl.split("/").slice(-1);
                        const repoName: string = urlBasename.endsWith(".git")
                          ? urlBasename.replace(".git", "")
                          : urlBasename;

                        return (
                          value
                            .toLowerCase()
                            .split("/")
                            .indexOf(repoName.toLowerCase()) !== 0
                        );
                      }

                      return false;
                    }
                  )
              ),
            })
        )}
      >
        {({ dirty, isSubmitting, values }): JSX.Element => (
          <Form>
            <React.Fragment>
              <fieldset className={"bn"}>
                <legend className={"f3 b"}>
                  {t("group.scope.git.repo.title")}
                </legend>
                <div className={"flex"}>
                  <div className={"w-70 mr3"}>
                    <ControlLabel>
                      <RequiredField>{"*"}&nbsp;</RequiredField>
                      {t("group.scope.git.repo.url")}
                    </ControlLabel>
                    <Field
                      component={FormikText}
                      disabled={isEditing}
                      name={"url"}
                      type={"text"}
                      validate={duplicated}
                    />
                  </div>
                  <div className={"w-30"}>
                    <ControlLabel>
                      <RequiredField>{"*"}&nbsp;</RequiredField>
                      {t("group.scope.git.repo.branch")}
                    </ControlLabel>
                    <Field
                      component={FormikText}
                      disabled={isEditing}
                      name={"branch"}
                      type={"text"}
                      validate={required}
                    />
                  </div>
                </div>
                <br />
                {isDuplicated ? (
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
                <div className={"flex"}>
                  <div className={"w-100"}>
                    <ControlLabel>
                      <RequiredField>{"*"}&nbsp;</RequiredField>
                      {t("group.scope.git.repo.environment")}
                    </ControlLabel>
                    <Field
                      component={FormikText}
                      name={"environment"}
                      placeholder={t("group.scope.git.repo.environmentHint")}
                      type={"text"}
                      validate={required}
                    />
                  </div>
                </div>
                <br />
              </fieldset>
              <fieldset className={"bn"}>
                <legend className={"f3 b"}>
                  {t("group.scope.git.healthCheck.title")}
                </legend>
                <div className={"flex"}>
                  <div className={"w-100"}>
                    <ControlLabel>
                      {t("group.scope.git.healthCheck.confirm")}
                    </ControlLabel>
                    <SwitchButton
                      checked={confirmHealthCheck}
                      offlabel={t("No")}
                      onChange={setConfirmHealthCheck}
                      onlabel={t("Yes")}
                    />
                    {confirmHealthCheck ? (
                      <Field
                        component={FormikCheckbox}
                        label={t("group.scope.git.healthCheck.accept")}
                        name={"includesHealthCheck"}
                        type={"checkbox"}
                        validate={checked}
                      >
                        <RequiredField>{"*"}&nbsp;</RequiredField>
                      </Field>
                    ) : undefined}
                  </div>
                </div>
              </fieldset>
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
                  <QuestionButton
                    // eslint-disable-next-line react/forbid-component-props
                    onClick={goToDocumentation}
                  >
                    <FontAwesomeIcon icon={faQuestionCircle} />
                  </QuestionButton>
                  {_.isUndefined(values.gitignore) ? undefined : _.isEmpty(
                      values.gitignore
                    ) ? undefined : (
                    <Alert>{t("group.scope.git.filter.warning")}</Alert>
                  )}
                  <FormikArrayField
                    allowEmpty={true}
                    arrayValues={values.gitignore}
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
            <hr />
            <Row>
              <Col100>
                <ButtonToolbar>
                  <Button onClick={onClose}>{t("confirmmodal.cancel")}</Button>
                  <Button
                    disabled={!dirty || isSubmitting}
                    id={"git-root-add-proceed"}
                    type={"submit"}
                  >
                    {t("confirmmodal.proceed")}
                  </Button>
                </ButtonToolbar>
              </Col100>
            </Row>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};

export { GitModal };
