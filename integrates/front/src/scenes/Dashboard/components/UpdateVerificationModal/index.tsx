import { useMutation } from "@apollo/client";
import type { ColumnDef } from "@tanstack/react-table";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { changeVulnStateFormatter } from "./Formatters/changeVulnState";
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
import { Tooltip } from "components/Tooltip";
import { RemediationModal } from "scenes/Dashboard/components/RemediationModal/index";
import {
  REQUEST_VULNERABILITIES_VERIFICATION,
  VERIFY_VULNERABILITIES,
} from "scenes/Dashboard/components/UpdateVerificationModal/queries";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/Finding-Content/queries";
import { GET_FINDING_AND_GROUP_INFO } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/queries";
import { GET_ME_VULNERABILITIES_ASSIGNED } from "scenes/Dashboard/containers/Tasks-Content/Vulnerabilities/queries";

interface IVulnData {
  findingId: string;
  groupName: string;
  id: string;
  specific: string;
  state: "REJECTED" | "SAFE" | "SUBMITTED" | "VULNERABLE";
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
          { query: GET_ME_VULNERABILITIES_ASSIGNED },
          { query: GET_ME_VULNERABILITIES_ASSIGNED_IDS },
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

  const handleSubmit = useCallback(
    async (values: { treatmentJustification: string }): Promise<void> => {
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
    },
    [
      clearSelected,
      closeRemediationModal,
      isReattacking,
      requestVerification,
      setRequestState,
      setVerifyState,
      verifyRequest,
      vulnerabilitiesList,
      vulns.length,
    ]
  );

  const handleOnChange = useCallback((): void => {
    setIsOpen((currentValue: boolean): boolean => {
      const newVulnList: IVulnData[] = vulnerabilitiesList.map(
        (vuln: IVulnData): IVulnData => ({
          ...vuln,
          state: currentValue ? "SAFE" : "VULNERABLE",
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
                state: vuln.state === "VULNERABLE" ? "SAFE" : "VULNERABLE",
              }
            : vuln
      );
      setVulnerabilitiesList([...newVulnList]);
    };

    const columns: ColumnDef<IVulnData>[] = [
      {
        accessorKey: "where",
        header: "Where",
      },
      {
        accessorKey: "specific",
        header: "Specific",
      },
      {
        accessorKey: "state",
        cell: (cell): JSX.Element =>
          changeVulnStateFormatter(
            cell.row.original as unknown as Record<string, string>,
            handleUpdateRepo
          ),
        header: "State",
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
              label={{ off: "Safe", on: "Vulnerable" }}
              onChange={handleOnChange}
            />
          </div>
        </Tooltip>
        <Table
          columns={columns}
          data={vulnerabilitiesList}
          id={"vulnstoverify"}
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
