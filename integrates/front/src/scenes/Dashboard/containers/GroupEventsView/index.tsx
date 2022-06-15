import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { useTranslation } from "react-i18next";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";

import type { IFormValues } from "./AddModal";
import { AddModal } from "./AddModal";
import { GET_VERIFIED_FINDING_INFO } from "./AffectedReattackAccordion/queries";
import type {
  IFinding,
  IFindingsQuery,
} from "./AffectedReattackAccordion/types";
import {
  handleCreationError,
  handleFileListUpload,
  handleRequestHoldError,
  handleRequestHoldsHelper,
} from "./helpers";
import {
  accessibilityOptions,
  afectCompsOptions,
  selectOptionType,
} from "./selectOptions";
import { UpdateAffectedModal } from "./UpdateAffectedModal";
import type { IUpdateAffectedValues } from "./UpdateAffectedModal/types";

import { Button } from "components/Button";
import { Table } from "components/Table";
import type { IFilterProps, IHeaderConfig } from "components/Table/types";
import {
  filterDateRange,
  filterSearchText,
  filterSelect,
} from "components/Table/utils";
import { TooltipWrapper } from "components/TooltipWrapper";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import {
  ADD_EVENT_MUTATION,
  GET_EVENTS,
  REQUEST_VULNS_HOLD_MUTATION,
} from "scenes/Dashboard/containers/GroupEventsView/queries";
import {
  formatEvents,
  formatReattacks,
} from "scenes/Dashboard/containers/GroupEventsView/utils";
import type { IEventConfig } from "scenes/Dashboard/containers/GroupEventsView/utils";
import { ButtonToolbar, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { castEventType } from "utils/formatHelpers";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IEventsDataset {
  group: {
    events: {
      accessibility: string[];
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

interface IFilterSet {
  accessibility: string;
  afectComps: string;
  closingDateRange: { max: string; min: string };
  dateRange: { max: string; min: string };
  status: string;
  type: string;
}

const GroupEventsView: React.FC = (): JSX.Element => {
  const { push } = useHistory();
  const { groupName } = useParams<{ groupName: string }>();
  const { url } = useRouteMatch();
  const { t } = useTranslation();

  const [optionType, setOptionType] = useState(selectOptionType);

  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("groupEventsFilters", false);

  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [filterGroupEventsTable, setFilterGroupEventsTable] =
    useStoredState<IFilterSet>(
      "filterGroupEventsSet",
      {
        accessibility: "",
        afectComps: "",
        closingDateRange: { max: "", min: "" },
        dateRange: { max: "", min: "" },
        status: "",
        type: "",
      },
      localStorage
    );

  const [columnItems, setColumnItems] = useStoredState<Record<string, boolean>>(
    "eventsTableSet",
    {
      accessibility: true,
      affectedComponents: true,
      closingDate: true,
      detail: true,
      eventDate: true,
      eventStatus: true,
      eventType: true,
      id: true,
    },
    localStorage
  );

  const handleUpdateCustomFilter: () => void = useCallback((): void => {
    setCustomFilterEnabled(!isCustomFilterEnabled);
  }, [isCustomFilterEnabled, setCustomFilterEnabled]);

  const onSortState: (dataField: string, order: SortOrder) => void = (
    dataField: string,
    order: SortOrder
  ): void => {
    const newSorted = { dataField, order };
    sessionStorage.setItem("eventSort", JSON.stringify(newSorted));
  };

  const handleColumnToggle: (columnName: string) => void = useCallback(
    (columnName: string): void => {
      if (
        Object.values(columnItems).filter((val: boolean): boolean => val)
          .length === 1 &&
        columnItems[columnName]
      ) {
        // eslint-disable-next-line no-alert
        alert(t("validations.columns"));
        setColumnItems({
          ...columnItems,
          [columnName]: true,
        });
      } else {
        setColumnItems({
          ...columnItems,
          [columnName]: !columnItems[columnName],
        });
      }
    },
    [columnItems, setColumnItems, t]
  );

  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "id",
      header: t("searchFindings.tabEvents.id"),
      onSort: onSortState,
      visible: columnItems.id,
      width: "8%",
      wrapped: true,
    },
    {
      dataField: "eventDate",
      header: t("searchFindings.tabEvents.date"),
      onSort: onSortState,
      visible: columnItems.eventDate,
      width: "10%",
      wrapped: true,
    },
    {
      dataField: "detail",
      header: t("searchFindings.tabEvents.description"),
      onSort: onSortState,
      visible: columnItems.detail,
      width: "50%",
      wrapped: true,
    },
    {
      dataField: "accessibility",
      header: t("searchFindings.tabEvents.accessibility"),
      onSort: onSortState,
      visible: columnItems.accessibility,
      width: "50%",
      wrapped: true,
    },
    {
      dataField: "affectedComponents",
      header: t("searchFindings.tabEvents.affectedComponents"),
      onSort: onSortState,
      visible: columnItems.affectedComponents,
      width: "50%",
      wrapped: true,
    },
    {
      dataField: "eventType",
      header: t("searchFindings.tabEvents.type"),
      onSort: onSortState,
      visible: columnItems.eventType,
      width: "20%",
      wrapped: true,
    },
    {
      dataField: "eventStatus",
      formatter: statusFormatter,
      header: t("searchFindings.tabEvents.status"),
      onSort: onSortState,
      visible: columnItems.eventStatus,
      width: "90px",
      wrapped: true,
    },
    {
      dataField: "closingDate",
      header: t("searchFindings.tabEvents.dateClosed"),
      onSort: onSortState,
      visible: columnItems.dateClosed,
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
        t(castEventType(option))
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
      msgError(t("groupAlerts.errorTextsad"));
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
    push(`${url}/${rowInfo.id}/description`);
  };

  // State Management
  const [affectsReattacks, setAffectsReattacks] = useState(false);
  const [selectedReattacks, setSelectedReattacks] = useState({});

  const [isEventModalOpen, setIsEventModalOpen] = useState(false);
  const openNewEventModal: () => void = useCallback((): void => {
    setIsEventModalOpen(true);
  }, []);
  const closeNewEventModal: () => void = useCallback((): void => {
    setIsEventModalOpen(false);
  }, []);

  const [isUpdateAffectedModalOpen, setIsUpdateAffectedModalOpen] =
    useState(false);
  const openUpdateAffectedModal: () => void = useCallback((): void => {
    setIsUpdateAffectedModalOpen(true);
  }, []);
  const closeUpdateAffectedModal: () => void = useCallback((): void => {
    setIsUpdateAffectedModalOpen(false);
  }, []);

  const { data, refetch } = useQuery(GET_EVENTS, {
    onCompleted: handleQryResult,
    onError: handleQryErrors,
    variables: { groupName },
  });

  const { data: findingsData, refetch: refetchReattacks } =
    useQuery<IFindingsQuery>(GET_VERIFIED_FINDING_INFO, {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          Logger.error("Couldn't load reattack vulns", error);
        });
      },
      variables: { groupName },
    });
  const findings =
    findingsData === undefined ? [] : findingsData.group.findings;
  const hasReattacks = findings.some(
    (finding: IFinding): boolean => !finding.verified
  );

  const [requestHold] = useMutation(REQUEST_VULNS_HOLD_MUTATION, {
    onError: handleRequestHoldError,
  });

  const handleCreationResult = async (result: {
    addEvent: { eventId: string; success: boolean };
  }): Promise<void> => {
    closeNewEventModal();

    if (result.addEvent.success) {
      msgSuccess(
        t("group.events.successCreate"),
        t("group.events.titleSuccess")
      );

      if (affectsReattacks && !_.isEmpty(selectedReattacks)) {
        const allHoldsValid = await handleRequestHoldsHelper(
          requestHold,
          selectedReattacks,
          result.addEvent.eventId,
          groupName
        );

        if (allHoldsValid) {
          msgSuccess(
            t("group.events.form.affectedReattacks.holdsCreate"),
            t("group.events.titleSuccess")
          );
        }
      }
      await refetch();
      await refetchReattacks();
    }
  };

  const [addEvent] = useMutation(ADD_EVENT_MUTATION, {
    onCompleted: handleCreationResult,
    onError: handleCreationError,
  });

  const handleSubmit = useCallback(
    async (values: IFormValues): Promise<void> => {
      setAffectsReattacks(values.affectsReattacks);
      setSelectedReattacks(formatReattacks(values.affectedReattacks));

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

      await addEvent({
        variables: {
          accessibility: selectedAccessibility,
          affectedComponents: selectedComponents,
          detail: values.detail,
          eventDate: values.eventDate,
          eventType: values.eventType,
          file: handleFileListUpload(values.file),
          groupName,
          image: handleFileListUpload(values.image),
          rootId: values.rootId,
        },
      });
    },
    [addEvent, groupName]
  );

  const handleUpdateAffectedSubmit = useCallback(
    async (values: IUpdateAffectedValues): Promise<void> => {
      setSelectedReattacks(formatReattacks(values.affectedReattacks));

      if (!_.isEmpty(selectedReattacks)) {
        const allHoldsValid = await handleRequestHoldsHelper(
          requestHold,
          selectedReattacks,
          values.eventId,
          groupName
        );

        if (allHoldsValid) {
          msgSuccess(
            t("group.events.form.affectedReattacks.holdsCreate"),
            t("group.events.titleSuccess")
          );
        }

        closeUpdateAffectedModal();
        await refetchReattacks();
      }
    },
    [
      closeUpdateAffectedModal,
      refetchReattacks,
      requestHold,
      groupName,
      selectedReattacks,
      t,
    ]
  );
  const dataset = data === undefined ? [] : formatEvents(data.group.events);
  const hasOpenEvents = dataset.some(
    (event: IEventConfig): boolean =>
      event.eventStatus.toUpperCase() !== "SOLVED"
  );

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const filterSearchTextResult: IEventConfig[] = filterSearchText(
    dataset,
    searchTextFilter
  );

  function onStatusChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterGroupEventsTable(
      (value): IFilterSet => ({
        ...value,
        status: event.target.value,
      })
    );
  }
  const filterStatusResult: IEventConfig[] = filterSelect(
    dataset,
    filterGroupEventsTable.status,
    "eventStatus"
  );

  function onTypeChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterGroupEventsTable(
      (value): IFilterSet => ({
        ...value,
        type: event.target.value,
      })
    );
  }
  const filterTypeResult: IEventConfig[] = filterSelect(
    dataset,
    filterGroupEventsTable.type,
    "eventType"
  );

  function onDateMaxChange(event: React.ChangeEvent<HTMLInputElement>): void {
    event.persist();
    setFilterGroupEventsTable(
      (value): IFilterSet => ({
        ...value,
        dateRange: { ...value.dateRange, max: event.currentTarget.value },
      })
    );
  }
  function onDateMinChange(event: React.ChangeEvent<HTMLInputElement>): void {
    event.persist();
    setFilterGroupEventsTable(
      (value): IFilterSet => ({
        ...value,
        dateRange: { ...value.dateRange, min: event.currentTarget.value },
      })
    );
  }
  const filterDateRangeResult: IEventConfig[] = filterDateRange(
    dataset,
    filterGroupEventsTable.dateRange,
    "eventDate"
  );

  function onClosingDateMaxChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    event.persist();
    setFilterGroupEventsTable(
      (value): IFilterSet => ({
        ...value,
        closingDateRange: {
          ...value.closingDateRange,
          max: event.currentTarget.value,
        },
      })
    );
  }
  function onClosingDateMinChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    event.persist();
    setFilterGroupEventsTable(
      (value): IFilterSet => ({
        ...value,
        closingDateRange: {
          ...value.closingDateRange,
          min: event.currentTarget.value,
        },
      })
    );
  }
  const filterClosingDateRangeResult: IEventConfig[] = filterDateRange(
    dataset,
    filterGroupEventsTable.closingDateRange,
    "closingDate"
  );

  function onAccessibilityChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    event.persist();
    setFilterGroupEventsTable(
      (value): IFilterSet => ({
        ...value,
        accessibility: event.target.value,
      })
    );
  }
  const filterAccessibilityResult: IEventConfig[] = filterSelect(
    dataset,
    filterGroupEventsTable.accessibility,
    "accessibility"
  );

  function onAfectCompsChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    event.persist();
    setFilterGroupEventsTable(
      (value): IFilterSet => ({
        ...value,
        afectComps: event.target.value,
      })
    );
  }
  const filterAfectCompsResult: IEventConfig[] = filterSelect(
    dataset,
    filterGroupEventsTable.afectComps,
    "affectedComponents"
  );

  function clearFilters(): void {
    setFilterGroupEventsTable(
      (): IFilterSet => ({
        accessibility: "",
        afectComps: "",
        closingDateRange: { max: "", min: "" },
        dateRange: { max: "", min: "" },
        status: "",
        type: "",
      })
    );
    setSearchTextFilter("");
  }

  const resultDataset: IEventConfig[] = _.intersection(
    filterSearchTextResult,
    filterStatusResult,
    filterTypeResult,
    filterDateRangeResult,
    filterClosingDateRangeResult,
    filterAccessibilityResult,
    filterAfectCompsResult
  );

  const customFiltersProps: IFilterProps[] = [
    {
      defaultValue: "",
      placeholder: "Date (range)",
      rangeProps: {
        defaultValue: filterGroupEventsTable.dateRange,
        onChangeMax: onDateMaxChange,
        onChangeMin: onDateMinChange,
      },
      tooltipId: "group.events.filtersTooltips.date.id",
      tooltipMessage: "group.events.filtersTooltips.date",
      type: "dateRange",
    },
    {
      defaultValue: filterGroupEventsTable.accessibility,
      onChangeSelect: onAccessibilityChange,
      placeholder: "Accessibility",
      selectOptions: accessibilityOptions,
      tooltipId: "group.events.filtersTooltips.accessibility.id",
      tooltipMessage: "group.events.filtersTooltips.accessibility",
      type: "select",
    },
    {
      defaultValue: filterGroupEventsTable.afectComps,
      onChangeSelect: onAfectCompsChange,
      placeholder: "Affected components",
      selectOptions: afectCompsOptions,
      tooltipId: "group.events.filtersTooltips.affectedComponents.id",
      tooltipMessage: "group.events.filtersTooltips.affectedComponents",
      type: "select",
    },
    {
      defaultValue: filterGroupEventsTable.type,
      onChangeSelect: onTypeChange,
      placeholder: "Type",
      selectOptions: optionType,
      tooltipId: "group.events.filtersTooltips.type.id",
      tooltipMessage: "group.events.filtersTooltips.type",
      type: "select",
    },
    {
      defaultValue: filterGroupEventsTable.status,
      onChangeSelect: onStatusChange,
      placeholder: "Status",
      selectOptions: {
        Solved: "Solved",
        Unsolved: "Unsolved",
      },
      tooltipId: "group.events.filtersTooltips.status.id",
      tooltipMessage: "group.events.filtersTooltips.status",
      type: "select",
    },
    {
      defaultValue: "",
      placeholder: "Closing date (range)",
      rangeProps: {
        defaultValue: filterGroupEventsTable.closingDateRange,
        onChangeMax: onClosingDateMaxChange,
        onChangeMin: onClosingDateMinChange,
      },
      tooltipId: "group.events.filtersTooltips.dateClosed.id",
      tooltipMessage: "group.events.filtersTooltips.dateClosed",
      type: "dateRange",
    },
  ];

  return (
    <React.Fragment>
      {isEventModalOpen ? (
        <AddModal
          groupName={groupName}
          onClose={closeNewEventModal}
          onSubmit={handleSubmit}
        />
      ) : undefined}
      {isUpdateAffectedModalOpen ? (
        <UpdateAffectedModal
          eventsInfo={data}
          findings={findings}
          onClose={closeUpdateAffectedModal}
          onSubmit={handleUpdateAffectedSubmit}
        />
      ) : undefined}
      <TooltipWrapper
        id={"group.events.help"}
        message={t("searchFindings.tabEvents.tableAdvice")}
      >
        <Table
          clearFiltersButton={clearFilters}
          columnToggle={true}
          customFilters={{
            customFiltersProps,
            isCustomFilterEnabled,
            onUpdateEnableCustomFilter: handleUpdateCustomFilter,
            resultSize: {
              current: resultDataset.length,
              total: dataset.length,
            },
          }}
          customSearch={{
            customSearchDefault: searchTextFilter,
            isCustomSearchEnabled: true,
            onUpdateCustomSearch: onSearchTextChange,
            position: "right",
          }}
          dataset={resultDataset}
          defaultSorted={JSON.parse(
            _.get(sessionStorage, "eventSort", "{}") as string
          )}
          exportCsv={true}
          extraButtons={
            <Row>
              <ButtonToolbar>
                <Can do={"api_mutations_add_event_mutate"}>
                  <TooltipWrapper
                    id={"group.events.btn.tooltip.id"}
                    message={t("group.events.btn.tooltip")}
                  >
                    <Button onClick={openNewEventModal} variant={"primary"}>
                      <FontAwesomeIcon icon={faPlus} />
                      &nbsp;{t("group.events.btn.text")}
                    </Button>
                  </TooltipWrapper>
                </Can>
              </ButtonToolbar>
              <ButtonToolbar>
                <Can do={"api_mutations_request_vulnerabilities_hold_mutate"}>
                  <TooltipWrapper
                    id={"group.events.form.affectedReattacks.btn.id"}
                    message={t(
                      "group.events.form.affectedReattacks.btn.tooltip"
                    )}
                  >
                    <Button
                      disabled={!(hasReattacks && hasOpenEvents)}
                      onClick={openUpdateAffectedModal}
                      variant={"secondary"}
                    >
                      <FontAwesomeIcon icon={faPlus} />
                      &nbsp;
                      {t("group.events.form.affectedReattacks.btn.text")}
                    </Button>
                  </TooltipWrapper>
                </Can>
              </ButtonToolbar>
            </Row>
          }
          headers={tableHeaders}
          id={"tblEvents"}
          onColumnToggle={handleColumnToggle}
          pageSize={10}
          rowEvents={{ onClick: goToEvent }}
          search={false}
        />
      </TooltipWrapper>
    </React.Fragment>
  );
};

export type { IEventsDataset };
export { GroupEventsView };
