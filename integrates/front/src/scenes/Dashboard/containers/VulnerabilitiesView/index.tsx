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
  filterDate,
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
import { HandleAcceptationModal } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import type { IGetFindingVulnInfoAttr } from "scenes/Dashboard/containers/VulnerabilitiesView/types";
import { isPendingToAcceptation } from "scenes/Dashboard/containers/VulnerabilitiesView/utils";
import { authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

export const VulnsView: React.FC = (): JSX.Element => {
  const { findingId, groupName } =
    useParams<{
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
  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [treatmentFilter, setTreatmentFilter] = useState("");
  const [reportDateFilter, setReportDateFilter] = useState("");
  const [tagFilter, setTagFilter] = useState("");
  const [currentStatusFilter, setCurrentStatusFilter] = useState("");
  const [treatmentCurrentStatusFilter, setTreatmentCurrentStatusFilter] =
    useState("");
  const [verificationFilter, setVerificationFilter] = useState("");

  const handleUpdateCustomFilter: () => void = useCallback((): void => {
    setCustomFilterEnabled(!isCustomFilterEnabled);
  }, [isCustomFilterEnabled, setCustomFilterEnabled]);

  const [isHandleAcceptationModalOpen, setHandleAcceptationModalOpen] =
    useState(false);
  function toggleHandleAcceptationModal(): void {
    setHandleAcceptationModalOpen(!isHandleAcceptationModalOpen);
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
    setSearchTextFilter(event.target.value);
  }
  const filterSearchTextVulnerabilities: IVulnRowAttr[] = filterSearchText(
    vulnerabilities,
    searchTextFilter
  );

  function onTreatmentChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    setTreatmentFilter(event.target.value);
  }
  const filterTreatmentVulnerabilities: IVulnRowAttr[] = filterTreatment(
    vulnerabilities,
    treatmentFilter
  );
  function onReportDateChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setReportDateFilter(event.target.value);
  }
  const filterReportDateVulnerabilities: IVulnRowAttr[] = filterDate(
    vulnerabilities,
    reportDateFilter,
    "reportDate"
  );

  function onTagChange(event: React.ChangeEvent<HTMLInputElement>): void {
    setTagFilter(event.target.value);
  }
  const filterTagVulnerabilities: IVulnRowAttr[] = filterText(
    vulnerabilities,
    tagFilter,
    "tag"
  );

  function onStatusChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    setCurrentStatusFilter(event.target.value);
  }
  const filterCurrentStatusVulnerabilities: IVulnRowAttr[] = filterSelect(
    vulnerabilities,
    currentStatusFilter,
    "currentState"
  );

  function onTreatmentStatusChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    setTreatmentCurrentStatusFilter(event.target.value);
  }
  const filterTreatmentCurrentStatusVulnerabilities: IVulnRowAttr[] =
    filterTreatmentCurrentStatus(vulnerabilities, treatmentCurrentStatusFilter);

  function onVerificationChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    setVerificationFilter(event.target.value);
  }
  const filterVerificationVulnerabilities: IVulnRowAttr[] = filterSelect(
    vulnerabilities,
    verificationFilter,
    "verification"
  );

  const resultVulnerabilities: IVulnRowAttr[] = _.intersection(
    filterSearchTextVulnerabilities,
    filterTreatmentCurrentStatusVulnerabilities,
    filterTreatmentVulnerabilities,
    filterCurrentStatusVulnerabilities,
    filterVerificationVulnerabilities,
    filterReportDateVulnerabilities,
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
      defaultValue: reportDateFilter,
      onChangeInput: onReportDateChange,
      placeholder: "Report date",
      tooltipId: "searchFindings.tabVuln.vulnTable.dateTooltip.id",
      tooltipMessage: "searchFindings.tabVuln.vulnTable.dateTooltip",
      type: "date",
    },
    {
      defaultValue: treatmentFilter,
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
      defaultValue: verificationFilter,
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
      defaultValue: currentStatusFilter,
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
      defaultValue: treatmentCurrentStatusFilter,
      onChangeSelect: onTreatmentStatusChange,
      placeholder: "Treatment Acceptation",
      selectOptions: {
        false: "Accepted",
        true: "Pending",
      },
      tooltipId: "searchFindings.tabVuln.treatmentStatus.id",
      tooltipMessage: "searchFindings.tabVuln.treatmentStatus",
      type: "select",
    },
    {
      defaultValue: tagFilter,
      onChangeInput: onTagChange,
      placeholder: "searchFindings.tabVuln.searchTag",
      tooltipId: "searchFindings.tabVuln.tagTooltip.id",
      tooltipMessage: "searchFindings.tabVuln.tagTooltip",
      type: "text",
    },
  ];

  return (
    <React.StrictMode>
      <React.Fragment>
        <div>
          <div>
            <ActionButtons
              areVulnerabilitiesPendingToAcceptation={isPendingToAcceptation(
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
              openHandleAcceptation={toggleHandleAcceptationModal}
              openModal={toggleModal}
              state={data.finding.state}
              subscription={data.group.subscription}
            />
            <div>
              <VulnComponent
                canDisplayHacker={canRetrieveHacker}
                customFilters={{
                  customFiltersProps,
                  isCustomFilterEnabled,
                  onUpdateEnableCustomFilter: handleUpdateCustomFilter,
                }}
                customSearch={{
                  customSearchDefault: searchTextFilter,
                  isCustomSearchEnabled: true,
                  onUpdateCustomSearch: onSearchTextChange,
                }}
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
        {isHandleAcceptationModalOpen ? (
          <HandleAcceptationModal
            findingId={findingId}
            groupName={groupName}
            handleCloseModal={toggleHandleAcceptationModal}
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
