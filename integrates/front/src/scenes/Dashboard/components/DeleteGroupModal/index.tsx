import { Button } from "components/Button";
import { Field } from "redux-form";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { InjectedFormProps } from "redux-form";
import { Modal } from "components/Modal";
import React from "react";
import { Text } from "utils/forms/fields";
import { required } from "utils/validations";
import { translate } from "utils/translations/translate";
import {
  Alert,
  ButtonToolbar,
  ControlLabel,
  FormGroup,
} from "styles/styledComponents";

interface IDeleteGroupModalProps {
  groupName: string;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: { confirmation: string }) => void;
}

const deleteGroupModal: React.FC<IDeleteGroupModalProps> = (
  props: IDeleteGroupModalProps
): JSX.Element => {
  const { groupName, isOpen, onClose, onSubmit } = props;

  function formValidations(values: {
    confirmation: string;
  }): { confirmation?: string } {
    return values.confirmation !== groupName
      ? {}
      : {
          confirmation: translate.t(
            "search_findings.services_table.errors.expected_group_name",
            { groupName }
          ),
        };
  }

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t(
          "search_findings.services_table.delete_group.delete_group"
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
                  "search_findings.services_table.delete_group.warning_title"
                )}
              </ControlLabel>
              <Alert>
                {translate.t(
                  "search_findings.services_table.delete_group.warning_body"
                )}
              </Alert>
              <FormGroup>
                <ControlLabel>
                  {translate.t(
                    "search_findings.services_table.delete_group.type_group_name"
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
            </React.Fragment>
          )}
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};

export { deleteGroupModal as DeleteGroupModal };
