import { Field, Form, Formik } from "formik";
import React from "react";
import type { ConfigurableValidator } from "revalidate";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import type { IEditGroupInformation } from "scenes/Dashboard/components/EditGroupInformationModal/types";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { FormikDropdown, FormikText } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import {
  composeValidators,
  maxLength,
  required,
  validTextField,
} from "utils/validations";

const MAX_DESCRIPTION_LENGTH: number = 200;

const maxDescriptionLength: ConfigurableValidator = maxLength(
  MAX_DESCRIPTION_LENGTH
);

const EditGroupInformationModal: React.FC<IEditGroupInformation> = (
  props: IEditGroupInformation
): JSX.Element => {
  const { initialValues, isOpen, onClose, onSubmit } = props;

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t(
          "searchFindings.tabResources.modalEditGroupInformation"
        )}
        onEsc={onClose}
        open={isOpen}
      >
        <Formik
          enableReinitialize={true}
          initialValues={initialValues}
          name={"editGroupInformation"}
          onSubmit={onSubmit}
        >
          {({ dirty }): React.ReactNode => (
            <Form>
              <Row>
                <Col100>
                  <FormGroup>
                    <ControlLabel>
                      {translate.t(
                        "organization.tabs.groups.newGroup.description.text"
                      )}
                    </ControlLabel>
                    <TooltipWrapper
                      id={
                        "organization.tabs.groups.newGroup.description.tooltip"
                      }
                      message={translate.t(
                        "organization.tabs.groups.newGroup.description.tooltip"
                      )}
                      placement={"top"}
                    >
                      <FormGroup>
                        <Field
                          component={FormikText}
                          id={"add-group-description"}
                          name={"description"}
                          type={"text"}
                          validate={composeValidators([
                            required,
                            maxDescriptionLength,
                            validTextField,
                          ])}
                        />
                      </FormGroup>
                    </TooltipWrapper>
                  </FormGroup>
                  <FormGroup>
                    <ControlLabel>
                      {translate.t(
                        "organization.tabs.groups.newGroup.language.text"
                      )}
                    </ControlLabel>
                    <TooltipWrapper
                      id={"organization.tabs.groups.newGroup.language.tooltip"}
                      message={translate.t(
                        "organization.tabs.groups.newGroup.language.tooltip"
                      )}
                      placement={"top"}
                    >
                      <FormGroup>
                        <Field component={FormikDropdown} name={"language"}>
                          <option value={"EN"}>
                            {translate.t(
                              "organization.tabs.groups.newGroup.language.EN"
                            )}
                          </option>
                          <option value={"ES"}>
                            {translate.t(
                              "organization.tabs.groups.newGroup.language.ES"
                            )}
                          </option>
                        </Field>
                      </FormGroup>
                    </TooltipWrapper>
                  </FormGroup>
                </Col100>
              </Row>
              <hr />
              <Row>
                <Col100>
                  <ButtonToolbar>
                    <Button id={"edit-group-inf-cancel"} onClick={onClose}>
                      {translate.t("confirmmodal.cancel")}
                    </Button>
                    <Button disabled={!dirty} type={"submit"}>
                      {translate.t("confirmmodal.proceed")}
                    </Button>
                  </ButtonToolbar>
                </Col100>
              </Row>
            </Form>
          )}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { EditGroupInformationModal };
