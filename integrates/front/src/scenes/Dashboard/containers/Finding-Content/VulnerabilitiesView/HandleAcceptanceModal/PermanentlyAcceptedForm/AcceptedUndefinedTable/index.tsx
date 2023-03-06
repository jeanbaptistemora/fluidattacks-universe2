import type { ColumnDef } from "@tanstack/react-table";
import React from "react";

import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";
import { changeVulnTreatmentFormatter } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/HandleAcceptanceModal/PermanentlyAcceptedForm/AcceptedUndefinedTable/changeVulnTreatmentFormatter";
import type { IAcceptedUndefinedTableProps } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/HandleAcceptanceModal/PermanentlyAcceptedForm/AcceptedUndefinedTable/types";
import type { IVulnDataAttr } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/HandleAcceptanceModal/types";

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
