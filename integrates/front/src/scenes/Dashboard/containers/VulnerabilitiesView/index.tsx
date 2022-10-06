/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type {
  ColumnDef,
  ColumnFilter,
  ColumnFiltersState,
} from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Modal, ModalConfirm } from "components/Modal";
import { filterDate } from "components/TableNew/filters/filterFunctions/filterDate";
import type { ICellHelper } from "components/TableNew/types";
import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import { setColumnHelper } from "scenes/Dashboard/components/Vulnerabilities/helpers";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateDescription } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription";
import { UploadVulnerabilities } from "scenes/Dashboard/components/Vulnerabilities/uploadFile";
import {
  filterOutVulnerabilities,
  filterZeroRisk,
  formatVulnerabilitiesTreatment,
  getNonSelectableVulnerabilitiesOnReattackIds,
  getNonSelectableVulnerabilitiesOnVerifyIds,
} from "scenes/Dashboard/components/Vulnerabilities/utils";
import { ActionButtons } from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons";
import { HandleAcceptanceModal } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptanceModal";
import {
  GET_FINDING_AND_GROUP_INFO,
  GET_FINDING_NZR_VULNS,
  GET_FINDING_ZR_VULNS,
  SEND_VULNERABILITY_NOTIFICATION,
} from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import type {
  IGetFindingAndGroupInfo,
  IModalConfig,
  ISendNotificationResultAttr,
  IVulnerabilitiesConnection,
  IVulnerabilityEdge,
} from "scenes/Dashboard/containers/VulnerabilitiesView/types";
import { isPendingToAcceptance } from "scenes/Dashboard/containers/VulnerabilitiesView/utils";
import { Col100 } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { Have } from "utils/authz/Have";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

