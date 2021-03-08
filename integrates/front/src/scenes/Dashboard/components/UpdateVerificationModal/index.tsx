import type { ApolloError } from "apollo-client";
import { DataTableNext } from "components/DataTableNext";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import type { GraphQLError } from "graphql";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Logger } from "utils/logger";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { RemediationModal } from "scenes/Dashboard/components/RemediationModal/index";
import { changeVulnStateFormatter } from "components/DataTableNext/formatters";
import mixpanel from "mixpanel-browser";
import { translate } from "utils/translations/translate";
import { useAbility } from "@casl/react";
import { useMutation } from "@apollo/react-hooks";
import type {
  IRequestVerificationVulnResult,
  IVerifyRequestVulnResult,
} from "scenes/Dashboard/components/UpdateVerificationModal/types";
import {
  REQUEST_VERIFICATION_VULN,
  VERIFY_VULNERABILITIES,
} from "scenes/Dashboard/components/UpdateVerificationModal/queries";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

interface IVulnData {
  currentState: string;
  id: string;
  specific: string;
  where: string;
}
interface IUpdateVerificationModal {
  findingId: string;
  groupName: string;
  isReattacking: boolean;
  isVerifying: boolean;
  vulns: IVulnData[];
  clearSelected: () => void;
  handleCloseModal: () => void;
  refetchData: () => void;
  setRequestState: () => void;
  setVerifyState: () => void;
}

