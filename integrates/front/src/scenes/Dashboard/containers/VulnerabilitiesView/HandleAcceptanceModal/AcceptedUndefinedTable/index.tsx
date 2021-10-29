import React from "react";

import type { IAcceptedUndefinedTableProps } from "./types";

import type { IVulnDataAttr } from "../types";
import { DataTableNext } from "components/DataTableNext";
import { changeVulnTreatmentFormatter } from "components/DataTableNext/formatters";
import type { IHeaderConfig } from "components/DataTableNext/types";

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
      align: "left",
      dataField: "where",
      header: "Where",
      width: "50%",
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
        <DataTableNext
          bordered={false}
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
