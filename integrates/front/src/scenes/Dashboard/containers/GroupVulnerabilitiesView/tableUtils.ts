import type { ColumnDef } from "@tanstack/react-table";

import { requirementsTitleFormatter } from "./formatters/requirementTitleFormatter";

import type { IFilter } from "components/Filter";
import { formatLinkHandler } from "components/Table/formatters/linkFormatter";
import type { ICellHelper } from "components/Table/types";
import { vulnerabilityFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/vulnerabilityFormat";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { translate } from "utils/translations/translate";

const tableColumns: ColumnDef<IVulnRowAttr>[] = [
  {
    accessorKey: "where",
    cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element =>
      vulnerabilityFormatter({
        reattack: cell.row.original.verification as string,
        source: cell.row.original.vulnerabilityType,
        specific: cell.row.original.specific,
        status: cell.row.original.currentState,
        treatment: cell.row.original.treatment,
        where: cell.getValue(),
      }),
    enableColumnFilter: false,
    header: "Vulnerability",
  },
  {
    accessorFn: (row: IVulnRowAttr): string => String(row.finding?.title),
    cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element => {
      const link = `vulns/${String(cell.row.original.finding?.id)}/description`;
      const text = cell.getValue<string>();

      return formatLinkHandler(link, text);
    },
    enableColumnFilter: false,
    header: "Type",
  },
  {
    accessorFn: (row: IVulnRowAttr): string => String(row.requirements),
    cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element =>
      requirementsTitleFormatter({
        reqsList: cell.row.original.requirements,
      }),
    enableColumnFilter: false,
    header: "Criteria",
  },
  {
    accessorKey: "reportDate",
    enableColumnFilter: false,
    header: "Found",
  },
  {
    accessorFn: (row: IVulnRowAttr): number =>
      Number(row.finding?.severityScore),
    cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element => {
      const link = `vulns/${String(cell.row.original.finding?.id)}/severity`;
      const text = cell.getValue<string>();

      return formatLinkHandler(link, text);
    },
    enableColumnFilter: false,
    header: "Severity",
  },
  {
    accessorFn: (): string => "View",
    cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element => {
      const link = `vulns/${String(cell.row.original.finding?.id)}/evidence`;
      const text = cell.getValue<string>();

      return formatLinkHandler(link, text);
    },
    enableColumnFilter: false,
    header: "Evidence",
  },
];

const tableFilters: IFilter<IVulnRowAttr>[] = [
  {
    id: "root",
    key: "where",
    label: "Root",
    type: "text",
  },
  {
    id: "currentState",
    key: "currentState",
    label: "Status",
    selectOptions: [
      {
        header: translate.t("searchFindings.header.status.stateLabel.open"),
        value: "open",
      },
      {
        header: translate.t("searchFindings.header.status.stateLabel.closed"),
        value: "closed",
      },
    ],
    type: "select",
  },
  {
    id: "type",
    key: "vulnerabilityType",
    label: "Source",
    selectOptions: [
      {
        header: translate.t(
          "searchFindings.tabVuln.vulnTable.vulnerabilityType.inputs"
        ),
        value: "INPUTS",
      },
      {
        header: translate.t(
          "searchFindings.tabVuln.vulnTable.vulnerabilityType.ports"
        ),
        value: "PORTS",
      },
      {
        header: translate.t(
          "searchFindings.tabVuln.vulnTable.vulnerabilityType.lines"
        ),
        value: "LINES",
      },
    ],
    type: "select",
  },
  {
    id: "treatment",
    key: "treatment",
    label: "Treatment",
    selectOptions: [
      { header: "In progress", value: "IN_PROGRESS" },
      { header: "New", value: "NEW" },
      { header: "Temporarily accepted", value: "ACCEPTED" },
      { header: "Permanently accepted", value: "ACCEPTED_UNDEFINED" },
    ],
    type: "select",
  },
  {
    id: "verification",
    key: "verification",
    label: "Reattack",
    selectOptions: ["Masked", "Requested", "On_hold", "Verified"],
    type: "select",
  },
];

export { tableColumns, tableFilters };
