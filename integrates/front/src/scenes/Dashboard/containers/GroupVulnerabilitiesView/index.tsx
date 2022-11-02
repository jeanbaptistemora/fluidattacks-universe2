/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint fp/no-mutation: 0 */
import { useQuery } from "@apollo/client";
import type { ColumnDef } from "@tanstack/react-table";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { GET_GROUP_VULNERABILITIES } from "./queries";
import type { IGroupVulnerabilities } from "./types";
import { formatVulnerability, isPendingToAcceptance } from "./utils";

import { formatState } from "../GroupFindingsView/utils";
import { ActionButtons } from "../VulnerabilitiesView/ActionButtons";
import { HandleAcceptanceModal } from "../VulnerabilitiesView/HandleAcceptanceModal";
import type { IModalConfig } from "../VulnerabilitiesView/types";
import { Modal } from "components/Modal";
import { formatLinkHandler } from "components/Table/formatters/linkFormatter";
import { UpdateVerificationModal } from "scenes/Dashboard/components/UpdateVerificationModal";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateDescription } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription";
import {
  filterOutVulnerabilities,
  filterZeroRisk,
  getNonSelectableVulnerabilitiesOnReattackIds,
  getNonSelectableVulnerabilitiesOnVerifyIds,
} from "scenes/Dashboard/components/Vulnerabilities/utils";
import { useDebouncedCallback } from "utils/hooks";
import { msgError } from "utils/notifications";

const tableColumns: ColumnDef<IVulnRowAttr>[] = [
  {
    accessorFn: (row): string => `${row.where} | ${row.specific}`,
    enableColumnFilter: false,
    header: "Vulnerability",
  },
  {
    accessorFn: (row): string => String(row.finding?.title),
    cell: (cell): JSX.Element => {
      const link = `vulns/${String(cell.row.original.finding?.id)}/description`;
      const text = cell.getValue<string>();

      return formatLinkHandler(link, text);
    },
    header: "Type",
    meta: { filterType: "select" },
  },
  {
    accessorKey: "currentState",
    cell: (cell): JSX.Element => formatState(cell.getValue()),
    header: "Status",
    meta: { filterType: "select" },
  },
  {
    accessorKey: "treatment",
    header: "Treatment",
    meta: { filterType: "select" },
  },
  {
    accessorKey: "verification",
    header: "Reattack",
    meta: { filterType: "select" },
  },

  {
    accessorKey: "reportDate",
    enableColumnFilter: false,
    header: "Found",
    meta: { filterType: "dateRange" },
  },
  {
    accessorFn: (row): number => Number(row.finding?.severityScore),
    cell: (cell): JSX.Element => {
      const link = `vulns/${String(cell.row.original.finding?.id)}/severity`;
      const text = cell.getValue<string>();

      return formatLinkHandler(link, text);
    },
    header: "Severity",
    meta: { filterType: "numberRange" },
  },
  {
    accessorFn: (): string => "View",
    cell: (cell): JSX.Element => {
      const link = `vulns/${String(cell.row.original.finding?.id)}/evidence`;
      const text = cell.getValue<string>();

      return formatLinkHandler(link, text);
    },
    enableColumnFilter: false,
    header: "Evidence",
  },
];

