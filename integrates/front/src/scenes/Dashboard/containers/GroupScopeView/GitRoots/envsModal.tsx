import { Button } from "components/Button";
import { Field } from "redux-form";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { IGitRootAttr } from "../types";
import type { InjectedFormProps } from "redux-form";
import { Modal } from "components/Modal";
import React from "react";
import { required } from "utils/validations";
import { useTranslation } from "react-i18next";
import { ArrayField, Text } from "utils/forms/fields";
import {
  ButtonToolbar,
  ControlLabel,
  RequiredField,
} from "styles/styledComponents";

interface IEnvsModalProps {
  initialValues: { environmentUrls: string[] };
  onClose: () => void;
  onSubmit: (values: IGitRootAttr) => Promise<void>;
}

const EnvsModal: React.FC<IEnvsModalProps> = ({
  initialValues,
  onClose,
  onSubmit,
}: IEnvsModalProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <Modal headerTitle={t("group.scope.git.manageEnvs")} open={true}>
      <GenericForm
        initialValues={initialValues}
        name={"gitEnvs"}
        onSubmit={onSubmit}
      >
        {({ pristine, submitting }: InjectedFormProps): JSX.Element => (
          <React.Fragment>
            <ControlLabel>
              <RequiredField>{"*"}&nbsp;</RequiredField>
              {t("group.scope.git.envUrls")}
            </ControlLabel>
            <ArrayField
              allowEmpty={false}
              initialValue={""}
              name={"environmentUrls"}
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

export { EnvsModal };