const UpdateVerificationModal: React.FC<IUpdateVerificationModal> = (
  props: IUpdateVerificationModal
): JSX.Element => {
  const {
    findingId,
    groupName,
    isReattacking,
    isVerifying,
    vulns,
    clearSelected,
    handleCloseModal,
    refetchData,
    setRequestState,
    setVerifyState,
  } = props;
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const groupPermissions: PureAbility<string> = useAbility(authzGroupContext);
  const canDisplayAnalyst: boolean = permissions.can(
    "backend_api_resolvers_finding_analyst_resolve"
  );
  const canDisplayExploit: boolean = groupPermissions.can("has_forces");

  // State management
  const [vulnerabilitiesList, setVulnerabilities] = React.useState(vulns);
  const closeRemediationModal: () => void = React.useCallback((): void => {
    handleCloseModal();
  }, [handleCloseModal]);

  // GraphQL operations
  const [requestVerification, { loading: submittingRequest }] = useMutation(
    REQUEST_VERIFICATION_VULN,
    {
      onCompleted: (data: IRequestVerificationVulnResult): void => {
        if (data.requestVerificationVuln.success) {
          msgSuccess(
            translate.t("group_alerts.verifiedSuccess"),
            translate.t("group_alerts.updatedTitle")
          );
          refetchData();
          clearSelected();
          setRequestState();
        }
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - Request verification already requested":
              msgError(
                translate.t("group_alerts.verificationAlreadyRequested")
              );
              break;
            case "Exception - The vulnerability has already been closed":
              msgError(translate.t("group_alerts."));
              break;
            case "Exception - Vulnerability not found":
              msgError(translate.t("group_alerts.no_found"));
              break;
            default:
              msgError(translate.t("group_alerts.error_textsad"));
              Logger.warning(
                "An error occurred requesting verification",
                error
              );
          }
        });
      },
      refetchQueries: [
        {
          query: GET_FINDING_VULN_INFO,
          variables: {
            canRetrieveAnalyst: permissions.can(
              "backend_api_resolvers_vulnerability_analyst_resolve"
            ),
            canRetrieveZeroRisk: permissions.can(
              "backend_api_resolvers_finding_zero_risk_resolve"
            ),
            findingId,
            groupName,
          },
        },
      ],
    }
  );

  const [verifyRequest, { loading: submittingVerify }] = useMutation(
    VERIFY_VULNERABILITIES,
    {
      onCompleted: (data: IVerifyRequestVulnResult): void => {
        if (data.verifyRequestVuln.success) {
          msgSuccess(
            translate.t("group_alerts.verifiedSuccess"),
            translate.t("group_alerts.updatedTitle")
          );
          refetchData();
          clearSelected();
          setVerifyState();
        }
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - Error verification not requested":
              msgError(translate.t("group_alerts.no_verification_requested"));
              break;
            case "Exception - Vulnerability not found":
              msgError(translate.t("group_alerts.no_found"));
              break;
            default:
              msgError(translate.t("group_alerts.error_textsad"));
              Logger.warning("An error occurred verifying a request", error);
          }
        });
      },
      refetchQueries: [
        {
          query: GET_FINDING_HEADER,
          variables: {
            canGetExploit: canDisplayExploit,
            canGetHistoricState: canDisplayAnalyst,
            findingId,
          },
        },
        {
          query: GET_FINDING_VULN_INFO,
          variables: {
            canRetrieveAnalyst: permissions.can(
              "backend_api_resolvers_vulnerability_analyst_resolve"
            ),
            canRetrieveZeroRisk: permissions.can(
              "backend_api_resolvers_finding_zero_risk_resolve"
            ),
            findingId,
            groupName,
          },
        },
      ],
    }
  );

  const handleSubmit: (values: {
    treatmentJustification: string;
  }) => void = React.useCallback(
    (values: { treatmentJustification: string }): void => {
      if (isReattacking) {
        const vulnerabilitiesId: string[] = vulns.map(
          (vuln: IVulnData): string => vuln.id
        );

        mixpanel.track("RequestReattack");
        requestVerification({
          variables: {
            findingId,
            justification: values.treatmentJustification,
            vulnerabilities: vulnerabilitiesId,
          },
        }).catch((): undefined => undefined);
      } else {
        const openVulnsId: string[] = vulnerabilitiesList.reduce(
          (acc: string[], vuln: IVulnData): string[] =>
            vuln.currentState === "open" ? [...acc, vuln.id] : acc,
          []
        );
        const closedVulnsId: string[] = vulnerabilitiesList.reduce(
          (acc: string[], vuln: IVulnData): string[] =>
            vuln.currentState === "closed" ? [...acc, vuln.id] : acc,
          []
        );
        verifyRequest({
          variables: {
            closedVulns: closedVulnsId,
            findingId,
            justification: values.treatmentJustification,
            openVulns: openVulnsId,
          },
        }).catch((): undefined => undefined);
      }
      closeRemediationModal();
    },
    [
      closeRemediationModal,
      findingId,
      isReattacking,
      vulns,
      requestVerification,
      verifyRequest,
      vulnerabilitiesList,
    ]
  );

  const renderVulnsToVerify: () => JSX.Element = (): JSX.Element => {
    const handleUpdateRepo: (vulnInfo: Dictionary<string>) => void = (
      vulnInfo: Dictionary<string>
    ): void => {
      const newVulnList: IVulnData[] = vulnerabilitiesList.map(
        (vuln: IVulnData): IVulnData =>
          vuln.id === vulnInfo.id
            ? {
                ...vuln,
                currentState: vuln.currentState === "open" ? "closed" : "open",
              }
            : vuln
      );
      setVulnerabilities([...newVulnList]);
    };
    const vulnsHeader: IHeaderConfig[] = [
      {
        align: "left",
        dataField: "where",
        header: "Where",
        width: "55%",
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
        changeFunction: handleUpdateRepo,
        dataField: "currentState",
        formatter: changeVulnStateFormatter,
        header: "State",
        width: "20%",
        wrapped: true,
      },
    ];

    return (
      <DataTableNext
        bordered={false}
        dataset={vulnerabilitiesList}
        exportCsv={false}
        headers={vulnsHeader}
        id={"vulnstoverify"}
        pageSize={10}
        search={false}
      />
    );
  };

  return (
    <React.StrictMode>
      <RemediationModal
        additionalInfo={
          isReattacking
            ? translate.t(
                "search_findings.tab_description.remediation_modal.message",
                { vulns: vulns.length }
              )
            : undefined
        }
        isLoading={submittingRequest || submittingVerify}
        isOpen={true}
        message={
          isReattacking
            ? translate.t(
                "search_findings.tab_description.remediation_modal.justification"
              )
            : translate.t(
                "search_findings.tab_description.remediation_modal.observations"
              )
        }
        onClose={closeRemediationModal}
        onSubmit={handleSubmit}
        title={
          isReattacking
            ? translate.t(
                "search_findings.tab_description.remediation_modal.title_request"
              )
            : translate.t(
                "search_findings.tab_description.remediation_modal.title_observations"
              )
        }
      >
        {isVerifying ? renderVulnsToVerify() : undefined}
      </RemediationModal>
    </React.StrictMode>
  );
};

export { UpdateVerificationModal, IUpdateVerificationModal };
