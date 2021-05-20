import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback } from "react";
import type { ConfigurableValidator } from "revalidate";

import {
  getSwitchButtonHandlers,
  handleCreateError,
  handleProjectNameErrorHelper,
} from "./helpers";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { SwitchButton } from "components/SwitchButton";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  CREATE_PROJECT_MUTATION,
  PROJECTS_NAME_QUERY,
} from "scenes/Dashboard/components/AddProjectModal/queries";
import type {
  IAddProjectModalProps,
  IProjectNameProps,
} from "scenes/Dashboard/components/AddProjectModal/types";
import {
  ButtonToolbar,
  Col100,
  Col40,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { FormikDropdown, FormikText } from "utils/forms/fields";
import { msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import {
  alphaNumeric,
  composeValidators,
  maxLength,
  required,
  validTextField,
} from "utils/validations";

/*
 * Business rules to create a project:
 *   - Integrates must enabled, because we are using Integrates right now, right?
 *   - Drills <--needs-- Integrates
 *   - Forces <--needs-- Drills
 *
 * Business rules after creating the project:
 *   - If Integrates is turned off the project will be immediately deleted
 */

const MAX_DESCRIPTION_LENGTH: number = 200;
const MAX_PROJECT_NAME_LENGTH: number = 20;
const MAX_ORGANIZATION_LENGTH: number = 50;

const maxDescriptionLength: ConfigurableValidator = maxLength(
  MAX_DESCRIPTION_LENGTH
);
const maxProjectNameLength: ConfigurableValidator = maxLength(
  MAX_PROJECT_NAME_LENGTH
);
const maxOrganizationLength: ConfigurableValidator = maxLength(
  MAX_ORGANIZATION_LENGTH
);
const AddProjectModal: React.FC<IAddProjectModalProps> = (
  props: IAddProjectModalProps
): JSX.Element => {
  const { onClose, organization } = props;

  const isContinuousType: (subsType: string) => boolean = (
    subsType: string
  ): boolean => subsType === "CONTINUOUS";

  const handleMutationResult = (result: {
    createProject: { success: boolean };
  }): void => {
    if (result.createProject.success) {
      onClose();
      msgSuccess(
        translate.t("organization.tabs.groups.newGroup.success"),
        translate.t("organization.tabs.groups.newGroup.titleSuccess")
      );
    }
  };

  const [createProject, { loading: submitting }] = useMutation(
    CREATE_PROJECT_MUTATION,
    {
      onCompleted: handleMutationResult,
      onError: handleCreateError,
    }
  );

  const handleSubmit = useCallback(
    (values: {
      description: string;
      name: string;
      language: string;
      organization: string;
      type: string;
      drills: boolean;
      forces: boolean;
      skims: boolean;
    }): void => {
      track("AddGroup");
      void createProject({
        variables: {
          description: values.description,
          hasDrills: values.drills,
          hasForces: values.forces,
          hasSkims: values.skims,
          language: values.language,
          organization: values.organization,
          projectName: values.name,
          subscription: values.type,
        },
      });
    },
    [createProject]
  );

  function handleProjectNameError({ graphQLErrors }: ApolloError): void {
    onClose();
    handleProjectNameErrorHelper(graphQLErrors);
  }

  const { data } = useQuery<IProjectNameProps>(PROJECTS_NAME_QUERY, {
    fetchPolicy: "no-cache",
    onError: handleProjectNameError,
  });

  const projectName: string =
    _.isUndefined(data) || _.isEmpty(data) ? "" : data.internalNames.name;

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t("organization.tabs.groups.newGroup.new.group")}
        open={true}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{
            description: "",
            drills: true,
            forces: true,
            language: "EN",
            name: projectName.toUpperCase(),
            organization: organization.toUpperCase(),
            skims: true,
            type: "CONTINUOUS",
          }}
          name={"newGroup"}
          onSubmit={handleSubmit}
        >
          {({ values, dirty, setFieldValue }): JSX.Element => {
            const handleSubscriptionTypeChange = getSwitchButtonHandlers(
              values,
              setFieldValue,
              "subscription"
            );

            const handleSkimsBtnChange = getSwitchButtonHandlers(
              values,
              setFieldValue,
              "skims"
            );

            const handleDrillsBtnChange = getSwitchButtonHandlers(
              values,
              setFieldValue,
              "drills"
            );

            const handleForcesBtnChange = getSwitchButtonHandlers(
              values,
              setFieldValue,
              "forces"
            );

            return (
              <Form>
                <Row>
                  <Col100>
                    <FormGroup>
                      <ControlLabel>
                        {translate.t(
                          "organization.tabs.groups.newGroup.organization.text"
                        )}
                      </ControlLabel>
                      <TooltipWrapper
                        id={
                          "organization.tabs.groups.newGroup.organization.tooltip"
                        }
                        message={translate.t(
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
                    <FormGroup>
                      <ControlLabel>
                        {translate.t("organization.tabs.groups.newGroup.name")}
                      </ControlLabel>
                      <Field
                        component={FormikText}
                        disabled={true}
                        name={"name"}
                        type={"text"}
                        validate={composeValidators([
                          alphaNumeric,
                          maxProjectNameLength,
                          required,
                          validTextField,
                        ])}
                      />
                    </FormGroup>
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
                          "organization.tabs.groups.newGroup.type.title"
                        )}
                      </ControlLabel>
                      <TooltipWrapper
                        id={"organization.tabs.groups.newGroup.type.tooltip"}
                        message={translate.t(
                          "organization.tabs.groups.newGroup.type.tooltip"
                        )}
                        placement={"top"}
                      >
                        <FormGroup>
                          <Field
                            component={FormikDropdown}
                            customChange={handleSubscriptionTypeChange}
                            name={"type"}
                          >
                            <option value={"CONTINUOUS"}>
                              {translate.t(
                                "organization.tabs.groups.newGroup.type.continuous"
                              )}
                            </option>
                            <option value={"ONESHOT"}>
                              {translate.t(
                                "organization.tabs.groups.newGroup.type.oneShot"
                              )}
                            </option>
                          </Field>
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
                        id={
                          "organization.tabs.groups.newGroup.language.tooltip"
                        }
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
                <Row>
                  <Col40>
                    <TooltipWrapper
                      id={
                        "organization.tabs.groups.newGroup.integrates.tooltip"
                      }
                      message={translate.t(
                        "organization.tabs.groups.newGroup.integrates.tooltip"
                      )}
                      placement={"top"}
                    >
                      <FormGroup>
                        <ControlLabel>
                          {translate.t(
                            "organization.tabs.groups.newGroup.integrates.text"
                          )}
                          {" *"}
                        </ControlLabel>
                        <SwitchButton
                          checked={true}
                          disabled={true}
                          name={"integrates"}
                          offlabel={translate.t(
                            "organization.tabs.groups.newGroup.switch.no"
                          )}
                          onlabel={translate.t(
                            "organization.tabs.groups.newGroup.switch.yes"
                          )}
                        />
                      </FormGroup>
                    </TooltipWrapper>
                  </Col40>
                </Row>
                {isContinuousType(values.type) ? (
                  <Row>
                    <Col40>
                      <TooltipWrapper
                        id={"organization.tabs.groups.newGroup.skims.tooltip"}
                        message={translate.t(
                          "organization.tabs.groups.newGroup.skims.tooltip"
                        )}
                        placement={"top"}
                      >
                        <FormGroup>
                          <ControlLabel>
                            {translate.t(
                              "organization.tabs.groups.newGroup.skims.text"
                            )}
                            {" *"}
                          </ControlLabel>
                          <SwitchButton
                            checked={values.skims}
                            name={"skims"}
                            offlabel={translate.t(
                              "organization.tabs.groups.newGroup.switch.no"
                            )}
                            onChange={handleSkimsBtnChange}
                            onlabel={translate.t(
                              "organization.tabs.groups.newGroup.switch.yes"
                            )}
                          />
                        </FormGroup>
                      </TooltipWrapper>
                    </Col40>
                  </Row>
                ) : undefined}
                <Row>
                  <Col40>
                    <TooltipWrapper
                      id={"organization.tabs.groups.newGroup.drills.tooltip"}
                      message={translate.t(
                        "organization.tabs.groups.newGroup.drills.tooltip"
                      )}
                      placement={"top"}
                    >
                      <FormGroup>
                        <ControlLabel>
                          {translate.t(
                            "organization.tabs.groups.newGroup.drills.text"
                          )}
                          {" *"}
                        </ControlLabel>
                        <SwitchButton
                          checked={values.drills}
                          name={"drills"}
                          offlabel={translate.t(
                            "organization.tabs.groups.newGroup.switch.no"
                          )}
                          onChange={handleDrillsBtnChange}
                          onlabel={translate.t(
                            "organization.tabs.groups.newGroup.switch.yes"
                          )}
                        />
                      </FormGroup>
                    </TooltipWrapper>
                  </Col40>
                </Row>
                {values.drills && isContinuousType(values.type) ? (
                  <Row>
                    <Col40>
                      <TooltipWrapper
                        id={"organization.tabs.groups.newGroup.forces.tooltip"}
                        message={translate.t(
                          "organization.tabs.groups.newGroup.forces.tooltip"
                        )}
                        placement={"top"}
                      >
                        <FormGroup>
                          <ControlLabel>
                            {translate.t(
                              "organization.tabs.groups.newGroup.forces.text"
                            )}
                            {" *"}
                          </ControlLabel>
                          <SwitchButton
                            checked={values.forces}
                            name={"forces"}
                            offlabel={translate.t(
                              "organization.tabs.groups.newGroup.switch.no"
                            )}
                            onChange={handleForcesBtnChange}
                            onlabel={translate.t(
                              "organization.tabs.groups.newGroup.switch.yes"
                            )}
                          />
                        </FormGroup>
                      </TooltipWrapper>
                    </Col40>
                  </Row>
                ) : undefined}
                {" *"}
                {translate.t(
                  "organization.tabs.groups.newGroup.extraChargesMayApply"
                )}
                <hr />
                <Row>
                  <Col100>
                    <ButtonToolbar>
                      <Button id={"add-group-cancel"} onClick={onClose}>
                        {translate.t("confirmmodal.cancel")}
                      </Button>
                      <Button
                        disabled={!dirty || submitting}
                        id={"add-group-proceed"}
                        type={"submit"}
                      >
                        {translate.t("confirmmodal.proceed")}
                      </Button>
                    </ButtonToolbar>
                  </Col100>
                </Row>
              </Form>
            );
          }}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { AddProjectModal };
