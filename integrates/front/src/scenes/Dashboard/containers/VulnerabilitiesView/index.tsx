import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Modal } from "components/Modal";
import type { IFilterProps } from "components/Table/types";
import {
  filterDateRange,
  filterSearchText,
  filterSelect,
  filterText,
} from "components/Table/utils";
import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";
import { setColumnHelper } from "scenes/Dashboard/components/Vulnerabilities/helpers";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateDescription } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription";
import { UploadVulnerabilities } from "scenes/Dashboard/components/Vulnerabilities/uploadFile";
import {
  filterCurrentStatus,
  filterOutVulnerabilities,
  filterTreatment,
  filterTreatmentCurrentStatus,
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
} from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import type {
  IGetFindingAndGroupInfo,
  IModalConfig,
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
import { msgError } from "utils/notifications";

interface IFilterSet {
  currentStatus: string;
  reportDateRange: { max: string; min: string };
  status: string;
  tag: string;
  treatment: string;
  treatmentCurrentStatus: string;
  verification: string;
}

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

  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("locationsCustomFilters", false);

  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [filterVulnerabilitiesTable, setFilterVulnerabilitiesTable] =
    useStoredState(
      "filterVulnerabilitiesSet",
      {
        currentStatus: "",
        reportDateRange: { max: "", min: "" },
        status: "open",
        tag: "",
        treatment: "",
        treatmentCurrentStatus: "",
        verification: "",
      },
      localStorage
    );
  const [
    filterGroupFindingsCurrentStatus,
    setFilterGroupFindingsCurrentStatus,
  ] = useStoredState<Record<string, string>>(
    "groupFindingsCurrentStatus",
    { currentStatus: "open" },
    localStorage
  );
  const handleUpdateCustomFilter: () => void = useCallback((): void => {
    setCustomFilterEnabled(!isCustomFilterEnabled);
  }, [isCustomFilterEnabled, setCustomFilterEnabled]);

  const [isHandleAcceptanceModalOpen, setIsHandleAcceptanceModalOpen] =
    useState(false);
  function toggleHandleAcceptanceModal(): void {
    setIsHandleAcceptanceModalOpen(!isHandleAcceptanceModalOpen);
  }

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
      state: _.isEmpty(filterGroupFindingsCurrentStatus.currentStatus)
        ? undefined
        : filterGroupFindingsCurrentStatus.currentStatus.toUpperCase(),
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
  const nzrVulnsEdges: IVulnerabilityEdge[] =
    vulnerabilitiesConnection === undefined
      ? []
      : vulnerabilitiesConnection.edges;
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
      })
    )
  );

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const filterSearchTextVulnerabilities: IVulnRowAttr[] = filterSearchText(
    vulnerabilities,
    searchTextFilter
  );

  function onTreatmentChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    event.persist();
    setFilterVulnerabilitiesTable(
      (value): IFilterSet => ({
        ...value,
        treatment: event.target.value,
      })
    );
  }
  const filterTreatmentVulnerabilities: IVulnRowAttr[] = filterTreatment(
    vulnerabilities,
    filterVulnerabilitiesTable.treatment
  );
  function onReportDateMaxChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    event.persist();
    setFilterVulnerabilitiesTable(
      (value): IFilterSet => ({
        ...value,
        reportDateRange: { ...value.reportDateRange, max: event.target.value },
      })
    );
  }
  function onReportDateMinChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    event.persist();
    setFilterVulnerabilitiesTable(
      (value): IFilterSet => ({
        ...value,
        reportDateRange: { ...value.reportDateRange, min: event.target.value },
      })
    );
  }
  const filterReportDateRangeVulnerabilities: IVulnRowAttr[] = filterDateRange(
    vulnerabilities,
    filterVulnerabilitiesTable.reportDateRange,
    "reportDate"
  );

  function onTagChange(event: React.ChangeEvent<HTMLInputElement>): void {
    event.persist();
    setFilterVulnerabilitiesTable(
      (value): IFilterSet => ({
        ...value,
        tag: event.target.value,
      })
    );
  }
  const filterTagVulnerabilities: IVulnRowAttr[] = filterText(
    vulnerabilities,
    filterVulnerabilitiesTable.tag,
    "tag"
  );

  function onStatusChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterGroupFindingsCurrentStatus(
      (value): Record<string, string> => ({
        ...value,
        currentStatus: event.target.value,
      })
    );
  }

  function onTreatmentStatusChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    event.persist();
    setFilterVulnerabilitiesTable(
      (value): IFilterSet => ({
        ...value,
        treatmentCurrentStatus: event.target.value,
      })
    );
  }
  const filterTreatmentCurrentStatusVulnerabilities: IVulnRowAttr[] =
    filterTreatmentCurrentStatus(
      vulnerabilities,
      filterVulnerabilitiesTable.treatmentCurrentStatus
    );

  function onVerificationChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    event.persist();
    setFilterVulnerabilitiesTable(
      (value): IFilterSet => ({
        ...value,
        verification: event.target.value,
      })
    );
  }
  const filterVerificationVulnerabilities: IVulnRowAttr[] = filterSelect(
    vulnerabilities,
    filterVulnerabilitiesTable.verification,
    "verification"
  );

  function clearFilters(): void {
    setFilterGroupFindingsCurrentStatus(
      (value): Record<string, string> => ({
        ...value,
        currentStatus: "open",
      })
    );
    setFilterVulnerabilitiesTable(
      (): IFilterSet => ({
        currentStatus: "",
        reportDateRange: { max: "", min: "" },
        status: "open",
        tag: "",
        treatment: "",
        treatmentCurrentStatus: "",
        verification: "",
      })
    );
    setSearchTextFilter("");
  }

  const resultVulnerabilities: IVulnRowAttr[] = _.intersection(
    filterSearchTextVulnerabilities,
    filterTreatmentCurrentStatusVulnerabilities,
    filterTreatmentVulnerabilities,
    filterVerificationVulnerabilities,
    filterReportDateRangeVulnerabilities,
    filterTagVulnerabilities
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
        filterZeroRisk(resultVulnerabilities),
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
        filterZeroRisk(resultVulnerabilities),
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

  const customFiltersProps: IFilterProps[] = [
    {
      defaultValue: filterVulnerabilitiesTable.treatment,
      onChangeSelect: onTreatmentChange,
      placeholder: "Treatment",
      /* eslint-disable sort-keys */
      selectOptions: {
        NEW: "searchFindings.tabDescription.treatment.new",
        IN_PROGRESS: "searchFindings.tabDescription.treatment.inProgress",
        ACCEPTED: "searchFindings.tabDescription.treatment.accepted",
        ACCEPTED_UNDEFINED:
          "searchFindings.tabDescription.treatment.acceptedUndefined",
      },
      /* eslint-enable sort-keys */
      tooltipId: "searchFindings.tabVuln.vulnTable.treatmentsTooltip.id",
      tooltipMessage: "searchFindings.tabVuln.vulnTable.treatmentsTooltip",
      type: "select",
    },
    {
      defaultValue: filterVulnerabilitiesTable.verification,
      onChangeSelect: onVerificationChange,
      placeholder: "Reattacks",
      selectOptions: {
        // eslint-disable-next-line camelcase
        On_hold: "searchFindings.tabVuln.onHold",
        Requested: "searchFindings.tabVuln.requested",
        Verified: "searchFindings.tabVuln.verified",
      },
      tooltipId: "searchFindings.tabVuln.vulnTable.reattacksTooltip.id",
      tooltipMessage: "searchFindings.tabVuln.vulnTable.reattacksTooltip",
      type: "select",
    },
    {
      defaultValue: filterGroupFindingsCurrentStatus.currentStatus,
      onChangeSelect: onStatusChange,
      placeholder: "Status",
      selectOptions: {
        closed: "searchFindings.tabVuln.closed",
        open: "searchFindings.tabVuln.open",
      },
      tooltipId: "searchFindings.tabVuln.statusTooltip.id",
      tooltipMessage: "searchFindings.tabVuln.statusTooltip",
      type: "select",
    },
    {
      defaultValue: filterVulnerabilitiesTable.treatmentCurrentStatus,
      onChangeSelect: onTreatmentStatusChange,
      placeholder: "Treatment Acceptance",
      selectOptions: {
        false: "Accepted",
        true: "Pending",
      },
      tooltipId: "searchFindings.tabVuln.treatmentStatus.id",
      tooltipMessage: "searchFindings.tabVuln.treatmentStatus",
      type: "select",
    },
    {
      defaultValue: filterVulnerabilitiesTable.tag,
      onChangeInput: onTagChange,
      placeholder: "searchFindings.tabVuln.searchTag",
      tooltipId: "searchFindings.tabVuln.tagTooltip.id",
      tooltipMessage: "searchFindings.tabVuln.tagTooltip",
      type: "text",
    },
    {
      defaultValue: "",
      placeholder: "Report date (range)",
      rangeProps: {
        defaultValue: filterVulnerabilitiesTable.reportDateRange,
        onChangeMax: onReportDateMaxChange,
        onChangeMin: onReportDateMinChange,
      },
      tooltipId: "searchFindings.tabVuln.vulnTable.dateTooltip.id",
      tooltipMessage: "searchFindings.tabVuln.vulnTable.dateTooltip",
      type: "dateRange",
    },
  ];

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
                clearFiltersButton={clearFilters}
                customFilters={{
                  customFiltersProps,
                  isCustomFilterEnabled,
                  onUpdateEnableCustomFilter: handleUpdateCustomFilter,
                  resultSize: {
                    current: filterZeroRisk(resultVulnerabilities).length,
                    total: filterZeroRisk(vulnerabilities).length,
                  },
                }}
                customSearch={{
                  customSearchDefault: searchTextFilter,
                  isCustomSearchEnabled: true,
                  onUpdateCustomSearch: onSearchTextChange,
                  position: "right",
                }}
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
                vulnerabilities={
                  isRequestingVerify
                    ? filterZeroRisk(
                        filterCurrentStatus(resultVulnerabilities, "open")
                      )
                    : filterZeroRisk(resultVulnerabilities)
                }
              />
            </div>
            {setColumn()}
          </div>
        </div>
        {isOpen ? (
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
        ) : undefined}
        {isHandleAcceptanceModalOpen ? (
          <HandleAcceptanceModal
            findingId={findingId}
            groupName={groupName}
            handleCloseModal={toggleHandleAcceptanceModal}
            refetchData={refetchVulnsData}
            vulns={vulnerabilities}
          />
        ) : undefined}
        {isEditing ? (
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
        ) : undefined}
      </React.Fragment>
    </React.StrictMode>
  );
};
