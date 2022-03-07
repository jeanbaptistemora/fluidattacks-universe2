import { Field, Formik } from "formik";
import React from "react";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  Alert,
  ButtonToolbar,
  Col100,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { FormikDropdown, FormikText } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { required } from "utils/validations";

interface IDeleteGroupModalProps {
  groupName: string;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: { confirmation: string; reason: string }) => void;
}

const DeleteGroupModal: React.FC<IDeleteGroupModalProps> = (
  props: IDeleteGroupModalProps
): JSX.Element => {
  const { groupName, isOpen, onClose, onSubmit } = props;

  function formValidations(values: { confirmation: string; reason: string }): {
    confirmation?: string;
    reason?: string;
  } {
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
        open={isOpen}
        title={translate.t(
          "searchFindings.servicesTable.deleteGroup.deleteGroup"
        )}
      >
        <Formik
          initialValues={{
            confirmation: "",
            reason: "NO_SYSTEM",
          }}
          name={"removeGroup"}
          onSubmit={onSubmit}
          validate={formValidations}
        >
          {({ submitForm, isValid, dirty }): JSX.Element => (
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
                  component={FormikText}
                  name={"confirmation"}
                  placeholder={groupName.toLowerCase()}
                  type={"text"}
                  validate={required}
                />
              </FormGroup>
              <FormGroup>
                <ControlLabel>
                  {translate.t(
                    "searchFindings.servicesTable.deleteGroup.reason.title"
                  )}
                </ControlLabel>
                <TooltipWrapper
                  id={"searchFindings.servicesTable.deleteGroup.reason.tooltip"}
                  message={translate.t(
                    "searchFindings.servicesTable.deleteGroup.reason.tooltip"
                  )}
                  placement={"top"}
                >
                  <FormGroup>
                    <Field component={FormikDropdown} name={"reason"}>
                      <option value={"NO_SYSTEM"}>
                        {translate.t(
                          "searchFindings.servicesTable.deleteGroup.reason.noSystem"
                        )}
                      </option>
                      <option value={"NO_SECTST"}>
                        {translate.t(
                          "searchFindings.servicesTable.deleteGroup.reason.noSectst"
                        )}
                      </option>
                      <option value={"DIFF_SECTST"}>
                        {translate.t(
                          "searchFindings.servicesTable.deleteGroup.reason.diffSectst"
                        )}
                      </option>
                      <option value={"MIGRATION"}>
                        {translate.t(
                          "searchFindings.servicesTable.deleteGroup.reason.migration"
                        )}
                      </option>
                      <option value={"OTHER"}>
                        {translate.t(
                          "searchFindings.servicesTable.deleteGroup.reason.other"
                        )}
                      </option>
                    </Field>
                  </FormGroup>
                </TooltipWrapper>
              </FormGroup>
              <hr />
              <Row>
                <Col100>
                  <ButtonToolbar>
                    <Button onClick={onClose} variant={"secondary"}>
                      {translate.t("confirmmodal.cancel")}
                    </Button>
                    <Button
                      disabled={!dirty || !isValid}
                      onClick={submitForm}
                      type={"submit"}
                      variant={"primary"}
                    >
                      {translate.t("confirmmodal.proceed")}
                    </Button>
                  </ButtonToolbar>
                </Col100>
              </Row>
            </React.Fragment>
          )}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { DeleteGroupModal };
