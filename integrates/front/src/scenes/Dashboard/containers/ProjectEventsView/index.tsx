import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { Can } from "utils/authz/Can";
import type { ConfigurableValidator } from "revalidate";
import { DataTableNext } from "components/DataTableNext";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { GraphQLError } from "graphql";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Logger } from "utils/logger";
import { Modal } from "components/Modal";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import _ from "lodash";
import { castEventType } from "utils/formatHelpers";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { formatEvents } from "scenes/Dashboard/containers/ProjectEventsView/utils";
import globalStyle from "styles/global.css";
import mixpanel from "mixpanel-browser";
import { selectFilter } from "react-bootstrap-table2-filter";
import { statusFormatter } from "components/DataTableNext/formatters";
import { translate } from "utils/translations/translate";
import { useSelector } from "react-redux";
import {
  ButtonToolbar,
  ButtonToolbarCenter,
  Col100,
  Col50,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import {
  CREATE_EVENT_MUTATION,
  GET_EVENTS,
} from "scenes/Dashboard/containers/ProjectEventsView/queries";
import {
  Checkbox,
  DateTime,
  Dropdown,
  FileInput,
  Text,
  TextArea,
} from "utils/forms/fields";
import { Field, FormSection, formValueSelector } from "redux-form";
import type { InjectedFormProps, Validator } from "redux-form";
import {
  dateTimeBeforeToday,
  isValidFileSize,
  maxLength,
  numeric,
  required,
  someRequired,
  validDatetime,
  validEventFile,
  validEvidenceImage,
  validTextField,
} from "utils/validations";
import { msgError, msgSuccess } from "utils/notifications";
import { useHistory, useParams } from "react-router";
import { useMutation, useQuery } from "@apollo/react-hooks";

interface IFormValues {
  accessibility: Record<string, boolean>;
  affectedComponents: Record<string, boolean>;
  file?: FileList;
  image?: FileList;
}

interface IEventsDataset {
  project: {
    events: {
      closingDate: string;
      detail: string;
      eventDate: string;
      eventStatus: string;
      eventType: string;
      id: string;
      projectName: string;
    }[];
  };
}

const MAX_EVENT_DETAILS_LENGTH = 300;
const maxEventDetailsLength: ConfigurableValidator = maxLength(
  MAX_EVENT_DETAILS_LENGTH
);

const ProjectEventsView: React.FC = (): JSX.Element => {
  const { push } = useHistory();
  const { projectName } = useParams<{ projectName: string }>();

  const selectOptionsStatus: optionSelectFilterProps[] = [
    { label: "Solved", value: "Solved" },
    { label: "Unsolved", value: "Unsolved" },
  ];
  const selectOptionType: optionSelectFilterProps[] = [
    {
      label: translate.t("group.events.form.type.specialAttack"),
      value: translate.t(castEventType("AUTHORIZATION_SPECIAL_ATTACK")),
    },
    {
      label: translate.t("group.events.form.type.toeChange"),
      value: translate.t(castEventType("CLIENT_APPROVES_CHANGE_TOE")),
    },
    {
      label: translate.t(castEventType("CLIENT_DETECTS_ATTACK")),
      value: translate.t(castEventType("CLIENT_DETECTS_ATTACK")),
    },
    {
      label: translate.t("group.events.form.type.highAvailability"),
      value: translate.t(castEventType("HIGH_AVAILABILITY_APPROVAL")),
    },
    {
      label: translate.t("group.events.form.type.missingSupplies"),
      value: translate.t(castEventType("INCORRECT_MISSING_SUPPLIES")),
    },
    {
      label: translate.t("group.events.form.type.toeDiffers"),
      value: translate.t(castEventType("TOE_DIFFERS_APPROVED")),
    },
    {
      label: translate.t("group.events.form.other"),
      value: translate.t(castEventType("OTHER")),
    },
  ];
  const [optionType, setOptionType] = React.useState(selectOptionType);

  const onSortState: (dataField: string, order: SortOrder) => void = (
    dataField: string,
    order: SortOrder
  ): void => {
    const newSorted: Sorted = { dataField, order };
    sessionStorage.setItem("eventSort", JSON.stringify(newSorted));
  };
  const onFilterStatus: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("eventStatusFilter", filterVal);
  };
  const onFilterType: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("eventTypeFilter", filterVal);
  };

  const tableHeaders: IHeaderConfig[] = [
    {
      align: "center",
      dataField: "id",
      header: translate.t("search_findings.tabEvents.id"),
      onSort: onSortState,
      width: "8%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "eventDate",
      header: translate.t("search_findings.tabEvents.date"),
      onSort: onSortState,
      width: "10%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "detail",
      header: translate.t("search_findings.tabEvents.description"),
      onSort: onSortState,
      width: "35%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "eventType",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "eventTypeFilter"),
        onFilter: onFilterType,
        options: optionType,
      }),
      header: translate.t("search_findings.tabEvents.type"),
      onSort: onSortState,
      width: "18%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "eventStatus",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "eventStatusFilter"),
        onFilter: onFilterStatus,
        options: selectOptionsStatus,
      }),
      formatter: statusFormatter,
      header: translate.t("search_findings.tabEvents.status"),
      onSort: onSortState,
      width: "16%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "closingDate",
      header: translate.t("search_findings.tabEvents.closingDate"),
      onSort: onSortState,
      width: "13%",
      wrapped: true,
    },
  ];

  const handleQryResult: (rData: IEventsDataset) => void = (
    rData: IEventsDataset
  ): void => {
    if (!_.isUndefined(rData)) {
      const eventOptions: string[] = Array.from(
        new Set(
          rData.project.events.map(
            (event: { eventType: string }): string => event.eventType
          )
        )
      );
      const transEventOptions = eventOptions.map((option: string): string =>
        translate.t(castEventType(option))
      );
      const filterOptions: optionSelectFilterProps[] = selectOptionType.filter(
        (option: optionSelectFilterProps): boolean =>
          _.includes(transEventOptions, option.value)
      );
      setOptionType(filterOptions);
    }
  };
  const handleQryErrors: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      Logger.warning("An error occurred loading project data", error);
      msgError(translate.t("groupAlerts.errorTextsad"));
    });
  };

  const goToEvent: (
    event: React.FormEvent<HTMLButtonElement>,
    rowInfo: { id: string }
  ) => void = (
    _0: React.FormEvent<HTMLButtonElement>,
    rowInfo: { id: string }
  ): void => {
    mixpanel.track("ReadEvent");
    push(`/groups/${projectName}/events/${rowInfo.id}/description`);
  };

  const [isEventModalOpen, setEventModalOpen] = React.useState(false);

  const openNewEventModal: () => void = React.useCallback((): void => {
    setEventModalOpen(true);
  }, []);

  const closeNewEventModal: () => void = React.useCallback((): void => {
    setEventModalOpen(false);
  }, []);

  // eslint-disable-next-line @typescript-eslint/ban-types, fp/no-rest-parameters -- Needed for compatibility with redux library
  const selector: (state: {}, ...field: string[]) => string = formValueSelector(
    "newEvent"
  );
  // eslint-disable-next-line @typescript-eslint/ban-types
  const eventType: string = useSelector((state: {}): string =>
    selector(state, "eventType")
  );

  const MAX_FILE_SIZE = 10;
  const maxFileSize: Validator = isValidFileSize(MAX_FILE_SIZE);

  const { data, refetch } = useQuery(GET_EVENTS, {
    onCompleted: handleQryResult,
    onError: handleQryErrors,
    variables: { projectName },
  });

  const handleCreationResult: (result: {
    createEvent: { success: boolean };
  }) => void = (result: { createEvent: { success: boolean } }): void => {
    if (result.createEvent.success) {
      closeNewEventModal();
      msgSuccess(
        translate.t("group.events.successCreate"),
        translate.t("group.events.titleSuccess")
      );
      void refetch();
    }
  };

  const handleCreationError: (creationError: ApolloError) => void = (
    creationError: ApolloError
  ): void => {
    creationError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
      switch (message) {
        case "Exception - Invalid File Size":
          msgError(translate.t("validations.fileSize", { count: 10 }));
          break;
        case "Exception - Invalid File Type: EVENT_IMAGE":
          msgError(translate.t("group.events.form.wrongImageType"));
          break;
        case "Exception - Invalid File Type: EVENT_FILE":
          msgError(translate.t("group.events.form.wrongFileType"));
          break;
        default:
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred updating event evidence",
            creationError
          );
      }
    });
  };

  const [createEvent, mtResult] = useMutation(CREATE_EVENT_MUTATION, {
    onCompleted: handleCreationResult,
    onError: handleCreationError,
  });

  const handleSubmit: (values: IFormValues) => void = React.useCallback(
    (values: IFormValues): void => {
      const selectedAccessibility: string[] = Object.keys(values.accessibility)
        .filter((key: string): boolean => values.accessibility[key])
        .map((key: string): string => key.toUpperCase());

      const selectedComponents: string[] | undefined = _.isUndefined(
        values.affectedComponents
      )
        ? undefined
        : Object.keys(values.affectedComponents)
            .filter((key: string): boolean => values.affectedComponents[key])
            .map((key: string): string => key.toUpperCase());

      void createEvent({
        variables: {
          projectName,
          ...values,
          accessibility: selectedAccessibility,
          affectedComponents: selectedComponents,
          file: _.isEmpty(values.file)
            ? undefined
            : (values.file as FileList)[0],
          image: _.isEmpty(values.image)
            ? undefined
            : (values.image as FileList)[0],
        },
      });
    },
    [createEvent, projectName]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <Row>
        <Col100>
          <ButtonToolbarCenter>
            <Can do={"backend_api_mutations_create_event_mutate"}>
              <TooltipWrapper
                id={"group.events.btn.tooltip.id"}
                message={translate.t("group.events.btn.tooltip")}
              >
                <Button onClick={openNewEventModal}>
                  <FontAwesomeIcon icon={faPlus} />
                  &nbsp;{translate.t("group.events.btn.text")}
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
        <GenericForm name={"newEvent"} onSubmit={handleSubmit}>
          {({ pristine }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              <Row>
                <Col50>
                  <FormGroup>
                    <ControlLabel>
                      {translate.t("group.events.form.date")}
                    </ControlLabel>
                    <Field
                      component={DateTime}
                      name={"eventDate"}
                      validate={[required, validDatetime, dateTimeBeforeToday]}
                    />
                  </FormGroup>
                </Col50>
                <Col50>
                  <FormGroup>
                    <ControlLabel>
                      {translate.t("group.events.form.type.title")}
                    </ControlLabel>
                    <Field
                      component={Dropdown}
                      name={"eventType"}
                      validate={required}
                    >
                      <option selected={true} value={""} />
                      <option value={"AUTHORIZATION_SPECIAL_ATTACK"}>
                        {translate.t("group.events.form.type.specialAttack")}
                      </option>
                      <option value={"CLIENT_APPROVES_CHANGE_TOE"}>
                        {translate.t("group.events.form.type.toeChange")}
                      </option>
                      <option value={"CLIENT_DETECTS_ATTACK"}>
                        {translate.t("group.events.form.type.detectsAttack")}
                      </option>
                      <option value={"HIGH_AVAILABILITY_APPROVAL"}>
                        {translate.t("group.events.form.type.highAvailability")}
                      </option>
                      <option value={"INCORRECT_MISSING_SUPPLIES"}>
                        {translate.t("group.events.form.type.missingSupplies")}
                      </option>
                      <option value={"TOE_DIFFERS_APPROVED"}>
                        {translate.t("group.events.form.type.toeDiffers")}
                      </option>
                      <option value={"OTHER"}>
                        {translate.t("group.events.form.other")}
                      </option>
                    </Field>
                  </FormGroup>
                </Col50>
              </Row>
              <Row>
                <Col50>
                  <FormGroup>
                    <ControlLabel>
                      {translate.t("group.events.form.context.title")}
                    </ControlLabel>
                    <Field
                      component={Dropdown}
                      name={"context"}
                      validate={required}
                    >
                      <option selected={true} value={""} />
                      <option value={"CLIENT"}>
                        {translate.t("group.events.form.context.client")}
                      </option>
                      <option value={"FLUID"}>
                        {translate.t("group.events.form.context.fluid")}
                      </option>
                      <option value={"PLANNING"}>
                        {translate.t("group.events.form.context.planning")}
                      </option>
                      <option value={"TELECOMMUTING"}>
                        {translate.t("group.events.form.context.telecommuting")}
                      </option>
                      <option value={"OTHER"}>
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
                    <FormSection name={"accessibility"}>
                      <Field
                        component={Checkbox}
                        name={"environment"}
                        validate={someRequired}
                      >
                        {` ${translate.t(
                          "group.events.form.accessibility.environment"
                        )}`}
                      </Field>
                      <br />
                      <Field
                        component={Checkbox}
                        name={"repository"}
                        validate={someRequired}
                      >
                        {` ${translate.t(
                          "group.events.form.accessibility.repository"
                        )}`}
                      </Field>
                    </FormSection>
                  </FormGroup>
                </Col50>
              </Row>
              {eventType === "INCORRECT_MISSING_SUPPLIES" ? (
                <Row>
                  <Col50>
                    <FormGroup>
                      <ControlLabel>
                        {translate.t("group.events.form.blockingHours")}
                      </ControlLabel>
                      <Field
                        component={Text}
                        name={"blockingHours"}
                        type={"number"}
                        validate={[numeric, required]}
                      />
                    </FormGroup>
                  </Col50>
                  <Col50>
                    <FormGroup>
                      <ControlLabel>
                        {translate.t("group.events.form.components.title")}
                      </ControlLabel>
                      <FormSection name={"affectedComponents"}>
                        <Field
                          component={Checkbox}
                          name={"FLUID_STATION"}
                          validate={someRequired}
                        >
                          {` ${translate.t(
                            "group.events.form.components.fluidStation"
                          )}`}
                        </Field>
                        <br />
                        <Field
                          component={Checkbox}
                          name={"CLIENT_STATION"}
                          validate={someRequired}
                        >
                          {` ${translate.t(
                            "group.events.form.components.clientStation"
                          )}`}
                        </Field>
                        <br />
                        <Field
                          component={Checkbox}
                          name={"TOE_EXCLUSSION"}
                          validate={someRequired}
                        >
                          {` ${translate.t(
                            "group.events.form.components.toeExclusion"
                          )}`}
                        </Field>
                        <br />
                        <Field
                          component={Checkbox}
                          name={"DOCUMENTATION"}
                          validate={someRequired}
                        >
                          {` ${translate.t(
                            "group.events.form.components.documentation"
                          )}`}
                        </Field>
                        <br />
                        <Field
                          component={Checkbox}
                          name={"LOCAL_CONNECTION"}
                          validate={someRequired}
                        >
                          {` ${translate.t(
                            "group.events.form.components.localConn"
                          )}`}
                        </Field>
                        <br />
                        <Field
                          component={Checkbox}
                          name={"INTERNET_CONNECTION"}
                          validate={someRequired}
                        >
                          {` ${translate.t(
                            "group.events.form.components.internetConn"
                          )}`}
                        </Field>
                        <br />
                        <Field
                          component={Checkbox}
                          name={"VPN_CONNECTION"}
                          validate={someRequired}
                        >
                          {` ${translate.t(
                            "group.events.form.components.vpnConn"
                          )}`}
                        </Field>
                        <br />
                        <Field
                          component={Checkbox}
                          name={"TOE_LOCATION"}
                          validate={someRequired}
                        >
                          {` ${translate.t(
                            "group.events.form.components.toeLocation"
                          )}`}
                        </Field>
                        <br />
                        <Field
                          component={Checkbox}
                          name={"TOE_CREDENTIALS"}
                          validate={someRequired}
                        >
                          {` ${translate.t(
                            "group.events.form.components.toeCredentials"
                          )}`}
                        </Field>
                        <br />
                        <Field
                          component={Checkbox}
                          name={"TOE_PRIVILEGES"}
                          validate={someRequired}
                        >
                          {` ${translate.t(
                            "group.events.form.components.toePrivileges"
                          )}`}
                        </Field>
                        <br />
                        <Field
                          component={Checkbox}
                          name={"TEST_DATA"}
                          validate={someRequired}
                        >
                          {` ${translate.t(
                            "group.events.form.components.testData"
                          )}`}
                        </Field>
                        <br />
                        <Field
                          component={Checkbox}
                          name={"TOE_UNSTABLE"}
                          validate={someRequired}
                        >
                          {` ${translate.t(
                            "group.events.form.components.toeUnstability"
                          )}`}
                        </Field>
                        <br />
                        <Field
                          component={Checkbox}
                          name={"TOE_UNACCESSIBLE"}
                          validate={someRequired}
                        >
                          {` ${translate.t(
                            "group.events.form.components.toeUnaccessible"
                          )}`}
                        </Field>
                        <br />
                        <Field
                          component={Checkbox}
                          name={"TOE_UNAVAILABLE"}
                          validate={someRequired}
                        >
                          {` ${translate.t(
                            "group.events.form.components.toeUnavailable"
                          )}`}
                        </Field>
                        <br />
                        <Field
                          component={Checkbox}
                          name={"TOE_ALTERATION"}
                          validate={someRequired}
                        >
                          {` ${translate.t(
                            "group.events.form.components.toeAlteration"
                          )}`}
                        </Field>
                        <br />
                        <Field
                          component={Checkbox}
                          name={"SOURCE_CODE"}
                          validate={someRequired}
                        >
                          {` ${translate.t(
                            "group.events.form.components.sourceCode"
                          )}`}
                        </Field>
                        <br />
                        <Field
                          component={Checkbox}
                          name={"COMPILE_ERROR"}
                          validate={someRequired}
                        >
                          {` ${translate.t(
                            "group.events.form.components.compileError"
                          )}`}
                        </Field>
                        <br />
                        <Field
                          component={Checkbox}
                          name={"OTHER"}
                          validate={someRequired}
                        >
                          {` ${translate.t("group.events.form.other")}`}
                        </Field>
                      </FormSection>
                    </FormGroup>
                  </Col50>
                </Row>
              ) : undefined}
              <Row>
                <Col100>
                  <FormGroup>
                    <ControlLabel>
                      {translate.t("group.events.form.details")}
                    </ControlLabel>
                    <Field
                      // eslint-disable-next-line react/forbid-component-props
                      className={globalStyle.noResize}
                      component={TextArea}
                      name={"detail"}
                      validate={[
                        required,
                        validTextField,
                        maxEventDetailsLength,
                      ]}
                    />
                  </FormGroup>
                </Col100>
              </Row>
              <Row>
                <Col50>
                  <FormGroup>
                    <ControlLabel>
                      {translate.t("group.events.form.actionBefore.title")}
                    </ControlLabel>
                    <Field
                      component={Dropdown}
                      name={"actionBeforeBlocking"}
                      validate={required}
                    >
                      <option selected={true} value={""} />
                      <option value={"DOCUMENT_PROJECT"}>
                        {translate.t("group.events.form.actionBefore.document")}
                      </option>
                      <option value={"TEST_OTHER_PART_TOE"}>
                        {translate.t(
                          "group.events.form.actionBefore.testOther"
                        )}
                      </option>
                      <option value={"NONE"}>
                        {translate.t("group.events.form.none")}
                      </option>
                      <option value={"OTHER"}>
                        {translate.t("group.events.form.other")}
                      </option>
                    </Field>
                  </FormGroup>
                </Col50>
                <Col50>
                  <FormGroup>
                    <ControlLabel>
                      {translate.t("group.events.form.actionAfter.title")}
                    </ControlLabel>
                    <Field
                      component={Dropdown}
                      name={"actionAfterBlocking"}
                      validate={required}
                    >
                      <option selected={true} value={""} />
                      <option value={"EXECUTE_OTHER_PROJECT_SAME_CLIENT"}>
                        {translate.t("group.events.form.actionAfter.otherSame")}
                      </option>
                      <option value={"EXECUTE_OTHER_PROJECT_OTHER_CLIENT"}>
                        {translate.t(
                          "group.events.form.actionAfter.otherOther"
                        )}
                      </option>
                      <option value={"TRAINING"}>
                        {translate.t("group.events.form.actionAfter.training")}
                      </option>
                      <option value={"NONE"}>
                        {translate.t("group.events.form.none")}
                      </option>
                      <option value={"OTHER"}>
                        {translate.t("group.events.form.other")}
                      </option>
                    </Field>
                  </FormGroup>
                </Col50>
              </Row>
              <Row>
                <Col50>
                  <FormGroup>
                    <ControlLabel>
                      {translate.t("group.events.form.evidence")}
                    </ControlLabel>
                    <Field
                      accept={"image/gif,image/png"}
                      component={FileInput}
                      id={"image"}
                      name={"image"}
                      validate={[validEvidenceImage, maxFileSize]}
                    />
                  </FormGroup>
                </Col50>
                <Col50>
                  <FormGroup>
                    <ControlLabel>
                      {translate.t("group.events.form.evidenceFile")}
                    </ControlLabel>
                    <Field
                      accept={
                        "application/pdf,application/zip,text/csv,text/plain"
                      }
                      component={FileInput}
                      id={"file"}
                      name={"file"}
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
                    <Button
                      disabled={pristine || mtResult.loading}
                      type={"submit"}
                    >
                      {translate.t("confirmmodal.proceed")}
                    </Button>
                  </ButtonToolbar>
                </Col100>
              </Row>
            </React.Fragment>
          )}
        </GenericForm>
      </Modal>
      <p>{translate.t("search_findings.tabEvents.tableAdvice")}</p>
      <DataTableNext
        bordered={true}
        dataset={formatEvents(data.project.events)}
        defaultSorted={JSON.parse(_.get(sessionStorage, "eventSort", "{}"))}
        exportCsv={true}
        headers={tableHeaders}
        id={"tblEvents"}
        pageSize={15}
        rowEvents={{ onClick: goToEvent }}
        search={true}
      />
    </React.StrictMode>
  );
};

export { ProjectEventsView };
