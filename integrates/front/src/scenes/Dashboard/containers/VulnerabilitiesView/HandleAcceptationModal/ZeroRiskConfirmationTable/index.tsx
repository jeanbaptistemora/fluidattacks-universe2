import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
import type { IVulnDataAttr } from "../types";
import type { IZeroRiskConfirmationTableProps } from "./types";
import React from "react";
import { changeZeroRiskConfirmationFormatter } from "components/DataTableNext/formatters/changeZeroRiskConfirmationFormatter";

const ZeroRiskConfirmationTable: React.FC<IZeroRiskConfirmationTableProps> = (
  props: IZeroRiskConfirmationTableProps
): JSX.Element => {
  const {
    acceptationVulns,
    isConfirmZeroRiskSelected,
    setAcceptationVulns,
  } = props;

  const handleUpdateZeroRiskConfirmation: (
    vulnInfo: Dictionary<string>
  ) => void = (vulnInfo: Dictionary<string>): void => {
    const newVulnList: IVulnDataAttr[] = acceptationVulns.map(
      (vuln: IVulnDataAttr): IVulnDataAttr =>
        vuln.id !== vulnInfo.id
          ? vuln
          : {
              ...vuln,
              acceptation: vuln.acceptation === "APPROVED" ? "" : "APPROVED",
            }
    );
    setAcceptationVulns([...newVulnList]);
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
      header: "Acceptation",
      width: "30%",
      wrapped: true,
    },
  ];

  return (
    <React.StrictMode>
      {isConfirmZeroRiskSelected ? (
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

export { ZeroRiskConfirmationTable };
