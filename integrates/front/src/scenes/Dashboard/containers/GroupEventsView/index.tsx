import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError, FetchResult } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faCheck, faPlus, faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type {
  ColumnDef,
  Row,
  SortingState,
  VisibilityState,
} from "@tanstack/react-table";
import { extend } from "dayjs";
import utc from "dayjs/plugin/utc";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import type { FormEvent } from "react";
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
  IRequestEventVerificationResultAttr,
} from "./types";
import { UpdateAffectedModal } from "./UpdateAffectedModal";
import type { IUpdateAffectedValues } from "./UpdateAffectedModal/types";

import { handleUpdateEvidenceError } from "../EventEvidenceView/helpers";
import { UPDATE_EVIDENCE_MUTATION } from "../EventEvidenceView/queries";
import type { IUpdateEventEvidenceResultAttr } from "../EventEvidenceView/types";
import { Button } from "components/Button";
import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { filterDate } from "components/Table/filters/filterFunctions/filterDate";
import { Table } from "components/Table/index";
import type { ICellHelper } from "components/Table/types";
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
  getNonSelectableEventIndexToRequestVerification,
} from "scenes/Dashboard/containers/GroupEventsView/utils";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { castEventStatus } from "utils/formatHelpers";
import { getErrors } from "utils/helpers";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const GroupEventsView: React.FC = (): JSX.Element => {
  const { push } = useHistory();
  const { groupName, organizationName } =
    useParams<{ groupName: string; organizationName: string }>();

  const { url } = useRouteMatch();
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRequestVerification: boolean = permissions.can(
    "api_mutations_request_event_verification_mutate"
  );

  const handleQryErrors: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      Logger.warning("An error occurred loading group data", error);
      msgError(t("groupAlerts.errorTextsad"));
    });
  };
  const { data, refetch } = useQuery<IEventsDataset>(GET_EVENTS, {
    onError: handleQryErrors,
    variables: { groupName },
  });
  const allEvents = data === undefined ? [] : data.group.events;
  const dataset = formatEvents(allEvents);
  const hasOpenEvents = dataset.some(
    (event: IEventData): boolean => event.eventStatus.toUpperCase() !== "SOLVED"
  );

  const columns: ColumnDef<IEventData>[] = [
    {
      accessorKey: "id",
      header: t("searchFindings.tabEvents.id"),
    },
    {
      accessorFn: (row: IEventData): string | undefined => row.root?.nickname,
      header: String(t("searchFindings.tabEvents.root")),
    },
    {
      accessorKey: "eventDate",
      filterFn: filterDate,
      header: t("searchFindings.tabEvents.date"),
    },
    {
      accessorKey: "detail",
      header: t("searchFindings.tabEvents.description"),
    },
    {
      accessorKey: "eventType",
      header: t("searchFindings.tabEvents.type"),
    },
    {
      accessorKey: "eventStatus",
      cell: (cell: ICellHelper<IEventData>): JSX.Element =>
        statusFormatter(cell.getValue()),
      header: t("searchFindings.tabEvents.status"),
    },
    {
      accessorKey: "closingDate",
      header: t("searchFindings.tabEvents.dateClosed"),
    },
  ];

  const [filters, setFilters] = useState<IFilter<IEventData>[]>([
    {
      id: "eventDate",
      key: "eventDate",
      label: t("searchFindings.tabEvents.date"),
      type: "dateRange",
    },
    {
      id: "eventType",
      key: "eventType",
      label: t("searchFindings.tabEvents.type"),
      selectOptions: selectOptionType,
      type: "select",
    },
    {
      filterFn: "caseInsensitive",
      id: "eventStatus",
      key: "eventStatus",
      label: t("searchFindings.tabEvents.status"),
      selectOptions: [
        {
          header: t(castEventStatus("VERIFICATION_REQUESTED")),
          value: "Pending",
        },
        { header: t(castEventStatus("CREATED")), value: "Unsolved" },
        { header: t(castEventStatus("SOLVED")), value: "Solved" },
      ],
      type: "select",
    },
    {
      id: "closingDate",
      key: "closingDate",
      label: t("searchFindings.tabEvents.dateClosed"),
      type: "dateRange",
    },
  ]);
  const [columnVisibility, setColumnVisibility] =
    useStoredState<VisibilityState>("tblEvents-visibilityState", {
      Assignees: false,
      Locations: false,
      Treatment: false,
      description: false,
      reattack: false,
      releaseDate: false,
    });
  const [sorting, setSorting] = useStoredState<SortingState>(
    "tblEvents-sortingState",
    []
  );

  function enabledRows(row: Row<IEventData>): boolean {
    const indexes = getNonSelectableEventIndexToRequestVerification(dataset);
    const nonselectables = indexes.map(
      (index: number): IEventData => dataset[index]
    );

    return !nonselectables.includes(row.original);
  }

  function goToEventz(rowInfo: Row<IEventData>): (event: FormEvent) => void {
    return (event: FormEvent): void => {
      mixpanel.track("ReadEvent");
      push(`${url}/${rowInfo.original.id}/description`);
      event.preventDefault();
    };
  }

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
      extend(utc);
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

  const isOpenMode = isOpenRequestVerificationMode;

  const filteredDataset = useFilters(dataset, filters);

  return (
    <React.Fragment>
      {isAddModalOpen ? (
        <AddModal
          groupName={groupName}
          onClose={closeAddModal}
          onSubmit={handleSubmit}
          organizationName={organizationName}
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
          columnToggle={true}
          columnVisibilitySetter={setColumnVisibility}
          columnVisibilityState={columnVisibility}
          columns={columns}
          data={filteredDataset}
          enableRowSelection={
            isOpenRequestVerificationMode ? enabledRows : undefined
          }
          exportCsv={true}
          extraButtons={
            <React.Fragment>
              {isOpenMode ? undefined : (
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
              )}
              {isOpenMode ? undefined : (
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
              )}
              <Can do={"api_mutations_request_event_verification_mutate"}>
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
          filters={<Filters filters={filters} setFilters={setFilters} />}
          id={"tblEvents"}
          onRowClick={goToEventz}
          rowSelectionSetter={
            canRequestVerification ? setSelectedEvents : undefined
          }
          rowSelectionState={selectedEvents}
          sortingSetter={setSorting}
          sortingState={sorting}
        />
      </Tooltip>
    </React.Fragment>
  );
};

export type { IEventsDataset };
export { GroupEventsView };
