import React from "react";
import { useTranslation } from "react-i18next";
import { Field } from "redux-form";
import type { InjectedFormProps } from "redux-form";

import type { IGitRootAttr } from "../types";
import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  RequiredField,
  Row,
} from "styles/styledComponents";
import { ArrayField, Text } from "utils/forms/fields";
import { required } from "utils/validations";

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
              allowEmpty={true}
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
            <hr />
            <Row>
              <Col100>
                <ButtonToolbar>
                  <Button onClick={onClose}>{t("confirmmodal.cancel")}</Button>
                  <Button
                    disabled={pristine || submitting}
                    id={"envs-manage-proceed"}
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

export { EnvsModal };
