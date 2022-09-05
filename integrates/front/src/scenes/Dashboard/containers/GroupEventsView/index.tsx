import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError, FetchResult } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faCheck, faPlus, faTimes } from "@fortawesome/free-solid-svg-icons";
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
  handleRequestHoldError,
  handleRequestHoldsHelper,
} from "./helpers";
import { selectOptionType } from "./selectOptions";
import type {
  IAddEventResultAttr,
  IEventData,
  IEventsDataset,
  IFilterSet,
  IRequestEventVerificationResultAttr,
} from "./types";
import { UpdateAffectedModal } from "./UpdateAffectedModal";
import type { IUpdateAffectedValues } from "./UpdateAffectedModal/types";

import { handleUpdateEvidenceError } from "../EventEvidenceView/helpers";
import { UPDATE_EVIDENCE_MUTATION } from "../EventEvidenceView/queries";
import type { IUpdateEventEvidenceResultAttr } from "../EventEvidenceView/types";
import { Button } from "components/Button";
import { Table } from "components/Table";
import type { IFilterProps, IHeaderConfig } from "components/Table/types";
import {
  filterDateRange,
  filterSearchText,
  filterSelect,
} from "components/Table/utils";
import { Tooltip } from "components/Tooltip";
import { RemediationModal } from "scenes/Dashboard/components/RemediationModal";
import { handleRequestVerificationError } from "scenes/Dashboard/components/UpdateVerificationModal/helpers";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import {
  ADD_EVENT_MUTATION,
  GET_EVENTS,
  REQUEST_EVENT_VERIFICATION_MUTATION,
  REQUEST_VULNS_HOLD_MUTATION,
} from "scenes/Dashboard/containers/GroupEventsView/queries";
import {
  formatEvents,
  formatReattacks,
  getEventIndex,
  getNonSelectableEventIndexToRequestVerification,
  onSelectSeveralEventsHelper,
} from "scenes/Dashboard/containers/GroupEventsView/utils";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { castEventStatus, castEventType } from "utils/formatHelpers";
import { getErrors } from "utils/helpers";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const GroupEventsView: React.FC = (): JSX.Element => {
  const { push } = useHistory();
  const { groupName } = useParams<{ groupName: string }>();

  const { url } = useRouteMatch();
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRequestVerification: boolean = permissions.can(
    "api_mutations_request_event_verification_mutate"
  );

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
  const [selectedEvents, setSelectedEvents] = useState<IEventData[]>([]);
  const unsolved = translate.t(castEventStatus("CREATED"));
  const selectedUnsolvedEvents = selectedEvents.filter(
    (event: IEventData): boolean => event.eventStatus === unsolved
  );

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

  const [isRequestVerificationModalOpen, setIsRequestVerificationModalOpen] =
    useState(false);
  const openRequestVerificationModal: () => void = useCallback((): void => {
    setIsRequestVerificationModalOpen(true);
  }, []);
  const closeRequestVerificationModal: () => void = useCallback((): void => {
    setIsRequestVerificationModalOpen(false);
  }, []);
  const [isOpenRequestVerificationMode, setIsOpenRequestVerificationMode] =
    useState(false);
  const openRequestVerificationMode: () => void = useCallback((): void => {
    if (
      selectedUnsolvedEvents.length === selectedEvents.length &&
      selectedEvents.length > 0
    ) {
      openRequestVerificationModal();
    } else {
      msgError(t("group.events.selectedError"));
      setSelectedEvents(selectedUnsolvedEvents);
    }

    setIsOpenRequestVerificationMode(true);
  }, [t, selectedUnsolvedEvents, selectedEvents, openRequestVerificationModal]);
  const closeRequestVerificationMode: () => void = useCallback((): void => {
    setIsOpenRequestVerificationMode(false);
    closeRequestVerificationModal();
  }, [closeRequestVerificationModal]);

  const closeOpenMode: () => void = useCallback((): void => {
    closeRequestVerificationMode();
  }, [closeRequestVerificationMode]);

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

  const [requestVerification] =
    useMutation<IRequestEventVerificationResultAttr>(
      REQUEST_EVENT_VERIFICATION_MUTATION,
      {
        onError: handleRequestVerificationError,
      }
    );

  const [addEvent] = useMutation<IAddEventResultAttr>(ADD_EVENT_MUTATION, {
    onError: handleCreationError,
  });

  const [updateEvidence] = useMutation<IUpdateEventEvidenceResultAttr>(
    UPDATE_EVIDENCE_MUTATION,
    {
      onError: (updateError: ApolloError): void => {
        handleUpdateEvidenceError(updateError);
      },
    }
  );

  const handleSubmit = useCallback(
    async (values: IFormValues): Promise<void> => {
      const {
        affectsReattacks,
        affectedReattacks,
        detail,
        eventDate,
        eventType,
        images,
        files,
        rootId,
      } = values;
      const selectedEventReattacks = formatReattacks(affectedReattacks);
      const result = await addEvent({
        variables: {
          detail,
          eventDate:
            typeof eventDate === "string"
              ? eventDate
              : eventDate.utc().format(),
          eventType,
          groupName,
          rootId,
        },
      });
      closeAddModal();
      if (!_.isNil(result.data) && result.data.addEvent.success) {
        const { eventId } = result.data.addEvent;
        if (!_.isUndefined(images)) {
          [...Array(images.length).keys()].forEach(
            async (
              index: number
            ): Promise<
              FetchResult<IUpdateEventEvidenceResultAttr> | undefined
            > =>
              _.isUndefined(images[index])
                ? undefined
                : updateEvidence({
                    variables: {
                      eventId,
                      evidenceType: `IMAGE_${index + 1}`,
                      file: images[index],
                    },
                  })
          );
        }

        if (!_.isUndefined(files) && !_.isUndefined(files[0])) {
          void updateEvidence({
            variables: {
              eventId,
              evidenceType: "FILE_1",
              file: files[0],
            },
          });
        }
        if (affectsReattacks && !_.isEmpty(selectedEventReattacks)) {
          const allHoldsValid = await handleRequestHoldsHelper(
            requestHold,
            selectedEventReattacks,
            eventId,
            groupName
          );

          if (allHoldsValid) {
            msgSuccess(
              t("group.events.form.affectedReattacks.holdsCreate"),
              t("group.events.titleSuccess")
            );
          }
        }
        msgSuccess(
          t("group.events.successCreate"),
          t("group.events.titleSuccess")
        );

        await refetch();
        await refetchReattacks();
      }
    },
    [
      addEvent,
      closeAddModal,
      groupName,
      refetch,
      refetchReattacks,
      requestHold,
      t,
      updateEvidence,
    ]
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

  const handleRequestVerification = useCallback(
    async (values: { treatmentJustification: string }): Promise<void> => {
      const results = await Promise.all(
        selectedEvents.map(
          async (
            event: IEventData
          ): Promise<FetchResult<IRequestEventVerificationResultAttr>> =>
            requestVerification({
              variables: {
                comments: values.treatmentJustification,
                eventId: event.id,
              },
            })
        )
      );
      void refetch();
      setSelectedEvents([]);
      setIsRequestVerificationModalOpen(false);
      const errors = getErrors<IRequestEventVerificationResultAttr>(results);

      if (!_.isEmpty(results) && _.isEmpty(errors)) {
        if (
          !_.isNil(results[0].data) &&
          results[0].data.requestEventVerification.success
        ) {
          msgSuccess(
            t("group.events.successRequestVerification"),
            t("groupAlerts.updatedTitle")
          );
          closeOpenMode();
        }
      }
    },

    [t, closeOpenMode, refetch, requestVerification, selectedEvents]
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
        translate.t(castEventType(option))
      );
      const filterOptions = _.pickBy(selectOptionType, (value): boolean =>
        _.includes(transEventOptions, value)
      );
      setOptionType(filterOptions);
    }
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
        [t(castEventStatus("VERIFICATION_REQUESTED"))]: "Pending",
        [t(castEventStatus("CREATED"))]: "Unsolved",
        [t(castEventStatus("SOLVED"))]: "Solved",
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

  function onSelectSeveralEvents(
    isSelect: boolean,
    eventsSelected: IEventData[]
  ): string[] {
    return onSelectSeveralEventsHelper(
      isSelect,
      eventsSelected,
      selectedEvents,
      setSelectedEvents
    );
  }
  function onSelectOneEvent(event: IEventData, isSelect: boolean): boolean {
    onSelectSeveralEvents(isSelect, [event]);

    return true;
  }
  const isOpenMode = isOpenRequestVerificationMode;

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
      {isRequestVerificationModalOpen ? (
        <RemediationModal
          isLoading={false}
          isOpen={true}
          maxJustificationLength={20000}
          message={t("group.events.remediationModal.justification")}
          onClose={closeRequestVerificationMode}
          onSubmit={handleRequestVerification}
          title={t("group.events.remediationModal.titleRequest")}
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
              <Can do={"api_mutations_add_event_mutate"} not={isOpenMode}>
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
              <Can
                do={"api_mutations_request_vulnerabilities_hold_mutate"}
                not={isOpenMode}
              >
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
              <Can
                do={"api_mutations_request_event_verification_mutate"}
                not={isOpenMode && !isOpenRequestVerificationMode}
              >
                <Tooltip
                  id={"group.events.remediationModal.btn.id"}
                  tip={t("group.events.remediationModal.btn.tooltip")}
                >
                  <Button
                    disabled={_.isEmpty(selectedUnsolvedEvents)}
                    onClick={
                      isOpenRequestVerificationMode
                        ? openRequestVerificationModal
                        : openRequestVerificationMode
                    }
                    variant={"secondary"}
                  >
                    <FontAwesomeIcon icon={faCheck} />
                    &nbsp;
                    {t("group.events.remediationModal.btn.text")}
                  </Button>
                </Tooltip>
              </Can>
              {isOpenMode ? (
                <Tooltip
                  id={"searchFindings.tabVuln.buttonsTooltip.cancelVerify.id"}
                  place={"top"}
                  tip={t("searchFindings.tabVuln.buttonsTooltip.cancel")}
                >
                  <Button onClick={closeOpenMode} variant={"secondary"}>
                    <React.Fragment>
                      <FontAwesomeIcon icon={faTimes} />
                      &nbsp;{t("searchFindings.tabDescription.cancelVerified")}
                    </React.Fragment>
                  </Button>
                </Tooltip>
              ) : undefined}
            </React.Fragment>
          }
          headers={tableHeaders}
          id={"tblEvents"}
          onColumnToggle={handleColumnToggle}
          pageSize={10}
          rowEvents={{ onClick: goToEvent }}
          search={false}
          selectionMode={{
            clickToSelect: false,
            hideSelectColumn: !canRequestVerification,
            mode: "checkbox",
            nonSelectable: isOpenRequestVerificationMode
              ? getNonSelectableEventIndexToRequestVerification(resultDataset)
              : undefined,
            onSelect: onSelectOneEvent,
            onSelectAll: onSelectSeveralEvents,
            selected: getEventIndex(selectedEvents, resultDataset),
          }}
        />
      </Tooltip>
    </React.Fragment>
  );
};

export type { IEventsDataset };
export { GroupEventsView };
