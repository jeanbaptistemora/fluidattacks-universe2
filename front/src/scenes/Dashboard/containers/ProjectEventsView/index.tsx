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
import { ButtonToolbar, Col, ControlLabel, FormGroup, Glyphicon, Row } from "react-bootstrap";
import { selectFilter } from "react-bootstrap-table2-filter";
import { useSelector } from "react-redux";
import { RouteComponentProps } from "react-router";
import { Field, FormSection, formValueSelector, InjectedFormProps, Validator } from "redux-form";
import { Button } from "../../../../components/Button";
import { statusFormatter } from "../../../../components/DataTableNext/formatters";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeader } from "../../../../components/DataTableNext/types";
import { Modal } from "../../../../components/Modal";
import { default as globalStyle } from "../../../../styles/global.css";
import { Can } from "../../../../utils/authz/Can";
import { castEventType, formatEvents, handleGraphQLErrors } from "../../../../utils/formatHelpers";
import {
  checkboxField, dateTimeField, dropdownField, fileInputField, textAreaField, textField,
} from "../../../../utils/forms/fields";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import {
  dateTimeBeforeToday, isValidFileSize, numeric, required, someRequired, validDatetime, validEventFile,
  validEvidenceImage,
} from "../../../../utils/validations";
import { GenericForm } from "../../components/GenericForm";
import { CREATE_EVENT_MUTATION, GET_EVENTS } from "./queries";

type EventsViewProps = RouteComponentProps<{ projectName: string }>;

