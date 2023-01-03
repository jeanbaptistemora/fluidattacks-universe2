import type { ColumnDef } from "@tanstack/react-table";
import React from "react";

import { changeSubmittedFormatter } from "./changeSubmittedFormatter";
import type { ISubmittedTableProps } from "./types";

import type { IVulnDataAttr } from "../types";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";

const SubmittedTable: React.FC<ISubmittedTableProps> = (
  props: ISubmittedTableProps
): JSX.Element => {
  const { acceptanceVulns, isOpenRejectLocationSelected, setAcceptanceVulns } =
    props;

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

  const handleOpenSubmitted = (vulnInfo?: IVulnDataAttr): void => {
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
      header: "Where",
    },
    {
      accessorKey: "specific",
      header: "Specific",
    },
    {
      accessorKey: "acceptance",
      cell: (cell: ICellHelper<IVulnDataAttr>): JSX.Element =>
        changeSubmittedFormatter(
          cell.row.original,
          handleOpenSubmitted,
          handleRejectSubmitted
        ),
      header: "Acceptance",
    },
  ];

  return (
    <React.StrictMode>
      {isOpenRejectLocationSelected ? (
        <Table columns={columns} data={acceptanceVulns} id={"submittedTable"} />
      ) : undefined}
    </React.StrictMode>
  );
};

export { SubmittedTable };
