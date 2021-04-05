import React from "react";

import type { IAcceptedUndefinedTableProps } from "./types";

import type { IVulnDataAttr } from "../types";
import { DataTableNext } from "components/DataTableNext";
import { changeVulnTreatmentFormatter } from "components/DataTableNext/formatters";
import type { IHeaderConfig } from "components/DataTableNext/types";

const AcceptedUndefinedTable: React.FC<IAcceptedUndefinedTableProps> = (
  props: IAcceptedUndefinedTableProps
): JSX.Element => {
  const {
    acceptationVulns,
    isAcceptedUndefinedSelected,
    setAcceptationVulns,
  } = props;

  const handleUpdateAcceptation: (vulnInfo: Dictionary<string>) => void = (
    vulnInfo: Dictionary<string>
  ): void => {
    const newVulnList: IVulnDataAttr[] = acceptationVulns.map(
      (vuln: IVulnDataAttr): IVulnDataAttr =>
        vuln.id === vulnInfo.id
          ? {
              ...vuln,
              acceptation:
                vuln.acceptation === "APPROVED" ? "REJECTED" : "APPROVED",
            }
          : vuln
    );
    setAcceptationVulns([...newVulnList]);
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
      changeFunction: handleUpdateAcceptation,
      dataField: "acceptation",
      formatter: changeVulnTreatmentFormatter,
      header: "Acceptation",
      width: "25%",
      wrapped: true,
    },
  ];

  return (
    <React.StrictMode>
      {isAcceptedUndefinedSelected ? (
        <DataTableNext
          bordered={false}
          dataset={acceptationVulns}
          exportCsv={false}
          headers={vulnsHeader}
          id={"vulnsToHandleAcceptation"}
          pageSize={10}
          search={false}
        />
      ) : undefined}
    </React.StrictMode>
  );
};

export { AcceptedUndefinedTable };
