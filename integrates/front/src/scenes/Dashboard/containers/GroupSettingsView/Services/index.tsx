import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useHistory } from "react-router-dom";
import type { Dispatch } from "redux";
import type {
  EventWithDataHandler,
  InjectedFormProps,
  Validator,
} from "redux-form";
import { Field, change, formValueSelector } from "redux-form";

import {
  editGroupDataHelper,
  getHandleASMBtnChange,
  getHandleMachineBtnChange,
  handleEditGroupDataError,
  handleForcesBtnChangeHelper,
  handleSquadBtnChangeHelper,
} from "./helpers";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Modal } from "components/Modal";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import {
  EDIT_GROUP_DATA,
  GET_GROUP_DATA,
} from "scenes/Dashboard/containers/GroupSettingsView/queries";
import {
  computeConfirmationMessage,
  isDowngrading,
  isDowngradingServices,
} from "scenes/Dashboard/containers/GroupSettingsView/Services/businessLogic";
import type {
  IFormData,
  IGroupData,
  IServicesDataSet,
  IServicesProps,
} from "scenes/Dashboard/containers/GroupSettingsView/Services/types";
import {
  Alert,
  ButtonToolbar,
  Col100,
  Col80,
  ControlLabel,
  FormGroup,
  Row,
  Well,
} from "styles/styledComponents";
import { Dropdown, Text, TextArea } from "utils/forms/fields";
import { FormSwitchButton } from "utils/forms/fields/SwitchButton";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { maxLength, required, validTextField } from "utils/validations";

const downgradeReasons: string[] = [
  "NONE",
  "PROJECT_SUSPENSION",
  "PROJECT_FINALIZATION",
  "BUDGET",
  "OTHER",
];

const isContinuousType: (type: string) => boolean = (type: string): boolean =>
  _.isUndefined(type) ? false : type.toLowerCase() === "continuous";

const MAX_LENGTH_VALIDATOR = 250;
const maxLength250: Validator = maxLength(MAX_LENGTH_VALIDATOR);

