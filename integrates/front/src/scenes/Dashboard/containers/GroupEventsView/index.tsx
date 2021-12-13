import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";

import type { IFormValues } from "./AddModal";
import { AddModal } from "./AddModal";
import { handleCreationError, handleFileListUpload } from "./helpers";
import {
  accessibilityOptions,
  afectCompsOptions,
  eventActionsAfterBlocking,
  eventActionsBeforeBlocking,
  selectOptionType,
} from "./selectOptions";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import type {
  IFilterProps,
  IHeaderConfig,
} from "components/DataTableNext/types";
import {
  filterDateRange,
  filterSearchText,
  filterSelect,
} from "components/DataTableNext/utils";
import { TooltipWrapper } from "components/TooltipWrapper";
import { pointStatusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import {
  ADD_EVENT_MUTATION,
  GET_EVENTS,
} from "scenes/Dashboard/containers/GroupEventsView/queries";
import { formatEvents } from "scenes/Dashboard/containers/GroupEventsView/utils";
import type { IEventConfig } from "scenes/Dashboard/containers/GroupEventsView/utils";
import { ButtonToolbar, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { castEventType } from "utils/formatHelpers";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IEventsDataset {
  group: {
    events: {
      accessibility: string;
      actionAfterBlocking: string;
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

interface IFilterSet {
  accessibility: string;
  actAfterBlock: string;
  actBefBlock: string;
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

  const [optionType, setOptionType] = useState(selectOptionType);

  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("groupEventsFilters", false);

  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [filterGroupEventsTable, setFilterGroupEventsTable] =
    useStoredState<IFilterSet>(
      "filterGroupEventsSet",
      {
        accessibility: "",
        actAfterBlock: "",
        actBefBlock: "",
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
      actionAfterBlocking: true,
      actionBeforeBlocking: true,
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
        alert(translate.t("validations.columns"));
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
    [columnItems, setColumnItems]
  );

  const tableHeaders: IHeaderConfig[] = [
    {
      align: "center",
      dataField: "id",
      header: translate.t("searchFindings.tabEvents.id"),
      onSort: onSortState,
      visible: columnItems.id,
      width: "8%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "eventDate",
      header: translate.t("searchFindings.tabEvents.date"),
      onSort: onSortState,
      visible: columnItems.eventDate,
      width: "10%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "detail",
      header: translate.t("searchFindings.tabEvents.description"),
      onSort: onSortState,
      visible: columnItems.detail,
      width: "50%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "accessibility",
      header: translate.t("searchFindings.tabEvents.accessibility"),
      onSort: onSortState,
      visible: columnItems.accessibility,
      width: "50%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "affectedComponents",
      header: translate.t("searchFindings.tabEvents.affectedComponents"),
      onSort: onSortState,
      visible: columnItems.affectedComponents,
      width: "50%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "actionAfterBlocking",
      header: translate.t("searchFindings.tabEvents.actionAfterBlocking"),
      onSort: onSortState,
      visible: columnItems.actionAfterBlocking,
      width: "50%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "actionBeforeBlocking",
      header: translate.t("searchFindings.tabEvents.actionBeforeBlocking"),
      onSort: onSortState,
      visible: columnItems.actionBeforeBlocking,
      width: "50%",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "eventType",
      header: translate.t("searchFindings.tabEvents.type"),
      onSort: onSortState,
      visible: columnItems.eventType,
      width: "20%",
      wrapped: true,
    },
    {
      align: "left",
      dataField: "eventStatus",
      formatter: pointStatusFormatter,
      header: translate.t("searchFindings.tabEvents.status"),
      onSort: onSortState,
      visible: columnItems.eventStatus,
      width: "90px",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "closingDate",
      header: translate.t("searchFindings.tabEvents.closingDate"),
      onSort: onSortState,
      visible: columnItems.closingDate,
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

  const [addEvent] = useMutation(ADD_EVENT_MUTATION, {
    onCompleted: handleCreationResult,
    onError: handleCreationError,
  });

  const handleSubmit = useCallback(
    async (values: IFormValues): Promise<void> => {
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

  const dataset = data === undefined ? [] : formatEvents(data.group.events);

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const filterSearchtextResult: IEventConfig[] = filterSearchText(
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

  function onActBefBlockChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    event.persist();
    setFilterGroupEventsTable(
      (value): IFilterSet => ({
        ...value,
        actBefBlock: event.target.value,
      })
    );
  }
  const filterActBefBlockResult: IEventConfig[] = filterSelect(
    dataset,
    filterGroupEventsTable.actBefBlock,
    "actionBeforeBlocking"
  );

  function onActAfterBlockChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    event.persist();
    setFilterGroupEventsTable(
      (value): IFilterSet => ({
        ...value,
        actAfterBlock: event.target.value,
      })
    );
  }
  const filterActAfterBlockResult: IEventConfig[] = filterSelect(
    dataset,
    filterGroupEventsTable.actAfterBlock,
    "actionAfterBlocking"
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
        actAfterBlock: "",
        actBefBlock: "",
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
    filterSearchtextResult,
    filterStatusResult,
    filterTypeResult,
    filterDateRangeResult,
    filterClosingDateRangeResult,
    filterActBefBlockResult,
    filterAccessibilityResult,
    filterAfectCompsResult,
    filterActAfterBlockResult
  );

  const customFiltersProps: IFilterProps[] = [
    {
      defaultValue: "",
      placeholder: "Date (Range)",
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
      defaultValue: filterGroupEventsTable.actAfterBlock,
      onChangeSelect: onActAfterBlockChange,
      placeholder: "Action after blocking",
      selectOptions: eventActionsAfterBlocking,
      tooltipId: "group.events.filtersTooltips.actAfterBlock.id",
      tooltipMessage: "group.events.filtersTooltips.actAfterBlock",
      type: "select",
    },
    {
      defaultValue: filterGroupEventsTable.actBefBlock,
      onChangeSelect: onActBefBlockChange,
      placeholder: "Action before blocking",
      selectOptions: eventActionsBeforeBlocking,
      tooltipId: "group.events.filtersTooltips.actBefBlock.id",
      tooltipMessage: "group.events.filtersTooltips.actBefBlock",
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
      placeholder: "Closing date (Range)",
      rangeProps: {
        defaultValue: filterGroupEventsTable.closingDateRange,
        onChangeMax: onClosingDateMaxChange,
        onChangeMin: onClosingDateMinChange,
      },
      tooltipId: "group.events.filtersTooltips.closingDate.id",
      tooltipMessage: "group.events.filtersTooltips.closingDate",
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
      <TooltipWrapper
        id={"group.events.help"}
        message={translate.t("searchFindings.tabEvents.tableAdvice")}
      >
        <DataTableNext
          bordered={true}
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
          }}
          dataset={resultDataset}
          defaultSorted={JSON.parse(_.get(sessionStorage, "eventSort", "{}"))}
          exportCsv={true}
          extraButtons={
            <Row>
              <ButtonToolbar>
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

export { GroupEventsView };