export const VulnsView: React.FC = (): JSX.Element => {
  const { findingId, groupName } = useParams<{
    findingId: string;
    groupName: string;
  }>();
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRetrieveHacker: boolean = permissions.can(
    "api_resolvers_vulnerability_hacker_resolve"
  );
  const canRetrieveZeroRisk: boolean = permissions.can(
    "api_resolvers_finding_zero_risk_connection_resolve"
  );

  const [isOpen, setIsOpen] = useState(false);

  const [isHandleAcceptanceModalOpen, setIsHandleAcceptanceModalOpen] =
    useState(false);
  function toggleHandleAcceptanceModal(): void {
    setIsHandleAcceptanceModalOpen(!isHandleAcceptanceModalOpen);
  }

  const [findsFilters, setFindsFilters] = useStoredState<ColumnFiltersState>(
    "tblFindings-columnFilters",
    [],
    localStorage
  );
  const [columnFilters, setColumnFilters] = useStoredState<ColumnFiltersState>(
    "vulnerabilitiesTable-columnFilters",
    [],
    localStorage
  );
  const [remediationModal, setRemediationModal] = useState<IModalConfig>({
    clearSelected: (): void => undefined,
    selectedVulnerabilities: [],
  });
  const openRemediationModal = useCallback(
    (
      selectedVulnerabilities: IVulnRowAttr[],
      clearSelected: () => void
    ): void => {
      setRemediationModal({ clearSelected, selectedVulnerabilities });
    },
    []
  );
  function closeRemediationModal(): void {
    setIsOpen(false);
  }
  const [isEditing, setIsEditing] = useState(false);
  function toggleEdit(): void {
    setIsEditing(!isEditing);
  }
  function handleCloseUpdateModal(): void {
    setIsEditing(false);
  }
  const [isNotify, setIsNotify] = useState(false);
  function toggleNotify(): void {
    setIsNotify(!isNotify);
  }
  function handleCloseNotifyModal(): void {
    setIsNotify(false);
  }
  const [isRequestingVerify, setIsRequestingVerify] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);

  const { data } = useQuery<IGetFindingAndGroupInfo>(
    GET_FINDING_AND_GROUP_INFO,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred loading finding", error);
        });
      },
      variables: {
        findingId,
      },
    }
  );

  const {
    data: nzrVulnsData,
    fetchMore: nzrFetchMore,
    refetch: nzrRefetch,
  } = useQuery<{
    finding: { vulnerabilitiesConnection: IVulnerabilitiesConnection };
  }>(GET_FINDING_NZR_VULNS, {
    fetchPolicy: "network-only",
    nextFetchPolicy: "cache-first",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred loading finding non zero risk vulnerabilities",
          error
        );
      });
    },
    variables: {
      findingId,
      first: 100,
    },
  });
  const vulnerabilitiesConnection =
    nzrVulnsData === undefined
      ? undefined
      : nzrVulnsData.finding.vulnerabilitiesConnection;

  const nzrVulnsPageInfo =
    vulnerabilitiesConnection === undefined
      ? undefined
      : vulnerabilitiesConnection.pageInfo;
  const nzrVulnsEdges: IVulnerabilityEdge[] = useMemo(
    (): IVulnerabilityEdge[] =>
      vulnerabilitiesConnection === undefined
        ? []
        : vulnerabilitiesConnection.edges,
    [vulnerabilitiesConnection]
  );
  const {
    data: zrVulnsData,
    fetchMore: zrFetchMore,
    refetch: zrRefetch,
  } = useQuery<{
    finding: { zeroRiskConnection: IVulnerabilitiesConnection | undefined };
  }>(GET_FINDING_ZR_VULNS, {
    fetchPolicy: "network-only",
    nextFetchPolicy: "cache-first",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred loading finding zero risk vulnerabilities",
          error
        );
      });
    },
    variables: {
      canRetrieveZeroRisk,
      findingId,
      first: 100,
    },
  });
  const zeroRiskConnection =
    zrVulnsData === undefined
      ? undefined
      : zrVulnsData.finding.zeroRiskConnection;
  const zrVulnsPageInfo =
    zeroRiskConnection === undefined ? undefined : zeroRiskConnection.pageInfo;
  const zrVulnsEdges: IVulnerabilityEdge[] =
    zeroRiskConnection === undefined ? [] : zeroRiskConnection.edges;

  const unformattedVulns: IVulnRowAttr[] = zrVulnsEdges
    .concat(nzrVulnsEdges)
    .map(
      (vulnerabilityEdge: IVulnerabilityEdge): IVulnRowAttr =>
        vulnerabilityEdge.node
    );

  const [sendNotification] = useMutation<ISendNotificationResultAttr>(
    SEND_VULNERABILITY_NOTIFICATION,
    {
      onCompleted: (result: ISendNotificationResultAttr): void => {
        if (result.sendVulnerabilityNotification.success) {
          msgSuccess(
            t("searchFindings.tabDescription.notify.emailNotificationText"),
            t("searchFindings.tabDescription.notify.emailNotificationTitle")
          );
        }
      },
      onError: (updateError: ApolloError): void => {
        updateError.graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(
            t("searchFindings.tabDescription.notify.emailNotificationError")
          );
          Logger.warning("An error occurred sending the notification", error);
        });
      },
    }
  );
  async function handleSendNotification(): Promise<void> {
    await sendNotification({
      variables: {
        findingId,
      },
    });
    setIsNotify(false);
  }

  useEffect((): void => {
    if (
      columnFilters.filter(
        (element: ColumnFilter): boolean => element.id === "currentState"
      ).length > 0
    ) {
      const filtervalue = columnFilters.filter(
        (element: ColumnFilter): boolean => element.id === "currentState"
      )[0].value;
      if (
        findsFilters.filter(
          (element: ColumnFilter): boolean => element.id === "state"
        ).length > 0
      ) {
        setFindsFilters(
          findsFilters.map((element: ColumnFilter): ColumnFilter => {
            if (element.id === "state") {
              return { id: "state", value: filtervalue };
            }

            return element;
          })
        );
      } else {
        setFindsFilters([...findsFilters, { id: "state", value: filtervalue }]);
      }
    } else {
      setFindsFilters(
        findsFilters
          .map((element: ColumnFilter): ColumnFilter => {
            if (element.id === "state") {
              return { id: "", value: "" };
            }

            return element;
          })
          .filter((element: ColumnFilter): boolean => element.id !== "")
      );
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [columnFilters]);

  useEffect((): void => {
    if (!_.isUndefined(nzrVulnsPageInfo)) {
      if (nzrVulnsPageInfo.hasNextPage) {
        void nzrFetchMore({
          variables: { after: nzrVulnsPageInfo.endCursor, first: 1200 },
        });
      }
    }
  }, [nzrVulnsPageInfo, nzrFetchMore]);
  useEffect((): void => {
    if (!_.isUndefined(zrVulnsPageInfo)) {
      if (zrVulnsPageInfo.hasNextPage) {
        void zrFetchMore({
          variables: { after: zrVulnsPageInfo.endCursor, first: 1200 },
        });
      }
    }
  }, [zrVulnsPageInfo, zrFetchMore]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.StrictMode />;
  }

  const vulnerabilities: IVulnRowAttr[] = formatVulnerabilitiesTreatment(
    unformattedVulns.map(
      (vulnerability: IVulnRowAttr): IVulnRowAttr => ({
        ...vulnerability,
        groupName,
        where:
          vulnerability.vulnerabilityType === "lines" &&
          vulnerability.rootNickname !== null &&
          vulnerability.rootNickname !== "" &&
          !vulnerability.where.startsWith(`${vulnerability.rootNickname}/`)
            ? `${vulnerability.rootNickname}/${vulnerability.where}`
            : vulnerability.where,
      })
    ),
    undefined
  );

  const isFindingReleased: boolean = !_.isEmpty(data.finding.releaseDate);
  function toggleModal(): void {
    setIsOpen(true);
  }
  function toggleRequestVerify(): void {
    if (isRequestingVerify) {
      setIsRequestingVerify(!isRequestingVerify);
    } else {
      const { selectedVulnerabilities } = remediationModal;
      const newVulnerabilities: IVulnRowAttr[] = filterOutVulnerabilities(
        selectedVulnerabilities,
        filterZeroRisk(vulnerabilities),
        getNonSelectableVulnerabilitiesOnReattackIds
      );
      if (selectedVulnerabilities.length > newVulnerabilities.length) {
        setIsRequestingVerify(!isRequestingVerify);
        msgError(t("searchFindings.tabVuln.errors.selectedVulnerabilities"));
      } else if (selectedVulnerabilities.length > 0) {
        setIsOpen(true);
        setIsRequestingVerify(!isRequestingVerify);
      } else {
        setIsRequestingVerify(!isRequestingVerify);
      }
    }
  }

  function toggleVerify(): void {
    if (isVerifying) {
      setIsVerifying(!isVerifying);
    } else {
      const { selectedVulnerabilities } = remediationModal;
      const newVulnerabilities: IVulnRowAttr[] = filterOutVulnerabilities(
        selectedVulnerabilities,
        filterZeroRisk(vulnerabilities),
        getNonSelectableVulnerabilitiesOnVerifyIds
      );
      if (selectedVulnerabilities.length > newVulnerabilities.length) {
        setIsVerifying(!isVerifying);
        msgError(t("searchFindings.tabVuln.errors.selectedVulnerabilities"));
      } else if (selectedVulnerabilities.length > 0) {
        setIsOpen(true);
        setIsVerifying(!isVerifying);
      } else {
        setIsVerifying(!isVerifying);
      }
    }
  }

  function refetchVulnsData(): void {
    void nzrRefetch();
    void zrRefetch();
  }

  function columnHelper(): JSX.Element {
    return (
      <Col100>
        <Have I={"can_report_vulnerabilities"}>
          <Can do={"api_mutations_upload_file_mutate"}>
            <UploadVulnerabilities
              findingId={findingId}
              refetchData={refetchVulnsData}
            />
          </Can>
        </Have>
      </Col100>
    );
  }

  const columns: ColumnDef<IVulnRowAttr>[] = [
    {
      accessorKey: "where",
      enableColumnFilter: false,
      header: t("searchFindings.tabVuln.vulnTable.where"),
    },
    {
      accessorKey: "specific",
      enableColumnFilter: false,
      header: t("searchFindings.tabVuln.vulnTable.specific"),
    },
    {
      accessorKey: "currentState",
      cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element =>
        statusFormatter(cell.getValue()),
      header: t("searchFindings.tabVuln.vulnTable.status"),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "reportDate",
      filterFn: filterDate,
      header: t("searchFindings.tabVuln.vulnTable.reportDate"),
      meta: { filterType: "dateRange" },
    },
    {
      accessorKey: "verification",
      header: t("searchFindings.tabVuln.vulnTable.reattack"),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "treatment",
      header: t("searchFindings.tabVuln.vulnTable.treatment"),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "tag",
      header: t("searchFindings.tabVuln.vulnTable.tags"),
    },
    {
      accessorKey: "treatmentAcceptanceStatus",
      header: "Treatment Acceptance",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "treatmentAssigned",
      header: "Asignees",
      meta: { filterType: "select" },
    },
  ];

  function setColumn(): JSX.Element | undefined {
    return setColumnHelper(true, columnHelper);
  }

  return (
    <React.StrictMode>
      <React.Fragment>
        <div>
          <div>
            <div>
              <VulnComponent
                canDisplayHacker={canRetrieveHacker}
                columnFilterSetter={setColumnFilters}
                columnFilterState={columnFilters}
                columns={columns}
                extraButtons={
                  <ActionButtons
                    areVulnerabilitiesPendingToAcceptance={isPendingToAcceptance(
                      vulnerabilities
                    )}
                    areVulnsSelected={
                      remediationModal.selectedVulnerabilities.length > 0
                    }
                    isEditing={isEditing}
                    isFindingReleased={isFindingReleased}
                    isOpen={isOpen}
                    isReattackRequestedInAllVuln={data.finding.remediated}
                    isRequestingReattack={isRequestingVerify}
                    isVerified={data.finding.verified}
                    isVerifying={isVerifying}
                    onEdit={toggleEdit}
                    onNotify={toggleNotify}
                    onRequestReattack={toggleRequestVerify}
                    onVerify={toggleVerify}
                    openHandleAcceptance={toggleHandleAcceptanceModal}
                    openModal={toggleModal}
                    state={data.finding.state}
                  />
                }
                findingState={data.finding.state}
                isEditing={isEditing}
                isFindingReleased={isFindingReleased}
                isRequestingReattack={isRequestingVerify}
                isVerifyingRequest={isVerifying}
                onVulnSelect={openRemediationModal}
                refetchData={refetchVulnsData}
                vulnerabilities={filterZeroRisk(vulnerabilities)}
              />
            </div>
            {setColumn()}
          </div>
        </div>
        {isOpen && (
          <UpdateVerificationModal
            clearSelected={_.get(remediationModal, "clearSelected")}
            handleCloseModal={closeRemediationModal}
            isReattacking={isRequestingVerify}
            isVerifying={isVerifying}
            refetchData={refetchVulnsData}
            setRequestState={toggleRequestVerify}
            setVerifyState={toggleVerify}
            vulns={remediationModal.selectedVulnerabilities}
          />
        )}
        {isHandleAcceptanceModalOpen && (
          <HandleAcceptanceModal
            findingId={findingId}
            groupName={groupName}
            handleCloseModal={toggleHandleAcceptanceModal}
            refetchData={refetchVulnsData}
            vulns={vulnerabilities}
          />
        )}
        {isEditing && (
          <Modal
            onClose={handleCloseUpdateModal}
            open={isEditing}
            title={t("searchFindings.tabDescription.editVuln")}
          >
            <UpdateDescription
              findingId={findingId}
              groupName={groupName}
              handleClearSelected={_.get(remediationModal, "clearSelected")}
              handleCloseModal={handleCloseUpdateModal}
              refetchData={refetchVulnsData}
              vulnerabilities={remediationModal.selectedVulnerabilities}
            />
          </Modal>
        )}
        {isNotify && (
          <Modal
            onClose={handleCloseNotifyModal}
            open={isNotify}
            title={t("searchFindings.notifyModal.body")}
          >
            <ModalConfirm
              onCancel={handleCloseNotifyModal}
              onConfirm={handleSendNotification}
              txtCancel={t("searchFindings.notifyModal.cancel")}
              txtConfirm={t("searchFindings.notifyModal.notify")}
            />
          </Modal>
        )}
      </React.Fragment>
    </React.StrictMode>
  );
};
