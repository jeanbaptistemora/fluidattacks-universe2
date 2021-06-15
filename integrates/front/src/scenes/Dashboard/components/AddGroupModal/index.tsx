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
  handleGroupNameErrorHelper,
} from "./helpers";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { SwitchButton } from "components/SwitchButton";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  CREATE_GROUP_MUTATION,
  GROUPS_NAME_QUERY,
} from "scenes/Dashboard/components/AddGroupModal/queries";
import type {
  IAddGroupModalProps,
  IGroupNameProps,
} from "scenes/Dashboard/components/AddGroupModal/types";
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
 * Business rules to create a group:
 *   - ASM must enabled, because we are using ASM right now, right?
 *   - Squad <--needs-- ASM
 *   - Forces <--needs-- Squad
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
  const { onClose, organization } = props;

  const isContinuousType: (subsType: string) => boolean = (
    subsType: string
  ): boolean => subsType === "CONTINUOUS";

  const handleMutationResult = (result: {
    createGroup: { success: boolean };
  }): void => {
    if (result.createGroup.success) {
      onClose();
      msgSuccess(
        translate.t("organization.tabs.groups.newGroup.success"),
        translate.t("organization.tabs.groups.newGroup.titleSuccess")
      );
    }
  };

  const [createGroup, { loading: submitting }] = useMutation(
    CREATE_GROUP_MUTATION,
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
      squad: boolean;
      forces: boolean;
      machine: boolean;
    }): void => {
      track("AddGroup");
      void createGroup({
        variables: {
          description: values.description,
          groupName: values.name,
          hasForces: values.forces,
          hasMachine: values.machine,
          hasSquad: values.squad,
          language: values.language,
          organization: values.organization,
          subscription: values.type,
        },
      });
    },
    [createGroup]
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
        headerTitle={translate.t("organization.tabs.groups.newGroup.new.group")}
        open={true}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{
            description: "",
            forces: true,
            language: "EN",
            machine: true,
            name: groupName.toUpperCase(),
            organization: organization.toUpperCase(),
            squad: true,
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
                          maxGroupNameLength,
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
                      id={"organization.tabs.groups.newGroup.asm.tooltip"}
                      message={translate.t(
                        "organization.tabs.groups.newGroup.asm.tooltip"
                      )}
                      placement={"top"}
                    >
                      <FormGroup>
                        <ControlLabel>
                          {translate.t(
                            "organization.tabs.groups.newGroup.asm.text"
                          )}
                          {" *"}
                        </ControlLabel>
                        <SwitchButton
                          checked={true}
                          disabled={true}
                          name={"asm"}
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
                        id={"organization.tabs.groups.newGroup.machine.tooltip"}
                        message={translate.t(
                          "organization.tabs.groups.newGroup.machine.tooltip"
                        )}
                        placement={"top"}
                      >
                        <FormGroup>
                          <ControlLabel>
                            {translate.t(
                              "organization.tabs.groups.newGroup.machine.text"
                            )}
                            {" *"}
                          </ControlLabel>
                          <SwitchButton
                            checked={values.machine}
                            name={"machine"}
                            offlabel={translate.t(
                              "organization.tabs.groups.newGroup.switch.no"
                            )}
                            onChange={handleMachineBtnChange}
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
                      id={"organization.tabs.groups.newGroup.squad.tooltip"}
                      message={translate.t(
                        "organization.tabs.groups.newGroup.squad.tooltip"
                      )}
                      placement={"top"}
                    >
                      <FormGroup>
                        <ControlLabel>
                          {translate.t(
                            "organization.tabs.groups.newGroup.squad.text"
                          )}
                          {" *"}
                        </ControlLabel>
                        <SwitchButton
                          checked={values.squad}
                          name={"squad"}
                          offlabel={translate.t(
                            "organization.tabs.groups.newGroup.switch.no"
                          )}
                          onChange={handleSquadBtnChange}
                          onlabel={translate.t(
                            "organization.tabs.groups.newGroup.switch.yes"
                          )}
                        />
                      </FormGroup>
                    </TooltipWrapper>
                  </Col40>
                </Row>
                {values.squad && isContinuousType(values.type) ? (
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

export { AddGroupModal };
