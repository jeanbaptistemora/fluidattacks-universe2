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

import { RemediationModal } from "scenes/Dashboard/components/RemediationModal/index";
import { GET_VULNERABILITIES } from "scenes/Dashboard/components/Vulnerabilities/queries";
import {
  CONFIRM_ZERO_RISK_VULN,
  REJECT_ZERO_RISK_VULN,
  REQUEST_ZERO_RISK_VULN,
} from "scenes/Dashboard/containers/VulnerabilitiesView/UpdateZeroRiskModal/queries";
import {
  IConfirmZeroRiskVulnResult,
  IRejectZeroRiskVulnResult,
  IRequestZeroRiskVulnResult,
} from "scenes/Dashboard/containers/VulnerabilitiesView/UpdateZeroRiskModal/types";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { GET_FINDING_HEADER } from "../../FindingContent/queries";

interface IVulnData {
  id: string;
}
export interface IUpdateZeroRiskModal {
  findingId: string;
  isConfirmingZeroRisk: boolean;
  isRejectingZeroRisk: boolean;
  isRequestingZeroRisk: boolean;
  vulns: IVulnData[];
  clearSelected(): void;
  handleCloseModal(): void;
  refetchData(): void;
  setConfirmState(): void;
  setRejectState(): void;
  setRequestState(): void;
}

const updateZeroRiskModal: React.FC<IUpdateZeroRiskModal> = (props: IUpdateZeroRiskModal): JSX.Element => {
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canDisplayAnalyst: boolean = permissions.can("backend_api_resolvers_new_finding_analyst_resolve");
  const canGetHistoricState: boolean = permissions.can("backend_api_resolvers_new_finding_historic_state_resolve");
  const groupPermissions: PureAbility<string> = useAbility(authzGroupContext);
  const canGetExploit: boolean = groupPermissions.can("has_forces");

  // State management
  const closeRemediationModal: (() => void) = (): void => { props.handleCloseModal(); };

  // GraphQL operations
  const [requestZeroRisk, { loading: submittingRequest }] = useMutation(
    REQUEST_ZERO_RISK_VULN, {
    onCompleted: (data: IRequestZeroRiskVulnResult): void => {
      if (data.requestZeroRiskVuln.success) {
        msgSuccess(
          translate.t("group_alerts.requested_zero_risk_success"),
          translate.t("group_alerts.updated_title"),
        );
        props.refetchData();
        props.clearSelected();
        props.setRequestState();
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Exception - Zero risk vulnerability is already requested":
            msgError(translate.t("group_alerts.zero_risk_already_requested"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("An error occurred requesting zero risk vuln", error);
        }
      });
    },
    refetchQueries: [
      { query: GET_VULNERABILITIES, variables: { analystField: canDisplayAnalyst, identifier: props.findingId } },
      { query: GET_FINDING_HEADER, variables: { canGetExploit, canGetHistoricState, findingId: props.findingId } },
    ],
  });

  const [confirmZeroRisk, { loading: submittingConfirm }] = useMutation(
    CONFIRM_ZERO_RISK_VULN, {
    onCompleted: (data: IConfirmZeroRiskVulnResult): void => {
      if (data.confirmZeroRiskVuln.success) {
        msgSuccess(
          translate.t("group_alerts.confirmed_zero_risk_success"),
          translate.t("group_alerts.updated_title"),
        );
        props.refetchData();
        props.clearSelected();
        props.setConfirmState();
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Exception - Zero risk vulnerability is not requested":
            msgError(translate.t("group_alerts.zero_risk_is_not_requested"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("An error occurred confirming zero risk vuln", error);
        }
      });
    },
    refetchQueries: [
      { query: GET_VULNERABILITIES, variables: { analystField: canDisplayAnalyst, identifier: props.findingId } },
      { query: GET_FINDING_HEADER, variables: { canGetExploit, canGetHistoricState, findingId: props.findingId } },
    ],
  });

  const [rejectZeroRisk, { loading: submittingReject }] = useMutation(
    REJECT_ZERO_RISK_VULN, {
    onCompleted: (data: IRejectZeroRiskVulnResult): void => {
      if (data.rejectZeroRiskVuln.success) {
        msgSuccess(
          translate.t("group_alerts.rejected_zero_risk_success"),
          translate.t("group_alerts.updated_title"),
        );
        props.refetchData();
        props.clearSelected();
        props.setRejectState();
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Exception - Zero risk vulnerability is not requested":
            msgError(translate.t("group_alerts.zero_risk_is_not_requested"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("An error occurred rejecting zero risk vuln", error);
        }
      });
    },
    refetchQueries: [
      { query: GET_VULNERABILITIES, variables: { analystField: canDisplayAnalyst, identifier: props.findingId } },
      { query: GET_FINDING_HEADER, variables: { canGetExploit, canGetHistoricState, findingId: props.findingId } },
    ],
  });

  const handleSubmit: ((values: { treatmentJustification: string }) => void) =
    (values: { treatmentJustification: string }): void => {
      if (props.isRequestingZeroRisk) {
        const vulnerabilitiesId: string[] = props.vulns.map((vuln: IVulnData) => vuln.id);
        void requestZeroRisk({
          variables: {
            findingId: props.findingId,
            justification: values.treatmentJustification,
            vulnerabilities: vulnerabilitiesId,
          },
        });
      }
      if (props.isConfirmingZeroRisk) {
        const vulnerabilitiesId: string[] = props.vulns.map((vuln: IVulnData) => vuln.id);
        void confirmZeroRisk({
          variables: {
            findingId: props.findingId,
            justification: values.treatmentJustification,
            vulnerabilities: vulnerabilitiesId,
          },
        });
      }
      if (props.isRejectingZeroRisk) {
        const vulnerabilitiesId: string[] = props.vulns.map((vuln: IVulnData) => vuln.id);
        void rejectZeroRisk({
          variables: {
            findingId: props.findingId,
            justification: values.treatmentJustification,
            vulnerabilities: vulnerabilitiesId,
          },
        });
      }
      closeRemediationModal();
    };

  return (
    <React.StrictMode>
      <RemediationModal
        additionalInfo={
          props.isRequestingZeroRisk
          ? translate.t("search_findings.tab_description.update_zero_risk_modal.request_message",
                        { vulns: props.vulns.length })
          : props.isConfirmingZeroRisk
            ? translate.t("search_findings.tab_description.update_zero_risk_modal.confirm_message",
                          { vulns: props.vulns.length })
            : props.isRejectingZeroRisk
              ? translate.t("search_findings.tab_description.update_zero_risk_modal.reject_message",
                            { vulns: props.vulns.length })
              : ""
        }
        isLoading={submittingRequest || submittingConfirm || submittingReject}
        isOpen={true}
        maxJustificationLength={2000}
        message={
          props.isRequestingZeroRisk
          ? translate.t("search_findings.tab_description.update_zero_risk_modal.request_justification")
          : props.isConfirmingZeroRisk
            ? translate.t("search_findings.tab_description.update_zero_risk_modal.confirm_justification")
            : props.isRejectingZeroRisk
              ? translate.t("search_findings.tab_description.update_zero_risk_modal.reject_justification")
              : ""
        }
        onClose={closeRemediationModal}
        onSubmit={handleSubmit}
        title={
          translate.t("search_findings.tab_description.update_zero_risk_modal.title")
        }
      />
    </React.StrictMode>
  );
};

export { updateZeroRiskModal as UpdateZeroRiskModal };
