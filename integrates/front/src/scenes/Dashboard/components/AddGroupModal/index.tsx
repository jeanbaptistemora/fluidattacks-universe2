/* eslint-disable react/forbid-component-props, fp/no-mutating-methods */
import { useMutation } from "@apollo/client";
import { Field, Form, Formik } from "formik";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import type { Step } from "react-joyride";
import LoadingOverlay from "react-loading-overlay";
import { useHistory } from "react-router-dom";
import FadeLoader from "react-spinners/FadeLoader";
import type { ConfigurableValidator } from "revalidate";

import {
  getSwitchButtonHandlers,
  handleCreateError,
  handleUpdateError,
} from "./helpers";

import { Button } from "components/Button";
import { Col, Row } from "components/Layout";
import { Modal, ModalFooter } from "components/Modal";
import { Switch } from "components/Switch";
import { TooltipWrapper } from "components/TooltipWrapper";
import { BaseStep, Tour } from "components/Tour/index";
import { UPDATE_TOURS } from "components/Tour/queries";
import { ADD_GROUP_MUTATION } from "scenes/Dashboard/components/AddGroupModal/queries";
import type { IAddGroupModalProps } from "scenes/Dashboard/components/AddGroupModal/types";
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

  const finishTour = useCallback((): void => {
    void updateTours({ variables: { newGroup: true, newRoot: false } });
    onClose();
  }, [onClose, updateTours]);

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
          groupName: values.name.toUpperCase(),
          hasMachine: values.machine,
          hasSquad: values.squad,
          language: values.language,
          organizationName: values.organization,
          service: values.service,
          subscription: values.type,
        },
      });
      if (runTour) {
        finishTour();
        push(`/orgs/${organization}/groups/${values.name}/scope`);
      }
    },
    [addGroup, organization, push, runTour, finishTour]
  );

  return (
    <React.StrictMode>
      <Modal
        onClose={onClose}
        open={true}
        title={t("organization.tabs.groups.newGroup.new.group")}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{
            description: "",
            language: "EN",
            machine: true,
            name: "",
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

            const isContinuous = values.type === "CONTINUOUS";

            const steps: Step[] = [
              {
                ...BaseStep,
                content: t("tours.addGroup.intro"),
                placement: "center",
                target: "#add-group-plan",
                title: t("organization.tabs.groups.newGroup.new.group"),
              },
              {
                ...BaseStep,
                content: t("tours.addGroup.groupDescription"),
                hideBackButton: true,
                hideFooter: values.description.length === 0,
                target: "#add-group-description-tour",
              },
              {
                ...BaseStep,
                content: t("tours.addGroup.serviceType"),
                target: "#add-group-service-type",
              },
              {
                ...BaseStep,
                content: t("tours.addGroup.testingType"),
                target: "#add-group-testing-type",
              },
              {
                ...BaseStep,
                content: t("tours.addGroup.reportLanguage"),
                target: "#add-group-report-language",
              },
              {
                ...BaseStep,
                content: t("tours.addGroup.squadPlan"),
                target: "#add-group-plan",
              },
              {
                ...BaseStep,
                content: t("tours.addGroup.proceedButton"),
                spotlightClicks: true,
                target: "#add-group-proceed",
              },
            ];

            const planStep = 5;

            if (!isContinuous) {
              steps.splice(planStep, 1);
            }

            return (
              <React.Fragment>
                <LoadingOverlay active={submitting} spinner={<FadeLoader />} />
                <Form>
                  <Row
                    id={"add-group-description-tour"}
                    justify={"space-between"}
                  >
                    <Col large={"33"} medium={"33"} small={"33"}>
                      <FormGroup>
                        <ControlLabel>
                          {t(
                            "organization.tabs.groups.newGroup.organization.text"
                          )}
                        </ControlLabel>
                        <TooltipWrapper
                          hide={runTour}
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
                      <FormGroup>
                        <ControlLabel>
                          {t("organization.tabs.groups.newGroup.name")}
                        </ControlLabel>
                        <Field
                          component={FormikText}
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
                      <FormGroup>
                        <ControlLabel>
                          {t(
                            "organization.tabs.groups.newGroup.description.text"
                          )}
                        </ControlLabel>
                        <TooltipWrapper
                          hide={runTour}
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
                    <Col
                      id={"add-group-service-type"}
                      large={"33"}
                      medium={"33"}
                      small={"33"}
                    >
                      <FormGroup>
                        <ControlLabel>
                          {t("organization.tabs.groups.newGroup.type.title")}
                        </ControlLabel>
                        <TooltipWrapper
                          hide={runTour}
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
                    <Col
                      id={"add-group-testing-type"}
                      large={"33"}
                      medium={"33"}
                      small={"33"}
                    >
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
                    <Col
                      id={"add-group-report-language"}
                      large={"33"}
                      medium={"33"}
                      small={"33"}
                    >
                      <FormGroup>
                        <ControlLabel>
                          {t("organization.tabs.groups.newGroup.language.text")}
                        </ControlLabel>
                        <TooltipWrapper
                          hide={runTour}
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
                  <Row justify={"center"}>
                    <Col hidden={true} large={"50"} medium={"50"} small={"50"}>
                      <TooltipWrapper
                        hide={runTour}
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
                    {isContinuous && (
                      <Col
                        id={"add-group-plan"}
                        large={"50"}
                        medium={"50"}
                        small={"50"}
                      >
                        <TooltipWrapper
                          hide={runTour}
                          id={"organization.tabs.groups.newGroup.squad.tooltip"}
                          message={t(
                            "organization.tabs.groups.newGroup.squad.tooltip"
                          )}
                          placement={"top"}
                        >
                          <FormGroup>
                            <ControlLabel>
                              {t(
                                "organization.tabs.groups.newGroup.squad.text"
                              )}
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
                    )}
                  </Row>
                  {isContinuous &&
                    `${" *"} ${t(
                      "organization.tabs.groups.newGroup.extraChargesMayApply"
                    )}`}
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
                <Tour onFinish={finishTour} run={runTour} steps={steps} />
              </React.Fragment>
            );
          }}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { AddGroupModal };
