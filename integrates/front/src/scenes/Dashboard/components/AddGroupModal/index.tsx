import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";
import type { ConfigurableValidator } from "revalidate";

import {
  getSwitchButtonHandlers,
  handleCreateError,
  handleGroupNameErrorHelper,
  handleUpdateError,
} from "./helpers";

import { Button } from "components/Button";
import { Col, Row } from "components/Layout";
import { Modal, ModalFooter } from "components/Modal";
import { Switch } from "components/Switch";
import { TooltipWrapper } from "components/TooltipWrapper";
import { BaseStep, Tour } from "components/Tour/index";
import { UPDATE_TOURS } from "components/Tour/queries";
import {
  ADD_GROUP_MUTATION,
  GROUPS_NAME_QUERY,
} from "scenes/Dashboard/components/AddGroupModal/queries";
import type {
  IAddGroupModalProps,
  IGroupNameProps,
} from "scenes/Dashboard/components/AddGroupModal/types";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikDropdown, FormikText } from "utils/forms/fields";
import { msgSuccess } from "utils/notifications";
import {
  alphaNumeric,
  composeValidators,
  maxLength,
  required,
  validTextField,
} from "utils/validations";

/*
 * Business rules to create a group:
 *   - ASM must enabled, because we are using ASM right now, right?
 *   - Squad <--needs-- ASM
 *
 * Business rules after creating the group:
 *   - If ASM is turned off, the group will be immediately deleted
 */

const MAX_DESCRIPTION_LENGTH: number = 200;
const MAX_GROUP_NAME_LENGTH: number = 20;
const MAX_ORGANIZATION_LENGTH: number = 50;

