import React from "react";

import type { IZeroRiskConfirmationTableProps } from "./types";

import type { IVulnDataAttr } from "../types";
import { DataTableNext } from "components/DataTableNext";
import { changeZeroRiskConfirmationFormatter } from "components/DataTableNext/formatters/changeZeroRiskConfirmationFormatter";
import type { IHeaderConfig } from "components/DataTableNext/types";

const ZeroRiskConfirmationTable: React.FC<IZeroRiskConfirmationTableProps> = (
  props: IZeroRiskConfirmationTableProps
): JSX.Element => {
  const { acceptanceVulns, isConfirmZeroRiskSelected, setAcceptanceVulns } =
    props;

  const handleUpdateZeroRiskConfirmation: (
    vulnInfo: Dictionary<string>
  ) => void = (vulnInfo: Dictionary<string>): void => {
    const newVulnList: IVulnDataAttr[] = acceptanceVulns.map(
      (vuln: IVulnDataAttr): IVulnDataAttr =>
        vuln.id === vulnInfo.id
          ? {
              ...vuln,
              acceptation: vuln.acceptation === "APPROVED" ? "" : "APPROVED",
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
      changeFunction: handleUpdateZeroRiskConfirmation,
      dataField: "acceptation",
      formatter: changeZeroRiskConfirmationFormatter,
      header: "Acceptance",
      width: "30%",
      wrapped: true,
    },
  ];

  return (
    <React.StrictMode>
      {isConfirmZeroRiskSelected ? (
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

export { ZeroRiskConfirmationTable };
