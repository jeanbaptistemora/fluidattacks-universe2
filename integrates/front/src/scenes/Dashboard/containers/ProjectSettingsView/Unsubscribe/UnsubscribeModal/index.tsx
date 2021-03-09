import { Button } from "components/Button";
import { Field } from "redux-form";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { InjectedFormProps } from "redux-form";
import { Modal } from "components/Modal";
import React from "react";
import { Text } from "utils/forms/fields";
import { required } from "utils/validations";
import { useTranslation } from "react-i18next";
import {
  Alert,
  ButtonToolbar,
  Col100,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";

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
            "search_findings.services_table.errors.expected_group_name",
            { groupName }
          ),
        };
  }

  return (
    <React.StrictMode>
      <Modal
        headerTitle={t("search_findings.services_table.unsubscribe.title")}
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
                {t("search_findings.services_table.unsubscribe.warningTitle")}
              </ControlLabel>
              <Alert>
                {t("search_findings.services_table.unsubscribe.warningBody")}
              </Alert>
              <FormGroup>
                <ControlLabel>
                  {t(
                    "search_findings.services_table.unsubscribe.type_group_name"
                  )}
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
