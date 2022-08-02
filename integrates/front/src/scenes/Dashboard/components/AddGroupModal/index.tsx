/* eslint-disable react/forbid-component-props, fp/no-mutating-methods */
import { useMutation } from "@apollo/client";
import { Field, Form, Formik } from "formik";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { Fragment, useCallback } from "react";
import { useTranslation } from "react-i18next";
import type { Step } from "react-joyride";
import LoadingOverlay from "react-loading-overlay-ts";
import { useHistory } from "react-router-dom";
import FadeLoader from "react-spinners/FadeLoader";
import type { ConfigurableValidator } from "revalidate";

import {
  getSwitchButtonHandlers,
  handleCreateError,
  handleUpdateError,
} from "./helpers";

import { Select } from "components/Input";
import { Col, Row } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Switch } from "components/Switch";
import { Text } from "components/Text";
import { Tooltip } from "components/Tooltip";
import { BaseStep, Tour } from "components/Tour/index";
import { UPDATE_TOURS } from "components/Tour/queries";
import { ADD_GROUP_MUTATION } from "scenes/Dashboard/components/AddGroupModal/queries";
import type { IAddGroupModalProps } from "scenes/Dashboard/components/AddGroupModal/types";
import { FormikText } from "utils/forms/fields";
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
        minWidth={600}
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
                target: "#add-group-confirm",
              },
            ];

            const planStep = 5;

            if (!isContinuous) {
              steps.splice(planStep, 1);
            }

            return (
              <Fragment>
                <LoadingOverlay active={submitting} spinner={<FadeLoader />} />
                <Form>
                  <Row id={"add-group-description-tour"} justify={"between"}>
                    <Col lg={33} md={33} sm={33}>
                      <Text mb={1}>
                        {t(
                          "organization.tabs.groups.newGroup.organization.text"
                        )}
                      </Text>
                      <Tooltip
                        hide={runTour}
                        id={
                          "organization.tabs.groups.newGroup.organization.tooltip"
                        }
                        place={"top"}
                        tip={t(
                          "organization.tabs.groups.newGroup.organization.tooltip"
                        )}
                      >
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
                      </Tooltip>
                    </Col>
                    <Col lg={33} md={33} sm={33}>
                      <Text mb={1}>
                        {t("organization.tabs.groups.newGroup.name")}
                      </Text>
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
                    </Col>
                    <Col lg={33} md={33} sm={33}>
                      <Text mb={1}>
                        {t(
                          "organization.tabs.groups.newGroup.description.text"
                        )}
                      </Text>
                      <Tooltip
                        hide={runTour}
                        id={
                          "organization.tabs.groups.newGroup.description.tooltip"
                        }
                        place={"top"}
                        tip={t(
                          "organization.tabs.groups.newGroup.description.tooltip"
                        )}
                      >
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
                      </Tooltip>
                    </Col>
                  </Row>
                  <Row justify={"between"}>
                    <Col id={"add-group-service-type"} lg={33} md={33} sm={33}>
                      <Tooltip
                        hide={runTour}
                        id={"organization.tabs.groups.newGroup.type.tooltip"}
                        place={"top"}
                        tip={t(
                          "organization.tabs.groups.newGroup.type.tooltip"
                        )}
                      >
                        <Select
                          label={t(
                            "organization.tabs.groups.newGroup.type.title"
                          )}
                          name={"type"}
                        >
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
                        </Select>
                      </Tooltip>
                    </Col>
                    <Col id={"add-group-testing-type"} lg={33} md={33} sm={33}>
                      <Select
                        label={t(
                          "organization.tabs.groups.newGroup.service.title"
                        )}
                        name={"service"}
                      >
                        <option value={"BLACK"}>
                          {t("organization.tabs.groups.newGroup.service.black")}
                        </option>
                        <option value={"WHITE"}>
                          {t("organization.tabs.groups.newGroup.service.white")}
                        </option>
                      </Select>
                    </Col>
                    <Col
                      id={"add-group-report-language"}
                      lg={33}
                      md={33}
                      sm={33}
                    >
                      <Tooltip
                        hide={runTour}
                        id={
                          "organization.tabs.groups.newGroup.language.tooltip"
                        }
                        place={"top"}
                        tip={t(
                          "organization.tabs.groups.newGroup.language.tooltip"
                        )}
                      >
                        <Select
                          label={t(
                            "organization.tabs.groups.newGroup.language.text"
                          )}
                          name={"language"}
                        >
                          <option value={"EN"}>
                            {t("organization.tabs.groups.newGroup.language.EN")}
                          </option>
                          <option value={"ES"}>
                            {t("organization.tabs.groups.newGroup.language.ES")}
                          </option>
                        </Select>
                      </Tooltip>
                    </Col>
                  </Row>
                  <div className={"mv2"} hidden={true}>
                    <Tooltip
                      hide={runTour}
                      id={"organization.tabs.groups.newGroup.machine.tooltip"}
                      place={"top"}
                      tip={t(
                        "organization.tabs.groups.newGroup.machine.tooltip"
                      )}
                    >
                      <Text mb={1}>
                        {"* "}
                        {t("organization.tabs.groups.newGroup.machine.text")}
                      </Text>
                      <Switch
                        checked={values.machine}
                        label={{
                          off: t("organization.tabs.groups.newGroup.switch.no"),
                          on: t("organization.tabs.groups.newGroup.switch.yes"),
                        }}
                        name={"machine"}
                        onChange={handleMachineBtnChange}
                      />
                    </Tooltip>
                  </div>
                  {isContinuous && (
                    <div className={"mv2"} id={"add-group-plan"}>
                      <Tooltip
                        hide={runTour}
                        id={"organization.tabs.groups.newGroup.squad.tooltip"}
                        place={"top"}
                        tip={t(
                          "organization.tabs.groups.newGroup.squad.tooltip"
                        )}
                      >
                        <Text mb={1}>
                          {"* "}
                          {t("organization.tabs.groups.newGroup.squad.text")}
                        </Text>
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
                      </Tooltip>
                    </div>
                  )}
                  {isContinuous &&
                    `${"* "} ${t(
                      "organization.tabs.groups.newGroup.extraChargesMayApply"
                    )}`}
                  <ModalConfirm
                    disabled={!dirty || submitting}
                    id={"add-group-confirm"}
                    onCancel={onClose}
                  />
                </Form>
                <Tour onFinish={finishTour} run={runTour} steps={steps} />
              </Fragment>
            );
          }}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { AddGroupModal };
