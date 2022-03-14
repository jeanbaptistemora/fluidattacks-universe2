import { useMutation } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import {
  getAreAllChunckedMutationValid,
  handleAltSubmitHelper,
  handleRequestVerification,
  handleRequestVerificationError,
  handleVerifyRequest,
  handleVerifyRequestError,
} from "./helpers";

import { Table } from "components/Table";
import { changeVulnStateFormatter } from "components/Table/formatters";
import type { IHeaderConfig } from "components/Table/types";
import { RemediationModal } from "scenes/Dashboard/components/RemediationModal/index";
import {
  REQUEST_VULNERABILITIES_VERIFICATION,
  VERIFY_VULNERABILITIES,
} from "scenes/Dashboard/components/UpdateVerificationModal/queries";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import {
  GET_FINDING_AND_GROUP_INFO,
  GET_FINDING_VULNS,
} from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { GET_ME_VULNERABILITIES_ASSIGNED } from "scenes/Dashboard/queries";
import { authzPermissionsContext } from "utils/authz/config";

interface IVulnData {
  currentState: string;
  findingId: string;
  groupName: string;
  id: string;
  specific: string;
  where: string;
}
interface IUpdateVerificationModal {
  isReattacking: boolean;
  isVerifying: boolean;
  vulns: IVulnData[];
  clearSelected: () => void;
  handleCloseModal: () => void;
  setRequestState: () => void;
  setVerifyState: () => void;
}

const UpdateVerificationModal: React.FC<IUpdateVerificationModal> = ({
  isReattacking,
  isVerifying,
  vulns,
  clearSelected,
  handleCloseModal,
  setRequestState,
  setVerifyState,
}: IUpdateVerificationModal): JSX.Element => {
  const MAX_JUSTIFICATION_LENGTH = 10000;
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canDisplayHacker: boolean = permissions.can(
    "api_resolvers_finding_hacker_resolve"
  );
  const { t } = useTranslation();

  // State management
  const [vulnerabilitiesList, setVulnerabilities] = useState(vulns);
  const closeRemediationModal: () => void = useCallback((): void => {
    handleCloseModal();
  }, [handleCloseModal]);

  // GraphQL operations
  const [requestVerification, { loading: submittingRequest }] = useMutation(
    REQUEST_VULNERABILITIES_VERIFICATION,
    {
      refetchQueries: [
        {
          query: GET_FINDING_AND_GROUP_INFO,
          variables: {
            findingId: vulnerabilitiesList[0].findingId,
          },
        },
        {
          query: GET_FINDING_VULNS,
          variables: {
            canRetrieveZeroRisk: permissions.can(
              "api_resolvers_finding_zero_risk_resolve"
            ),
            findingId: vulnerabilitiesList[0].findingId,
          },
        },
        { query: GET_ME_VULNERABILITIES_ASSIGNED },
      ],
    }
  );

  const [verifyRequest, { loading: submittingVerify }] = useMutation(
    VERIFY_VULNERABILITIES,
    {
      refetchQueries: [
        {
          query: GET_FINDING_HEADER,
          variables: {
            canGetHistoricState: canDisplayHacker,
            findingId: vulnerabilitiesList[0].findingId,
          },
        },
        {
          query: GET_FINDING_AND_GROUP_INFO,
          variables: {
            findingId: vulnerabilitiesList[0].findingId,
          },
        },
        {
          query: GET_FINDING_VULNS,
          variables: {
            canRetrieveZeroRisk: permissions.can(
              "api_resolvers_finding_zero_risk_resolve"
            ),
            findingId: vulnerabilitiesList[0].findingId,
          },
        },
      ],
    }
  );

  async function handleSubmit(values: {
    treatmentJustification: string;
  }): Promise<void> {
    try {
      const results = await handleAltSubmitHelper(
        requestVerification,
        verifyRequest,
        values,
        vulnerabilitiesList,
        isReattacking
      );
      const areAllMutationValid = getAreAllChunckedMutationValid(results);
      if (areAllMutationValid.every(Boolean)) {
        if (isReattacking) {
          handleRequestVerification(clearSelected, setRequestState, true);
        } else {
          handleVerifyRequest(
            clearSelected,
            setVerifyState,
            true,
            vulns.length
          );
        }
      }
    } catch (requestError: unknown) {
      if (isReattacking) {
        handleRequestVerificationError(requestError);
      } else {
        handleVerifyRequestError(requestError);
      }
    }
    closeRemediationModal();
  }

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
        dataField: "where",
        header: "Where",
        width: "55%",
        wrapped: true,
      },
      {
        dataField: "specific",
        header: "Specific",
        width: "25%",
        wrapped: true,
      },
      {
        changeFunction: handleUpdateRepo,
        dataField: "currentState",
        formatter: changeVulnStateFormatter,
        header: "State",
        width: "20%",
        wrapped: true,
      },
    ];

    return (
      <Table
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
            ? t("searchFindings.tabDescription.remediationModal.message", {
                vulns: vulns.length,
              })
            : undefined
        }
        isLoading={submittingRequest || submittingVerify}
        isOpen={true}
        maxJustificationLength={MAX_JUSTIFICATION_LENGTH}
        message={
          isReattacking
            ? t("searchFindings.tabDescription.remediationModal.justification")
            : t("searchFindings.tabDescription.remediationModal.observations")
        }
        onClose={closeRemediationModal}
        onSubmit={handleSubmit}
        title={
          isReattacking
            ? t("searchFindings.tabDescription.remediationModal.titleRequest")
            : t(
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
