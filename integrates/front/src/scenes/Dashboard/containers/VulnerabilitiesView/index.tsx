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

import {
  ActionsContainer,
  Filters,
  SearchText,
  Select,
  SelectContainer,
  SelectDate,
} from "./styles";

import { FiltersButton } from "components/FiltersButton";
import { Modal } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateDescription } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription";
import {
  filterCurrentStatus,
  filterOutVulnerabilities,
  filterReportDate,
  filterTag,
  filterText,
  filterTreatment,
  filterTreatmentCurrentStatus,
  filterVerification,
  filterZeroRisk,
  getNonSelectableVulnerabilitiesOnReattackIds,
  getNonSelectableVulnerabilitiesOnVerifyIds,
} from "scenes/Dashboard/components/Vulnerabilities/utils";
import { ActionButtons } from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons";
import { HandleAcceptationModal } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import type { IGetFindingVulnInfoAttr } from "scenes/Dashboard/containers/VulnerabilitiesView/types";
import { isPendingToAcceptation } from "scenes/Dashboard/containers/VulnerabilitiesView/utils";
import { ButtonToolbarRow, Col50Ph, Row } from "styles/styledComponents";
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
  const canRetrieveAnalyst: boolean = permissions.can(
    "api_resolvers_vulnerability_analyst_resolve"
  );
  const canRetrieveZeroRisk: boolean = permissions.can(
    "api_resolvers_finding_zero_risk_resolve"
  );

  const [treatmentFilter, setTreatmentFilter] = useState("");
  const [reportDateFilter, setReportDateFilter] = useState("");
  const [tagFilter, setTagFilter] = useState("");
  const [currentStatusFilter, setCurrentStatusFilter] = useState("");
  const [treatmentCurrentStatusFilter, setTreatmentCurrentStatusFilter] =
    useState("");
  const [verificationFilter, setVerificationFilter] = useState("");
  const [textFilter, setTextFilter] = useState("");
  const [isOpen, setOpen] = useState(false);
  const [isFilterEnabled, setFilterEnabled] = useStoredState<boolean>(
    "vulnerabilitiesFilters",
    false
  );

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

  const handleUpdateFilter: () => void = useCallback((): void => {
    setFilterEnabled(!isFilterEnabled);
  }, [isFilterEnabled, setFilterEnabled]);

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
        canRetrieveAnalyst,
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

  const vulns: IVulnRowAttr[] =
    data.finding.vulnerabilities.concat(zeroRiskVulns);

  function onTreatmentChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    setTreatmentFilter(event.target.value);
  }
  function onReportDateChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setReportDateFilter(event.target.value);
  }
  function onTagChange(event: React.ChangeEvent<HTMLInputElement>): void {
    setTagFilter(event.target.value);
  }
  function onStatusChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    setCurrentStatusFilter(event.target.value);
  }
  function onTreatmentStatusChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    setTreatmentCurrentStatusFilter(event.target.value);
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
  const filterReportDateVulnerabilities: IVulnRowAttr[] = filterReportDate(
    vulns,
    reportDateFilter
  );
  const filterTagVulnerabilities: IVulnRowAttr[] = filterTag(vulns, tagFilter);
  const filterCurrentStatusVulnerabilities: IVulnRowAttr[] = isRequestingVerify
    ? vulns
    : filterCurrentStatus(vulns, currentStatusFilter);
  const filterTreatmentCurrentStatusVulnerabilities: IVulnRowAttr[] =
    filterTreatmentCurrentStatus(vulns, treatmentCurrentStatusFilter);
  const filterVerificationVulnerabilities: IVulnRowAttr[] = filterVerification(
    vulns,
    verificationFilter
  );
  const filterTextVulnerabilities: IVulnRowAttr[] = filterText(
    vulns,
    textFilter
  );

  const vulnerabilities: IVulnRowAttr[] = _.intersection(
    filterTreatmentCurrentStatusVulnerabilities,
    filterTreatmentVulnerabilities,
    filterCurrentStatusVulnerabilities,
    filterVerificationVulnerabilities,
    filterTextVulnerabilities,
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
        filterZeroRisk(vulnerabilities),
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
        filterZeroRisk(vulnerabilities),
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

  return (
    <React.StrictMode>
      <React.Fragment>
        <div>
          <div>
            <ActionsContainer>
              <SelectContainer>
                <Row>
                  <Col50Ph>
                    <SearchText
                      defaultValue={textFilter}
                      onChange={onSearchChange}
                      placeholder={t("searchFindings.tabVuln.searchText")}
                    />
                  </Col50Ph>
                  <ButtonToolbarRow>
                    <FiltersButton
                      isFilterEnabled={isFilterEnabled}
                      onUpdateEnableFilter={handleUpdateFilter}
                    />
                  </ButtonToolbarRow>
                </Row>
              </SelectContainer>
              <ActionButtons
                areVulnerabilitiesPendingToAcceptation={isPendingToAcceptation(
                  vulnerabilities
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
            </ActionsContainer>
            {isFilterEnabled ? (
              <React.Fragment>
                <br />
                <Filters>
                  <SelectContainer>
                    <TooltipWrapper
                      id={"searchFindings.tabVuln.vulnTable.dateTooltip.id"}
                      message={t(
                        "searchFindings.tabVuln.vulnTable.dateTooltip"
                      )}
                    >
                      <SelectDate
                        defaultValue={reportDateFilter}
                        onChange={onReportDateChange}
                      />
                    </TooltipWrapper>
                  </SelectContainer>
                  <SelectContainer>
                    <TooltipWrapper
                      id={
                        "searchFindings.tabVuln.vulnTable.treatmentsTooltip.id"
                      }
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
                          {t(
                            "searchFindings.tabDescription.treatment.accepted"
                          )}
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
                      id={
                        "searchFindings.tabVuln.vulnTable.reattacksTooltip.id"
                      }
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
                  <SelectContainer>
                    <TooltipWrapper
                      id={"searchFindings.tabVuln.treatmentStatus.id"}
                      message={t("searchFindings.tabVuln.treatmentStatus")}
                    >
                      <Select
                        defaultValue={treatmentCurrentStatusFilter}
                        onChange={onTreatmentStatusChange}
                      >
                        <option value={""}>{"Treatment Acceptation"}</option>
                        <option value={"true"}>{"Pending"}</option>
                        <option value={"false"}>{"Accepted"}</option>
                      </Select>
                    </TooltipWrapper>
                  </SelectContainer>
                  <SelectContainer>
                    <TooltipWrapper
                      id={"searchFindings.tabVuln.tagTooltip.id"}
                      message={t("searchFindings.tabVuln.tagTooltip")}
                    >
                      <SearchText
                        defaultValue={tagFilter}
                        onChange={onTagChange}
                        placeholder={t("searchFindings.tabVuln.searchTag")}
                      />
                    </TooltipWrapper>
                  </SelectContainer>
                </Filters>
              </React.Fragment>
            ) : undefined}

            <div>
              <VulnComponent
                canDisplayAnalyst={canRetrieveAnalyst}
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
                        filterCurrentStatus(vulnerabilities, "open")
                      )
                    : filterZeroRisk(vulnerabilities)
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
            refetchData={refetch}
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
            vulns={vulnerabilities}
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
