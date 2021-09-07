import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import type { Moment } from "moment";
import React, { useCallback, useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { selectFilter } from "react-bootstrap-table2-filter";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";
import type { Validator } from "redux-form";
import type { ConfigurableValidator } from "revalidate";
import type { BaseSchema } from "yup";
import { array, lazy, object } from "yup";

import { handleCreationError, handleFileListUpload } from "./helpers";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Modal } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import { pointStatusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import {
  ADD_EVENT_MUTATION,
  GET_EVENTS,
} from "scenes/Dashboard/containers/GroupEventsView/queries";
import { formatEvents } from "scenes/Dashboard/containers/GroupEventsView/utils";
import globalStyle from "styles/global.css";
import {
  ButtonToolbar,
  ButtonToolbarCenter,
  Col100,
  Col50,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { castEventType } from "utils/formatHelpers";
import {
  FormikCheckbox,
  FormikDateTime,
  FormikDropdown,
  FormikFileInput,
  FormikText,
  FormikTextArea,
} from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import {
  composeValidators,
  dateTimeBeforeToday,
  isValidFileSize,
  maxLength,
  numeric,
  required,
  validDatetime,
  validEventFile,
  validEvidenceImage,
  validTextField,
} from "utils/validations";

interface IFormValues {
  eventDate: Moment;
  blockingHours: number;
  context: string;
  accessibility: string[];
  affectedComponents: string[];
  eventType: string;
  detail: string;
  actionBeforeBlocking: string;
  actionAfterBlocking: string;
  file?: FileList;
  image?: FileList;
}

interface IEventsDataset {
  group: {
    events: {
      accessibility: string;
      actionBeforeBlocking: string;
      affectedComponents: string;
      closingDate: string;
      detail: string;
      eventDate: string;
      eventStatus: string;
      eventType: string;
      id: string;
      groupName: string;
    }[];
  };
}

const MAX_EVENT_DETAILS_LENGTH = 300;
const maxEventDetailsLength: ConfigurableValidator = maxLength(
  MAX_EVENT_DETAILS_LENGTH
);

const GroupEventsView: React.FC = (): JSX.Element => {
  const { push } = useHistory();
  const { groupName } = useParams<{ groupName: string }>();
  const { url } = useRouteMatch();

  const selectOptionsStatus = {
    Solved: "Solved",
    Unsolved: "Unsolved",
  };
  const selectOptionType = {
    [translate.t("group.events.form.type.specialAttack")]: translate.t(
      castEventType("AUTHORIZATION_SPECIAL_ATTACK")
    ),
    [translate.t("group.events.form.type.toeChange")]: translate.t(
      castEventType("CLIENT_APPROVES_CHANGE_TOE")
    ),
    [translate.t(castEventType("CLIENT_DETECTS_ATTACK"))]: translate.t(
      castEventType("CLIENT_DETECTS_ATTACK")
    ),
    [translate.t("group.events.form.type.highAvailability")]: translate.t(
      castEventType("HIGH_AVAILABILITY_APPROVAL")
    ),
    [translate.t("group.events.form.type.missingSupplies")]: translate.t(
      castEventType("INCORRECT_MISSING_SUPPLIES")
    ),
    [translate.t("group.events.form.type.toeDiffers")]: translate.t(
      castEventType("TOE_DIFFERS_APPROVED")
    ),
    [translate.t("group.events.form.other")]: translate.t(
      castEventType("OTHER")
    ),
  };
  const [optionType, setOptionType] = useState(selectOptionType);

  const onSortState: (dataField: string, order: SortOrder) => void = (
    dataField: string,
    order: SortOrder
  ): void => {
    const newSorted = { dataField, order };
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
      header: translate.t("searchFindings.tabEvents.id"),
      onSort: onSortState,
      width: "8%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "eventDate",
      header: translate.t("searchFindings.tabEvents.date"),
      onSort: onSortState,
      width: "10%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "detail",
      header: translate.t("searchFindings.tabEvents.description"),
      onSort: onSortState,
      width: "50%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "accessibility",
      header: translate.t("searchFindings.tabEvents.accessibility"),
      onSort: onSortState,
      width: "50%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "affectedComponents",
      header: translate.t("searchFindings.tabEvents.affectedComponents"),
      onSort: onSortState,
      width: "50%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "actionBeforeBlocking",
      header: translate.t("searchFindings.tabEvents.actionBeforeBlocking"),
      onSort: onSortState,
      width: "50%",
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
      header: translate.t("searchFindings.tabEvents.type"),
      onSort: onSortState,
      width: "20%",
      wrapped: true,
    },
    {
      align: "left",
      dataField: "eventStatus",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "eventStatusFilter"),
        onFilter: onFilterStatus,
        options: selectOptionsStatus,
      }),
      formatter: pointStatusFormatter,
      header: translate.t("searchFindings.tabEvents.status"),
      onSort: onSortState,
      width: "90px",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "closingDate",
      header: translate.t("searchFindings.tabEvents.closingDate"),
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
          rData.group.events.map(
            (event: { eventType: string }): string => event.eventType
          )
        )
      );
      const transEventOptions = eventOptions.map((option: string): string =>
        translate.t(castEventType(option))
      );
      const filterOptions = _.pickBy(selectOptionType, (value): boolean =>
        _.includes(transEventOptions, value)
      );
      setOptionType(filterOptions);
    }
  };
  const handleQryErrors: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      Logger.warning("An error occurred loading group data", error);
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
    track("ReadEvent");
    push(`${url}/${rowInfo.id}/description`);
  };

  const [isEventModalOpen, setEventModalOpen] = useState(false);

  const openNewEventModal: () => void = useCallback((): void => {
    setEventModalOpen(true);
  }, []);

  const closeNewEventModal: () => void = useCallback((): void => {
    setEventModalOpen(false);
  }, []);

  const MAX_FILE_SIZE = 10;
  const maxFileSize: Validator = isValidFileSize(MAX_FILE_SIZE);

  const { data, refetch } = useQuery(GET_EVENTS, {
    onCompleted: handleQryResult,
    onError: handleQryErrors,
    variables: { groupName },
  });

  const handleCreationResult: (result: {
    addEvent: { success: boolean };
  }) => void = (result: { addEvent: { success: boolean } }): void => {
    if (result.addEvent.success) {
      closeNewEventModal();
      msgSuccess(
        translate.t("group.events.successCreate"),
        translate.t("group.events.titleSuccess")
      );
      void refetch();
    }
  };

  const [addEvent, mtResult] = useMutation(ADD_EVENT_MUTATION, {
    onCompleted: handleCreationResult,
    onError: handleCreationError,
  });

  const handleSubmit: (values: IFormValues) => void = useCallback(
    (values: IFormValues): void => {
      const selectedAccessibility: string[] = values.accessibility.map(
        (element: string): string => element.toUpperCase()
      );

      const selectedComponents: string[] | undefined = _.isUndefined(
        values.affectedComponents
      )
        ? undefined
        : values.affectedComponents.map((component: string): string =>
            component.toUpperCase()
          );

      void addEvent({
        variables: {
          groupName,
          ...values,
          accessibility: selectedAccessibility,
          affectedComponents: selectedComponents,
          blockingHours: String(values.blockingHours),
          file: handleFileListUpload(values.file),
          image: handleFileListUpload(values.image),
        },
      });
    },
    [addEvent, groupName]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const initialValues = {
    accessibility: [],
    actionAfterBlocking: "",
    actionBeforeBlocking: "",
    affectedComponents: [],
    blockingHours: "" as unknown as number,
    context: "",
    detail: "",
    eventDate: undefined as unknown as Moment,
    eventType: "",
    file: undefined as unknown as FileList,
    image: undefined as unknown as FileList,
  };

  return (
    <React.StrictMode>
      <Row>
        <Col100>
          <ButtonToolbarCenter>
            <Can do={"api_mutations_add_event_mutate"}>
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
        onEsc={closeNewEventModal}
        open={isEventModalOpen}
      >
        <Formik
          initialValues={initialValues}
          name={"newEvent"}
          onSubmit={handleSubmit}
          validationSchema={lazy(
            (): BaseSchema =>
              object().shape({
                accessibility: array().min(
                  1,
                  translate.t("validations.someRequired")
                ),
                affectedComponents: array().when("eventType", {
                  is: "INCORRECT_MISSING_SUPPLIES",
                  otherwise: array().notRequired(),
                  then: array().min(1, translate.t("validations.someRequired")),
                }),
              })
          )}
        >
          {({ dirty, values }): JSX.Element => (
            <Form>
              <Row>
                <Col50>
                  <FormGroup>
                    <ControlLabel>
                      {translate.t("group.events.form.date")}
                    </ControlLabel>
                    <Field
                      component={FormikDateTime}
                      name={"eventDate"}
                      validate={composeValidators([
                        required,
                        validDatetime,
                        dateTimeBeforeToday,
                      ])}
                    />
                  </FormGroup>
                </Col50>
                <Col50>
                  <FormGroup>
                    <ControlLabel>
                      {translate.t("group.events.form.type.title")}
                    </ControlLabel>
                    <Field
                      component={FormikDropdown}
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
                      component={FormikDropdown}
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
                    <br />
                    <Field
                      component={FormikCheckbox}
                      label={translate.t(
                        "group.events.form.accessibility.environment"
                      )}
                      name={"accessibility"}
                      type={"checkbox"}
                      value={"environment"}
                    />
                    <Field
                      component={FormikCheckbox}
                      label={translate.t(
                        "group.events.form.accessibility.repository"
                      )}
                      name={"accessibility"}
                      type={"checkbox"}
                      value={"repository"}
                    />
                  </FormGroup>
                </Col50>
              </Row>
              {values.eventType === "INCORRECT_MISSING_SUPPLIES" ? (
                <Row>
                  <Col50>
                    <FormGroup>
                      <ControlLabel>
                        {translate.t("group.events.form.blockingHours")}
                      </ControlLabel>
                      <Field
                        component={FormikText}
                        name={"blockingHours"}
                        type={"number"}
                        validate={composeValidators([numeric, required])}
                      />
                    </FormGroup>
                  </Col50>
                  <Col50>
                    <FormGroup>
                      <ControlLabel>
                        {translate.t("group.events.form.components.title")}
                      </ControlLabel>
                      <br />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t(
                          "group.events.form.components.fluidStation"
                        )}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"FLUID_STATION"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t(
                          "group.events.form.components.clientStation"
                        )}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"CLIENT_STATION"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t(
                          "group.events.form.components.toeExclusion"
                        )}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"TOE_EXCLUSSION"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t(
                          "group.events.form.components.documentation"
                        )}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"DOCUMENTATION"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t(
                          "group.events.form.components.localConn"
                        )}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"LOCAL_CONNECTION"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t(
                          "group.events.form.components.internetConn"
                        )}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"INTERNET_CONNECTION"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t(
                          "group.events.form.components.vpnConn"
                        )}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"VPN_CONNECTION"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t(
                          "group.events.form.components.toeLocation"
                        )}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"TOE_LOCATION"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t(
                          "group.events.form.components.toeCredentials"
                        )}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"TOE_CREDENTIALS"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t(
                          "group.events.form.components.toePrivileges"
                        )}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"TOE_PRIVILEGES"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t(
                          "group.events.form.components.testData"
                        )}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"TEST_DATA"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t(
                          "group.events.form.components.toeUnstability"
                        )}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"TOE_UNSTABLE"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t(
                          "group.events.form.components.toeUnaccessible"
                        )}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"TOE_UNACCESSIBLE"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t(
                          "group.events.form.components.toeUnavailable"
                        )}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"TOE_UNAVAILABLE"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t(
                          "group.events.form.components.toeAlteration"
                        )}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"TOE_ALTERATION"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t(
                          "group.events.form.components.sourceCode"
                        )}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"SOURCE_CODE"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t(
                          "group.events.form.components.compileError"
                        )}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"COMPILE_ERROR"}
                      />
                      <Field
                        component={FormikCheckbox}
                        label={translate.t("group.events.form.other")}
                        name={"affectedComponents"}
                        type={"checkbox"}
                        value={"OTHER"}
                      />
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
                      component={FormikTextArea}
                      name={"detail"}
                      validate={composeValidators([
                        required,
                        validTextField,
                        maxEventDetailsLength,
                      ])}
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
                      component={FormikDropdown}
                      name={"actionBeforeBlocking"}
                      validate={required}
                    >
                      <option selected={true} value={""} />
                      <option value={"DOCUMENT_GROUP"}>
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
                      component={FormikDropdown}
                      name={"actionAfterBlocking"}
                      validate={required}
                    >
                      <option selected={true} value={""} />
                      <option value={"EXECUTE_OTHER_GROUP_SAME_CLIENT"}>
                        {translate.t("group.events.form.actionAfter.otherSame")}
                      </option>
                      <option value={"EXECUTE_OTHER_GROUP_OTHER_CLIENT"}>
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
                      component={FormikFileInput}
                      id={"image"}
                      name={"image"}
                      validate={composeValidators([
                        validEvidenceImage,
                        maxFileSize,
                      ])}
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
                      component={FormikFileInput}
                      id={"file"}
                      name={"file"}
                      validate={composeValidators([
                        validEventFile,
                        maxFileSize,
                      ])}
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
                      disabled={!dirty || mtResult.loading}
                      type={"submit"}
                    >
                      {translate.t("confirmmodal.proceed")}
                    </Button>
                  </ButtonToolbar>
                </Col100>
              </Row>
            </Form>
          )}
        </Formik>
      </Modal>
      <p>{translate.t("searchFindings.tabEvents.tableAdvice")}</p>
      <DataTableNext
        bordered={true}
        dataset={formatEvents(data.group.events)}
        defaultSorted={JSON.parse(_.get(sessionStorage, "eventSort", "{}"))}
        exportCsv={true}
        headers={tableHeaders}
        id={"tblEvents"}
        pageSize={10}
        rowEvents={{ onClick: goToEvent }}
        search={true}
      />
    </React.StrictMode>
  );
};

export { GroupEventsView };
