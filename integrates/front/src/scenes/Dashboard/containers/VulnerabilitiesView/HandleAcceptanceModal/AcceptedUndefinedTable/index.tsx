import React from "react";

import type { IAcceptedUndefinedTableProps } from "./types";

import type { IVulnDataAttr } from "../types";
import { Table } from "components/Table";
import { changeVulnTreatmentFormatter } from "components/Table/formatters";
import type { IHeaderConfig } from "components/Table/types";

const AcceptedUndefinedTable: React.FC<IAcceptedUndefinedTableProps> = (
  props: IAcceptedUndefinedTableProps
): JSX.Element => {
  const { acceptanceVulns, isAcceptedUndefinedSelected, setAcceptanceVulns } =
    props;

  const handleUpdateAcceptance: (vulnInfo: Dictionary<string>) => void = (
    vulnInfo: Dictionary<string>
  ): void => {
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
  const vulnsHeader: IHeaderConfig[] = [
    {
      dataField: "where",
      header: "Where",
      width: "50%",
      wrapped: true,
    },
    {
      dataField: "specific",
      header: "Specific",
      width: "25%",
      wrapped: true,
    },
    {
      changeFunction: handleUpdateAcceptance,
      dataField: "acceptance",
      formatter: changeVulnTreatmentFormatter,
      header: "Acceptance",
      width: "25%",
      wrapped: true,
    },
  ];

  return (
    <React.StrictMode>
      {isAcceptedUndefinedSelected ? (
        <Table
          dataset={acceptanceVulns}
          exportCsv={false}
          headers={vulnsHeader}
          id={"vulnsToHandleAcceptance"}
          pageSize={10}
          search={false}
        />
      ) : undefined}
    </React.StrictMode>
  );
};

export { AcceptedUndefinedTable };
