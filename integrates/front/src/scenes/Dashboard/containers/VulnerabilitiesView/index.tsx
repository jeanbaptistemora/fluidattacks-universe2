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
import { useParams } from "react-router";

import {
  ActionsContainer,
  Filters,
  SearchText,
  Select,
  SelectContainer,
} from "./styles";

import { TooltipWrapper } from "components/TooltipWrapper";
import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";
import type {
  IVulnDataTypeAttr,
  IVulnRowAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import {
  filterCurrentStatus,
  filterText,
  filterTreatment,
  filterVerification,
  filterZeroRisk,
} from "scenes/Dashboard/components/Vulnerabilities/utils";
import { ActionButtons } from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons";
import { HandleAcceptationModal } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import type { IGetFindingVulnInfoAttr } from "scenes/Dashboard/containers/VulnerabilitiesView/types";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

export const VulnsView: React.FC = (): JSX.Element => {
  const { findingId, projectName } = useParams<{
    findingId: string;
    projectName: string;
  }>();
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRetrieveAnalyst: boolean = permissions.can(
    "api_resolvers_vulnerability_analyst_resolve"
  );
  const canRetrieveZeroRisk: boolean = permissions.can(
    "api_resolvers_finding_zero_risk_resolve"
  );

  const [treatmentFilter, setTreatmentFilter] = useState("");
  const [currentStatusFilter, setCurrentStatusFilter] = useState("");
  const [verificationFilter, setVerificationFilter] = useState("");
  const [textFilter, setTextFilter] = useState("");
  const [isOpen, setOpen] = useState(false);
  function toggleModal(): void {
    setOpen(true);
  }

  const [
    isHandleAcceptationModalOpen,
    setHandleAcceptationModalOpen,
  ] = useState(false);
  function toggleHandleAcceptationModal(): void {
    setHandleAcceptationModalOpen(!isHandleAcceptationModalOpen);
  }

  const [remediationModalConfig, setRemediationModalConfig] = useState<{
    vulnerabilities: IVulnDataTypeAttr[];
    clearSelected: () => void;
  }>({
    clearSelected: (): void => undefined,
    vulnerabilities: [],
  });
  const openRemediationModal: (
    vulnerabilities: IVulnDataTypeAttr[],
    clearSelected: () => void
  ) => void = useCallback(
    (vulnerabilities: IVulnDataTypeAttr[], clearSelected: () => void): void => {
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
  const [isRequestingVerify, setRequestingVerify] = useState(false);
  function toggleRequestVerify(): void {
    setRequestingVerify(!isRequestingVerify);
  }
  const [isVerifying, setVerifying] = useState(false);
  function toggleVerify(): void {
    setVerifying(!isVerifying);
  }

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
        canRetrieveAnalyst,
        canRetrieveZeroRisk,
        findingId,
        groupName: projectName,
      },
    }
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.StrictMode />;
  }

  const zeroRiskVulns: IVulnRowAttr[] = data.finding.zeroRisk
    ? data.finding.zeroRisk
    : [];

  const vulns: IVulnRowAttr[] = data.finding.vulnerabilities.concat(
    zeroRiskVulns
  );

  function onTreatmentChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    setTreatmentFilter(event.target.value);
  }
  function onStatusChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    setCurrentStatusFilter(event.target.value);
  }
  function onVerificationChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    setVerificationFilter(event.target.value);
  }
  function onSearchChange(event: React.ChangeEvent<HTMLInputElement>): void {
    setTextFilter(event.target.value);
  }
  const filterTreatmentVulnerabilities: IVulnRowAttr[] = filterTreatment(
    vulns,
    treatmentFilter
  );
  const filterCurrentStatusVulnerabilities: IVulnRowAttr[] = filterCurrentStatus(
    vulns,
    currentStatusFilter
  );
  const filterVerificationVulnerabilities: IVulnRowAttr[] = filterVerification(
    vulns,
    verificationFilter
  );
  const filterTextVulnerabilities: IVulnRowAttr[] = filterText(
    vulns,
    textFilter
  );

  const vulnerabilities: IVulnRowAttr[] = _.intersection(
    filterTreatmentVulnerabilities,
    filterCurrentStatusVulnerabilities,
    filterVerificationVulnerabilities,
    filterTextVulnerabilities
  );
  const isFindingReleased: boolean = !_.isEmpty(data.finding.releaseDate);

  return (
    <React.StrictMode>
      <React.Fragment>
        <div>
          <div>
            <ActionsContainer>
              <Filters>
                <SelectContainer>
                  <SearchText
                    defaultValue={textFilter}
                    onChange={onSearchChange}
                    placeholder={t("searchFindings.tabVuln.searchText")}
                  />
                </SelectContainer>
                <SelectContainer>
                  <TooltipWrapper
                    id={"searchFindings.tabVuln.vulnTable.treatmentsTooltip.id"}
                    message={t(
                      "searchFindings.tabVuln.vulnTable.treatmentsTooltip"
                    )}
                  >
                    <Select
                      defaultValue={treatmentFilter}
                      onChange={onTreatmentChange}
                    >
                      <option value={""}>
                        {t("searchFindings.tabVuln.vulnTable.treatments")}
                      </option>
                      <option value={"NEW"}>
                        {t("searchFindings.tabDescription.treatment.new")}
                      </option>
                      <option value={"IN_PROGRESS"}>
                        {t(
                          "searchFindings.tabDescription.treatment.inProgress"
                        )}
                      </option>
                      <option value={"ACCEPTED"}>
                        {t("searchFindings.tabDescription.treatment.accepted")}
                      </option>
                      <option value={"ACCEPTED_UNDEFINED"}>
                        {t(
                          "searchFindings.tabDescription.treatment.acceptedUndefined"
                        )}
                      </option>
                    </Select>
                  </TooltipWrapper>
                </SelectContainer>
                <SelectContainer>
                  <TooltipWrapper
                    id={"searchFindings.tabVuln.vulnTable.reattacksTooltip.id"}
                    message={t(
                      "searchFindings.tabVuln.vulnTable.reattacksTooltip"
                    )}
                  >
                    <Select
                      defaultValue={verificationFilter}
                      onChange={onVerificationChange}
                    >
                      <option value={""}>
                        {t("searchFindings.tabVuln.vulnTable.reattacks")}
                      </option>
                      <option value={"Requested"}>
                        {t("searchFindings.tabVuln.requested")}
                      </option>
                      <option value={"Verified"}>
                        {t("searchFindings.tabVuln.verified")}
                      </option>
                    </Select>
                  </TooltipWrapper>
                </SelectContainer>
                <SelectContainer>
                  <TooltipWrapper
                    id={"searchFindings.tabVuln.statusTooltip.id"}
                    message={t("searchFindings.tabVuln.statusTooltip")}
                  >
                    <Select
                      defaultValue={currentStatusFilter}
                      onChange={onStatusChange}
                    >
                      <option value={""}>
                        {t("searchFindings.tabVuln.status")}
                      </option>
                      <option value={"open"}>
                        {t("searchFindings.tabVuln.open")}
                      </option>
                      <option value={"closed"}>
                        {t("searchFindings.tabVuln.closed")}
                      </option>
                    </Select>
                  </TooltipWrapper>
                </SelectContainer>
              </Filters>
              <ActionButtons
                areVulnsSelected={
                  remediationModalConfig.vulnerabilities.length > 0
                }
                isEditing={isEditing}
                isFindingReleased={isFindingReleased}
                isReattackRequestedInAllVuln={data.finding.newRemediated}
                isRequestingReattack={isRequestingVerify}
                isVerified={data.finding.verified}
                isVerifying={isVerifying}
                onEdit={toggleEdit}
                onRequestReattack={toggleRequestVerify}
                onVerify={toggleVerify}
                openHandleAcceptation={toggleHandleAcceptationModal}
                openModal={toggleModal}
                state={data.finding.state}
                subscription={data.project.subscription}
              />
            </ActionsContainer>
            <div>
              <VulnComponent
                canDisplayAnalyst={canRetrieveAnalyst}
                findingId={findingId}
                groupName={projectName}
                isEditing={isEditing}
                isFindingReleased={isFindingReleased}
                isRequestingReattack={isRequestingVerify}
                isVerifyingRequest={isVerifying}
                onVulnSelect={openRemediationModal}
                vulnerabilities={filterZeroRisk(vulnerabilities)}
              />
            </div>
          </div>
        </div>
        {isOpen ? (
          <UpdateVerificationModal
            clearSelected={_.get(remediationModalConfig, "clearSelected")}
            findingId={findingId}
            groupName={projectName}
            handleCloseModal={closeRemediationModal}
            isReattacking={isRequestingVerify}
            isVerifying={isVerifying}
            refetchData={refetch}
            setRequestState={toggleRequestVerify}
            setVerifyState={toggleVerify}
            vulns={remediationModalConfig.vulnerabilities}
          />
        ) : undefined}
        {isHandleAcceptationModalOpen ? (
          <HandleAcceptationModal
            findingId={findingId}
            groupName={projectName}
            handleCloseModal={toggleHandleAcceptationModal}
            refetchData={refetch}
            vulns={vulnerabilities}
          />
        ) : undefined}
      </React.Fragment>
    </React.StrictMode>
  );
};
