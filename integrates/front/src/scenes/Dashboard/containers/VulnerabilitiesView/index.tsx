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

import { Modal } from "components/Modal";
import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateDescription } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription";
import {
  filterCurrentStatus,
  filterOutVulnerabilities,
  filterZeroRisk,
  getNonSelectableVulnerabilitiesOnReattackIds,
  getNonSelectableVulnerabilitiesOnVerifyIds,
} from "scenes/Dashboard/components/Vulnerabilities/utils";
import { ActionButtons } from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons";
import { HandleAcceptationModal } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import type { IGetFindingVulnInfoAttr } from "scenes/Dashboard/containers/VulnerabilitiesView/types";
import { isPendingToAcceptation } from "scenes/Dashboard/containers/VulnerabilitiesView/utils";
import { ButtonToolbar } from "styles/styledComponents";
import { authzPermissionsContext } from "utils/authz/config";
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

  const [isOpen, setOpen] = useState(false);

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

  const vulnerabilities: IVulnRowAttr[] =
    data.finding.vulnerabilities.concat(zeroRiskVulns);

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
            <ButtonToolbar>
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
            </ButtonToolbar>
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
