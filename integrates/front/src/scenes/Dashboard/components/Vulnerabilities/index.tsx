import { AdditionalInfo } from "./AdditionalInfo";
import { Button } from "components/Button";
import { Can } from "utils/authz/Can";
import { Col100 } from "scenes/Dashboard/containers/ChartsGenericView/components/ChartCols";
import { DataTableNext } from "components/DataTableNext";
import { DeleteVulnerabilityModal } from "scenes/Dashboard/components/DeleteVulnerability/index";
import { FluidIcon } from "components/FluidIcon";
import type { IDeleteVulnAttr } from "../DeleteVulnerability/types";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Modal } from "components/NewModal";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { UpdateTreatmentModal } from "./UpdateDescription";
import { UploadVulnerabilities } from "./uploadFile";
import _ from "lodash";
import { authzPermissionsContext } from "utils/authz/config";
import { filterFormatter } from "components/DataTableNext/headerFormatters/filterFormatter";
import { useAbility } from "@casl/react";
import { useTranslation } from "react-i18next";
import { ButtonToolbar, Row, RowCenter } from "styles/styledComponents";
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
  canDisplayAnalyst,
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
  const [isAdditionalInfoOpen, setAdditionalInfoOpen] = React.useState(false);
  const [currentRow, updateRow] = React.useState<IVulnRowAttr>();

  function openAdditionalInfoModal(
    _0: React.FormEvent,
    vulnerability: IVulnRowAttr
  ): void {
    updateRow(vulnerability);
    setAdditionalInfoOpen(true);
  }
  function closeAdditionalInfoModal(): void {
    setAdditionalInfoOpen(false);
  }
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
      width: "40%",
      wrapped: true,
    },
    {
      dataField: "specific",
      header: t("search_findings.tab_vuln.vulnTable.specific"),
      onSort: onSortVulns,
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
    },
    {
      dataField: "verification",
      formatter: statusFormatter,
      header: t("search_findings.tab_vuln.vulnTable.verification"),
      onSort: onSortVulns,
    },
    {
      dataField: "treatment",
      header: t("search_findings.tab_description.treatment.title"),
      onSort: onSortVulns,
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
        dataset={formatVulnerabilities(vulnerabilities)}
        defaultSorted={JSON.parse(
          _.get(sessionStorage, "vulnerabilitiesSort", "{}")
        )}
        exportCsv={false}
        headers={[...headers, ...(canDeleteVulns ? deleteHeader : [])]}
        id={"vulnerabilitiesTable"}
        pageSize={15}
        rowEvents={{ onClick: openAdditionalInfoModal }}
        search={true}
        selectionMode={selectionMode}
      />
      <DeleteVulnerabilityModal
        findingId={findingId}
        groupName={groupName}
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
      <Modal
        headerTitle={t("search_findings.tab_vuln.vulnerabilityInfo")}
        open={isAdditionalInfoOpen}
      >
        {_.isUndefined(currentRow) ? undefined : (
          <AdditionalInfo
            canDisplayAnalyst={canDisplayAnalyst}
            vulnerability={currentRow}
          />
        )}
        <hr />
        <Row>
          <Col100>
            <ButtonToolbar>
              <Button
                id={"close-vuln-modal"}
                onClick={closeAdditionalInfoModal}
              >
                {t("search_findings.tab_vuln.close")}
              </Button>
            </ButtonToolbar>
          </Col100>
        </Row>
      </Modal>
    </React.StrictMode>
  );
};
