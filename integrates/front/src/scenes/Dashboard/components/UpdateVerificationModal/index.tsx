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
import type {
  IRequestVulnVerificationResult,
  IVerifyRequestVulnResult,
} from "./types";

import { GET_ME_VULNERABILITIES_ASSIGNED_IDS } from "../Navbar/Tasks/queries";
import { Switch } from "components/Switch";
import { Table } from "components/Table";
import { changeVulnStateFormatter } from "components/Table/formatters";
import type { IHeaderConfig } from "components/Table/types";
import { Tooltip } from "components/Tooltip";
import { RemediationModal } from "scenes/Dashboard/components/RemediationModal/index";
import {
  REQUEST_VULNERABILITIES_VERIFICATION,
  VERIFY_VULNERABILITIES,
} from "scenes/Dashboard/components/UpdateVerificationModal/queries";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import { GET_ME_VULNERABILITIES_ASSIGNED } from "scenes/Dashboard/containers/Tasks/Vulnerabilities/queries";
import { GET_FINDING_AND_GROUP_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
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
  refetchData: () => void;
}

const UpdateVerificationModal: React.FC<IUpdateVerificationModal> = ({
  isReattacking,
  isVerifying,
  vulns,
  clearSelected,
  handleCloseModal,
  setRequestState,
  setVerifyState,
  refetchData,
}: IUpdateVerificationModal): JSX.Element => {
  const MAX_JUSTIFICATION_LENGTH = 10000;
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canDisplayHacker: boolean = permissions.can(
    "api_resolvers_finding_hacker_resolve"
  );
  const { t } = useTranslation();

  // State management
  const [vulnerabilitiesList, setVulnerabilitiesList] = useState(vulns);
  const [isOpen, setIsOpen] = useState(true);
  const closeRemediationModal: () => void = useCallback((): void => {
    handleCloseModal();
  }, [handleCloseModal]);

  // GraphQL operations
  const [requestVerification, { loading: submittingRequest }] =
    useMutation<IRequestVulnVerificationResult>(
      REQUEST_VULNERABILITIES_VERIFICATION,
      {
        onCompleted: (data: IRequestVulnVerificationResult): void => {
          if (data.requestVulnerabilitiesVerification.success) {
            refetchData();
          }
        },
        refetchQueries: [
          {
            query: GET_FINDING_AND_GROUP_INFO,
            variables: {
              findingId: vulnerabilitiesList[0].findingId,
            },
          },
          GET_ME_VULNERABILITIES_ASSIGNED,
          GET_ME_VULNERABILITIES_ASSIGNED_IDS,
        ],
      }
    );

  const [verifyRequest, { loading: submittingVerify }] =
    useMutation<IVerifyRequestVulnResult>(VERIFY_VULNERABILITIES, {
      onCompleted: (data: IVerifyRequestVulnResult): void => {
        if (data.verifyVulnerabilitiesRequest.success) {
          refetchData();
        }
      },
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
      ],
    });

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

  const handleOnChange = useCallback((): void => {
    setIsOpen((currentValue: boolean): boolean => {
      const newVulnList: IVulnData[] = vulnerabilitiesList.map(
        (vuln: IVulnData): IVulnData => ({
          ...vuln,
          currentState: currentValue ? "closed" : "open",
        })
      );
      setVulnerabilitiesList([...newVulnList]);

      return !currentValue;
    });
  }, [vulnerabilitiesList]);

  const renderVulnsToVerify: () => JSX.Element = (): JSX.Element => {
    const handleUpdateRepo: (vulnInfo: Record<string, string>) => void = (
      vulnInfo: Record<string, string>
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
      setVulnerabilitiesList([...newVulnList]);
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
      <React.StrictMode>
        <Tooltip
          id={"toogleToolTip"}
          place={"top"}
          tip={t(
            "searchFindings.tabDescription.remediationModal.globalSwitch.tooltip"
          )}
        >
          <div className={"pr4 tr w-100"}>
            <span className={"mb0 mt1 pr2"}>
              {t(
                "searchFindings.tabDescription.remediationModal.globalSwitch.text"
              )}
            </span>
            &nbsp;
            <Switch
              checked={isOpen}
              label={{ off: "closed", on: "open" }}
              onChange={handleOnChange}
            />
          </div>
        </Tooltip>
        <Table
          dataset={vulnerabilitiesList}
          exportCsv={false}
          headers={vulnsHeader}
          id={"vulnstoverify"}
          pageSize={10}
          search={false}
        />
      </React.StrictMode>
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

export type { IUpdateVerificationModal, IVulnData };
export { UpdateVerificationModal };
