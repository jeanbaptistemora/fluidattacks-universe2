import { Button } from "components/Button";
import { Can } from "utils/authz/Can";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { IGitRootAttr } from "../types";
import type { InjectedFormProps } from "redux-form";
import { Modal } from "components/Modal";
import React from "react";
import { SwitchButton } from "components/SwitchButton";
import { useTranslation } from "react-i18next";
import { ArrayField, Checkbox, Text } from "utils/forms/fields";
import {
  ButtonToolbar,
  ControlLabel,
  RequiredField,
} from "styles/styledComponents";
import { Field, FormSection } from "redux-form";
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
    filter: { exclude: [], include: ["*"] },
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
  const [confirmHealthCheck, setConfirmHealthCheck] = React.useState(
    initialValues.includesHealthCheck
  );

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
                <FormSection name={"filter"}>
                  <fieldset>
                    <legend className={"f3 b"}>
                      {t("group.scope.git.filter.title")}
                    </legend>
                    <ControlLabel>
                      <RequiredField>{"*"}&nbsp;</RequiredField>
                      {t("group.scope.git.filter.include")}
                    </ControlLabel>
                    <ArrayField
                      allowEmpty={false}
                      initialValue={""}
                      name={"include"}
                    >
                      {(fieldName: string): JSX.Element => (
                        <Field
                          component={Text}
                          name={fieldName}
                          type={"text"}
                          validate={required}
                        />
                      )}
                    </ArrayField>
                    <ControlLabel>
                      {t("group.scope.git.filter.exclude")}
                    </ControlLabel>
                    <ArrayField
                      allowEmpty={true}
                      initialValue={""}
                      name={"exclude"}
                    >
                      {(fieldName: string): JSX.Element => (
                        <Field
                          component={Text}
                          name={fieldName}
                          type={"text"}
                          validate={excludeFormat}
                        />
                      )}
                    </ArrayField>
                  </fieldset>
                </FormSection>
              </Can>
            </React.Fragment>
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
          </React.Fragment>
        )}
      </GenericForm>
    </Modal>
  );
};

export { GitModal };
