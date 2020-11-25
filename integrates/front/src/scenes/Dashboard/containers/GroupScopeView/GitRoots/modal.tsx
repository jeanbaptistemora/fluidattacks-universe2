import { Button } from "components/Button";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { InjectedFormProps } from "redux-form";
import { Modal } from "components/Modal";
import React from "react";
import { required } from "utils/validations";
import { useSelector } from "react-redux";
import { useTranslation } from "react-i18next";
import { ArrayField, Dropdown, Text } from "utils/forms/fields";
import {
  ButtonToolbar,
  ControlLabel,
  RequiredField,
} from "styles/styledComponents";
import { Field, FormSection, formValueSelector } from "redux-form";

interface IGitRootsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: () => void;
}

const GitRootsModal: React.FC<IGitRootsModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
}: IGitRootsModalProps): JSX.Element => {
  const { t } = useTranslation();

  // State management
  const selector: (
    state: Record<string, unknown>,
    field: string
  ) => string = formValueSelector("gitRoots");
  const filterPolicy: string = useSelector(
    (state: Record<string, unknown>): string => selector(state, "filter.policy")
  );

  return (
    <Modal headerTitle={t("group.scope.common.add")} open={isOpen}>
      <GenericForm
        initialValues={{ filter: { paths: [""], policy: "NONE" } }}
        name={"gitRoots"}
        onSubmit={onSubmit}
      >
        {({ pristine }: InjectedFormProps): JSX.Element => (
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
                      type={"text"}
                      validate={[required]}
                    />
                  </div>
                </div>
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
              <Button disabled={pristine} type={"submit"}>
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
