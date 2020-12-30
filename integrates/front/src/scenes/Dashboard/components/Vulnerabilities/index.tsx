import { Button } from "components/Button";
import { Can } from "utils/authz/Can";
import { Col100 } from "scenes/Dashboard/containers/ChartsGenericView/components/ChartCols";
import { DataTableNext } from "components/DataTableNext";
import { DeleteVulnerabilityModal } from "scenes/Dashboard/components/DeleteVulnerability/index";
import { FluidIcon } from "components/FluidIcon";
import type { IDeleteVulnAttr } from "../DeleteVulnerability/types";
import type { IHeaderConfig } from "components/DataTableNext/types";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { RowCenter } from "styles/styledComponents";
import { UpdateTreatmentModal } from "./UpdateDescription";
import { UploadVulnerabilities } from "./uploadFile";
import _ from "lodash";
import { authzPermissionsContext } from "utils/authz/config";
import { filterFormatter } from "components/DataTableNext/headerFormatters/filterFormatter";
import { proFormatter } from "components/DataTableNext/headerFormatters/proFormatter";
import { useAbility } from "@casl/react";
import { useStoredState } from "utils/hooks";
import { useTranslation } from "react-i18next";
import type {
  IVulnComponentProps,
  IVulnDataTypeAttr,
  IVulnRowAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import {
  deleteFormatter,
  statusFormatter,
} from "components/DataTableNext/formatters";
import {
  formatVulnerabilities,
  getNonSelectableVulnerabilitiesOnEdit,
  getNonSelectableVulnerabilitiesOnReattack,
  getNonSelectableVulnerabilitiesOnVerify,
  getVulnerabilitiesIds,
  getVulnerabilitiesIndex,
} from "scenes/Dashboard/components/Vulnerabilities/utils";
import { msgError, msgSuccess } from "utils/notifications";
import { selectFilter, textFilter } from "react-bootstrap-table2-filter";

export const VulnComponent: React.FC<IVulnComponentProps> = ({
  findingId,
  groupName,
  isEditing,
  isRequestingReattack,
  isVerifyingRequest,
  vulnerabilities,
  onVulnSelect,
}: IVulnComponentProps): JSX.Element => {
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRequestZeroRiskVuln: boolean = permissions.can(
    "backend_api_mutations_request_zero_risk_vuln_mutate"
  );
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "backend_api_mutations_update_vulns_treatment_mutate"
  );
  const canDeleteVulns: boolean =
    isEditing &&
    permissions.can("backend_api_mutations_delete_vulnerability_mutate");

  const [selectedVulnerabilities, setSelectedVulnerabilities] = React.useState<
    IVulnRowAttr[]
  >([]);
  const [vulnerabilityId, setVulnerabilityId] = React.useState("");
  const [isUpdateVulnOpen, setUpdateVulnOpen] = React.useState(false);
  const [isDeleteVulnOpen, setDeleteVulnOpen] = React.useState(false);
  const [checkedItems, setCheckedItems] = useStoredState<
    Record<string, boolean>
  >(
    "VulnerabilitiesTableSet",
    {
      currentState: true,
      cycles: false,
      efficacy: false,
      lastReattackDate: false,
      lastRequestedReattackDate: false,
      reportDate: false,
      severity: true,
      specific: true,
      tag: true,
      treatment: true,
      treatmentChanges: false,
      treatmentDate: false,
      treatmentManager: true,
      verification: true,
      vulnType: true,
      where: true,
      zeroRisk: true,
    },
    localStorage
  );

  function handleCloseUpdateModal(): void {
    setUpdateVulnOpen(false);
  }
  function handleCloseDeleteModal(): void {
    setDeleteVulnOpen(false);
  }
  function onDeleteVulnResult(deleteVulnResult: IDeleteVulnAttr): void {
    if (deleteVulnResult.deleteVulnerability.success) {
      msgSuccess(
        t("search_findings.tab_description.vulnDeleted"),
        t("group_alerts.title_success")
      );
    } else {
      msgError(t("delete_vulns.not_success"));
    }
    setDeleteVulnOpen(false);
  }
  function handleDeleteVulnerability(
    vulnInfo: Record<string, string> | undefined
  ): void {
    if (vulnInfo !== undefined) {
      setVulnerabilityId(vulnInfo.id);
      setDeleteVulnOpen(true);
    }
  }
  function openUpdateVulnModal(): void {
    setUpdateVulnOpen(true);
  }
  function clearSelectedVulns(): void {
    setSelectedVulnerabilities([]);
  }

  function onVulnSelection(): void {
    onVulnSelect(selectedVulnerabilities, clearSelectedVulns);
  }

  React.useEffect(onVulnSelection, [selectedVulnerabilities, onVulnSelect]);

  const selectOptionsStatus: optionSelectFilterProps[] = [
    { label: "Open", value: "Open" },
    { label: "Closed", value: "Closed" },
  ];

  function onFilterStatus(filterValue: string): void {
    sessionStorage.setItem("statusFilter", filterValue);
  }

  function handleChange(columnName: string): void {
    if (
      Object.values(checkedItems).filter((val: boolean): boolean => val)
        .length === 1 &&
      checkedItems[columnName]
    ) {
      msgError(t("validations.columns"));
      setCheckedItems({
        ...checkedItems,
        [columnName]: true,
      });
    } else {
      setCheckedItems({
        ...checkedItems,
        [columnName]: !checkedItems[columnName],
      });
    }
  }

  function onSelectVariousVulnerabilities(
    isSelect: boolean,
    vulnerabilitiesSelected: IVulnRowAttr[]
  ): void {
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
              (selectedVulnerability: IVulnDataTypeAttr): boolean =>
                !vulnerabilitiesIds.includes(selectedVulnerability.id)
            )
          )
        )
      );
    }
  }

  function onSelectOneVulnerability(
    vulnerability: IVulnRowAttr,
    isSelect: boolean
  ): void {
    onSelectVariousVulnerabilities(isSelect, [vulnerability]);
  }

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

  function onSortVulns(dataField: string, order: SortOrder): void {
    const newSorted: Sorted = { dataField, order };
    sessionStorage.setItem("vulnerabilitiesSort", JSON.stringify(newSorted));
  }

  function onFilterWhere(filterVal: string): void {
    sessionStorage.setItem("vulnWhereFilter", filterVal);
  }

  const headers: IHeaderConfig[] = [
    {
      dataField: "vulnType",
      header: t("search_findings.tab_vuln.vulnTable.vulnType.title"),
      onSort: onSortVulns,
      visible: checkedItems.vulnType,
    },
    {
      dataField: "where",
      filter: textFilter({
        defaultValue: _.get(sessionStorage, "vulnWhereFilter"),
        onFilter: onFilterWhere,
      }),
      header: t("search_findings.tab_vuln.vulnTable.where"),
      headerFormatter: filterFormatter,
      onSort: onSortVulns,
      visible: checkedItems.where,
    },
    {
      dataField: "specific",
      header: t("search_findings.tab_vuln.vulnTable.specific"),
      onSort: onSortVulns,
      visible: checkedItems.specific,
    },
    {
      dataField: "reportDate",
      header: t("search_findings.tab_vuln.vulnTable.reportDate"),
      onSort: onSortVulns,
      visible: checkedItems.reportDate,
    },
    {
      dataField: "currentStateCapitalized",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "statusFilter"),
        onFilter: onFilterStatus,
        options: selectOptionsStatus,
      }),
      formatter: statusFormatter,
      header: t("search_findings.tab_vuln.vulnTable.status"),
      headerFormatter: filterFormatter,
      onSort: onSortVulns,
      visible: checkedItems.currentState,
    },
    {
      dataField: "tag",
      header: t("search_findings.tab_description.tag"),
      headerFormatter: proFormatter,
      onSort: onSortVulns,
      visible: checkedItems.tag,
    },
    {
      dataField: "severity",
      header: t("search_findings.tab_description.business_criticality"),
      headerFormatter: proFormatter,
      onSort: onSortVulns,
      visible: checkedItems.severity,
    },
    {
      dataField: "verification",
      formatter: statusFormatter,
      header: t("search_findings.tab_vuln.vulnTable.verification"),
      onSort: onSortVulns,
      visible: checkedItems.verification,
    },
    {
      align: "left",
      dataField: "zeroRisk",
      formatter: statusFormatter,
      header: t("search_findings.tab_description.zero_risk"),
      onSort: onSortVulns,
      visible: checkedItems.zeroRisk,
    },
    {
      dataField: "lastRequestedReattackDate",
      header: t("search_findings.tab_vuln.vulnTable.lastRequestedReattackDate"),
      onSort: onSortVulns,
      visible: checkedItems.lastRequestedReattackDate,
    },
    {
      dataField: "lastReattackDate",
      header: t("search_findings.tab_vuln.vulnTable.lastReattackDate"),
      onSort: onSortVulns,
      visible: checkedItems.lastReattackDate,
    },
    {
      dataField: "cycles",
      header: t("search_findings.tab_vuln.vulnTable.cycles"),
      onSort: onSortVulns,
      visible: checkedItems.cycles,
    },
    {
      dataField: "efficacy",
      header: t("search_findings.tab_vuln.vulnTable.efficacy"),
      onSort: onSortVulns,
      visible: checkedItems.efficacy,
    },
    {
      dataField: "treatment",
      header: t("search_findings.tab_description.treatment.title"),
      onSort: onSortVulns,
      visible: checkedItems.treatment,
    },
    {
      dataField: "treatmentManager",
      header: t("search_findings.tab_description.treatment_mgr"),
      onSort: onSortVulns,
      visible: checkedItems.treatmentManager,
    },
    {
      dataField: "treatmentDate",
      header: t("search_findings.tab_vuln.vulnTable.treatmentDate"),
      onSort: onSortVulns,
      visible: checkedItems.treatmentDate,
    },
    {
      dataField: "treatmentChanges",
      header: t("search_findings.tab_vuln.vulnTable.treatmentChanges"),
      onSort: onSortVulns,
      visible: checkedItems.treatmentChanges,
    },
  ];
  const deleteHeader: IHeaderConfig[] = [
    {
      align: "center",
      dataField: "id",
      deleteFunction: handleDeleteVulnerability,
      formatter: deleteFormatter,
      header: t("search_findings.tab_description.action"),
      visible: canDeleteVulns,
    },
  ];

  return (
    <React.StrictMode>
      <DataTableNext
        bordered={true}
        columnToggle={true}
        dataset={formatVulnerabilities(vulnerabilities)}
        defaultSorted={JSON.parse(
          _.get(sessionStorage, "vulnerabilitiesSort", "{}")
        )}
        exportCsv={false}
        headers={[...headers, ...(canDeleteVulns ? deleteHeader : [])]}
        id={"vulnerabilitiesTable"}
        onColumnToggle={handleChange}
        pageSize={15}
        search={true}
        selectionMode={selectionMode}
      />
      <DeleteVulnerabilityModal
        findingId={findingId}
        id={vulnerabilityId}
        onClose={handleCloseDeleteModal}
        onDeleteVulnRes={onDeleteVulnResult}
        open={isDeleteVulnOpen}
      />
      {isUpdateVulnOpen ? (
        <UpdateTreatmentModal
          findingId={findingId}
          handleClearSelected={clearSelectedVulns}
          handleCloseModal={handleCloseUpdateModal}
          projectName={groupName}
          vulnerabilities={selectedVulnerabilities}
          vulnerabilitiesChunk={100}
        />
      ) : undefined}
      {isEditing ? (
        <Col100>
          {canUpdateVulnsTreatment || canRequestZeroRiskVuln ? (
            <React.Fragment>
              <RowCenter>
                <Button
                  disabled={selectedVulnerabilities.length === 0}
                  onClick={openUpdateVulnModal}
                >
                  <FluidIcon icon={"edit"} />
                  {t("search_findings.tab_description.editVuln")}
                </Button>
              </RowCenter>
              <br />
            </React.Fragment>
          ) : undefined}
          <Can do={"backend_api_mutations_upload_file_mutate"}>
            <UploadVulnerabilities
              findingId={findingId}
              groupName={groupName}
            />
          </Can>
        </Col100>
      ) : undefined}
    </React.StrictMode>
  );
};
