/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for using components with render props
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Alert, ButtonToolbar, Col, ControlLabel, FormGroup, Row, Well } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { useHistory } from "react-router-dom";
import { Dispatch } from "redux";
import { change, EventWithDataHandler, Field, formValueSelector, InjectedFormProps, Validator } from "redux-form";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { IHeaderConfig } from "components/DataTableNext/types";
import { Modal } from "components/Modal";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { EDIT_GROUP_DATA, GET_GROUP_DATA } from "scenes/Dashboard/containers/ProjectSettingsView/queries";
import {
  computeConfirmationMessage,
  isDowngrading,
  isDowngradingServices,
} from "scenes/Dashboard/containers/ProjectSettingsView/Services/businessLogic";
import styles from "scenes/Dashboard/containers/ProjectSettingsView/Services/index.css";
import {
  IFormData,
  IServicesDataSet,
  IServicesProps,
} from "scenes/Dashboard/containers/ProjectSettingsView/Services/types";
import { Dropdown, SwitchButton, Text, TextArea } from "utils/forms/fields";
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

const maxLength250: Validator = maxLength(250);

const services: React.FC<IServicesProps> = (props: IServicesProps): JSX.Element => {
  const { groupName } = props;

  // State management
  const { push } = useHistory();
  const dispatch: Dispatch = useDispatch();
  const selector: (state: {}, ...fields: string[]) => IFormData = formValueSelector("editGroup");
  const formValues: IFormData = useSelector((state: {}) =>
    selector(state, "comments", "confirmation", "drills", "forces", "integrates", "reason", "type"));
  const [isModalOpen, setIsModalOpen] = React.useState(false);

  // Business Logic handlers
  const handleSubscriptionTypeChange: EventWithDataHandler<React.ChangeEvent<string>> = (
    event: React.ChangeEvent<string> | undefined, subsType: string,
  ): void => {
    dispatch(change("editGroup", "drills", true));
    dispatch(change("editGroup", "forces", isContinuousType(subsType)));
  };
  const handleIntegratesBtnChange: ((withIntegrates: boolean) => void) = (withIntegrates: boolean): void => {
    dispatch(change("editGroup", "integrates", withIntegrates));

    if (!withIntegrates) {
      dispatch(change("editGroup", "forces", false));
      dispatch(change("editGroup", "drills", false));
    }
  };
  const handleDrillsBtnChange: ((withDrills: boolean) => void) = (withDrills: boolean): void => {
    dispatch(change("editGroup", "drills", withDrills));

    if (withDrills) {
      dispatch(change("editGroup", "integrates", true));
    } else {
      dispatch(change("editGroup", "forces", false));
    }
  };
  const handleForcesBtnChange: ((withForces: boolean) => void) = (withForces: boolean): void => {
    dispatch(change("editGroup", "forces", isContinuousType(formValues.type) && withForces));

    if (withForces) {
      dispatch(change("editGroup", "integrates", true));
      dispatch(change("editGroup", "drills", true));
    }
  };

  // GraphQL Logic
  const { data, loading: loadingGroupData, refetch: refetchGroupData } = useQuery(GET_GROUP_DATA, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred getting group data", error);
      });
    },
    variables: { groupName },
  });

  const [editGroupData, { loading: submittingGroupData }] = useMutation(EDIT_GROUP_DATA, {
    onCompleted: (): void => {
      mixpanel.track("EditGroupData", formValues);
      msgSuccess(
        translate.t("search_findings.services_table.success"),
        translate.t("search_findings.services_table.success_title"),
      );

      if (formValues.integrates) {
        refetchGroupData({ groupName });
      } else {
        push("/home");
      }
    },
    onError: (error: ApolloError): void => {
      error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        let msg: string;

        switch (message) {
          case "Exception - Forces is only available when Drills is too":
            msg = "search_findings.services_table.errors.forces_only_if_drills";
            break;
          case "Exception - Forces is only available in projects of type Continuous":
            msg = "search_findings.services_table.errors.forces_only_if_continuous";
            break;
          default:
            msg = "group_alerts.error_textsad";
            Logger.warning("An error occurred editing group services", error);
        }

        msgError(translate.t(msg));
      });
    },
    variables: {
      comments: formValues.comments,
      groupName,
      hasDrills: formValues.drills,
      hasForces: formValues.forces,
      hasIntegrates: formValues.integrates,
      reason: formValues.reason,
      subscription: formValues.type,
    },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  const handleClose: (() => void) = (): void => {
    setIsModalOpen(false);
  };
  const handleFormSubmit: (() => void) = (): void => {
    editGroupData();
    setIsModalOpen(false);
  };
  const handleTblButtonClick: (() => void) = (): void => {
    setIsModalOpen(true);
  };

  // Rendered elements
  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "service",
      header: translate.t("search_findings.services_table.service"),
      width: "75%",
      wrapped: true,
    },
    {
      dataField: "status",
      header: translate.t("search_findings.services_table.status"),
      width: "25%",
      wrapped: true,
    },
  ];
  const servicesList: IServicesDataSet[] = [
    {
      canHave: true,
      onChange: handleIntegratesBtnChange,
      service: "integrates",
    },
    {
      canHave: true,
      onChange: handleDrillsBtnChange,
      service: "drills",
    },
    {
      canHave: isContinuousType(formValues.type),
      onChange: handleForcesBtnChange,
      service: "forces",
    },
  ].filter((element: IServicesDataSet): boolean => element.canHave);

  const servicesDataSet: Array<{ [key: string]: JSX.Element }> = [
    {
      service: (
        <p>{translate.t("search_findings.services_table.type")}</p>
      ),
      status: (
        <Field
          component={Dropdown}
          name="type"
          onChange={handleSubscriptionTypeChange}
        >
          <option value="CONTINUOUS">
            {translate.t("search_findings.services_table.continuous")}
          </option>
          <option value="ONESHOT">
            {translate.t("search_findings.services_table.one_shot")}
          </option>
        </Field>
      ),
    },
  ].concat(servicesList.map((element: IServicesDataSet) => ({
    service: (
      <p>{translate.t(`search_findings.services_table.${element.service}`)}</p>
    ),
    status: (
      <React.Fragment>
        <FormGroup>
          <Field
            component={SwitchButton}
            name={element.service}
            props={{
              disabled: false,
              offlabel: translate.t("search_findings.services_table.inactive"),
              onChange: _.isUndefined(element.onChange) ? undefined : element.onChange,
              onlabel: translate.t("search_findings.services_table.active"),
              onstyle: "danger",
              style: "btn-block",
            }}
            type="checkbox"
          />
        </FormGroup>
      </React.Fragment>
    ),
   })));

  // Using form validation instead of field validation to avoid an infinite-loop error
  const formValidations: (values: { confirmation: string }) => { confirmation?: string } =
    (values: { confirmation: string }): { confirmation?: string } => {
      const errorsFound: { confirmation?: string } = {};

      if (values.confirmation !== groupName) {
        errorsFound.confirmation =
          translate.t("search_findings.services_table.errors.expected_group_name", { groupName });
      }

      return errorsFound;
    };

  return (
    <React.StrictMode>
      <div className={styles.wrapper}>
        <Row>
          <Col lg={8} md={10} xs={7}>
            <h3>{translate.t("search_findings.services_table.services")}</h3>
          </Col>
        </Row>
        <GenericForm
          name="editGroup"
          onSubmit={handleFormSubmit}
          initialValues={{
            comments: "",
            confirmation: "",
            drills: data.project.hasDrills,
            forces: data.project.hasForces,
            integrates: true,
            reason: "NONE",
            type: data.project.subscription.toUpperCase(),
          }}
          validate={formValidations}
        >
          {({ handleSubmit, pristine, valid }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              <DataTableNext
                bordered={true}
                dataset={servicesDataSet}
                exportCsv={false}
                search={false}
                headers={tableHeaders}
                id="tblServices"
                pageSize={5}
                striped={true}
              />
              {/* Intentionally hidden while loading/submitting to offer a better UX
                *   this way the button does not twinkle and is visually stable
                */}
              {pristine || loadingGroupData || submittingGroupData ? undefined : (
                <ButtonToolbar className="pull-right">
                  <Button bsStyle="success" onClick={handleTblButtonClick}>
                    {translate.t("search_findings.services_table.modal.continue")}
                  </Button>
                </ButtonToolbar>
              )}
              <Modal
                headerTitle={translate.t("search_findings.services_table.modal.title")}
                open={isModalOpen}
                footer={
                  <ButtonToolbar className="pull-right">
                    <Button onClick={handleClose}>{translate.t("confirmmodal.cancel")}</Button>
                    <Button
                      disabled={!valid}
                      onClick={handleSubmit}
                      type="submit"
                    >
                      {translate.t("confirmmodal.proceed")}
                    </Button>
                  </ButtonToolbar>
                }
              >
                <ControlLabel>{translate.t("search_findings.services_table.modal.changes_to_apply")}</ControlLabel>
                <Well>
                  {computeConfirmationMessage(data, formValues)
                    .map((line: string) => <p key={line}>{line}</p>)}
                </Well>
                <FormGroup>
                  <ControlLabel>{translate.t("search_findings.services_table.modal.observations")}</ControlLabel>
                  <Field
                    name="comments"
                    component={TextArea}
                    placeholder={translate.t("search_findings.services_table.modal.observations_placeholder")}
                    type="text"
                    validate={[validTextField, maxLength250]}
                  />
                </FormGroup>
                {isDowngradingServices(data, formValues) ? (
                  <FormGroup>
                    <ControlLabel>{translate.t("search_findings.services_table.modal.downgrading")}</ControlLabel>
                    <Field
                      name="reason"
                      component={Dropdown}
                      type="text"
                    >
                      {downgradeReasons.map((reason: string) => (
                        <option value={reason} key={reason}>
                          {translate.t(`search_findings.services_table.modal.${reason.toLowerCase()}`)}
                        </option>
                      ))}
                    </Field>
                  </FormGroup>
                ) : undefined}
                {isDowngrading(true, formValues.integrates) ? (
                  <FormGroup>
                    <ControlLabel>{translate.t("search_findings.services_table.modal.warning")}</ControlLabel>
                    <Alert bsStyle="danger">
                      {translate.t("search_findings.services_table.modal.warning_downgrade_integrates")}
                    </Alert>
                  </FormGroup>
                ) : undefined}
                <FormGroup>
                  <ControlLabel>{translate.t("search_findings.services_table.modal.type_group_name")}</ControlLabel>
                  <Field
                    name="confirmation"
                    component={Text}
                    placeholder={groupName.toLowerCase()}
                    type="text"
                    validate={required}
                  />
                </FormGroup>
                <Alert bsStyle="warning">
                  * {translate.t("organization.tabs.groups.newGroup.extra_charges_may_apply")}
                </Alert>
              </Modal>
            </React.Fragment>
          )}
        </GenericForm>
      </div>
    </React.StrictMode>
  );
};

export { services as Services };