const maxDescriptionLength: ConfigurableValidator = maxLength(
  MAX_DESCRIPTION_LENGTH
);
const maxGroupNameLength: ConfigurableValidator = maxLength(
  MAX_GROUP_NAME_LENGTH
);
const maxOrganizationLength: ConfigurableValidator = maxLength(
  MAX_ORGANIZATION_LENGTH
);
const AddGroupModal: React.FC<IAddGroupModalProps> = (
  props: IAddGroupModalProps
): JSX.Element => {
  const { onClose, organization, runTour } = props;
  const { t } = useTranslation();

  const { push } = useHistory();

  const handleMutationResult = (result: {
    addGroup: { success: boolean };
  }): void => {
    if (result.addGroup.success) {
      onClose();
      msgSuccess(
        t("organization.tabs.groups.newGroup.success"),
        t("organization.tabs.groups.newGroup.titleSuccess")
      );
    }
  };

  const [addGroup, { loading: submitting }] = useMutation(ADD_GROUP_MUTATION, {
    onCompleted: handleMutationResult,
    onError: handleCreateError,
  });

  const [updateTours] = useMutation(UPDATE_TOURS, {
    onError: handleUpdateError,
  });

  const handleSubmit = useCallback(
    async (values: {
      description: string;
      name: string;
      language: string;
      organization: string;
      type: string;
      service: string;
      squad: boolean;
      machine: boolean;
    }): Promise<void> => {
      mixpanel.track("AddGroup");
      await addGroup({
        variables: {
          description: values.description,
          groupName: values.name,
          hasMachine: values.machine,
          hasSquad: values.squad,
          language: values.language,
          organizationName: values.organization,
          service: values.service,
          subscription: values.type,
        },
      });
      if (runTour) {
        void updateTours({ variables: { newGroup: true, newRoot: false } });
        push(`/orgs/${organization}/groups/${values.name}/scope`);
      }
    },
    [addGroup, organization, push, runTour, updateTours]
  );

  function handleGroupNameError({ graphQLErrors }: ApolloError): void {
    onClose();
    handleGroupNameErrorHelper(graphQLErrors);
  }

  const { data } = useQuery<IGroupNameProps>(GROUPS_NAME_QUERY, {
    fetchPolicy: "no-cache",
    onError: handleGroupNameError,
  });

  const groupName: string =
    _.isUndefined(data) || _.isEmpty(data) ? "" : data.internalNames.name;

  return (
    <React.StrictMode>
      <Modal
        onClose={onClose}
        open={true}
        size={"large"}
        title={t("organization.tabs.groups.newGroup.new.group")}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{
            description: "",
            language: "EN",
            machine: true,
            name: groupName.toUpperCase(),
            organization: organization.toUpperCase(),
            service: "WHITE",
            squad: true,
            type: "CONTINUOUS",
          }}
          name={"newGroup"}
          onSubmit={handleSubmit}
        >
          {({ values, dirty, setFieldValue }): JSX.Element => {
            const handleMachineBtnChange = getSwitchButtonHandlers(
              values,
              setFieldValue,
              "machine"
            );

            const handleSquadBtnChange = getSwitchButtonHandlers(
              values,
              setFieldValue,
              "squad"
            );

            return (
              <React.Fragment>
                <Form>
                  <Row justify={"space-between"}>
                    <Col large={"33"} medium={"33"} small={"33"}>
                      <FormGroup>
                        <ControlLabel>
                          {t(
                            "organization.tabs.groups.newGroup.organization.text"
                          )}
                        </ControlLabel>
                        <TooltipWrapper
                          id={
                            "organization.tabs.groups.newGroup.organization.tooltip"
                          }
                          message={t(
                            "organization.tabs.groups.newGroup.organization.tooltip"
                          )}
                          placement={"top"}
                        >
                          <FormGroup>
                            <Field
                              component={FormikText}
                              disabled={true}
                              name={"organization"}
                              type={"text"}
                              validate={composeValidators([
                                required,
                                maxOrganizationLength,
                                validTextField,
                              ])}
                            />
                          </FormGroup>
                        </TooltipWrapper>
                      </FormGroup>
                    </Col>
                    <Col large={"33"} medium={"33"} small={"33"}>
                      <FormGroup id={"add-group-name-tour"}>
                        <ControlLabel>
                          {t("organization.tabs.groups.newGroup.name")}
                        </ControlLabel>
                        <Field
                          component={FormikText}
                          disabled={true}
                          id={"add-group-name"}
                          name={"name"}
                          type={"text"}
                          validate={composeValidators([
                            alphaNumeric,
                            maxGroupNameLength,
                            required,
                            validTextField,
                          ])}
                        />
                      </FormGroup>
                    </Col>
                    <Col large={"33"} medium={"33"} small={"33"}>
                      <FormGroup id={"add-group-description-tour"}>
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
                    </Col>
                  </Row>
                  <Row justify={"space-between"}>
                    <Col large={"33"} medium={"33"} small={"33"}>
                      <FormGroup>
                        <ControlLabel>
                          {t("organization.tabs.groups.newGroup.type.title")}
                        </ControlLabel>
                        <TooltipWrapper
                          id={"organization.tabs.groups.newGroup.type.tooltip"}
                          message={t(
                            "organization.tabs.groups.newGroup.type.tooltip"
                          )}
                          placement={"top"}
                        >
                          <FormGroup>
                            <Field component={FormikDropdown} name={"type"}>
                              <option value={"CONTINUOUS"}>
                                {t(
                                  "organization.tabs.groups.newGroup.type.continuous"
                                )}
                              </option>
                              <option value={"ONESHOT"}>
                                {t(
                                  "organization.tabs.groups.newGroup.type.oneShot"
                                )}
                              </option>
                            </Field>
                          </FormGroup>
                        </TooltipWrapper>
                      </FormGroup>
                    </Col>
                    <Col large={"33"} medium={"33"} small={"33"}>
                      <FormGroup>
                        <ControlLabel>
                          {t("organization.tabs.groups.newGroup.service.title")}
                        </ControlLabel>
                        <Field component={FormikDropdown} name={"service"}>
                          <option value={"BLACK"}>
                            {t(
                              "organization.tabs.groups.newGroup.service.black"
                            )}
                          </option>
                          <option value={"WHITE"}>
                            {t(
                              "organization.tabs.groups.newGroup.service.white"
                            )}
                          </option>
                        </Field>
                      </FormGroup>
                    </Col>
                    <Col large={"33"} medium={"33"} small={"33"}>
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
                    </Col>
                  </Row>
                  <Row justify={"space-between"}>
                    <Col large={"50"} medium={"50"} small={"50"}>
                      <TooltipWrapper
                        id={"organization.tabs.groups.newGroup.machine.tooltip"}
                        message={t(
                          "organization.tabs.groups.newGroup.machine.tooltip"
                        )}
                        placement={"top"}
                      >
                        <FormGroup>
                          <ControlLabel>
                            {t(
                              "organization.tabs.groups.newGroup.machine.text"
                            )}
                            {" *"}
                          </ControlLabel>
                          <Switch
                            checked={values.machine}
                            label={{
                              off: t(
                                "organization.tabs.groups.newGroup.switch.no"
                              ),
                              on: t(
                                "organization.tabs.groups.newGroup.switch.yes"
                              ),
                            }}
                            name={"machine"}
                            onChange={handleMachineBtnChange}
                          />
                        </FormGroup>
                      </TooltipWrapper>
                    </Col>
                    <Col large={"50"} medium={"50"} small={"50"}>
                      <TooltipWrapper
                        id={"organization.tabs.groups.newGroup.squad.tooltip"}
                        message={t(
                          "organization.tabs.groups.newGroup.squad.tooltip"
                        )}
                        placement={"top"}
                      >
                        <FormGroup>
                          <ControlLabel>
                            {t("organization.tabs.groups.newGroup.squad.text")}
                            {" *"}
                          </ControlLabel>
                          <Switch
                            checked={values.squad}
                            label={{
                              off: t(
                                "organization.tabs.groups.newGroup.switch.no"
                              ),
                              on: t(
                                "organization.tabs.groups.newGroup.switch.yes"
                              ),
                            }}
                            name={"squad"}
                            onChange={handleSquadBtnChange}
                          />
                        </FormGroup>
                      </TooltipWrapper>
                    </Col>
                  </Row>
                  {" *"}
                  {t("organization.tabs.groups.newGroup.extraChargesMayApply")}
                  <ModalFooter>
                    <Button
                      id={"add-group-cancel"}
                      onClick={onClose}
                      variant={"secondary"}
                    >
                      {t("confirmmodal.cancel")}
                    </Button>
                    <Button
                      disabled={!dirty || submitting}
                      id={"add-group-proceed"}
                      type={"submit"}
                      variant={"primary"}
                    >
                      {t("confirmmodal.proceed")}
                    </Button>
                  </ModalFooter>
                </Form>
                <Tour
                  run={runTour}
                  steps={[
                    {
                      ...BaseStep,
                      content: t("tours.addGroup.groupName"),
                      target: "#add-group-name-tour",
                    },
                    {
                      ...BaseStep,
                      content: t("tours.addGroup.groupDescription"),
                      hideFooter: values.description.length === 0,
                      target: "#add-group-description-tour",
                    },
                    {
                      ...BaseStep,
                      content: t("tours.addGroup.proceedButton"),
                      hideFooter: true,
                      target: "#add-group-proceed",
                    },
                  ]}
                />
              </React.Fragment>
            );
          }}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { AddGroupModal };
