/* tslint:disable:jsx-no-multiline-js
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import { MutationFunction, MutationResult, QueryResult } from "@apollo/react-common";
import { Mutation, Query } from "@apollo/react-components";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Glyphicon } from "react-bootstrap";
import { selectFilter } from "react-bootstrap-table2-filter";
import { useSelector } from "react-redux";
import { useHistory, useParams } from "react-router";
import { Field, FormSection, formValueSelector, InjectedFormProps, Validator } from "redux-form";
import { ConfigurableValidator } from "revalidate";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { statusFormatter } from "components/DataTableNext/formatters";
import { IHeaderConfig } from "components/DataTableNext/types";
import { Modal } from "components/NewModal";
import { TooltipWrapper } from "components/TooltipWrapper";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { CREATE_EVENT_MUTATION, GET_EVENTS } from "scenes/Dashboard/containers/ProjectEventsView/queries";
import { formatEvents } from "scenes/Dashboard/containers/ProjectEventsView/utils";
import { default as globalStyle } from "styles/global.css";
import { ButtonToolbar, ButtonToolbarCenter, Col100, Col50, ControlLabel, FormGroup, Row } from "styles/styledComponents";

import { authContext, IAuthContext } from "utils/auth";
import { Can } from "utils/authz/Can";
import { castEventType } from "utils/formatHelpers";
import {
  Checkbox, DateTime, Dropdown, FileInput, Text, TextArea,
} from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import {
  dateTimeBeforeToday, isValidFileSize, maxLength, numeric, required, someRequired, validDatetime,
  validEventFile, validEvidenceImage, validTextField,
} from "utils/validations";

const maxEventDetailsLength: ConfigurableValidator = maxLength(300);
const projectEventsView: React.FC = (): JSX.Element => {
  const { push } = useHistory();
  const { projectName } = useParams<{ projectName: string }>();
  const { userName }: IAuthContext = React.useContext(authContext);

  const selectOptionsStatus: optionSelectFilterProps[] = [
    { value: "Solved", label: "Solved" },
    { value: "Unsolved", label: "Unsolved" },
  ];
  const selectOptionType: optionSelectFilterProps[] = [
    {
      label: translate.t("group.events.form.type.special_attack"),
      value: translate.t(castEventType("AUTHORIZATION_SPECIAL_ATTACK")),
    },
    {
      label: translate.t("group.events.form.type.toe_change"),
      value: translate.t(castEventType("CLIENT_APPROVES_CHANGE_TOE")),
    },
    {
      label: translate.t(castEventType("CLIENT_DETECTS_ATTACK")),
      value: translate.t(castEventType("CLIENT_DETECTS_ATTACK")),
    },
    {
      label: translate.t("group.events.form.type.high_availability"),
      value: translate.t(castEventType("HIGH_AVAILABILITY_APPROVAL")),
    },
    {
      label: translate.t("group.events.form.type.missing_supplies"),
      value: translate.t(castEventType("INCORRECT_MISSING_SUPPLIES")),
    },
    {
      label: translate.t("group.events.form.type.toe_differs"),
      value: translate.t(castEventType("TOE_DIFFERS_APPROVED")),
    },
    {
      label: translate.t("group.events.form.other"),
      value: translate.t(castEventType("OTHER")),
    },
  ];
  const [optionType, setOptionType] = React.useState(selectOptionType);

  const onSortState: ((dataField: string, order: SortOrder) => void) = (
    dataField: string, order: SortOrder,
  ): void => {
    const newSorted: Sorted = { dataField, order };
    sessionStorage.setItem("eventSort", JSON.stringify(newSorted));
  };
  const onFilterStatus: ((filterVal: string) => void) = (filterVal: string): void => {
    sessionStorage.setItem("eventStatusFilter", filterVal);
  };
  const onFilterType: ((filterVal: string) => void) = (filterVal: string): void => {
    sessionStorage.setItem("eventTypeFilter", filterVal);
  };

  const tableHeaders: IHeaderConfig[] = [
    {
      align: "center", dataField: "id", header: translate.t("search_findings.tab_events.id"), onSort: onSortState,
      width: "8%", wrapped: true,
    },
    {
      align: "center", dataField: "eventDate", header: translate.t("search_findings.tab_events.date"),
      onSort: onSortState, width: "10%", wrapped: true,
    },
    {
      align: "center", dataField: "detail", header: translate.t("search_findings.tab_events.description"),
      onSort: onSortState, width: "35%", wrapped: true,
    },
    {
      align: "center", dataField: "eventType",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "eventTypeFilter"),
        onFilter: onFilterType,
        options: optionType,
      }),
      header: translate.t("search_findings.tab_events.type"), onSort: onSortState, width: "18%", wrapped: true,
    },
    {
      align: "center", dataField: "eventStatus",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "eventStatusFilter"),
        onFilter: onFilterStatus,
        options: selectOptionsStatus,
      }),
      formatter: statusFormatter, header: translate.t("search_findings.tab_events.status"), onSort: onSortState,
      width: "16%", wrapped: true,
    },
    {
      align: "center", dataField: "closingDate", header: translate.t("search_findings.tab_events.closing_date"),
      onSort: onSortState, width: "13%", wrapped: true,
    },
  ];
  interface IEventsDataset { project: { events: Array<{ eventType: string }> }; }
  const handleQryResult: ((data: IEventsDataset) => void) = (data: IEventsDataset): void => {
    if (!_.isUndefined(data)) {
      let eventOptions: string[] = Array.from(new Set(data.project.events.map(
        (event: { eventType: string }) => event.eventType)));
      eventOptions = eventOptions.map((option: string) => translate.t(castEventType(option)));
      const filterOptions: optionSelectFilterProps[] = selectOptionType.filter(
        (option: optionSelectFilterProps) => (_.includes(eventOptions, option.value)));
      setOptionType(filterOptions);
      mixpanel.track("ProjectEvents", { User: userName });
    }
  };
  const handleQryErrors: ((error: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      Logger.warning("An error occurred loading project data", error);
      msgError(translate.t("group_alerts.error_textsad"));
    });
  };

  const goToEvent: ((event: React.FormEvent<HTMLButtonElement>, rowInfo: { id: string }) => void) = (
    _0: React.FormEvent<HTMLButtonElement>, rowInfo: { id: string },
  ): void => {
    mixpanel.track("ReadEvent", { User: userName });
    push(`/groups/${projectName}/events/${rowInfo.id}/description`);
  };

  const [isEventModalOpen, setEventModalOpen] = React.useState(false);

  const openNewEventModal: (() => void) = (): void => {
    setEventModalOpen(true);
  };

  const closeNewEventModal: (() => void) = (): void => {
    setEventModalOpen(false);
  };

  const selector: (state: {}, ...field: string[]) => string = formValueSelector("newEvent");
  const eventType: string = useSelector((state: {}) => selector(state, "eventType"));

  const maxFileSize: Validator = isValidFileSize(10);

  return (
    <Query
      query={GET_EVENTS}
      variables={{ projectName }}
      onCompleted={handleQryResult}
      onError={handleQryErrors}
    >
      {
        ({ data, refetch }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) {

            return <React.Fragment />;
          }

          const handleCreationResult: ((result: { createEvent: { success: boolean } }) => void) = (
              result: { createEvent: { success: boolean } },
            ): void => {
              if (result.createEvent.success) {
                closeNewEventModal();
                msgSuccess(
                  translate.t("group.events.success_create"),
                  translate.t("group.events.title_success"),
                );
                void refetch();
              }
            };

          const handleCreationError: ((creationError: ApolloError) => void) = (creationError: ApolloError): void => {
              creationError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
                switch (message) {
                  case "Exception - Invalid File Size":
                    msgError(translate.t("validations.file_size", { count: 10 }));
                    break;
                  case "Exception - Invalid File Type: EVENT_IMAGE":
                    msgError(translate.t("group.events.form.wrong_image_type"));
                    break;
                  case "Exception - Invalid File Type: EVENT_FILE":
                    msgError(translate.t("group.events.form.wrong_file_type"));
                    break;
                  default:
                    msgError(translate.t("group_alerts.error_textsad"));
                    Logger.warning("An error occurred updating event evidence", creationError);
                }
              });
            };

          return (
              <React.StrictMode>
                <Row>
                  <Col100>
                    <ButtonToolbarCenter>
                      <Can do="backend_api_mutations_create_event_mutate">
                        <TooltipWrapper message={translate.t("group.events.btn.tooltip")}>
                          <Button onClick={openNewEventModal}>
                            <Glyphicon glyph="plus" />&nbsp;{translate.t("group.events.btn.text")}
                          </Button>
                        </TooltipWrapper>
                      </Can>
                    </ButtonToolbarCenter>
                  </Col100>
                </Row>
                <Modal
                  headerTitle={translate.t("group.events.new")}
                  open={isEventModalOpen}
                >
                  <Mutation
                    mutation={CREATE_EVENT_MUTATION}
                    onCompleted={handleCreationResult}
                    onError={handleCreationError}
                  >
                    {(createEvent: MutationFunction, mtResult: MutationResult): JSX.Element => {
                      interface IFormValues {
                        accessibility: { [key: string]: boolean };
                        affectedComponents: { [key: string]: boolean };
                        file?: FileList;
                        image?: FileList;
                      }

                      const handleSubmit: ((values: IFormValues) => void) = (values: IFormValues): void => {
                        const selectedAccessibility: string[] = Object.keys(values.accessibility)
                          .filter((key: string) => values.accessibility[key])
                          .map((key: string) => key.toUpperCase());

                        const selectedComponents: string[] | undefined = _.isUndefined(values.affectedComponents)
                          ? undefined
                          : Object.keys(values.affectedComponents)
                            .filter((key: string) => values.affectedComponents[key])
                            .map((key: string) => key.toUpperCase());

                        void createEvent({
                          variables: {
                            projectName,
                            ...values,
                            accessibility: selectedAccessibility,
                            affectedComponents: selectedComponents,
                            file: _.isEmpty(values.file) ? undefined : (values.file as FileList)[0],
                            image: _.isEmpty(values.image) ? undefined : (values.image as FileList)[0],
                          },
                        });
                      };

                      return (
                        <GenericForm name="newEvent" onSubmit={handleSubmit}>
                          {({ pristine }: InjectedFormProps): JSX.Element => (
                            <React.Fragment>
                              <Row>
                                <Col50>
                                  <FormGroup>
                                    <ControlLabel>{translate.t("group.events.form.date")}</ControlLabel>
                                    <Field
                                      component={DateTime}
                                      name="eventDate"
                                      validate={[required, validDatetime, dateTimeBeforeToday]}
                                    />
                                  </FormGroup>
                                </Col50>
                                <Col50>
                                  <FormGroup>
                                    <ControlLabel>{translate.t("group.events.form.type.title")}</ControlLabel>
                                    <Field component={Dropdown} name="eventType" validate={required}>
                                      <option value="" selected={true} />
                                      <option value="AUTHORIZATION_SPECIAL_ATTACK">
                                        {translate.t("group.events.form.type.special_attack")}
                                      </option>
                                      <option value="CLIENT_APPROVES_CHANGE_TOE">
                                        {translate.t("group.events.form.type.toe_change")}
                                      </option>
                                      <option value="CLIENT_DETECTS_ATTACK">
                                        {translate.t("group.events.form.type.detects_attack")}
                                      </option>
                                      <option value="HIGH_AVAILABILITY_APPROVAL">
                                        {translate.t("group.events.form.type.high_availability")}
                                      </option>
                                      <option value="INCORRECT_MISSING_SUPPLIES">
                                        {translate.t("group.events.form.type.missing_supplies")}
                                      </option>
                                      <option value="TOE_DIFFERS_APPROVED">
                                        {translate.t("group.events.form.type.toe_differs")}
                                      </option>
                                      <option value="OTHER">
                                        {translate.t("group.events.form.other")}
                                      </option>
                                    </Field>
                                  </FormGroup>
                                </Col50>
                              </Row>
                              <Row>
                                <Col50>
                                  <FormGroup>
                                    <ControlLabel>{translate.t("group.events.form.context.title")}</ControlLabel>
                                    <Field component={Dropdown} name="context" validate={required}>
                                      <option value="" selected={true} />
                                      <option value="CLIENT">
                                        {translate.t("group.events.form.context.client")}
                                      </option>
                                      <option value="FLUID">
                                        {translate.t("group.events.form.context.fluid")}
                                      </option>
                                      <option value="PLANNING">
                                        {translate.t("group.events.form.context.planning")}
                                      </option>
                                      <option value="TELECOMMUTING">
                                        {translate.t("group.events.form.context.telecommuting")}
                                      </option>
                                      <option value="OTHER">
                                        {translate.t("group.events.form.other")}
                                      </option>
                                    </Field>
                                  </FormGroup>
                                </Col50>
                                <Col50>
                                  <FormGroup>
                                    <ControlLabel>
                                      {translate.t("group.events.form.accessibility.title")}
                                    </ControlLabel>
                                    <FormSection name="accessibility">
                                      <Field component={Checkbox} name="environment" validate={someRequired}>
                                        {translate.t("group.events.form.accessibility.environment")}
                                      </Field>
                                      <Field component={Checkbox} name="repository" validate={someRequired}>
                                        {translate.t("group.events.form.accessibility.repository")}
                                      </Field>
                                    </FormSection>
                                  </FormGroup>
                                </Col50>
                              </Row>
                              {eventType === "INCORRECT_MISSING_SUPPLIES" ?
                                <Row>
                                  <Col50>
                                    <FormGroup>
                                      <ControlLabel>{translate.t("group.events.form.blocking_hours")}</ControlLabel>
                                      <Field
                                        component={Text}
                                        name="blockingHours"
                                        type="number"
                                        validate={[numeric, required]}
                                      />
                                    </FormGroup>
                                  </Col50>
                                  <Col50>
                                    <FormGroup>
                                      <ControlLabel>
                                        {translate.t("group.events.form.components.title")}
                                      </ControlLabel>
                                      <FormSection name="affectedComponents">
                                        <Field component={Checkbox} name="FLUID_STATION" validate={someRequired}>
                                          {translate.t("group.events.form.components.fluid_station")}
                                        </Field>
                                        <Field component={Checkbox} name="CLIENT_STATION" validate={someRequired}>
                                          {translate.t("group.events.form.components.client_station")}
                                        </Field>
                                        <Field component={Checkbox} name="TOE_EXCLUSSION" validate={someRequired}>
                                          {translate.t("group.events.form.components.toe_exclussion")}
                                        </Field>
                                        <Field component={Checkbox} name="DOCUMENTATION" validate={someRequired}>
                                          {translate.t("group.events.form.components.documentation")}
                                        </Field>
                                        <Field
                                          component={Checkbox}
                                          name="LOCAL_CONNECTION"
                                          validate={someRequired}
                                        >
                                          {translate.t("group.events.form.components.local_conn")}
                                        </Field>
                                        <Field
                                          component={Checkbox}
                                          name="INTERNET_CONNECTION"
                                          validate={someRequired}
                                        >
                                          {translate.t("group.events.form.components.internet_conn")}
                                        </Field>
                                        <Field component={Checkbox} name="VPN_CONNECTION" validate={someRequired}>
                                          {translate.t("group.events.form.components.vpn_conn")}
                                        </Field>
                                        <Field component={Checkbox} name="TOE_LOCATION" validate={someRequired}>
                                          {translate.t("group.events.form.components.toe_location")}
                                        </Field>
                                        <Field component={Checkbox} name="TOE_CREDENTIALS" validate={someRequired}>
                                          {translate.t("group.events.form.components.toe_credentials")}
                                        </Field>
                                        <Field component={Checkbox} name="TOE_PRIVILEGES" validate={someRequired}>
                                          {translate.t("group.events.form.components.toe_privileges")}
                                        </Field>
                                        <Field component={Checkbox} name="TEST_DATA" validate={someRequired}>
                                          {translate.t("group.events.form.components.test_data")}
                                        </Field>
                                        <Field component={Checkbox} name="TOE_UNSTABLE" validate={someRequired}>
                                          {translate.t("group.events.form.components.toe_unstability")}
                                        </Field>
                                        <Field
                                          component={Checkbox}
                                          name="TOE_UNACCESSIBLE"
                                          validate={someRequired}
                                        >
                                          {translate.t("group.events.form.components.toe_unaccessible")}
                                        </Field>
                                        <Field component={Checkbox} name="TOE_UNAVAILABLE" validate={someRequired}>
                                          {translate.t("group.events.form.components.toe_unavailable")}
                                        </Field>
                                        <Field component={Checkbox} name="TOE_ALTERATION" validate={someRequired}>
                                          {translate.t("group.events.form.components.toe_alteration")}
                                        </Field>
                                        <Field component={Checkbox} name="SOURCE_CODE" validate={someRequired}>
                                          {translate.t("group.events.form.components.source_code")}
                                        </Field>
                                        <Field component={Checkbox} name="COMPILE_ERROR" validate={someRequired}>
                                          {translate.t("group.events.form.components.compile_error")}
                                        </Field>
                                        <Field component={Checkbox} name="OTHER" validate={someRequired}>
                                          {translate.t("group.events.form.other")}
                                        </Field>
                                      </FormSection>
                                    </FormGroup>
                                  </Col50>
                                </Row>
                                : undefined}
                              <Row>
                                <Col100>
                                  <FormGroup>
                                    <ControlLabel>{translate.t("group.events.form.details")}</ControlLabel>
                                    <Field
                                      className={globalStyle.noResize}
                                      component={TextArea}
                                      name="detail"
                                      validate={[required, validTextField, maxEventDetailsLength]}
                                    />
                                  </FormGroup>
                                </Col100>
                              </Row>
                              <Row>
                                <Col50>
                                  <FormGroup>
                                    <ControlLabel>
                                      {translate.t("group.events.form.action_before.title")}
                                    </ControlLabel>
                                    <Field component={Dropdown} name="actionBeforeBlocking" validate={required}>
                                      <option value="" selected={true} />
                                      <option value="DOCUMENT_PROJECT">
                                        {translate.t("group.events.form.action_before.document")}
                                      </option>
                                      <option value="TEST_OTHER_PART_TOE">
                                        {translate.t("group.events.form.action_before.test_other")}
                                      </option>
                                      <option value="NONE">
                                        {translate.t("group.events.form.none")}
                                      </option>
                                      <option value="OTHER">
                                        {translate.t("group.events.form.other")}
                                      </option>
                                    </Field>
                                  </FormGroup>
                                </Col50>
                                <Col50>
                                  <FormGroup>
                                    <ControlLabel>{translate.t("group.events.form.action_after.title")}</ControlLabel>
                                    <Field component={Dropdown} name="actionAfterBlocking" validate={required}>
                                      <option value="" selected={true} />
                                      <option value="EXECUTE_OTHER_PROJECT_SAME_CLIENT">
                                        {translate.t("group.events.form.action_after.other_same")}
                                      </option>
                                      <option value="EXECUTE_OTHER_PROJECT_OTHER_CLIENT">
                                        {translate.t("group.events.form.action_after.other_other")}
                                      </option>
                                      <option value="TRAINING">
                                        {translate.t("group.events.form.action_after.training")}
                                      </option>
                                      <option value="NONE">
                                        {translate.t("group.events.form.none")}
                                      </option>
                                      <option value="OTHER">
                                        {translate.t("group.events.form.other")}
                                      </option>
                                    </Field>
                                  </FormGroup>
                                </Col50>
                              </Row>
                              <Row>
                                <Col50>
                                  <FormGroup>
                                    <ControlLabel>{translate.t("group.events.form.evidence")}</ControlLabel>
                                    <Field
                                      accept="image/gif,image/png"
                                      component={FileInput}
                                      id="image"
                                      name="image"
                                      validate={[validEvidenceImage, maxFileSize]}
                                    />
                                  </FormGroup>
                                </Col50>
                                <Col50>
                                  <FormGroup>
                                    <ControlLabel>{translate.t("group.events.form.evidence_file")}</ControlLabel>
                                    <Field
                                      accept="application/pdf,application/zip,text/csv,text/plain"
                                      component={FileInput}
                                      id="file"
                                      name="file"
                                      validate={[validEventFile, maxFileSize]}
                                    />
                                  </FormGroup>
                                </Col50>
                              </Row>
                              <hr />
                              <Row>
                                <Col100>
                                  <ButtonToolbar>
                                    <Button onClick={closeNewEventModal}>
                                      {translate.t("confirmmodal.cancel")}
                                    </Button>
                                    <Button type="submit" disabled={pristine || mtResult.loading}>
                                      {translate.t("confirmmodal.proceed")}
                                    </Button>
                                  </ButtonToolbar>
                                </Col100>
                              </Row>
                            </React.Fragment>
                          )}
                        </GenericForm>
                      );
                    }}
                  </Mutation>
                </Modal>
                <p>{translate.t("search_findings.tab_events.table_advice")}</p>
                <DataTableNext
                  bordered={true}
                  dataset={formatEvents(data.project.events)}
                  defaultSorted={JSON.parse(_.get(sessionStorage, "eventSort", "{}"))}
                  exportCsv={true}
                  search={true}
                  headers={tableHeaders}
                  id="tblEvents"
                  pageSize={15}
                  rowEvents={{ onClick: goToEvent }}
                />
              </React.StrictMode>
            );
        }}
    </Query>
  );
};

export { projectEventsView as ProjectEventsView };
