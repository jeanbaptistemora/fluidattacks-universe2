import { ActionButtons } from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons";
import type { ApolloError } from "apollo-client";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import type { GraphQLError } from "graphql";
import { HandleAcceptationModal } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal";
import type { IGetFindingVulnInfo } from "scenes/Dashboard/containers/VulnerabilitiesView/types";
import type { IVulnData } from "./HandleAcceptationModal/types";
import type { IVulnDataType } from "scenes/Dashboard/components/Vulnerabilities/types";
import { Logger } from "utils/logger";
import React from "react";
import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import { UpdateZeroRiskModal } from "scenes/Dashboard/containers/VulnerabilitiesView/UpdateZeroRiskModal";
import { VulnerabilitiesView } from "scenes/Dashboard/components/Vulnerabilities/index";
import _ from "lodash";
import { getVulnsPendingOfAcceptation } from "./utils";
import mixpanel from "mixpanel-browser";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { useParams } from "react-router";
import { useQuery } from "@apollo/react-hooks";
import { Col100, ControlLabel, Row } from "styles/styledComponents";

export const VulnsView: React.FC = (): JSX.Element => {
  const { findingId, projectName } = useParams<{
    findingId: string;
    projectName: string;
  }>();
  const { userName } = window as typeof window & Dictionary<string>;

  const onMount: () => void = (): void => {
    mixpanel.track("FindingVulnerabilities", { User: userName });
  };
  React.useEffect(onMount, [userName]);

  const [isOpen, setOpen] = React.useState(false);
  function toggleModal(): void {
    setOpen(true);
  }

  const [
    isUpdateZeroRiskModalOpen,
    setUpdateZeroRiskModalOpen,
  ] = React.useState(false);
  function toggleUpdateZeroRiskModal(): void {
    setUpdateZeroRiskModalOpen(!isUpdateZeroRiskModalOpen);
  }

  const [
    isHandleAcceptationModalOpen,
    setHandleAcceptationModalOpen,
  ] = React.useState(false);
  function toggleHandleAcceptationModal(): void {
    setHandleAcceptationModalOpen(!isHandleAcceptationModalOpen);
  }

  const [remediationModalConfig, setRemediationModalConfig] = React.useState<{
    vulnerabilities: IVulnDataType[];
    clearSelected: () => void;
  }>({
    clearSelected: (): void => undefined,
    vulnerabilities: [],
  });
  function openRemediationModal(
    vulnerabilities: IVulnDataType[],
    clearSelected: () => void
  ): void {
    setRemediationModalConfig({ clearSelected, vulnerabilities });
  }
  function closeRemediationModal(): void {
    setOpen(false);
  }
  const [isEditing, setEditing] = React.useState(false);
  function toggleEdit(): void {
    setEditing(!isEditing);
  }
  const [isConfirmingZeroRisk, setConfirmingZeroRisk] = React.useState(false);
  function toggleConfirmZeroRisk(): void {
    setConfirmingZeroRisk(!isConfirmingZeroRisk);
  }
  const [isRejectingZeroRisk, setRejectingZeroRisk] = React.useState(false);
  function toggleRejectZeroRisk(): void {
    setRejectingZeroRisk(!isRejectingZeroRisk);
  }
  const [isRequestingZeroRisk, setRequestingZeroRisk] = React.useState(false);
  function toggleRequestZeroRisk(): void {
    setRequestingZeroRisk(!isRequestingZeroRisk);
  }
  const [isRequestingVerify, setRequestingVerify] = React.useState(false);
  function toggleRequestVerify(): void {
    setRequestingVerify(!isRequestingVerify);
  }
  const [isVerifying, setVerifying] = React.useState(false);
  function toggleVerify(): void {
    setVerifying(!isVerifying);
  }

  const { data, refetch } = useQuery<IGetFindingVulnInfo>(
    GET_FINDING_VULN_INFO,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(translate.t("group_alerts.error_textsad"));
          Logger.warning("An error occurred loading finding", error);
        });
      },
      variables: { findingId, groupName: projectName },
    }
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.StrictMode />;
  }

  const pendingVulnsToHandleAcceptation: IVulnData[] = getVulnsPendingOfAcceptation(
    data.finding.vulnerabilities
  );
  const canHandleAcceptation: boolean =
    pendingVulnsToHandleAcceptation.length > 0;

  return (
    <React.StrictMode>
      <React.Fragment>
        <ActionButtons
          areVulnsSelected={remediationModalConfig.vulnerabilities.length > 0}
          canHandleAcceptation={canHandleAcceptation}
          isConfirmingZeroRisk={isConfirmingZeroRisk}
          isEditing={isEditing}
          isReattackRequestedInAllVuln={data.finding.newRemediated}
          isRejectingZeroRisk={isRejectingZeroRisk}
          isRequestingReattack={isRequestingVerify}
          isRequestingZeroRisk={isRequestingZeroRisk}
          isVerified={data.finding.verified}
          isVerifying={isVerifying}
          onConfirmZeroRisk={toggleConfirmZeroRisk}
          onEdit={toggleEdit}
          onRejectZeroRisk={toggleRejectZeroRisk}
          onRequestReattack={toggleRequestVerify}
          onRequestZeroRisk={toggleRequestZeroRisk}
          onVerify={toggleVerify}
          openHandleAcceptation={toggleHandleAcceptationModal}
          openModal={toggleModal}
          openUpdateZeroRiskModal={toggleUpdateZeroRiskModal}
          state={data.finding.state}
          subscription={data.project.subscription}
        />
        <Row>
          <Col100>
            <Row>
              <Col100>
                <ControlLabel>
                  <b>{translate.t("search_findings.tab_vuln.open")}</b>
                </ControlLabel>
                <br />
                <VulnerabilitiesView
                  editMode={isEditing}
                  findingId={findingId}
                  isConfirmingZeroRisk={isConfirmingZeroRisk}
                  isRejectingZeroRisk={isRejectingZeroRisk}
                  isRequestVerification={isRequestingVerify}
                  isRequestingZeroRisk={isRequestingZeroRisk}
                  isVerifyRequest={isVerifying}
                  projectName={projectName}
                  separatedRow={true}
                  state={"open"}
                  verificationFn={openRemediationModal}
                />
              </Col100>
            </Row>
            <Row>
              <Col100>
                {isRequestingVerify ? undefined : (
                  <ControlLabel>
                    <b>{translate.t("search_findings.tab_vuln.closed")}</b>
                  </ControlLabel>
                )}
                <br />
                <VulnerabilitiesView
                  editMode={false}
                  findingId={findingId}
                  isRequestVerification={isRequestingVerify}
                  state={"closed"}
                />
              </Col100>
            </Row>
          </Col100>
        </Row>
        {isOpen ? (
          <UpdateVerificationModal
            clearSelected={_.get(remediationModalConfig, "clearSelected")}
            findingId={findingId}
            handleCloseModal={closeRemediationModal}
            isReattacking={isRequestingVerify}
            isVerifying={isVerifying}
            refetchData={refetch}
            setRequestState={toggleRequestVerify}
            setVerifyState={toggleVerify}
            vulns={remediationModalConfig.vulnerabilities}
          />
        ) : undefined}
        {isUpdateZeroRiskModalOpen ? (
          <UpdateZeroRiskModal
            clearSelected={_.get(remediationModalConfig, "clearSelected")}
            findingId={findingId}
            handleCloseModal={toggleUpdateZeroRiskModal}
            isConfirmingZeroRisk={isConfirmingZeroRisk}
            isRejectingZeroRisk={isRejectingZeroRisk}
            isRequestingZeroRisk={isRequestingZeroRisk}
            refetchData={refetch}
            setConfirmState={toggleConfirmZeroRisk}
            setRejectState={toggleRejectZeroRisk}
            setRequestState={toggleRequestZeroRisk}
            vulns={remediationModalConfig.vulnerabilities}
          />
        ) : undefined}
        {isHandleAcceptationModalOpen ? (
          <HandleAcceptationModal
            findingId={findingId}
            handleCloseModal={toggleHandleAcceptationModal}
            refetchData={refetch}
            vulns={pendingVulnsToHandleAcceptation}
          />
        ) : undefined}
      </React.Fragment>
    </React.StrictMode>
  );
};
