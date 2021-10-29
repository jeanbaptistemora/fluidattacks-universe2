import React from "react";

import type { IZeroRiskTableProps } from "./types";

import type { IVulnDataAttr } from "../types";
import { DataTableNext } from "components/DataTableNext";
import { changeZeroRiskFormatter } from "components/DataTableNext/formatters/changeZeroRiskFormatter";
import type { IHeaderConfig } from "components/DataTableNext/types";

const ZeroRiskTable: React.FC<IZeroRiskTableProps> = (
  props: IZeroRiskTableProps
): JSX.Element => {
  const {
    acceptanceVulns,
    isConfirmRejectZeroRiskSelected,
    setAcceptanceVulns,
  } = props;

  const handleRejectZeroRisk: (vulnInfo?: Dictionary<string>) => void = (
    vulnInfo?: Dictionary<string>
  ): void => {
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

  const handleConfirmZeroRisk: (vulnInfo?: Dictionary<string>) => void = (
    vulnInfo?: Dictionary<string>
  ): void => {
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

  const vulnsHeader: IHeaderConfig[] = [
    {
      align: "left",
      dataField: "where",
      header: "Where",
      width: "45%",
      wordBreak: "break-word",
      wrapped: true,
    },
    {
      align: "left",
      dataField: "specific",
      header: "Specific",
      width: "25%",
      wordBreak: "break-word",
      wrapped: true,
    },
    {
      align: "left",
      approveFunction: handleConfirmZeroRisk,
      dataField: "acceptance",
      deleteFunction: handleRejectZeroRisk,
      formatter: changeZeroRiskFormatter,
      header: "Acceptance",
      width: "30%",
      wordBreak: "break-word",
      wrapped: true,
    },
  ];

  return (
    <React.StrictMode>
      {isConfirmRejectZeroRiskSelected ? (
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

export { ZeroRiskTable };