const Services: React.FC<IServicesProps> = (
  props: IServicesProps
): JSX.Element => {
  const { groupName } = props;

  // State management
  const { push } = useHistory();
  const dispatch: Dispatch = useDispatch();
  const selector: (
    state: Record<string, unknown>,
    // eslint-disable-next-line fp/no-rest-parameters
    ...fields: string[]
  ) => IFormData = formValueSelector("editGroup");
  const formValues: IFormData = useSelector(
    (state: Record<string, unknown>): IFormData =>
      selector(
        state,
        "comments",
        "confirmation",
        "squad",
        "forces",
        "integrates",
        "reason",
        "machine",
        "type"
      )
  );
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Business Logic handlers
  const handleSubscriptionTypeChange: EventWithDataHandler<
    React.ChangeEvent<string>
  > = useCallback(
    (_0: React.ChangeEvent<string> | undefined, subsType: string): void => {
      dispatch(change("editGroup", "machine", isContinuousType(subsType)));
      dispatch(change("editGroup", "squad", true));
      dispatch(change("editGroup", "forces", isContinuousType(subsType)));
    },
    [dispatch]
  );
  const handleASMBtnChange = getHandleASMBtnChange(dispatch);
  const handleMachineBtnChange = getHandleMachineBtnChange(dispatch);
  const handleSquadBtnChange: (withSquad: boolean) => void = (
    withSquad: boolean
  ): void => {
    dispatch(change("editGroup", "squad", withSquad));

    handleSquadBtnChangeHelper(
      dispatch,
      withSquad,
      formValues.type,
      isContinuousType
    );
  };
  const handleForcesBtnChange: (withForces: boolean) => void = (
    withForces: boolean
  ): void => {
    dispatch(
      change(
        "editGroup",
        "forces",
        isContinuousType(formValues.type) && withForces
      )
    );

    handleForcesBtnChangeHelper(dispatch, withForces);
  };

  // GraphQL Logic
  const {
    data,
    loading: loadingGroupData,
    refetch: refetchGroupData,
  } = useQuery<IGroupData>(GET_GROUP_DATA, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred getting group data", error);
      });
    },
    variables: { groupName },
  });

  const [editGroupData, { loading: submittingGroupData }] = useMutation(
    EDIT_GROUP_DATA,
    {
      onCompleted: (): void => {
        track("EditGroupData", formValues);
        msgSuccess(
          translate.t("searchFindings.servicesTable.success"),
          translate.t("searchFindings.servicesTable.successTitle")
        );

        editGroupDataHelper(
          formValues.integrates,
          groupName,
          push,
          refetchGroupData
        );
      },
      onError: (error: ApolloError): void => {
        handleEditGroupDataError(error);
      },
      variables: {
        comments: formValues.comments,
        groupName,
        hasForces: formValues.forces,
        hasIntegrates: formValues.integrates,
        hasMachine: formValues.machine,
        hasSquad: formValues.squad,
        reason: formValues.reason,
        subscription: formValues.type,
      },
    }
  );

  const handleClose: () => void = useCallback((): void => {
    setIsModalOpen(false);
  }, []);
  const handleFormSubmit: () => void = useCallback((): void => {
    void editGroupData();
    setIsModalOpen(false);
  }, [editGroupData]);
  const handleTblButtonClick: () => void = useCallback((): void => {
    setIsModalOpen(true);
  }, []);

  // Rendered elements
  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "service",
      header: translate.t("searchFindings.servicesTable.service"),
      width: "75%",
      wrapped: true,
    },
    {
      dataField: "status",
      header: translate.t("searchFindings.servicesTable.status"),
      width: "25%",
      wrapped: true,
    },
  ];
  const servicesList: IServicesDataSet[] = [
    {
      canHave: true,
      id: "integratesSwitch",
      onChange: handleASMBtnChange,
      service: "integrates",
    },
    {
      canHave: isContinuousType(formValues.type),
      id: "machineSwitch",
      onChange: handleMachineBtnChange,
      service: "machine",
    },
    {
      canHave: true,
      id: "squadSwitch",
      onChange: handleSquadBtnChange,
      service: "squad",
    },
    {
      canHave: isContinuousType(formValues.type),
      id: "forcesSwitch",
      onChange: handleForcesBtnChange,
      service: "forces",
    },
  ].filter((element: IServicesDataSet): boolean => element.canHave);

  const servicesDataSet: Record<string, JSX.Element>[] = [
    {
      service: <p>{translate.t("searchFindings.servicesTable.type")}</p>,
      status: (
        <Field
          component={Dropdown}
          name={"type"}
          onChange={handleSubscriptionTypeChange}
        >
          <option value={"CONTINUOUS"}>
            {translate.t("searchFindings.servicesTable.continuous")}
          </option>
          <option value={"ONESHOT"}>
            {translate.t("searchFindings.servicesTable.oneShot")}
          </option>
        </Field>
      ),
    },
  ].concat(
    servicesList.map((element: IServicesDataSet): {
      service: JSX.Element;
      status: JSX.Element;
    } => ({
      service: (
        <p>{translate.t(`searchFindings.servicesTable.${element.service}`)}</p>
      ),
      status: (
        <FormGroup>
          <Field
            component={FormSwitchButton}
            name={element.service}
            props={{
              id: element.id,
              offlabel: translate.t("searchFindings.servicesTable.inactive"),
              onChange: _.isUndefined(element.onChange)
                ? undefined
                : element.onChange,
              onlabel: translate.t("searchFindings.servicesTable.active"),
            }}
            type={"checkbox"}
          />
        </FormGroup>
      ),
    }))
  );

  // Using form validation instead of field validation to avoid an infinite-loop error
  const formValidations: (values: { confirmation: string }) => {
    confirmation?: string;
  } = useCallback(
    (values: { confirmation: string }): { confirmation?: string } => {
      if (values.confirmation === groupName) {
        return {};
      }

      const errorsFound: { confirmation?: string } = {
        // Exception: FP(Implicit treatment in assignment)
        // eslint-disable-next-line
        confirmation: translate.t( // NOSONAR
          "searchFindings.servicesTable.errors.expectedGroupName",
          { groupName }
        ),
      };

      return errorsFound;
    },
    [groupName]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <div>
        <Row>
          {/* eslint-disable-next-line react/forbid-component-props */}
          <Col80 className={"pa0"}>
            <h2>{translate.t("searchFindings.servicesTable.services")}</h2>
          </Col80>
        </Row>
        <GenericForm
          initialValues={{
            comments: "",
            confirmation: "",
            forces: data.group.hasForces,
            integrates: true,
            machine: data.group.hasSkims,
            reason: "NONE",
            squad: data.group.hasDrills,
            type: data.group.subscription.toUpperCase(),
          }}
          name={"editGroup"}
          onSubmit={handleFormSubmit}
          validate={formValidations}
        >
          {({
            handleSubmit,
            pristine,
            valid,
          }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              <DataTableNext
                bordered={true}
                dataset={servicesDataSet}
                exportCsv={false}
                headers={tableHeaders}
                id={"tblServices"}
                pageSize={10}
                search={false}
                striped={true}
              />
              {/* Intentionally hidden while loading/submitting to offer a better UX
               *   this way the button does not twinkle and is visually stable
               */}
              {pristine ||
              loadingGroupData ||
              submittingGroupData ? undefined : (
                <Row>
                  <Col100>
                    <ButtonToolbar>
                      <Button onClick={handleTblButtonClick}>
                        {translate.t(
                          "searchFindings.servicesTable.modal.continue"
                        )}
                      </Button>
                    </ButtonToolbar>
                  </Col100>
                </Row>
              )}
              <Modal
                headerTitle={translate.t(
                  "searchFindings.servicesTable.modal.title"
                )}
                open={isModalOpen}
              >
                <ControlLabel>
                  {translate.t(
                    "searchFindings.servicesTable.modal.changesToApply"
                  )}
                </ControlLabel>
                <Well>
                  {computeConfirmationMessage(data, formValues).map(
                    (line: string): JSX.Element => (
                      <p key={line}>{line}</p>
                    )
                  )}
                </Well>
                <FormGroup>
                  <ControlLabel>
                    {translate.t(
                      "searchFindings.servicesTable.modal.observations"
                    )}
                  </ControlLabel>
                  <Field
                    component={TextArea}
                    name={"comments"}
                    placeholder={translate.t(
                      "searchFindings.servicesTable.modal.observationsPlaceholder"
                    )}
                    type={"text"}
                    validate={[validTextField, maxLength250]}
                  />
                </FormGroup>
                {isDowngradingServices(data, formValues) ? (
                  <FormGroup>
                    <ControlLabel>
                      {translate.t(
                        "searchFindings.servicesTable.modal.downgrading"
                      )}
                    </ControlLabel>
                    <Field component={Dropdown} name={"reason"} type={"text"}>
                      {downgradeReasons.map(
                        (reason: string): JSX.Element => (
                          <option key={reason} value={reason}>
                            {translate.t(
                              `searchFindings.servicesTable.modal.${_.camelCase(
                                reason.toLowerCase()
                              )}`
                            )}
                          </option>
                        )
                      )}
                    </Field>
                  </FormGroup>
                ) : undefined}
                {isDowngrading(true, formValues.integrates) ? (
                  <FormGroup>
                    <ControlLabel>
                      {translate.t(
                        "searchFindings.servicesTable.modal.warning"
                      )}
                    </ControlLabel>
                    <Alert>
                      {translate.t(
                        "searchFindings.servicesTable.modal.warningDowngradeASM"
                      )}
                    </Alert>
                  </FormGroup>
                ) : undefined}
                <FormGroup>
                  <ControlLabel>
                    {translate.t(
                      "searchFindings.servicesTable.modal.typeGroupName"
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
                <Alert>
                  {"* "}
                  {translate.t(
                    "organization.tabs.groups.newGroup.extraChargesMayApply"
                  )}
                </Alert>
                <hr />
                <Row>
                  <Col100>
                    <ButtonToolbar>
                      <Button onClick={handleClose}>
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
              </Modal>
            </React.Fragment>
          )}
        </GenericForm>
      </div>
    </React.StrictMode>
  );
};

export { Services };
