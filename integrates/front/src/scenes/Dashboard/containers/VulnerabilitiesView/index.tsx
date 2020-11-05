/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { useParams } from "react-router";

import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import { VulnerabilitiesView } from "scenes/Dashboard/components/Vulnerabilities/index";
import { IVulnDataType } from "scenes/Dashboard/components/Vulnerabilities/types";
import { getLastTreatment } from "scenes/Dashboard/containers/DescriptionView/utils";
import { ActionButtons } from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { Col100, ControlLabel } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

type verificationFn = (
  vulnerabilities: IVulnDataType[], type: "request" | "verify", clearSelected: () => void,
) => void;

const vulnsView: React.FC = (): JSX.Element => {
  const { findingId, projectName } = useParams<{ findingId: string; projectName: string }>();
  const { userName } = window as typeof window & Dictionary<string>;

  const onMount: (() => void) = (): void => {
    mixpanel.track("FindingVulnerabilities", { User: userName });
  };
  React.useEffect(onMount, []);

  const [remediationModalConfig, setRemediationModalConfig] = React.useState<{
    open: boolean;
    type: "request" | "verify";
    vulnerabilities: IVulnDataType[];
    clearSelected(): void;
  }>({
    clearSelected: (): void => undefined,
    open: false,
    type: "request",
    vulnerabilities: [],
  });
  const openRemediationModal: verificationFn = (
    vulnerabilities: IVulnDataType[], type: "request" | "verify", clearSelected: () => void,
  ): void => {
    setRemediationModalConfig({ open: true, type, vulnerabilities, clearSelected });
  };
  const closeRemediationModal: (() => void) = (): void => {
    setRemediationModalConfig({
      clearSelected: (): void => undefined,
      open: false,
      type: "request",
      vulnerabilities: [],
    });
  };
  const [isEditing, setEditing] = React.useState(false);
  const toggleEdit: (() => void) = (): void => {
    setEditing(!isEditing);
  };
  const [isRequestingVerify, setRequestingVerify] = React.useState(false);
  const toggleRequestVerify: (() => void) = (): void => {
    setRequestingVerify(!isRequestingVerify);
  };
  const [isVerifying, setVerifying] = React.useState(false);
  const toggleVerify: (() => void) = (): void => {
    setVerifying(!isVerifying);
  };

  const { data, refetch } = useQuery(GET_FINDING_VULN_INFO, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred loading finding", error);
      });
    },
    variables: { findingId, groupName: projectName },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  return (
    <React.StrictMode>
      <React.Fragment>
        <ActionButtons
          isEditing={isEditing}
          isReattackRequestedInAllVuln={data.finding.newRemediated}
          isRequestingReattack={isRequestingVerify}
          isVerified={data.finding.verified}
          isVerifying={isVerifying}
          onEdit={toggleEdit}
          onRequestReattack={toggleRequestVerify}
          onVerify={toggleVerify}
          state={data.finding.state}
          subscription={data.project.subscription}
        />
        <Row>
          <Col md={12}>
            <Row>
              <Col100>
                <ControlLabel>
                  <b>{translate.t("search_findings.tab_vuln.open")}</b>
                </ControlLabel>
                <br />
                <VulnerabilitiesView
                  editMode={isEditing}
                  findingId={findingId}
                  isRequestVerification={isRequestingVerify}
                  isVerifyRequest={isVerifying}
                  lastTreatment={getLastTreatment(data.finding.historicTreatment)}
                  projectName={projectName}
                  separatedRow={true}
                  state="open"
                  verificationFn={openRemediationModal}
                />
              </Col100>
            </Row>
            <Row>
              <Col100>
                <ControlLabel>
                  <b>{translate.t("search_findings.tab_vuln.closed")}</b>
                </ControlLabel>
                <br />
                <VulnerabilitiesView
                  editMode={false}
                  findingId={findingId}
                  state="closed"
                />
              </Col100>
            </Row>
          </Col>
        </Row>
        {remediationModalConfig.open ? (
          <UpdateVerificationModal
            clearSelected={_.get(remediationModalConfig, "clearSelected")}
            findingId={findingId}
            handleCloseModal={closeRemediationModal}
            isOpen={true}
            refetchData={refetch}
            remediationType={remediationModalConfig.type}
            setRequestState={toggleRequestVerify}
            setVerifyState={toggleVerify}
            vulns={remediationModalConfig.vulnerabilities}
          />
        ) : undefined}
      </React.Fragment>
    </React.StrictMode>
  );
};

export { vulnsView as VulnsView };
