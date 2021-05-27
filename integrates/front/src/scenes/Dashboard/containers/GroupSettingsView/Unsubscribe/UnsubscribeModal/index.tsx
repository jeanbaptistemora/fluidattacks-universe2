import React from "react";
import { useTranslation } from "react-i18next";
import { Field } from "redux-form";
import type { InjectedFormProps } from "redux-form";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import {
  Alert,
  ButtonToolbar,
  Col100,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { Text } from "utils/forms/fields";
import { required } from "utils/validations";

interface IUnsubscribeModalProps {
  groupName: string;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: { confirmation: string }) => void;
}

const UnsubscribeModal: React.FC<IUnsubscribeModalProps> = (
  props: IUnsubscribeModalProps
): JSX.Element => {
  const { groupName, isOpen, onClose, onSubmit } = props;
  const { t } = useTranslation();

  function formValidations(values: {
    confirmation: string;
  }): { confirmation?: string } {
    return values.confirmation === groupName
      ? {}
      : {
          confirmation: t(
            "searchFindings.servicesTable.errors.expectedGroupName",
            { groupName }
          ),
        };
  }

  return (
    <React.StrictMode>
      <Modal
        headerTitle={t("searchFindings.servicesTable.unsubscribe.title")}
        open={isOpen}
      >
        <GenericForm
          initialValues={{
            confirmation: "",
          }}
          name={"unsubscribeFromGroup"}
          onSubmit={onSubmit}
          validate={formValidations}
        >
          {({ handleSubmit, valid }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              <ControlLabel>
                {t("searchFindings.servicesTable.unsubscribe.warningTitle")}
              </ControlLabel>
              <Alert>
                {t("searchFindings.servicesTable.unsubscribe.warningBody")}
              </Alert>
              <FormGroup>
                <ControlLabel>
                  {t("searchFindings.servicesTable.unsubscribe.typeGroupName")}
                </ControlLabel>
                <Field
                  component={Text}
                  name={"confirmation"}
                  placeholder={groupName.toLowerCase()}
                  type={"text"}
                  validate={required}
                />
              </FormGroup>
              <hr />
              <Row>
                <Col100>
                  <ButtonToolbar>
                    <Button onClick={onClose}>
                      {t("confirmmodal.cancel")}
                    </Button>
                    <Button
                      disabled={!valid}
                      onClick={handleSubmit}
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
    </React.StrictMode>
  );
};

export { UnsubscribeModal, IUnsubscribeModalProps };
