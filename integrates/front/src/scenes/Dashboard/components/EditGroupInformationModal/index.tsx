import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";

import { Modal, ModalConfirm } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import type { IEditGroupInformation } from "scenes/Dashboard/components/EditGroupInformationModal/types";
import { Col100, ControlLabel, FormGroup, Row } from "styles/styledComponents";
import { FormikDate, FormikDropdown, FormikText } from "utils/forms/fields";
import { FormikSwitchButton } from "utils/forms/fields/SwitchButton/FormikSwitchButton";
import {
  composeValidators,
  isGreaterDate,
  maxLength,
  numberBetween,
  numeric,
  required,
  validTextField,
} from "utils/validations";

const MAX_BUSINESS_INFO_LENGTH: number = 60;
const MAX_DESCRIPTION_LENGTH: number = 200;
const MIN_SPRINT_DURATION: number = 1;
const MAX_SPRINT_DURATION: number = 10;

const maxBusinessInfoLength: ConfigurableValidator = maxLength(
  MAX_BUSINESS_INFO_LENGTH
);
const maxDescriptionLength: ConfigurableValidator = maxLength(
  MAX_DESCRIPTION_LENGTH
);

const EditGroupInformationModal: React.FC<IEditGroupInformation> = ({
  initialValues,
  isOpen,
  onClose,
  onSubmit,
}: IEditGroupInformation): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <Modal
        minWidth={600}
        onClose={onClose}
        open={isOpen}
        title={t("searchFindings.tabResources.modalEditGroupInformation")}
      >
        <Formik
          enableReinitialize={true}
          initialValues={initialValues}
          name={"editGroupInformation"}
          onSubmit={onSubmit}
        >
          {({ dirty, setFieldValue }): JSX.Element => {
            function managedOnChange(managed: boolean): void {
              setFieldValue("managed", managed);
            }

            return (
              <Form>
                <Row>
                  <Col100>
                    <FormGroup>
                      <ControlLabel>
                        {t("organization.tabs.groups.newGroup.businessId.text")}
                      </ControlLabel>
                      <TooltipWrapper
                        id={
                          "organization.tabs.groups.newGroup.businessId.tooltip"
                        }
                        message={t(
                          "organization.tabs.groups.newGroup.businessId.tooltip"
                        )}
                        placement={"top"}
                      >
                        <FormGroup>
                          <Field
                            component={FormikText}
                            id={"add-group-description"}
                            name={"businessId"}
                            type={"text"}
                            validate={composeValidators([
                              maxBusinessInfoLength,
                              validTextField,
                            ])}
                          />
                        </FormGroup>
                      </TooltipWrapper>
                    </FormGroup>
                    <FormGroup>
                      <ControlLabel>
                        {t(
                          "organization.tabs.groups.newGroup.businessName.text"
                        )}
                      </ControlLabel>
                      <TooltipWrapper
                        id={
                          "organization.tabs.groups.newGroup.businessName.tooltip"
                        }
                        message={t(
                          "organization.tabs.groups.newGroup.businessName.tooltip"
                        )}
                        placement={"top"}
                      >
                        <FormGroup>
                          <Field
                            component={FormikText}
                            id={"add-group-description"}
                            name={"businessName"}
                            type={"text"}
                            validate={composeValidators([
                              maxBusinessInfoLength,
                              validTextField,
                            ])}
                          />
                        </FormGroup>
                      </TooltipWrapper>
                    </FormGroup>
                    <FormGroup>
                      <ControlLabel>
                        {t(
                          "organization.tabs.groups.newGroup.description.text"
                        )}
                      </ControlLabel>
                      <TooltipWrapper
                        id={
                          "organization.tabs.groups.newGroup.description.tooltip"
                        }
                        message={t(
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
                        {t("organization.tabs.groups.newGroup.language.text")}
                      </ControlLabel>
                      <TooltipWrapper
                        id={
                          "organization.tabs.groups.newGroup.language.tooltip"
                        }
                        message={t(
                          "organization.tabs.groups.newGroup.language.tooltip"
                        )}
                        placement={"top"}
                      >
                        <FormGroup>
                          <Field component={FormikDropdown} name={"language"}>
                            <option value={"EN"}>
                              {t(
                                "organization.tabs.groups.newGroup.language.EN"
                              )}
                            </option>
                            <option value={"ES"}>
                              {t(
                                "organization.tabs.groups.newGroup.language.ES"
                              )}
                            </option>
                          </Field>
                        </FormGroup>
                      </TooltipWrapper>
                    </FormGroup>
                    <FormGroup>
                      <ControlLabel>
                        {t("organization.tabs.groups.newGroup.managed.text")}
                      </ControlLabel>
                      <TooltipWrapper
                        id={"organization.tabs.groups.newGroup.managed.tooltip"}
                        message={t(
                          "organization.tabs.groups.newGroup.managed.tooltip"
                        )}
                        placement={"top"}
                      >
                        <FormGroup>
                          <Field
                            component={FormikSwitchButton}
                            name={"managed"}
                            offlabel={t(
                              "organization.tabs.groups.newGroup.managed.notManually"
                            )}
                            onChange={managedOnChange}
                            onlabel={t(
                              "organization.tabs.groups.newGroup.managed.manually"
                            )}
                            type={"checkbox"}
                          />
                        </FormGroup>
                      </TooltipWrapper>
                    </FormGroup>
                    <FormGroup>
                      <ControlLabel>
                        {t(
                          "organization.tabs.groups.newGroup.sprintDuration.text"
                        )}
                      </ControlLabel>
                      <TooltipWrapper
                        id={
                          "organization.tabs.groups.newGroup.sprintDuration.tooltip"
                        }
                        message={t(
                          "organization.tabs.groups.newGroup.sprintDuration.tooltip"
                        )}
                        placement={"top"}
                      >
                        <FormGroup>
                          <Field
                            component={FormikText}
                            id={"add-group-description"}
                            name={"sprintDuration"}
                            type={"text"}
                            validate={composeValidators([
                              numberBetween(
                                MIN_SPRINT_DURATION,
                                MAX_SPRINT_DURATION
                              ),
                              numeric,
                            ])}
                          />
                        </FormGroup>
                      </TooltipWrapper>
                    </FormGroup>
                    <FormGroup>
                      <ControlLabel>
                        {t(
                          "organization.tabs.groups.editGroup.sprintStartDate.text"
                        )}
                      </ControlLabel>
                      <TooltipWrapper
                        id={
                          "organization.tabs.groups.editGroup.sprintStartDate.tooltip"
                        }
                        message={t(
                          "organization.tabs.groups.editGroup.sprintStartDate.tooltip"
                        )}
                        placement={"top"}
                      >
                        <FormGroup>
                          <Field
                            component={FormikDate}
                            name={"sprintStartDate"}
                            validate={composeValidators([
                              required,
                              isGreaterDate,
                            ])}
                          />
                        </FormGroup>
                      </TooltipWrapper>
                    </FormGroup>
                  </Col100>
                </Row>
                <ModalConfirm disabled={!dirty} onCancel={onClose} />
              </Form>
            );
          }}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { EditGroupInformationModal };
