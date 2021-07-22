import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React, { useCallback, useState } from "react";

import {
  handleRequestVerification,
  handleRequestVerificationError,
  handleSubmitHelper,
  handleVerifyRequest,
  handleVerifyRequestError,
} from "./helpers";

import { DataTableNext } from "components/DataTableNext";
import { changeVulnStateFormatter } from "components/DataTableNext/formatters";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { RemediationModal } from "scenes/Dashboard/components/RemediationModal/index";
import {
  REQUEST_VERIFICATION_VULNERABILITIES,
  VERIFY_VULNERABILITIES,
} from "scenes/Dashboard/components/UpdateVerificationModal/queries";
import type {
  IRequestVerificationVulnResult,
  IVerifyRequestVulnResult,
} from "scenes/Dashboard/components/UpdateVerificationModal/types";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { authzPermissionsContext } from "utils/authz/config";
import { translate } from "utils/translations/translate";

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
  const canDisplayAnalyst: boolean = permissions.can(
    "api_resolvers_finding_analyst_resolve"
  );

  // State management
  const [vulnerabilitiesList, setVulnerabilities] = useState(vulns);
  const closeRemediationModal: () => void = useCallback((): void => {
    handleCloseModal();
  }, [handleCloseModal]);

  // GraphQL operations
  const [requestVerification, { loading: submittingRequest }] = useMutation(
    REQUEST_VERIFICATION_VULNERABILITIES,
    {
      onCompleted: (data: IRequestVerificationVulnResult): void => {
        handleRequestVerification(
          refetchData,
          clearSelected,
          setRequestState,
          data
        );
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        handleRequestVerificationError(graphQLErrors);
      },
      refetchQueries: [
        {
          query: GET_FINDING_VULN_INFO,
          variables: {
            canRetrieveAnalyst: permissions.can(
              "api_resolvers_vulnerability_analyst_resolve"
            ),
            canRetrieveZeroRisk: permissions.can(
              "api_resolvers_finding_zero_risk_resolve"
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
        handleVerifyRequest(
          refetchData,
          clearSelected,
          setVerifyState,
          data,
          vulns.length
        );
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        handleVerifyRequestError(graphQLErrors);
      },
      refetchQueries: [
        {
          query: GET_FINDING_HEADER,
          variables: {
            canGetHistoricState: canDisplayAnalyst,
            findingId,
          },
        },
        {
          query: GET_FINDING_VULN_INFO,
          variables: {
            canRetrieveAnalyst: permissions.can(
              "api_resolvers_vulnerability_analyst_resolve"
            ),
            canRetrieveZeroRisk: permissions.can(
              "api_resolvers_finding_zero_risk_resolve"
            ),
            findingId,
            groupName,
          },
        },
      ],
    }
  );

  const handleSubmit: (values: { treatmentJustification: string }) => void =
    useCallback(
      (values: { treatmentJustification: string }): void => {
        handleSubmitHelper(
          requestVerification,
          verifyRequest,
          findingId,
          values,
          vulns,
          vulnerabilitiesList,
          isReattacking
        );
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
                "searchFindings.tabDescription.remediationModal.message",
                { vulns: vulns.length }
              )
            : undefined
        }
        isLoading={submittingRequest || submittingVerify}
        isOpen={true}
        message={
          isReattacking
            ? translate.t(
                "searchFindings.tabDescription.remediationModal.justification"
              )
            : translate.t(
                "searchFindings.tabDescription.remediationModal.observations"
              )
        }
        onClose={closeRemediationModal}
        onSubmit={handleSubmit}
        title={
          isReattacking
            ? translate.t(
                "searchFindings.tabDescription.remediationModal.titleRequest"
              )
            : translate.t(
                "searchFindings.tabDescription.remediationModal.titleObservations"
              )
        }
      >
        {isVerifying ? renderVulnsToVerify() : undefined}
      </RemediationModal>
    </React.StrictMode>
  );
};

export { UpdateVerificationModal, IUpdateVerificationModal, IVulnData };
