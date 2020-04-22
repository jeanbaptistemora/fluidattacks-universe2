/* tslint:disable:jsx-no-multiline-js
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of readability of the code
 */
import { useMutation } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { DataTableNext } from "../../../../components/DataTableNext";
import { changeVulnStateFormatter } from "../../../../components/DataTableNext/formatters";
import { IHeader } from "../../../../components/DataTableNext/types";
import { authzContext } from "../../../../utils/authz/config";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { GET_FINDING_HEADER } from "../../containers/FindingContent/queries";
import { RemediationModal } from "../RemediationModal/index";
import { GET_VULNERABILITIES } from "../Vulnerabilities/queries";
import { default as style } from "./index.css";
import { REQUEST_VERIFICATION_VULN, VERIFY_VULNERABILITIES } from "./queries";
import { IRequestVerificationVulnResult, IVerifyRequestVulnResult } from "./types";

interface IVulnData {
  currentState: string;
  id: string;
  specific: string;
  where: string;
}
export interface IUpdateVerificationModal {
  findingId: string;
  isOpen: boolean;
  remediationType: "request" | "verify";
  vulns: IVulnData[];
  clearSelected(): void;
  handleCloseModal(): void;
  refetchData(): void;
  setRequestState(): void;
  setVerifyState(): void;
}

const updateVerificationModal: React.FC<IUpdateVerificationModal> = (props: IUpdateVerificationModal): JSX.Element => {
  const permissions: PureAbility<string> = useAbility(authzContext);
  const canDisplayAnalyst: boolean = permissions.can("backend_api_dataloaders_finding__get_analyst");

  // State management
  const [vulnerabilitiesList, setVulnerabilities] = React.useState(props.vulns);
  const closeRemediationModal: (() => void) = (): void => { props.handleCloseModal(); };

  // GraphQL operations
  const [requestVerification, { loading: submittingRequest }] = useMutation(REQUEST_VERIFICATION_VULN, {
    onCompleted: (data: IRequestVerificationVulnResult): void => {
      if (data.requestVerificationVuln.success) {
        msgSuccess(
          translate.t("proj_alerts.verified_success"),
          translate.t("proj_alerts.updated_title"),
        );
        props.refetchData();
        props.clearSelected();
        props.setRequestState();
      }
    },
    onError: (error: ApolloError): void => {
      error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Request verification already requested":
            msgError(translate.t("proj_alerts.verification_already_requested"));
            break;
          case "Exception - The vulnerability has already been closed":
            msgError(translate.t("proj_alerts."));
            break;
          case "Exception - Vulnerability not found":
            msgError(translate.t("proj_alerts.no_found"));
            break;
          default:
            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error("An error occurred requesting verification", error);
        }
      });
    },
    refetchQueries: [
      { query: GET_VULNERABILITIES, variables: { analystField: canDisplayAnalyst, identifier: props.findingId } },
    ],
  });

  const [verifyRequest, { loading: submittingVerify }] = useMutation(VERIFY_VULNERABILITIES, {
    onCompleted: (data: IVerifyRequestVulnResult): void => {
      if (data.verifyRequestVuln.success) {
        msgSuccess(
          translate.t("proj_alerts.verified_success"),
          translate.t("proj_alerts.updated_title"),
        );
        props.refetchData();
        props.clearSelected();
        props.setVerifyState();
      }
    },
    onError: (error: ApolloError): void => {
      error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Error verification not requested":
            msgError(translate.t("proj_alerts.no_verification_requested"));
            break;
          case "Exception - Vulnerability not found":
            msgError(translate.t("proj_alerts.no_found"));
            break;
          default:
            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error("An error occurred verifying a request", error);
        }
      });
    },
    refetchQueries: [
      { query: GET_FINDING_HEADER, variables: { findingId: props.findingId, canGetHistoricState: canDisplayAnalyst } },
      { query: GET_VULNERABILITIES, variables: { analystField: canDisplayAnalyst, identifier: props.findingId } },
    ],
  });

  const handleSubmit: ((values: { treatmentJustification: string }) => void) =
    (values: { treatmentJustification: string }): void => {
      if (props.remediationType === "request") {
        const vulnerabilitiesId: string[] = props.vulns.map((vuln: IVulnData) => vuln.id);
        requestVerification({
          variables: {
            findingId: props.findingId,
            justification: values.treatmentJustification,
            vulnerabilities: vulnerabilitiesId,
          },
        })
          .catch();
      } else {
        const openVulnsId: string[] = vulnerabilitiesList.reduce(
          (acc: string[], vuln: IVulnData) => (vuln.currentState === "open" ? [...acc, vuln.id] : acc), []);
        const closedVulnsId: string[] = vulnerabilitiesList.reduce(
          (acc: string[], vuln: IVulnData) => (vuln.currentState === "closed" ? [...acc, vuln.id] : acc), []);
        verifyRequest({
          variables: {
            closedVulns: closedVulnsId, findingId: props.findingId, justification: values.treatmentJustification,
            openVulns: openVulnsId,
          },
        })
          .catch();
      }
      closeRemediationModal();
    };

  const renderVulnsToVerify: (() => JSX.Element) = (): JSX.Element => {
    const handleUpdateRepo: ((vulnInfo: Dictionary<string>) => void) = (
      vulnInfo: Dictionary<string>,
    ): void => {
      const newVulnList: IVulnData[] = vulnerabilitiesList.map(
        (vuln: IVulnData) => vuln.id !== vulnInfo.id ? vuln :
          { ...vuln, currentState: vuln.currentState === "open" ? "closed" : "open" });
      setVulnerabilities([...newVulnList]);
    };
    const vulnsHeader: IHeader[] = [
      { align: "left", dataField: "where", header: "Where", width: "55%", wrapped: true },
      { align: "left", dataField: "specific", header: "Specific", width: "25%", wrapped: true },
      {
        align: "left", changeFunction: handleUpdateRepo, dataField: "currentState", formatter: changeVulnStateFormatter,
        header: "State", width: "20%", wrapped: true,
      }];

    return (
      <DataTableNext
        id="vulnstoverify"
        bordered={false}
        dataset={vulnerabilitiesList}
        exportCsv={false}
        headers={vulnsHeader}
        onClickRow={undefined}
        pageSize={10}
        remote={false}
        search={false}
        title=""
        tableBody={style.tableBody}
        tableHeader={style.tableHeader}
      />
    );
  };

  return (
    <React.StrictMode>
      <RemediationModal
        additionalInfo={
          props.remediationType === "request"
            ? translate.t("search_findings.tab_description.remediation_modal.message", { vulns: props.vulns.length })
            : undefined
        }
        isLoading={submittingRequest || submittingVerify}
        isOpen={props.isOpen}
        message={
          props.remediationType === "request"
            ? translate.t("search_findings.tab_description.remediation_modal.justification")
            : translate.t("search_findings.tab_description.remediation_modal.observations")
        }
        onClose={closeRemediationModal}
        onSubmit={handleSubmit}
        title={
          props.remediationType === "request"
            ? translate.t("search_findings.tab_description.remediation_modal.title_request")
            : translate.t("search_findings.tab_description.remediation_modal.title_observations")
        }
      >
        {props.remediationType === "verify" ? renderVulnsToVerify : undefined}
      </RemediationModal>
    </React.StrictMode>
  );
};

export { updateVerificationModal as UpdateVerificationModal };
