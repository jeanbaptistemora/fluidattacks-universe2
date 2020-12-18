import type { ApolloError } from "apollo-client";
import { DataTableNext } from "components/DataTableNext";
import { GET_VULNERABILITIES } from "scenes/Dashboard/components/Vulnerabilities/queries";
import type { GraphQLError } from "graphql";
import { HANDLE_VULNS_ACCEPTATION } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/queries";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Logger } from "utils/logger";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { RemediationModal } from "scenes/Dashboard/components/RemediationModal/index";
import { authzPermissionsContext } from "utils/authz/config";
import { changeVulnTreatmentFormatter } from "components/DataTableNext/formatters";
import { translate } from "utils/translations/translate";
import { useAbility } from "@casl/react";
import { useMutation } from "@apollo/react-hooks";
import type {
  IHandleVulnsAcceptationModalProps,
  IHandleVulnsAcceptationResultAttr,
  IVulnDataAttr,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/types";
import { msgError, msgSuccess } from "utils/notifications";

const HandleAcceptationModal: React.FC<IHandleVulnsAcceptationModalProps> = (
  props: IHandleVulnsAcceptationModalProps
): JSX.Element => {
  const { findingId, vulns, handleCloseModal, refetchData } = props;

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canDisplayAnalyst: boolean = permissions.can(
    "backend_api_resolvers_new_finding_analyst_resolve"
  );
  const [vulnerabilitiesList, setVulnerabilities] = React.useState(vulns);

  // GraphQL operations
  const [handleAcceptation, { loading: handlingAcceptation }] = useMutation(
    HANDLE_VULNS_ACCEPTATION,
    {
      onCompleted: (data: IHandleVulnsAcceptationResultAttr): void => {
        if (data.handleVulnsAcceptation.success) {
          msgSuccess(
            translate.t("search_findings.tab_vuln.alerts.acceptation_success"),
            translate.t("group_alerts.updated_title")
          );
          refetchData();
          handleCloseModal();
        }
      },
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - It cant handle acceptation without being requested":
              msgError(
                translate.t(
                  "search_findings.tab_vuln.alerts.acceptation_not_requested"
                )
              );
              break;
            case "Exception - Vulnerability not found":
              msgError(translate.t("group_alerts.no_found"));
              break;
            case "Exception - Invalid characters":
              msgError(translate.t("validations.invalid_char"));
              break;
            default:
              msgError(translate.t("group_alerts.error_textsad"));
              Logger.warning("An error occurred handling acceptation", error);
          }
        });
      },
      refetchQueries: [
        {
          query: GET_VULNERABILITIES,
          variables: {
            analystField: canDisplayAnalyst,
            identifier: findingId,
          },
        },
      ],
    }
  );

  function handleSubmit(values: { treatmentJustification: string }): void {
    const acceptedVulns: string[] = vulnerabilitiesList.reduce(
      (acc: string[], vuln: IVulnDataAttr): string[] =>
        vuln.acceptation === "APPROVED" ? [...acc, vuln.id] : acc,
      []
    );
    const rejectedVulns: string[] = vulnerabilitiesList.reduce(
      (acc: string[], vuln: IVulnDataAttr): string[] =>
        vuln.acceptation === "REJECTED" ? [...acc, vuln.id] : acc,
      []
    );
    void handleAcceptation({
      variables: {
        acceptedVulns,
        findingId: props.findingId,
        justification: values.treatmentJustification,
        rejectedVulns,
      },
    });
  }

  const handleUpdateAcceptation: (vulnInfo: Dictionary<string>) => void = (
    vulnInfo: Dictionary<string>
  ): void => {
    const newVulnList: IVulnDataAttr[] = vulnerabilitiesList.map(
      (vuln: IVulnDataAttr): IVulnDataAttr =>
        vuln.id !== vulnInfo.id
          ? vuln
          : {
              ...vuln,
              acceptation:
                vuln.acceptation === "APPROVED" ? "REJECTED" : "APPROVED",
            }
    );
    setVulnerabilities([...newVulnList]);
  };
  const vulnsHeader: IHeaderConfig[] = [
    {
      align: "left",
      dataField: "where",
      header: "Where",
      width: "50%",
      wrapped: true,
    },
    {
      align: "left",
      dataField: "specific",
      header: "Specific",
      width: "25%",
      wrapped: true,
    },
    {
      align: "left",
      changeFunction: handleUpdateAcceptation,
      dataField: "acceptation",
      formatter: changeVulnTreatmentFormatter,
      header: "Acceptation",
      width: "25%",
      wrapped: true,
    },
  ];

  return (
    <React.StrictMode>
      <RemediationModal
        isLoading={handlingAcceptation}
        isOpen={true}
        maxJustificationLength={200}
        message={translate.t(
          "search_findings.tab_description.remediation_modal.observations"
        )}
        onClose={handleCloseModal}
        onSubmit={handleSubmit}
        title={translate.t(
          "search_findings.tab_description.remediation_modal.title_observations"
        )}
      >
        <DataTableNext
          bordered={false}
          dataset={vulnerabilitiesList}
          exportCsv={false}
          headers={vulnsHeader}
          id={"vulnsToHandleAcceptation"}
          pageSize={10}
          search={false}
        />
      </RemediationModal>
    </React.StrictMode>
  );
};

export { HandleAcceptationModal };
