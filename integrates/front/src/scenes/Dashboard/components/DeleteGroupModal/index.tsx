import React from "react";
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
import { translate } from "utils/translations/translate";
import { required } from "utils/validations";

interface IDeleteGroupModalProps {
  groupName: string;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: { confirmation: string }) => void;
}

const DeleteGroupModal: React.FC<IDeleteGroupModalProps> = (
  props: IDeleteGroupModalProps
): JSX.Element => {
  const { groupName, isOpen, onClose, onSubmit } = props;

  function formValidations(values: {
    confirmation: string;
  }): { confirmation?: string } {
    return values.confirmation === groupName
      ? {}
      : {
          confirmation: translate.t(
            "searchFindings.servicesTable.errors.expectedGroupName",
            { groupName }
          ),
        };
  }

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t(
          "searchFindings.servicesTable.deleteGroup.deleteGroup"
        )}
        open={isOpen}
      >
        <GenericForm
          initialValues={{
            confirmation: "",
          }}
          name={"removeGroup"}
          onSubmit={onSubmit}
          validate={formValidations}
        >
          {({ handleSubmit, valid }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              <ControlLabel>
                {translate.t(
                  "searchFindings.servicesTable.deleteGroup.warningTitle"
                )}
              </ControlLabel>
              <Alert>
                {translate.t(
                  "searchFindings.servicesTable.deleteGroup.warningBody"
                )}
              </Alert>
              <FormGroup>
                <ControlLabel>
                  {translate.t(
                    "searchFindings.servicesTable.deleteGroup.typeGroupName"
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
                      {translate.t("confirmmodal.cancel")}
                    </Button>
                    <Button
                      disabled={!valid}
                      onClick={handleSubmit}
                      type={"submit"}
                    >
                      {translate.t("confirmmodal.proceed")}
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

export { DeleteGroupModal };