const GroupVulnerabilitiesView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { t } = useTranslation();
  const [remediationModal, setRemediationModal] = useState<IModalConfig>({
    clearSelected: (): void => undefined,
    selectedVulnerabilities: [],
  });
  const [isRequestingVerify, setIsRequestingVerify] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const openRemediationModal = useCallback(
    (
      selectedVulnerabilities: IVulnRowAttr[],
      clearSelected: () => void
    ): void => {
      setRemediationModal({ clearSelected, selectedVulnerabilities });
    },
    []
  );
  function closeRemediationModal(): void {
    setIsOpen(false);
  }
  const [isVerifying, setIsVerifying] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  function toggleEdit(): void {
    setIsEditing(!isEditing);
  }
  function handleCloseUpdateModal(): void {
    setIsEditing(false);
  }

  const [isHandleAcceptanceModalOpen, setIsHandleAcceptanceModalOpen] =
    useState(false);
  function toggleHandleAcceptanceModal(): void {
    setIsHandleAcceptanceModalOpen(!isHandleAcceptanceModalOpen);
  }

  // GraphQL operations
  const { data: vulnsZeroRisk } = useQuery<IGroupVulnerabilities>(
    GET_GROUP_VULNERABILITIES,
    {
      fetchPolicy: "no-cache",
      variables: { first: 100, groupName, zeroRisk: "REQUESTED" },
    }
  );

  const { data, fetchMore, refetch } = useQuery<IGroupVulnerabilities>(
    GET_GROUP_VULNERABILITIES,
    {
      fetchPolicy: "cache-first",
      variables: { first: 100, groupName, search: "" },
    }
  );

  const vulnerabilities = data === undefined ? [] : formatVulnerability(data);
  const size = data?.group.vulnerabilities.total;

  const vulnerabilitiesZeroRisk =
    vulnsZeroRisk === undefined ? [] : formatVulnerability(vulnsZeroRisk);

  const handleNextPage = useCallback(async (): Promise<void> => {
    const pageInfo =
      data === undefined
        ? { endCursor: "", hasNextPage: false }
        : data.group.vulnerabilities.pageInfo;

    if (pageInfo.hasNextPage) {
      await fetchMore({
        updateQuery: (
          previousResult,
          { fetchMoreResult }
        ): IGroupVulnerabilities => {
          if (!fetchMoreResult) {
            return previousResult;
          }

          const previousEdges = previousResult.group.vulnerabilities.edges;
          const fetchMoreEdges = fetchMoreResult.group.vulnerabilities.edges;

          fetchMoreResult.group.vulnerabilities.edges = [
            ...previousEdges,
            ...fetchMoreEdges,
          ];

          return { ...fetchMoreResult };
        },
        variables: { after: pageInfo.endCursor },
      });
    }
  }, [data, fetchMore]);

  function toggleModal(): void {
    setIsOpen(true);
  }
  function toggleRequestVerify(): void {
    if (isRequestingVerify) {
      setIsRequestingVerify(!isRequestingVerify);
    } else {
      const { selectedVulnerabilities } = remediationModal;
      const newVulnerabilities: IVulnRowAttr[] = filterOutVulnerabilities(
        selectedVulnerabilities,
        filterZeroRisk(vulnerabilities),
        getNonSelectableVulnerabilitiesOnReattackIds
      );
      if (selectedVulnerabilities.length > newVulnerabilities.length) {
        setIsRequestingVerify(!isRequestingVerify);
        msgError(t("searchFindings.tabVuln.errors.selectedVulnerabilities"));
      } else if (selectedVulnerabilities.length > 0) {
        setIsOpen(true);
        setIsRequestingVerify(!isRequestingVerify);
      } else {
        setIsRequestingVerify(!isRequestingVerify);
      }
    }
  }

  function toggleVerify(): void {
    if (isVerifying) {
      setIsVerifying(!isVerifying);
    } else {
      const { selectedVulnerabilities } = remediationModal;
      const newVulnerabilities: IVulnRowAttr[] = filterOutVulnerabilities(
        selectedVulnerabilities,
        filterZeroRisk(vulnerabilities),
        getNonSelectableVulnerabilitiesOnVerifyIds
      );
      if (selectedVulnerabilities.length > newVulnerabilities.length) {
        setIsVerifying(!isVerifying);
        msgError(t("searchFindings.tabVuln.errors.selectedVulnerabilities"));
      } else if (selectedVulnerabilities.length > 0) {
        setIsOpen(true);
        setIsVerifying(!isVerifying);
      } else {
        setIsVerifying(!isVerifying);
      }
    }
  }

  const handleSearch = useDebouncedCallback((search: string): void => {
    void refetch({ search });
  }, 500);

  return (
    <React.StrictMode>
      <React.Fragment>
        <div>
          <VulnComponent
            columnToggle={true}
            columns={tableColumns}
            extraButtons={
              <ActionButtons
                areVulnerabilitiesPendingToAcceptance={isPendingToAcceptance(
                  vulnerabilitiesZeroRisk
                )}
                areVulnsSelected={
                  remediationModal.selectedVulnerabilities.length > 0
                }
                isEditing={isEditing}
                isOpen={isOpen}
                isRequestingReattack={isRequestingVerify}
                isVerifying={isVerifying}
                onEdit={toggleEdit}
                onRequestReattack={toggleRequestVerify}
                onVerify={toggleVerify}
                openHandleAcceptance={toggleHandleAcceptanceModal}
                openModal={toggleModal}
              />
            }
            isEditing={isEditing}
            isRequestingReattack={isRequestingVerify}
            isVerifyingRequest={isVerifying}
            onNextPage={handleNextPage}
            onSearch={handleSearch}
            onVulnSelect={openRemediationModal}
            refetchData={refetch}
            size={size}
            vulnerabilities={vulnerabilities}
          />
        </div>
        {isOpen && (
          <UpdateVerificationModal
            clearSelected={_.get(remediationModal, "clearSelected")}
            handleCloseModal={closeRemediationModal}
            isReattacking={isRequestingVerify}
            isVerifying={isVerifying}
            refetchData={refetch}
            setRequestState={toggleRequestVerify}
            setVerifyState={toggleVerify}
            vulns={remediationModal.selectedVulnerabilities}
          />
        )}
        {isHandleAcceptanceModalOpen && (
          <HandleAcceptanceModal
            groupName={groupName}
            handleCloseModal={toggleHandleAcceptanceModal}
            refetchData={refetch}
            vulns={vulnerabilitiesZeroRisk}
          />
        )}
        {isEditing && (
          <Modal
            onClose={handleCloseUpdateModal}
            open={isEditing}
            title={t("searchFindings.tabDescription.editVuln")}
          >
            <UpdateDescription
              groupName={groupName}
              handleClearSelected={_.get(remediationModal, "clearSelected")}
              handleCloseModal={handleCloseUpdateModal}
              refetchData={refetch}
              vulnerabilities={remediationModal.selectedVulnerabilities}
            />
          </Modal>
        )}
      </React.Fragment>
    </React.StrictMode>
  );
};

export { GroupVulnerabilitiesView };
