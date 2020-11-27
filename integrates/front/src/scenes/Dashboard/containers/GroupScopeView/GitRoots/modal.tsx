import { Button } from "components/Button";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { IGitFormAttr } from "../types";
import type { InjectedFormProps } from "redux-form";
import { Modal } from "components/Modal";
import React from "react";
import { SwitchButton } from "components/SwitchButton";
import { useSelector } from "react-redux";
import { useTranslation } from "react-i18next";
import { ArrayField, Checkbox, Dropdown, Text } from "utils/forms/fields";
import {
  ButtonToolbar,
  ControlLabel,
  RequiredField,
} from "styles/styledComponents";
import { Field, FormSection, formValueSelector } from "redux-form";
import { checked, required } from "utils/validations";

interface IGitRootsModalProps {
  onClose: () => void;
  onSubmit: (values: IGitFormAttr) => Promise<void>;
}

const GitRootsModal: React.FC<IGitRootsModalProps> = ({
  onClose,
  onSubmit,
}: IGitRootsModalProps): JSX.Element => {
  const { t } = useTranslation();

  // State management
  const [hasCode, setHasCode] = React.useState(false);
  const [confirmHealthCheck, setConfirmHealthCheck] = React.useState(false);

  const selector: (
    state: Record<string, unknown>,
    field1: string
  ) => string = formValueSelector("gitRoot");
  const filterPolicy: string = useSelector(
    (state: Record<string, unknown>): string => selector(state, "filter.policy")
  );

  return (
    <Modal headerTitle={t("group.scope.common.add")} open={true}>
      <GenericForm
        initialValues={{
          filter: { paths: [""], policy: "NONE" },
          includesHealthCheck: false,
        }}
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
                      name={"url"}
                      type={"text"}
                      validate={[required]}
                    />
                  </div>
                  <div className={"w-30"}>
                    <ControlLabel>
                      <RequiredField>{"*"}&nbsp;</RequiredField>
                      {t("group.scope.git.repo.branch")}
                    </ControlLabel>
                    <Field
                      component={Text}
                      name={"branch"}
                      type={"text"}
                      validate={[required]}
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
                      validate={[required]}
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
                      <RequiredField>{"*"}&nbsp;</RequiredField>
                      {t("group.scope.git.healthCheck.hasCode")}
                    </ControlLabel>
                    <SwitchButton
                      checked={hasCode}
                      offlabel={t("No")}
                      onChange={setHasCode}
                      onlabel={t("Yes")}
                    />
                  </div>
                </div>
                {hasCode ? (
                  <div className={"flex"}>
                    <div className={"w-100"}>
                      <ControlLabel>
                        <RequiredField>{"*"}&nbsp;</RequiredField>
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
                          validate={[checked]}
                        >
                          <RequiredField>{"*"}&nbsp;</RequiredField>
                          {t("group.scope.git.healthCheck.accept")}
                        </Field>
                      ) : undefined}
                    </div>
                  </div>
                ) : undefined}
              </fieldset>
              <FormSection name={"filter"}>
                <fieldset>
                  <legend className={"f3 b"}>
                    {t("group.scope.git.filter.title")}
                  </legend>
                  <ControlLabel>
                    <RequiredField>{"*"}&nbsp;</RequiredField>
                    {t("group.scope.git.filter.policy")}
                  </ControlLabel>
                  <Field
                    component={Dropdown}
                    name={"policy"}
                    validate={[required]}
                  >
                    <option value={"NONE"}>
                      {t("group.scope.git.filter.none")}
                    </option>
                    <option value={"INCLUDE"}>
                      {t("group.scope.git.filter.include")}
                    </option>
                    <option value={"EXCLUDE"}>
                      {t("group.scope.git.filter.exclude")}
                    </option>
                  </Field>
                  {filterPolicy === "NONE" ? undefined : (
                    <React.Fragment>
                      <ControlLabel>
                        <RequiredField>{"*"}&nbsp;</RequiredField>
                        {t("group.scope.git.filter.paths")}
                      </ControlLabel>
                      <ArrayField initialValue={""} name={"paths"}>
                        {(fieldName: string): JSX.Element => (
                          <Field
                            component={Text}
                            name={fieldName}
                            type={"text"}
                            validate={[required]}
                          />
                        )}
                      </ArrayField>
                    </React.Fragment>
                  )}
                </fieldset>
              </FormSection>
            </React.Fragment>
            <ButtonToolbar>
              <Button onClick={onClose}>{t("confirmmodal.cancel")}</Button>
              <Button disabled={pristine || submitting} type={"submit"}>
                {t("confirmmodal.proceed")}
              </Button>
            </ButtonToolbar>
          </React.Fragment>
        )}
      </GenericForm>
    </Modal>
  );
};

export { GitRootsModal };
