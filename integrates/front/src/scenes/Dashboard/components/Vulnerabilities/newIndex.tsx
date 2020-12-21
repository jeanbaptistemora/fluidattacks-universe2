import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
import React from "react";
import _ from "lodash";
import { proFormatter } from "components/DataTableNext/headerFormatters/proFormatter";
import { statusFormatter } from "components/DataTableNext/formatters";
import { useTranslation } from "react-i18next";
import type {
  IVulnComponentProps,
  IVulnDataType,
  IVulnRowAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import {
  formatVulnerabilities,
  getNonSelectableVulnerabilitiesOnEdit,
  getNonSelectableVulnerabilitiesOnReattack,
  getNonSelectableVulnerabilitiesOnVerify,
  getVulnerabilitiesIds,
  getVulnerabilitiesIndex,
} from "scenes/Dashboard/components/Vulnerabilities/utils";
import { selectFilter, textFilter } from "react-bootstrap-table2-filter";

export const VulnComponent: React.FC<IVulnComponentProps> = ({
  isEditing,
  isRequestingReattack,
  isVerifyingRequest,
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

  const selectOptionsStatus: optionSelectFilterProps[] = [
    { label: "Open", value: "Open" },
    { label: "Closed", value: "Closed" },
  ];

  const onFilterStatus: (filterValue: string) => void = (
    filterValue: string
  ): void => {
    sessionStorage.setItem("statusFilter", filterValue);
  };

  const onSelectVariousVulnerabilities: (
    isSelect: boolean,
    vulnerabilitiesSelected: IVulnRowAttr[]
  ) => void = (
    isSelect: boolean,
    vulnerabilitiesSelected: IVulnRowAttr[]
  ): void => {
    if (isSelect) {
      setSelectedVulnerabilities(
        Array.from(
          new Set([...selectedVulnerabilities, ...vulnerabilitiesSelected])
        )
      );
    } else {
      const vulnerabilitiesIds: string[] = getVulnerabilitiesIds(
        vulnerabilitiesSelected
      );
      setSelectedVulnerabilities(
        Array.from(
          new Set(
            selectedVulnerabilities.filter(
              (selectedVulnerability: IVulnDataType): boolean =>
                !vulnerabilitiesIds.includes(selectedVulnerability.id)
            )
          )
        )
      );
    }
  };

  const onSelectOneVulnerability: (
    vulnerability: IVulnRowAttr,
    isSelect: boolean
  ) => void = (vulnerability: IVulnRowAttr, isSelect: boolean): void => {
    onSelectVariousVulnerabilities(isSelect, [vulnerability]);
  };

  const selectionMode: SelectRowOptions = {
    clickToSelect: false,
    hideSelectColumn: !(
      isEditing ||
      isRequestingReattack ||
      isVerifyingRequest
    ),
    mode: "checkbox",
    nonSelectable: isEditing
      ? getNonSelectableVulnerabilitiesOnEdit(vulnerabilities)
      : isRequestingReattack
      ? getNonSelectableVulnerabilitiesOnReattack(vulnerabilities)
      : isVerifyingRequest
      ? getNonSelectableVulnerabilitiesOnVerify(vulnerabilities)
      : undefined,
    onSelect: onSelectOneVulnerability,
    onSelectAll: onSelectVariousVulnerabilities,
    selected: getVulnerabilitiesIndex(selectedVulnerabilities, vulnerabilities),
  };

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
      header: t("search_findings.tab_vuln.vulnTable.reportDate"),
      onSort: onSortVulns,
    },
    {
      dataField: "currentState",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "statusFilter"),
        onFilter: onFilterStatus,
        options: selectOptionsStatus,
      }),
      formatter: statusFormatter,
      header: t("search_findings.tab_vuln.vulnTable.status"),
      onSort: onSortVulns,
    },
    {
      dataField: "tag",
      header: t("search_findings.tab_description.tag"),
      headerFormatter: proFormatter,
      onSort: onSortVulns,
    },
    {
      dataField: "severity",
      header: t("search_findings.tab_description.business_criticality"),
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
    {
      dataField: "treatmentDate",
      header: t("search_findings.tab_vuln.vulnTable.treatmentDate"),
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
        selectionMode={selectionMode}
      />
    </React.StrictMode>
  );
};
