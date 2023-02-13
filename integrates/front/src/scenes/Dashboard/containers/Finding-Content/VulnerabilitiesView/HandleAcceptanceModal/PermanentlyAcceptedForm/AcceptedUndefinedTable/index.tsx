import type { ColumnDef } from "@tanstack/react-table";
import React from "react";

import { changeVulnTreatmentFormatter } from "./changeVulnTreatmentFormatter";
import type { IAcceptedUndefinedTableProps } from "./types";

import type { IVulnDataAttr } from "../../types";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";

const AcceptedUndefinedTable: React.FC<IAcceptedUndefinedTableProps> = (
  props: IAcceptedUndefinedTableProps
): JSX.Element => {
  const { acceptanceVulns, isAcceptedUndefinedSelected, setAcceptanceVulns } =
    props;

  const handleUpdateAcceptance = (vulnInfo: IVulnDataAttr): void => {
    const newVulnList: IVulnDataAttr[] = acceptanceVulns.map(
      (vuln: IVulnDataAttr): IVulnDataAttr =>
        vuln.id === vulnInfo.id
          ? {
              ...vuln,
              acceptance:
                vuln.acceptance === "APPROVED" ? "REJECTED" : "APPROVED",
            }
          : vuln
    );
    setAcceptanceVulns([...newVulnList]);
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
        changeVulnTreatmentFormatter(cell.row.original, handleUpdateAcceptance),
      header: "Acceptance",
    },
  ];

  return (
    <React.StrictMode>
      {isAcceptedUndefinedSelected ? (
        <Table
          columns={columns}
          data={acceptanceVulns}
          enableSearchBar={false}
          id={"vulnsToHandleAcceptance"}
        />
      ) : undefined}
    </React.StrictMode>
  );
};

export { AcceptedUndefinedTable };
