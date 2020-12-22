import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
import type { IVulnDataAttr } from "../types";
import type { IZeroRiskRejectionTableProps } from "./types";
import React from "react";
import { changeZeroRiskRejectionFormatter } from "components/DataTableNext/formatters/changeZeroRiskRejectionFormatter";

const ZeroRiskRejectionTable: React.FC<IZeroRiskRejectionTableProps> = (
  props: IZeroRiskRejectionTableProps
): JSX.Element => {
  const {
    acceptationVulns,
    isRejectZeroRiskSelected,
    setAcceptationVulns,
  } = props;

  const handleUpdateZeroRiskRejection: (
    vulnInfo: Dictionary<string>
  ) => void = (vulnInfo: Dictionary<string>): void => {
    const newVulnList: IVulnDataAttr[] = acceptationVulns.map(
      (vuln: IVulnDataAttr): IVulnDataAttr =>
        vuln.id !== vulnInfo.id
          ? vuln
          : {
              ...vuln,
              acceptation: vuln.acceptation === "REJECTED" ? "" : "REJECTED",
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
      changeFunction: handleUpdateZeroRiskRejection,
      dataField: "acceptation",
      formatter: changeZeroRiskRejectionFormatter,
      header: "Acceptation",
      width: "30%",
      wrapped: true,
    },
  ];

  return (
    <React.StrictMode>
      {isRejectZeroRiskSelected ? (
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

export { ZeroRiskRejectionTable };
