import { useMutation } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";

import { DataTableNext } from "components/DataTableNext";
import { changeVulnTreatmentFormatter } from "components/DataTableNext/formatters";
import { IHeaderConfig } from "components/DataTableNext/types";
import { RemediationModal } from "scenes/Dashboard/components/RemediationModal/index";
import { GET_VULNERABILITIES } from "scenes/Dashboard/components/Vulnerabilities/queries";
import {
  HANDLE_VULNS_ACCEPTATION,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/queries";
import {
  IHandleVulnsAcceptationModal,
  IHandleVulnsAcceptationResult,
  IVulnData,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/types";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleAcceptationModal: React.FC<IHandleVulnsAcceptationModal> = (
  props: IHandleVulnsAcceptationModal,
): JSX.Element => {
  const { handleCloseModal, refetchData } = props;
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canDisplayAnalyst: boolean = permissions.can("backend_api_resolvers_new_finding_analyst_resolve");
  const [vulnerabilitiesList, setVulnerabilities] = React.useState(props.vulns);

  // GraphQL operations
  const [handleAcceptation, { loading: handlingAcceptation }] = useMutation(
    HANDLE_VULNS_ACCEPTATION, {
    onCompleted: (data: IHandleVulnsAcceptationResult): void => {
      if (data.handleVulnsAcceptation.success) {
        msgSuccess(
          translate.t("search_findings.tab_vuln.alerts.acceptation_success"),
          translate.t("group_alerts.updated_title"),
        );
        refetchData();
        handleCloseModal();
      }
    },
    onError: (errors: ApolloError): void => {
      errors.graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Exception - It cant handle acceptation without being requested":
            msgError(translate.t("search_findings.tab_vuln.alerts.acceptation_not_requested"));
            break;
          case "Exception - Vulnerability not found":
            msgError(translate.t("group_alerts.no_found"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("An error occurred handling acceptation", error);
        }
      });
    },
    refetchQueries: [
      { query: GET_VULNERABILITIES, variables: { analystField: canDisplayAnalyst, identifier: props.findingId } },
    ],
  });

  const handleSubmit: ((values: { treatmentJustification: string }) => void) = (
    values: { treatmentJustification: string },
  ): void => {
    const acceptedVulns: string[] = vulnerabilitiesList.reduce(
      (acc: string[], vuln: IVulnData) => (vuln.acceptation === "APPROVED" ? [...acc, vuln.id] : acc), []);
    const rejectedVulns: string[] = vulnerabilitiesList.reduce(
      (acc: string[], vuln: IVulnData) => (vuln.acceptation === "REJECTED" ? [...acc, vuln.id] : acc), []);
    handleAcceptation({variables: {
        acceptedVulns,
        findingId: props.findingId,
        justification: values.treatmentJustification,
        rejectedVulns,
      },
    });
  };

  const handleUpdateAcceptation: ((vulnInfo: Dictionary<string>) => void) = (
    vulnInfo: Dictionary<string>,
  ): void => {
    const newVulnList: IVulnData[] = vulnerabilitiesList.map(
      (vuln: IVulnData) => vuln.id !== vulnInfo.id ? vuln :
        { ...vuln, acceptation: vuln.acceptation === "APPROVED" ? "REJECTED" : "APPROVED" });
    setVulnerabilities([...newVulnList]);
  };
  const vulnsHeader: IHeaderConfig[] = [
    { align: "left", dataField: "where", header: "Where", width: "50%", wrapped: true },
    { align: "left", dataField: "specific", header: "Specific", width: "25%", wrapped: true },
    {
      align: "left", changeFunction: handleUpdateAcceptation, dataField: "acceptation",
      formatter: changeVulnTreatmentFormatter, header: "Acceptation", width: "25%", wrapped: true,
    },
  ];

  return (
    <React.StrictMode>
      <RemediationModal
        isLoading={handlingAcceptation}
        isOpen={true}
        maxJustificationLength={200}
        message={translate.t("search_findings.tab_description.remediation_modal.observations")}
        onClose={handleCloseModal}
        onSubmit={handleSubmit}
        title={translate.t("search_findings.tab_description.remediation_modal.title_observations")}
      >
        <React.Fragment>
          <DataTableNext
            id="vulnsToHandleAcceptation"
            bordered={false}
            dataset={vulnerabilitiesList}
            exportCsv={false}
            headers={vulnsHeader}
            pageSize={10}
            search={false}
          />
        </React.Fragment>
      </RemediationModal>
    </React.StrictMode>
  );
};

export { handleAcceptationModal as HandleAcceptationModal };
