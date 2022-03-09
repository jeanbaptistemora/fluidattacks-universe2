import React from "react";

import type { IZeroRiskTableProps } from "./types";

import type { IVulnDataAttr } from "../types";
import { Table } from "components/Table";
import { changeZeroRiskFormatter } from "components/Table/formatters/changeZeroRiskFormatter";
import type { IHeaderConfig } from "components/Table/types";

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
      dataField: "where",
      header: "Where",
      width: "45%",
      wordBreak: "break-word",
      wrapped: true,
    },
    {
      dataField: "specific",
      header: "Specific",
      width: "25%",
      wordBreak: "break-word",
      wrapped: true,
    },
    {
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
        <Table
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
