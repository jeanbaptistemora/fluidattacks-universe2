import type { ColumnDef } from "@tanstack/react-table";
import React from "react";
import { useTranslation } from "react-i18next";

import { changeSubmittedFormatter } from "./changeSubmittedFormatter";
import type { ISubmittedTableProps } from "./types";

import type { IVulnDataAttr } from "../../types";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";

const SubmittedTable: React.FC<ISubmittedTableProps> = (
  props: ISubmittedTableProps
): JSX.Element => {
  const {
    acceptanceVulns,
    isConfirmRejectVulnerabilitySelected,
    setAcceptanceVulns,
  } = props;

  const { t } = useTranslation();

  const handleRejectSubmitted = (vulnInfo?: IVulnDataAttr): void => {
    if (vulnInfo) {
      const newVulnList: IVulnDataAttr[] = acceptanceVulns.map(
        (vuln: IVulnDataAttr): IVulnDataAttr =>
          vuln.id === vulnInfo.id
            ? {
                ...vuln,
                acceptance: vuln.acceptance === "REJECTED" ? "" : "REJECTED",
              }
            : vuln
      );
      setAcceptanceVulns([...newVulnList]);
    }
  };

  const handleConfirmSubmitted = (vulnInfo?: IVulnDataAttr): void => {
    if (vulnInfo) {
      const newVulnList: IVulnDataAttr[] = acceptanceVulns.map(
        (vuln: IVulnDataAttr): IVulnDataAttr =>
          vuln.id === vulnInfo.id
            ? {
                ...vuln,
                acceptance: vuln.acceptance === "APPROVED" ? "" : "APPROVED",
              }
            : vuln
      );
      setAcceptanceVulns([...newVulnList]);
    }
  };

  const columns: ColumnDef<IVulnDataAttr>[] = [
    {
      accessorKey: "where",
      header: t(
        "searchFindings.tabVuln.handleAcceptanceModal.submittedForm.submittedTable.where"
      ),
    },
    {
      accessorKey: "specific",
      header: t(
        "searchFindings.tabVuln.handleAcceptanceModal.submittedForm.submittedTable.specific"
      ),
    },
    {
      accessorKey: "acceptance",
      cell: (cell: ICellHelper<IVulnDataAttr>): JSX.Element =>
        changeSubmittedFormatter(
          cell.row.original,
          handleConfirmSubmitted,
          handleRejectSubmitted
        ),
      header: t(
        "searchFindings.tabVuln.handleAcceptanceModal.submittedForm.submittedTable.acceptance"
      ),
    },
  ];

  return (
    <React.StrictMode>
      {isConfirmRejectVulnerabilitySelected ? (
        <Table columns={columns} data={acceptanceVulns} id={"submittedTable"} />
      ) : undefined}
    </React.StrictMode>
  );
};

export { SubmittedTable };