const projectEventsView: React.FunctionComponent<EventsViewProps> = (props: EventsViewProps): JSX.Element => {
  const selectOptionsStatus: optionSelectFilterProps[] = [
    { value: "Solved", label: "Solved" },
    { value: "Unsolved", label: "Unsolved" },
  ];
  const selectOptionType: optionSelectFilterProps[] = [
    {
      label: translate.t("project.events.form.type.special_attack"),
      value: translate.t(castEventType("AUTHORIZATION_SPECIAL_ATTACK")),
    },
    {
      label: translate.t("project.events.form.type.toe_change"),
      value: translate.t(castEventType("CLIENT_APPROVES_CHANGE_TOE")),
    },
    {
      label: translate.t(castEventType("CLIENT_DETECTS_ATTACK")),
      value: translate.t(castEventType("CLIENT_DETECTS_ATTACK")),
    },
    {
      label: translate.t("project.events.form.type.suspends_project"),
      value: translate.t(castEventType("CLIENT_EXPLICITLY_SUSPENDS_PROJECT")),
    },
    {
      label: translate.t("project.events.form.type.high_availability"),
      value: translate.t(castEventType("HIGH_AVAILABILITY_APPROVAL")),
    },
    {
      label: translate.t("project.events.form.type.missing_supplies"),
      value: translate.t(castEventType("INCORRECT_MISSING_SUPPLIES")),
    },
    {
      label: translate.t("project.events.form.type.toe_differs"),
      value: translate.t(castEventType("TOE_DIFFERS_APPROVED")),
    },
    {
      label: translate.t("project.events.form.other"),
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

  const tableHeaders: IHeader[] = [
    {
      align: "center", dataField: "id", header: translate.t("search_findings.tab_events.id"), onSort: onSortState,
      width: "8%", wrapped: true,
    },
    {
      align: "center", dataField: "eventDate", header: translate.t("search_findings.tab_events.date"),
      onSort: onSortState, width: "13%", wrapped: true,
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
      width: "13%", wrapped: true,
    },
    {
      align: "center", dataField: "closingDate", header: translate.t("search_findings.tab_events.closing_date"),
      onSort: onSortState, width: "13%", wrapped: true,
    },
  ];
  const { projectName } = props.match.params;
  interface IEventsDataset { project: { events: Array<{ eventType: string }> }; }
  const handleQryResult: ((data: IEventsDataset) => void) = (data: IEventsDataset): void => {
    let eventOptions: string[] = Array.from(new Set(data.project.events.map(
      (event: { eventType: string }) => event.eventType)));
    eventOptions = eventOptions.map((option: string) => translate.t(castEventType(option)));
    const filterOptions: optionSelectFilterProps[] = selectOptionType.filter(
      (option: optionSelectFilterProps) => (_.includes(eventOptions, option.value)));
    setOptionType(filterOptions);
    mixpanel.track("ProjectEvents", {
      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
      User: (window as typeof window & { userName: string }).userName,
    });
  };

  const goToEvent: ((event: React.FormEvent<HTMLButtonElement>, rowInfo: { id: string }) => void) = (
    _0: React.FormEvent<HTMLButtonElement>, rowInfo: { id: string },
  ): void => {
    mixpanel.track("ReadEvent", {
      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
      User: (window as typeof window & { userName: string }).userName,
    });
    location.hash = `#!/project/${projectName}/events/${rowInfo.id}/description`;
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
    >
      {
        ({ data, error, refetch }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) {

            return <React.Fragment />;
          }
          if (!_.isUndefined(error)) {
            handleGraphQLErrors("An error occurred getting eventualities", error);

            return <React.Fragment />;
          }
          if (!_.isUndefined(data)) {
            const handleCreationResult: ((result: { createEvent: { success: boolean } }) => void) = (
              result: { createEvent: { success: boolean } },
            ): void => {
              if (result.createEvent.success) {
                closeNewEventModal();
                msgSuccess(
                  translate.t("project.events.success_create"),
                  translate.t("project.events.title_success"),
                );
                refetch()
                  .catch();
              }
            };

            const handleCreationError: ((creationError: ApolloError) => void) = (creationError: ApolloError): void => {
              creationError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
                switch (message) {
                  case "Exception - Invalid File Size":
                    msgError(translate.t("validations.file_size", { count: 10 }));
                    break;
                  case "Exception - Invalid File Type: EVENT_IMAGE":
                    msgError(translate.t("project.events.form.wrong_image_type"));
                    break;
                  case "Exception - Invalid File Type: EVENT_FILE":
                    msgError(translate.t("project.events.form.wrong_file_type"));
                    break;
                  default:
                    msgError(translate.t("proj_alerts.error_textsad"));
                    rollbar.error("An error occurred updating event evidence", creationError);
                }
              });
            };

            return (
              <React.StrictMode>
                <Row>
                  <Col md={2} mdOffset={5}>
                    <ButtonToolbar>
                      <Can do="backend_api_resolvers_event__do_create_event">
                        <Button onClick={openNewEventModal}>
                          <Glyphicon glyph="plus" />&nbsp;{translate.t("project.events.new")}
                        </Button>
                      </Can>
                    </ButtonToolbar>
                  </Col>
                </Row>
                <Modal
                  footer={<div />}
                  headerTitle={translate.t("project.events.new")}
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

                        createEvent({
                          variables: {
                            projectName,
                            ...values,
                            accessibility: selectedAccessibility,
                            affectedComponents: selectedComponents,
                            file: _.isEmpty(values.file) ? undefined : (values.file as FileList)[0],
                            image: _.isEmpty(values.image) ? undefined : (values.image as FileList)[0],
                          },
                        })
                          .catch();
                      };

                      return (
                        <GenericForm name="newEvent" onSubmit={handleSubmit}>
                          {({ pristine }: InjectedFormProps): JSX.Element => (
                            <React.Fragment>
                              <Row>
                                <Col md={5}>
                                  <FormGroup>
                                    <ControlLabel>{translate.t("project.events.form.date")}</ControlLabel>
                                    <Field
                                      component={dateTimeField}
                                      name="eventDate"
                                      validate={[required, validDatetime, dateTimeBeforeToday]}
                                    />
                                  </FormGroup>
                                </Col>
                                <Col md={7}>
                                  <FormGroup>
                                    <ControlLabel>{translate.t("project.events.form.type.title")}</ControlLabel>
                                    <Field component={dropdownField} name="eventType" validate={required}>
                                      <option value="" selected={true} />
                                      <option value="AUTHORIZATION_SPECIAL_ATTACK">
                                        {translate.t("project.events.form.type.special_attack")}
                                      </option>
                                      <option value="CLIENT_APPROVES_CHANGE_TOE">
                                        {translate.t("project.events.form.type.toe_change")}
                                      </option>
                                      <option value="CLIENT_CANCELS_PROJECT_MILESTONE">
                                        {translate.t("project.events.form.type.cancel_project")}
                                      </option>
                                      <option value="CLIENT_DETECTS_ATTACK">
                                        {translate.t("project.events.form.type.detects_attack")}
                                      </option>
                                      <option value="CLIENT_EXPLICITLY_SUSPENDS_PROJECT">
                                        {translate.t("project.events.form.type.suspends_project")}
                                      </option>
                                      <option value="HIGH_AVAILABILITY_APPROVAL">
                                        {translate.t("project.events.form.type.high_availability")}
                                      </option>
                                      <option value="INCORRECT_MISSING_SUPPLIES">
                                        {translate.t("project.events.form.type.missing_supplies")}
                                      </option>
                                      <option value="TOE_DIFFERS_APPROVED">
                                        {translate.t("project.events.form.type.toe_differs")}
                                      </option>
                                      <option value="OTHER">
                                        {translate.t("project.events.form.other")}
                                      </option>
                                    </Field>
                                  </FormGroup>
                                </Col>
                              </Row>
                              <Row>
                                <Col md={6}>
                                  <FormGroup>
                                    <ControlLabel>{translate.t("project.events.form.context.title")}</ControlLabel>
                                    <Field component={dropdownField} name="context" validate={required}>
                                      <option value="" selected={true} />
                                      <option value="CLIENT">
                                        {translate.t("project.events.form.context.client")}
                                      </option>
                                      <option value="FLUID">
                                        {translate.t("project.events.form.context.fluid")}
                                      </option>
                                      <option value="PLANNING">
                                        {translate.t("project.events.form.context.planning")}
                                      </option>
                                      <option value="TELECOMMUTING">
                                        {translate.t("project.events.form.context.telecommuting")}
                                      </option>
                                      <option value="OTHER">
                                        {translate.t("project.events.form.other")}
                                      </option>
                                    </Field>
                                  </FormGroup>
                                </Col>
                                <Col md={6}>
                                  <FormGroup>
                                    <ControlLabel>
                                      {translate.t("project.events.form.accessibility.title")}
                                    </ControlLabel>
                                    <FormSection name="accessibility">
                                      <Field component={checkboxField} name="environment" validate={someRequired}>
                                        {translate.t("project.events.form.accessibility.environment")}
                                      </Field>
                                      <Field component={checkboxField} name="repository" validate={someRequired}>
                                        {translate.t("project.events.form.accessibility.repository")}
                                      </Field>
                                    </FormSection>
                                  </FormGroup>
                                </Col>
                              </Row>
                              {eventType === "INCORRECT_MISSING_SUPPLIES" ?
                                <Row>
                                  <Col md={6}>
                                    <FormGroup>
                                      <ControlLabel>{translate.t("project.events.form.blocking_hours")}</ControlLabel>
                                      <Field
                                        component={textField}
                                        name="blockingHours"
                                        type="number"
                                        validate={[numeric, required]}
                                      />
                                    </FormGroup>
                                  </Col>
                                  <Col md={6}>
                                    <FormGroup>
                                      <ControlLabel>
                                        {translate.t("project.events.form.components.title")}
                                      </ControlLabel>
                                      <FormSection name="affectedComponents">
                                        <Field component={checkboxField} name="FLUID_STATION" validate={someRequired}>
                                          {translate.t("project.events.form.components.fluid_station")}
                                        </Field>
                                        <Field component={checkboxField} name="CLIENT_STATION" validate={someRequired}>
                                          {translate.t("project.events.form.components.client_station")}
                                        </Field>
                                        <Field component={checkboxField} name="TOE_EXCLUSSION" validate={someRequired}>
                                          {translate.t("project.events.form.components.toe_exclussion")}
                                        </Field>
                                        <Field component={checkboxField} name="DOCUMENTATION" validate={someRequired}>
                                          {translate.t("project.events.form.components.documentation")}
                                        </Field>
                                        <Field
                                          component={checkboxField}
                                          name="LOCAL_CONNECTION"
                                          validate={someRequired}
                                        >
                                          {translate.t("project.events.form.components.local_conn")}
                                        </Field>
                                        <Field
                                          component={checkboxField}
                                          name="INTERNET_CONNECTION"
                                          validate={someRequired}
                                        >
                                          {translate.t("project.events.form.components.internet_conn")}
                                        </Field>
                                        <Field component={checkboxField} name="VPN_CONNECTION" validate={someRequired}>
                                          {translate.t("project.events.form.components.vpn_conn")}
                                        </Field>
                                        <Field component={checkboxField} name="TOE_LOCATION" validate={someRequired}>
                                          {translate.t("project.events.form.components.toe_location")}
                                        </Field>
                                        <Field component={checkboxField} name="TOE_CREDENTIALS" validate={someRequired}>
                                          {translate.t("project.events.form.components.toe_credentials")}
                                        </Field>
                                        <Field component={checkboxField} name="TOE_PRIVILEGES" validate={someRequired}>
                                          {translate.t("project.events.form.components.toe_privileges")}
                                        </Field>
                                        <Field component={checkboxField} name="TEST_DATA" validate={someRequired}>
                                          {translate.t("project.events.form.components.test_data")}
                                        </Field>
                                        <Field component={checkboxField} name="TOE_UNSTABLE" validate={someRequired}>
                                          {translate.t("project.events.form.components.toe_unstability")}
                                        </Field>
                                        <Field
                                          component={checkboxField}
                                          name="TOE_UNACCESSIBLE"
                                          validate={someRequired}
                                        >
                                          {translate.t("project.events.form.components.toe_unaccessible")}
                                        </Field>
                                        <Field component={checkboxField} name="TOE_UNAVAILABLE" validate={someRequired}>
                                          {translate.t("project.events.form.components.toe_unavailable")}
                                        </Field>
                                        <Field component={checkboxField} name="TOE_ALTERATION" validate={someRequired}>
                                          {translate.t("project.events.form.components.toe_alteration")}
                                        </Field>
                                        <Field component={checkboxField} name="SOURCE_CODE" validate={someRequired}>
                                          {translate.t("project.events.form.components.source_code")}
                                        </Field>
                                        <Field component={checkboxField} name="COMPILE_ERROR" validate={someRequired}>
                                          {translate.t("project.events.form.components.compile_error")}
                                        </Field>
                                        <Field component={checkboxField} name="OTHER" validate={someRequired}>
                                          {translate.t("project.events.form.other")}
                                        </Field>
                                      </FormSection>
                                    </FormGroup>
                                  </Col>
                                </Row>
                                : undefined}
                              <Row>
                                <Col md={12}>
                                  <FormGroup>
                                    <ControlLabel>{translate.t("project.events.form.details")}</ControlLabel>
                                    <Field
                                      className={globalStyle.noResize}
                                      component={textAreaField}
                                      name="detail"
                                      validate={required}
                                    />
                                  </FormGroup>
                                </Col>
                              </Row>
                              <Row>
                                <Col md={5}>
                                  <FormGroup>
                                    <ControlLabel>
                                      {translate.t("project.events.form.action_before.title")}
                                    </ControlLabel>
                                    <Field component={dropdownField} name="actionBeforeBlocking" validate={required}>
                                      <option value="" selected={true} />
                                      <option value="DOCUMENT_PROJECT">
                                        {translate.t("project.events.form.action_before.document")}
                                      </option>
                                      <option value="TEST_OTHER_PART_TOE">
                                        {translate.t("project.events.form.action_before.test_other")}
                                      </option>
                                      <option value="NONE">
                                        {translate.t("project.events.form.none")}
                                      </option>
                                      <option value="OTHER">
                                        {translate.t("project.events.form.other")}
                                      </option>
                                    </Field>
                                  </FormGroup>
                                </Col>
                                <Col md={7}>
                                  <FormGroup>
                                    <ControlLabel>{translate.t("project.events.form.action_after.title")}</ControlLabel>
                                    <Field component={dropdownField} name="actionAfterBlocking" validate={required}>
                                      <option value="" selected={true} />
                                      <option value="EXECUTE_OTHER_PROJECT_SAME_CLIENT">
                                        {translate.t("project.events.form.action_after.other_same")}
                                      </option>
                                      <option value="EXECUTE_OTHER_PROJECT_OTHER_CLIENT">
                                        {translate.t("project.events.form.action_after.other_other")}
                                      </option>
                                      <option value="TRAINING">
                                        {translate.t("project.events.form.action_after.training")}
                                      </option>
                                      <option value="NONE">
                                        {translate.t("project.events.form.none")}
                                      </option>
                                      <option value="OTHER">
                                        {translate.t("project.events.form.other")}
                                      </option>
                                    </Field>
                                  </FormGroup>
                                </Col>
                              </Row>
                              <Row>
                                <Col md={6}>
                                  <FormGroup>
                                    <ControlLabel>{translate.t("project.events.form.evidence")}</ControlLabel>
                                    <Field
                                      accept="image/gif,image/png"
                                      component={fileInputField}
                                      id="image"
                                      name="image"
                                      validate={[validEvidenceImage, maxFileSize]}
                                    />
                                  </FormGroup>
                                </Col>
                                <Col md={6}>
                                  <FormGroup>
                                    <ControlLabel>{translate.t("project.events.form.evidence_file")}</ControlLabel>
                                    <Field
                                      accept="application/pdf,application/zip,text/csv,text/plain"
                                      component={fileInputField}
                                      id="file"
                                      name="file"
                                      validate={[validEventFile, maxFileSize]}
                                    />
                                  </FormGroup>
                                </Col>
                              </Row>
                              <ButtonToolbar className="pull-right">
                                <Button bsStyle="success" onClick={closeNewEventModal}>
                                  {translate.t("confirmmodal.cancel")}
                                </Button>
                                <Button bsStyle="success" type="submit" disabled={pristine || mtResult.loading}>
                                  {translate.t("confirmmodal.proceed")}
                                </Button>
                              </ButtonToolbar>
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
                  remote={false}
                  rowEvents={{ onClick: goToEvent }}
                  title=""
                />
              </React.StrictMode>
            );
          } else { return <React.Fragment />; }
        }}
    </Query>
  );
};

export { projectEventsView as ProjectEventsView };
