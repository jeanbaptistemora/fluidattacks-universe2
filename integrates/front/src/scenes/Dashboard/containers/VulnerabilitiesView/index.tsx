import { ActionButtons } from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons";
import type { ApolloError } from "apollo-client";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import type { GraphQLError } from "graphql";
import { HandleAcceptationModal } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal";
import type { IGetFindingVulnInfo } from "scenes/Dashboard/containers/VulnerabilitiesView/types";
import type { IVulnDataType } from "scenes/Dashboard/components/Vulnerabilities/types";
import { Logger } from "utils/logger";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities/newIndex";
import _ from "lodash";
import { authzPermissionsContext } from "utils/authz/config";
import { filterZeroRisk } from "scenes/Dashboard/components/Vulnerabilities/utils";
import mixpanel from "mixpanel-browser";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { useAbility } from "@casl/react";
import { useParams } from "react-router";
import { useQuery } from "@apollo/react-hooks";
import { Col100, Row } from "styles/styledComponents";

export const VulnsView: React.FC = (): JSX.Element => {
  const { findingId, projectName } = useParams<{
    findingId: string;
    projectName: string;
  }>();
  const { userName } = window as typeof window & Dictionary<string>;
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canConfirmZeroRiskVuln: boolean = permissions.can(
    "backend_api_mutations_confirm_zero_risk_vuln_mutate"
  );
  const canRejectZeroRiskVuln: boolean = permissions.can(
    "backend_api_mutations_reject_zero_risk_vuln_mutate"
  );
  const shouldFilterZeroRisk: boolean = !(
    canConfirmZeroRiskVuln || canRejectZeroRiskVuln
  );

  const onMount: () => void = (): void => {
    mixpanel.track("FindingVulnerabilities", { User: userName });
  };
  React.useEffect(onMount, [userName]);

  const [isOpen, setOpen] = React.useState(false);
  function toggleModal(): void {
    setOpen(true);
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
  const openRemediationModal: (
    vulnerabilities: IVulnDataType[],
    clearSelected: () => void
  ) => void = React.useCallback(
    (vulnerabilities: IVulnDataType[], clearSelected: () => void): void => {
      setRemediationModalConfig({ clearSelected, vulnerabilities });
    },
    []
  );

  function closeRemediationModal(): void {
    setOpen(false);
  }
  const [isEditing, setEditing] = React.useState(false);
  function toggleEdit(): void {
    setEditing(!isEditing);
  }
  const [isRejectingZeroRisk] = React.useState(false);
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

  return (
    <React.StrictMode>
      <React.Fragment>
        <Row>
          <Col100>
            <ActionButtons
              areVulnsSelected={
                remediationModalConfig.vulnerabilities.length > 0
              }
              isEditing={isEditing}
              isReattackRequestedInAllVuln={data.finding.newRemediated}
              isRejectingZeroRisk={isRejectingZeroRisk}
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
          </Col100>
        </Row>
        <Row>
          <Col100>
            <Row>
              <VulnComponent
                findingId={findingId}
                groupName={projectName}
                isEditing={isEditing}
                isRejectingZeroRisk={isRejectingZeroRisk}
                isRequestingReattack={isRequestingVerify}
                isVerifyingRequest={isVerifying}
                onVulnSelect={openRemediationModal}
                vulnerabilities={
                  shouldFilterZeroRisk
                    ? filterZeroRisk(data.finding.vulnerabilities)
                    : data.finding.vulnerabilities
                }
              />
            </Row>
          </Col100>
        </Row>
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
            vulns={data.finding.vulnerabilities}
          />
        ) : undefined}
      </React.Fragment>
    </React.StrictMode>
  );
};
