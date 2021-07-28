import React from "react";

import type { IZeroRiskTableProps } from "./types";

import type { IVulnDataAttr } from "../types";
import { DataTableNext } from "components/DataTableNext";
import { changeZeroRiskFormatter } from "components/DataTableNext/formatters/changeZeroRiskFormatter";
import type { IHeaderConfig } from "components/DataTableNext/types";

const ZeroRiskTable: React.FC<IZeroRiskTableProps> = (
  props: IZeroRiskTableProps
): JSX.Element => {
  const { acceptationVulns, setAcceptationVulns } = props;

  const handleRejectZeroRisk: (vulnInfo?: Dictionary<string>) => void = (
    vulnInfo?: Dictionary<string>
  ): void => {
    if (vulnInfo) {
      const newVulnList: IVulnDataAttr[] = acceptationVulns.map(
        (vuln: IVulnDataAttr): IVulnDataAttr =>
          vuln.id === vulnInfo.id
            ? {
                ...vuln,
                acceptation: vuln.acceptation === "REJECTED" ? "" : "REJECTED",
              }
            : vuln
      );
      setAcceptationVulns([...newVulnList]);
    }
  };

  const handleConfirmZeroRisk: (vulnInfo?: Dictionary<string>) => void = (
    vulnInfo?: Dictionary<string>
  ): void => {
    if (vulnInfo) {
      const newVulnList: IVulnDataAttr[] = acceptationVulns.map(
        (vuln: IVulnDataAttr): IVulnDataAttr =>
          vuln.id === vulnInfo.id
            ? {
                ...vuln,
                acceptation: vuln.acceptation === "APPROVED" ? "" : "APPROVED",
              }
            : vuln
      );
      setAcceptationVulns([...newVulnList]);
    }
  };

  const vulnsHeader: IHeaderConfig[] = [
    {
      align: "left",
      dataField: "where",
      header: "Where",
      width: "45%",
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
      approveFunction: handleConfirmZeroRisk,
      dataField: "acceptation",
      deleteFunction: handleRejectZeroRisk,
      formatter: changeZeroRiskFormatter,
      header: "Acceptation",
      width: "30%",
      wrapped: true,
    },
  ];

  return (
    <React.StrictMode>
      <DataTableNext
        bordered={false}
        dataset={acceptationVulns}
        exportCsv={false}
        headers={vulnsHeader}
        id={"vulnsToHandleAcceptation"}
        pageSize={10}
        search={false}
      />
    </React.StrictMode>
  );
};

export { ZeroRiskTable };
