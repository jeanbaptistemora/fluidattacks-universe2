import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useEffect, useState } from "react";
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
import { selectOptionType } from "./selectOptions";
import type { IEventData, IEventsDataset, IFilterSet } from "./types";
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
import { Tooltip } from "components/Tooltip";
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
import { Can } from "utils/authz/Can";
import { castEventType } from "utils/formatHelpers";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

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
      closingDate: true,
      detail: true,
      eventDate: true,
      eventStatus: true,
      eventType: true,
      id: true,
      "root.nickname": true,
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
      wrapped: true,
    },
    {
      dataField: "root.nickname",
      header: t("searchFindings.tabEvents.root"),
      onSort: onSortState,
      visible: columnItems["root.nickname"],
      wrapped: true,
    },
    {
      dataField: "eventDate",
      header: t("searchFindings.tabEvents.date"),
      onSort: onSortState,
      visible: columnItems.eventDate,
      wrapped: true,
    },
    {
      dataField: "detail",
      header: t("searchFindings.tabEvents.description"),
      onSort: onSortState,
      visible: columnItems.detail,
      wrapped: true,
    },
    {
      dataField: "eventType",
      header: t("searchFindings.tabEvents.type"),
      onSort: onSortState,
      visible: columnItems.eventType,
      wrapped: true,
    },
    {
      dataField: "eventStatus",
      formatter: statusFormatter,
      header: t("searchFindings.tabEvents.status"),
      onSort: onSortState,
      visible: columnItems.eventStatus,
      wrapped: true,
    },
    {
      dataField: "closingDate",
      header: t("searchFindings.tabEvents.dateClosed"),
      onSort: onSortState,
      visible: columnItems.closingDate,
      wrapped: true,
    },
  ];

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

  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const openAddModal: () => void = useCallback((): void => {
    setIsAddModalOpen(true);
  }, []);
  const closeAddModal: () => void = useCallback((): void => {
    setIsAddModalOpen(false);
  }, []);

  const [isUpdateAffectedModalOpen, setIsUpdateAffectedModalOpen] =
    useState(false);
  const openUpdateAffectedModal: () => void = useCallback((): void => {
    setIsUpdateAffectedModalOpen(true);
  }, []);
  const closeUpdateAffectedModal: () => void = useCallback((): void => {
    setIsUpdateAffectedModalOpen(false);
  }, []);

  const { data, refetch } = useQuery<IEventsDataset>(GET_EVENTS, {
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
    closeAddModal();

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

      await addEvent({
        variables: {
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

  useEffect((): void => {
    if (!_.isUndefined(data)) {
      const eventOptions: string[] = Array.from(
        new Set(
          data.group.events.map(
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data]);

  const allEvents = data === undefined ? [] : data.group.events;
  const dataset = formatEvents(allEvents);
  const hasOpenEvents = dataset.some(
    (event: IEventData): boolean => event.eventStatus.toUpperCase() !== "SOLVED"
  );

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const filterSearchTextResult = filterSearchText(dataset, searchTextFilter);

  function onStatusChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterGroupEventsTable(
      (value): IFilterSet => ({
        ...value,
        status: event.target.value,
      })
    );
  }
  const filterStatusResult = filterSelect(
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
  const filterTypeResult = filterSelect(
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
  const filterDateRangeResult = filterDateRange(
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
  const filterClosingDateRangeResult = filterDateRange(
    dataset,
    filterGroupEventsTable.closingDateRange,
    "closingDate"
  );

  function clearFilters(): void {
    setFilterGroupEventsTable(
      (): IFilterSet => ({
        closingDateRange: { max: "", min: "" },
        dateRange: { max: "", min: "" },
        status: "",
        type: "",
      })
    );
    setSearchTextFilter("");
  }

  const resultDataset = _.intersection(
    filterSearchTextResult,
    filterStatusResult,
    filterTypeResult,
    filterDateRangeResult,
    filterClosingDateRangeResult
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
      {isAddModalOpen ? (
        <AddModal
          groupName={groupName}
          onClose={closeAddModal}
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
      <Tooltip
        id={"group.events.help"}
        tip={t("searchFindings.tabEvents.tableAdvice")}
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
            <React.Fragment>
              <Can do={"api_mutations_add_event_mutate"}>
                <Tooltip
                  id={"group.events.btn.tooltip.id"}
                  tip={t("group.events.btn.tooltip")}
                >
                  <Button onClick={openAddModal} variant={"primary"}>
                    <FontAwesomeIcon icon={faPlus} />
                    &nbsp;{t("group.events.btn.text")}
                  </Button>
                </Tooltip>
              </Can>
              <Can do={"api_mutations_request_vulnerabilities_hold_mutate"}>
                <Tooltip
                  id={"group.events.form.affectedReattacks.btn.id"}
                  tip={t("group.events.form.affectedReattacks.btn.tooltip")}
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
                </Tooltip>
              </Can>
            </React.Fragment>
          }
          headers={tableHeaders}
          id={"tblEvents"}
          onColumnToggle={handleColumnToggle}
          pageSize={10}
          rowEvents={{ onClick: goToEvent }}
          search={false}
        />
      </Tooltip>
    </React.Fragment>
  );
};

export type { IEventsDataset };
export { GroupEventsView };
