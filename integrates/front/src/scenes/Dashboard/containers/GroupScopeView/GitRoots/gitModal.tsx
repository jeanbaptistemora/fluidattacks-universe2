import { Button } from "components/Button";
import { Can } from "utils/authz/Can";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { Glyphicon } from "react-bootstrap";
import type { IGitRootAttr } from "../types";
import type { InjectedFormProps } from "redux-form";
import { Modal } from "components/NewModal";
import React from "react";
import { SwitchButton } from "components/SwitchButton";
import { TooltipWrapper } from "components/TooltipWrapper";
import _ from "lodash";
import style from "./index.css";
import { useSelector } from "react-redux";
import { useTranslation } from "react-i18next";
import {
  Alert,
  ButtonToolbar,
  Col100,
  ControlLabel,
  RequiredField,
  Row,
} from "styles/styledComponents";
import { ArrayField, Checkbox, Text } from "utils/forms/fields";
import { Field, formValueSelector } from "redux-form";
import { checked, excludeFormat, required } from "utils/validations";

interface IGitModalProps {
  initialValues: IGitRootAttr | undefined;
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
    state: "ACTIVE",
    url: "",
  },
  onClose,
  onSubmit,
}: IGitModalProps): JSX.Element => {
  const isEditing: boolean = initialValues.url !== "";

  const { t } = useTranslation();

  // State management
  const selector: (
    state: Record<string, unknown>,
    field: string
  ) => string[] = formValueSelector("gitRoot");
  const gitIgnoreValues: string[] = useSelector(
    (state: Record<string, unknown>): string[] =>
      selector(state, "filter.exclude")
  );

  const [confirmHealthCheck, setConfirmHealthCheck] = React.useState(
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
      <GenericForm
        initialValues={initialValues}
        name={"gitRoot"}
        onSubmit={onSubmit}
      >
        {({ pristine, submitting }: InjectedFormProps): JSX.Element => (
          <React.Fragment>
            <React.Fragment>
              <fieldset>
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
                      component={Text}
                      disabled={isEditing}
                      name={"url"}
                      type={"text"}
                      validate={required}
                    />
                  </div>
                  <div className={"w-30"}>
                    <ControlLabel>
                      <RequiredField>{"*"}&nbsp;</RequiredField>
                      {t("group.scope.git.repo.branch")}
                    </ControlLabel>
                    <Field
                      component={Text}
                      disabled={isEditing}
                      name={"branch"}
                      type={"text"}
                      validate={required}
                    />
                  </div>
                </div>
                <div className={"flex"}>
                  <div className={"w-100"}>
                    <ControlLabel>
                      <RequiredField>{"*"}&nbsp;</RequiredField>
                      {t("group.scope.git.repo.environment")}
                    </ControlLabel>
                    <Field
                      component={Text}
                      name={"environment"}
                      placeholder={t("group.scope.git.repo.environmentHint")}
                      type={"text"}
                      validate={required}
                    />
                  </div>
                </div>
              </fieldset>
              <fieldset>
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
                        component={Checkbox}
                        name={"includesHealthCheck"}
                        type={"checkbox"}
                        validate={checked}
                      >
                        <RequiredField>{"*"}&nbsp;</RequiredField>
                        {t("group.scope.git.healthCheck.accept")}
                      </Field>
                    ) : undefined}
                  </div>
                </div>
              </fieldset>
              <Can do={"update_git_root_filter"}>
                <fieldset>
                  <TooltipWrapper message={t("group.scope.git.filter.tooltip")}>
                    <ControlLabel>
                      {t("group.scope.git.filter.exclude")}
                    </ControlLabel>
                  </TooltipWrapper>
                  <Button
                    // eslint-disable-next-line react/forbid-component-props
                    className={style.button}
                    onClick={goToDocumentation}
                  >
                    <Glyphicon glyph={"glyphicon glyphicon-question-sign"} />
                  </Button>
                  {_.isUndefined(gitIgnoreValues) ? undefined : _.isEmpty(
                      gitIgnoreValues
                    ) ? undefined : (
                    <Alert>{t("group.scope.git.filter.warning")}</Alert>
                  )}
                  <ArrayField
                    allowEmpty={true}
                    initialValue={""}
                    name={"gitignore"}
                  >
                    {(fieldName: string): JSX.Element => (
                      <Field
                        component={Text}
                        name={fieldName}
                        placeholder={t("group.scope.git.filter.placeholder")}
                        type={"text"}
                        validate={excludeFormat}
                      />
                    )}
                  </ArrayField>
                </fieldset>
              </Can>
            </React.Fragment>
            <hr />
            <Row>
              <Col100>
                <ButtonToolbar>
                  <Button onClick={onClose}>{t("confirmmodal.cancel")}</Button>
                  <Button
                    disabled={pristine || submitting}
                    id={"git-root-add-proceed"}
                    type={"submit"}
                  >
                    {t("confirmmodal.proceed")}
                  </Button>
                </ButtonToolbar>
              </Col100>
            </Row>
          </React.Fragment>
        )}
      </GenericForm>
    </Modal>
  );
};

export { GitModal };
