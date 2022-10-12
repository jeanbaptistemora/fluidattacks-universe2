/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ColumnDef } from "@tanstack/react-table";
import React from "react";

import { changeZeroRiskFormatter } from "./changeZeroRiskFormatter";
import type { IZeroRiskTableProps } from "./types";

import type { IVulnDataAttr } from "../types";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";

const ZeroRiskTable: React.FC<IZeroRiskTableProps> = (
  props: IZeroRiskTableProps
): JSX.Element => {
  const {
    acceptanceVulns,
    isConfirmRejectZeroRiskSelected,
    setAcceptanceVulns,
  } = props;

  const handleRejectZeroRisk = (vulnInfo?: IVulnDataAttr): void => {
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

  const handleConfirmZeroRisk = (vulnInfo?: IVulnDataAttr): void => {
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
        changeZeroRiskFormatter(
          cell.row.original,
          handleConfirmZeroRisk,
          handleRejectZeroRisk
        ),
      header: "Acceptance",
    },
  ];

  return (
    <React.StrictMode>
      {isConfirmRejectZeroRiskSelected ? (
        <Table
          columns={columns}
          data={acceptanceVulns}
          id={"vulnsToHandleAcceptance"}
        />
      ) : undefined}
    </React.StrictMode>
  );
};

export { ZeroRiskTable };
