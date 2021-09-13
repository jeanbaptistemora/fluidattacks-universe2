import { faQuestionCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FieldValidator } from "formik";
import { Field, Form, Formik } from "formik";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import type { IGitRootAttr } from "../../types";
import { GitIgnoreAlert, gitModalSchema } from "../helpers";
import { Button } from "components/Button";
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
import { openUrl } from "utils/resourceHelpers";
import { checked, required } from "utils/validations";

interface IRepositoryProps {
  initialValues: IGitRootAttr;
  isEditing: boolean;
  nicknames: string[];
  onClose: () => void;
  onSubmit: (values: IGitRootAttr) => Promise<void>;
}

const Repository: React.FC<IRepositoryProps> = ({
  initialValues,
  isEditing,
  nicknames,
  onClose,
  onSubmit,
}: IRepositoryProps): JSX.Element => {
  const { t } = useTranslation();

  const isDuplicated = (field: string): boolean => {
    const repoName: string = field
      ? field.split("/").slice(-1)[0].replace(".git", "")
      : "";
    const { nickname: initialNickname } = initialValues;

    return nicknames.includes(repoName) && initialNickname !== repoName;
  };

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

  const [confirmHealthCheck, setConfirmHealthCheck] = useState(
    initialValues.includesHealthCheck
  );

  const goToDocumentation = useCallback((): void => {
    openUrl(
      "https://mirrors.edge.kernel.org/pub/software/scm/git/docs/gitignore.html#_pattern_format"
    );
  }, []);

  return (
    <div>
      <Formik
        initialValues={initialValues}
        name={"gitRoot"}
        onSubmit={onSubmit}
        validationSchema={gitModalSchema}
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
                    <Field component={FormikText} name={"url"} type={"text"} />
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
    </div>
  );
};

export { Repository };
