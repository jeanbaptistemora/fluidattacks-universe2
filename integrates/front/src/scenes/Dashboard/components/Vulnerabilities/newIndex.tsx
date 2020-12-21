import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
import React from "react";
import _ from "lodash";
import { formatVulnerabilities } from "scenes/Dashboard/components/Vulnerabilities/utils";
import { proFormatter } from "components/DataTableNext/headerFormatters/proFormatter";
import { statusFormatter } from "components/DataTableNext/formatters";
import { textFilter } from "react-bootstrap-table2-filter";
import { useTranslation } from "react-i18next";
import type {
  IVulnComponentProps,
  IVulnRowAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";

export const VulnComponent: React.FC<IVulnComponentProps> = ({
  vulnerabilities,
  onVulnSelect,
}: IVulnComponentProps): JSX.Element => {
  const { t } = useTranslation();
  const [selectedVulnerabilities, setSelectedVulnerabilities] = React.useState<
    IVulnRowAttr[]
  >([]);

  const clearSelectedVulns: () => void = (): void => {
    setSelectedVulnerabilities([]);
  };

  const onVulnSelection: () => void = (): void => {
    onVulnSelect(selectedVulnerabilities, clearSelectedVulns);
  };

  React.useEffect(onVulnSelection, [selectedVulnerabilities, onVulnSelect]);

  const onSortVulns: (dataField: string, order: SortOrder) => void = (
    dataField: string,
    order: SortOrder
  ): void => {
    const newSorted: Sorted = { dataField, order };
    sessionStorage.setItem("vulnerabilitiesSort", JSON.stringify(newSorted));
  };

  const onFilterWhere: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("vulnWhereFilter", filterVal);
  };

  const headers: IHeaderConfig[] = [
    {
      dataField: "where",
      filter: textFilter({
        defaultValue: _.get(sessionStorage, "vulnWhereFilter"),
        onFilter: onFilterWhere,
      }),
      header: t("search_findings.tab_vuln.vulnTable.where"),
      onSort: onSortVulns,
    },
    {
      dataField: "specific",
      header: t("search_findings.tab_description.field"),
      onSort: onSortVulns,
    },
    {
      dataField: "reportDate",
      header: t("Report date"),
      onSort: onSortVulns,
    },
    {
      dataField: "tag",
      header: t("search_findings.tab_description.tag"),
      headerFormatter: proFormatter,
      onSort: onSortVulns,
    },
    {
      dataField: "verification",
      formatter: statusFormatter,
      header: t("search_findings.tab_vuln.vulnTable.verification"),
      onSort: onSortVulns,
    },
    {
      dataField: "lastRequestedReattackDate",
      header: t("search_findings.tab_vuln.vulnTable.lastRequestedReattackDate"),
      onSort: onSortVulns,
    },
    {
      dataField: "cycles",
      header: t("search_findings.tab_vuln.vulnTable.cycles"),
      onSort: onSortVulns,
    },
    {
      dataField: "efficacy",
      header: t("search_findings.tab_vuln.vulnTable.efficacy"),
      onSort: onSortVulns,
    },
    {
      dataField: "treatment",
      header: t("search_findings.tab_description.treatment.title"),
      onSort: onSortVulns,
    },
    {
      dataField: "treatmentManager",
      header: t("search_findings.tab_description.treatment_mgr"),
      onSort: onSortVulns,
    },
  ];

  return (
    <React.StrictMode>
      <DataTableNext
        bordered={true}
        dataset={formatVulnerabilities(vulnerabilities)}
        defaultSorted={JSON.parse(
          _.get(sessionStorage, "vulnerabilitiesSort", "{}")
        )}
        exportCsv={false}
        headers={headers}
        id={"vulnerabilitiesTable"}
        pageSize={15}
        search={true}
      />
    </React.StrictMode>
  );
};
