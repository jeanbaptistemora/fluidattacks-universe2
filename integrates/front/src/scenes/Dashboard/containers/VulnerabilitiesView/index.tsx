/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/

import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import type { IFilterProps } from "components/DataTableNext/types";
import {
  filterDateRange,
  filterSearchText,
  filterSelect,
  filterText,
} from "components/DataTableNext/utils";
import { Modal } from "components/Modal";
import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateDescription } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription";
import {
  filterCurrentStatus,
  filterOutVulnerabilities,
  filterTreatment,
  filterTreatmentCurrentStatus,
  filterZeroRisk,
  getNonSelectableVulnerabilitiesOnReattackIds,
  getNonSelectableVulnerabilitiesOnVerifyIds,
} from "scenes/Dashboard/components/Vulnerabilities/utils";
import { ActionButtons } from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons";
import { HandleAcceptanceModal } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptanceModal";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import type { IGetFindingVulnInfoAttr } from "scenes/Dashboard/containers/VulnerabilitiesView/types";
import { isPendingToAcceptance } from "scenes/Dashboard/containers/VulnerabilitiesView/utils";
import { authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface IFilterSet {
  currentStatus: string;
  reportDateRange: { max: string; min: string };
  searchText: string;
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
    "api_resolvers_finding_zero_risk_resolve"
  );

  const [isOpen, setOpen] = useState(false);

  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("locationsCustomFilters", false);

  const [filterVulnerabilitiesTable, setFilterVulnerabilitiesTable] =
    useStoredState(
      "filterVulnerabilitiesSet",
      {
        currentStatus: "",
        reportDateRange: { max: "", min: "" },
        searchText: "",
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

  const [isHandleAcceptanceModalOpen, setHandleAcceptanceModalOpen] =
    useState(false);
  function toggleHandleAcceptanceModal(): void {
    setHandleAcceptanceModalOpen(!isHandleAcceptanceModalOpen);
  }

  const [remediationModalConfig, setRemediationModalConfig] = useState<{
    vulnerabilities: IVulnRowAttr[];
    clearSelected: () => void;
  }>({
    clearSelected: (): void => undefined,
    vulnerabilities: [],
  });
  const openRemediationModal: (
    vulnerabilities: IVulnRowAttr[],
    clearSelected: () => void
  ) => void = useCallback(
    (vulnerabilities: IVulnRowAttr[], clearSelected: () => void): void => {
      setRemediationModalConfig({ clearSelected, vulnerabilities });
    },
    []
  );

  function closeRemediationModal(): void {
    setOpen(false);
  }
  const [isEditing, setEditing] = useState(false);
  function toggleEdit(): void {
    setEditing(!isEditing);
  }
  function handleCloseUpdateModal(): void {
    setEditing(false);
  }
  const [isRequestingVerify, setRequestingVerify] = useState(false);
  const [isVerifying, setVerifying] = useState(false);

  const { data, refetch } = useQuery<IGetFindingVulnInfoAttr>(
    GET_FINDING_VULN_INFO,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred loading finding", error);
        });
      },
      variables: {
        canRetrieveHacker,
        canRetrieveZeroRisk,
        findingId,
        groupName,
      },
    }
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.StrictMode />;
  }

  const zeroRiskVulns: IVulnRowAttr[] = data.finding.zeroRisk
    ? data.finding.zeroRisk
    : [];

  const vulnerabilities: IVulnRowAttr[] =
    data.finding.vulnerabilities.concat(zeroRiskVulns);

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    event.persist();
    setFilterVulnerabilitiesTable(
      (value): IFilterSet => ({
        ...value,
        searchText: event.target.value,
      })
    );
  }
  const filterSearchTextVulnerabilities: IVulnRowAttr[] = filterSearchText(
    vulnerabilities,
    filterVulnerabilitiesTable.searchText
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
  const filterCurrentStatusVulnerabilities: IVulnRowAttr[] = filterSelect(
    vulnerabilities,
    filterGroupFindingsCurrentStatus.currentStatus,
    "currentState"
  );

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

  const resultVulnerabilities: IVulnRowAttr[] = _.intersection(
    filterSearchTextVulnerabilities,
    filterTreatmentCurrentStatusVulnerabilities,
    filterTreatmentVulnerabilities,
    filterCurrentStatusVulnerabilities,
    filterVerificationVulnerabilities,
    filterReportDateRangeVulnerabilities,
    filterTagVulnerabilities
  );

  const isFindingReleased: boolean = !_.isEmpty(data.finding.releaseDate);
  function toggleModal(): void {
    setOpen(true);
  }
  function toggleRequestVerify(): void {
    if (isRequestingVerify) {
      setRequestingVerify(!isRequestingVerify);
    } else {
      const selectedVulnerabilities: IVulnRowAttr[] =
        remediationModalConfig.vulnerabilities;
      const newVulnerabilities: IVulnRowAttr[] = filterOutVulnerabilities(
        selectedVulnerabilities,
        filterZeroRisk(resultVulnerabilities),
        getNonSelectableVulnerabilitiesOnReattackIds
      );
      if (selectedVulnerabilities.length > newVulnerabilities.length) {
        setRequestingVerify(!isRequestingVerify);
        msgError(t("searchFindings.tabVuln.errors.selectedVulnerabilities"));
      } else if (selectedVulnerabilities.length > 0) {
        setOpen(true);
        setRequestingVerify(!isRequestingVerify);
      } else {
        setRequestingVerify(!isRequestingVerify);
      }
    }
  }

  function toggleVerify(): void {
    if (isVerifying) {
      setVerifying(!isVerifying);
    } else {
      const selectedVulnerabilities: IVulnRowAttr[] =
        remediationModalConfig.vulnerabilities;
      const newVulnerabilities: IVulnRowAttr[] = filterOutVulnerabilities(
        selectedVulnerabilities,
        filterZeroRisk(resultVulnerabilities),
        getNonSelectableVulnerabilitiesOnVerifyIds
      );
      if (selectedVulnerabilities.length > newVulnerabilities.length) {
        setVerifying(!isVerifying);
        msgError(t("searchFindings.tabVuln.errors.selectedVulnerabilities"));
      } else if (selectedVulnerabilities.length > 0) {
        setOpen(true);
        setVerifying(!isVerifying);
      } else {
        setVerifying(!isVerifying);
      }
    }
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
      placeholder: "Report date (Range)",
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

  return (
    <React.StrictMode>
      <React.Fragment>
        <div>
          <div>
            <div>
              <VulnComponent
                canDisplayHacker={canRetrieveHacker}
                customFilters={{
                  customFiltersProps,
                  isCustomFilterEnabled,
                  onUpdateEnableCustomFilter: handleUpdateCustomFilter,
                  resultSize: {
                    current: resultVulnerabilities.length,
                    total: vulnerabilities.length,
                  },
                }}
                customSearch={{
                  customSearchDefault: filterVulnerabilitiesTable.searchText,
                  isCustomSearchEnabled: true,
                  onUpdateCustomSearch: onSearchTextChange,
                }}
                extraButtons={
                  <ActionButtons
                    areVulnerabilitiesPendingToAcceptance={isPendingToAcceptance(
                      resultVulnerabilities
                    )}
                    areVulnsSelected={
                      remediationModalConfig.vulnerabilities.length > 0
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
                    subscription={data.group.subscription}
                  />
                }
                findingId={findingId}
                findingState={data.finding.state}
                groupName={groupName}
                isEditing={isEditing}
                isFindingReleased={isFindingReleased}
                isRequestingReattack={isRequestingVerify}
                isVerifyingRequest={isVerifying}
                onVulnSelect={openRemediationModal}
                vulnerabilities={
                  isRequestingVerify
                    ? filterZeroRisk(
                        filterCurrentStatus(resultVulnerabilities, "open")
                      )
                    : filterZeroRisk(resultVulnerabilities)
                }
              />
            </div>
          </div>
        </div>
        {isOpen ? (
          <UpdateVerificationModal
            clearSelected={_.get(remediationModalConfig, "clearSelected")}
            findingId={findingId}
            groupName={groupName}
            handleCloseModal={closeRemediationModal}
            isReattacking={isRequestingVerify}
            isVerifying={isVerifying}
            setRequestState={toggleRequestVerify}
            setVerifyState={toggleVerify}
            vulns={remediationModalConfig.vulnerabilities}
          />
        ) : undefined}
        {isHandleAcceptanceModalOpen ? (
          <HandleAcceptanceModal
            findingId={findingId}
            groupName={groupName}
            handleCloseModal={toggleHandleAcceptanceModal}
            refetchData={refetch}
            vulns={resultVulnerabilities}
          />
        ) : undefined}
        {isEditing ? (
          <Modal
            headerTitle={t("searchFindings.tabDescription.editVuln")}
            onEsc={handleCloseUpdateModal}
            open={isEditing}
            size={"largeModal"}
          >
            <UpdateDescription
              findingId={findingId}
              groupName={groupName}
              handleClearSelected={_.get(
                remediationModalConfig,
                "clearSelected"
              )}
              handleCloseModal={handleCloseUpdateModal}
              vulnerabilities={remediationModalConfig.vulnerabilities}
            />
          </Modal>
        ) : undefined}
      </React.Fragment>
    </React.StrictMode>
  );
};
