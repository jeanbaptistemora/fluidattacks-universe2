import { AdditionalInfo } from "./AdditionalInfo";
import { Button } from "components/Button";
import { Can } from "utils/authz/Can";
import { Col100 } from "scenes/Dashboard/containers/ChartsGenericView/components/ChartCols";
import { ContentTab } from "../ContentTab";
import { DataTableNext } from "components/DataTableNext";
import { DeleteVulnerabilityModal } from "scenes/Dashboard/components/DeleteVulnerability/index";
import { FluidIcon } from "components/FluidIcon";
import type { IDeleteVulnAttr } from "../DeleteVulnerability/types";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Modal } from "components/Modal";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import { UpdateTreatmentModal } from "./UpdateDescription";
import { UploadVulnerabilities } from "./uploadFile";
import _ from "lodash";
import { authzPermissionsContext } from "utils/authz/config";
import { deleteFormatter } from "components/DataTableNext/formatters";
import { filterFormatter } from "components/DataTableNext/headerFormatters/filterFormatter";
import mixpanel from "mixpanel-browser";
import { useAbility } from "@casl/react";
import { useTranslation } from "react-i18next";
import { vulnerabilityInfo } from "scenes/Dashboard/components/Vulnerabilities/vulnerabilityInfo";
import type {
  IVulnComponentProps,
  IVulnDataTypeAttr,
  IVulnRowAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import { MemoryRouter, Route } from "react-router";
import { RowCenter, TabsContainer } from "styles/styledComponents";
import {
  formatVulnerabilities,
  getNonSelectableVulnerabilitiesOnEdit,
  getNonSelectableVulnerabilitiesOnReattack,
  getNonSelectableVulnerabilitiesOnVerify,
  getVulnerabilitiesIds,
  getVulnerabilitiesIndex,
} from "scenes/Dashboard/components/Vulnerabilities/utils";
import { msgError, msgSuccess } from "utils/notifications";

export const VulnComponent: React.FC<IVulnComponentProps> = ({
  canDisplayAnalyst,
  findingId,
  groupName,
  isEditing,
  isFindingReleased,
  isRequestingReattack,
  isVerifyingRequest,
  vulnerabilities,
  onVulnSelect,
}: IVulnComponentProps): JSX.Element => {
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canDeleteVulnsTags: boolean = permissions.can(
    "backend_api_mutations_delete_vulnerability_tags_mutate"
  );
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
    mixpanel.track("ViewVulnerability", { groupName });
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
        t("groupAlerts.titleSuccess")
      );
    } else {
      msgError(t("deleteVulns.notSuccess"));
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

  const batchLimit: number = 50;

  function onSelectVariousVulnerabilities(
    isSelect: boolean,
    vulnerabilitiesSelected: IVulnRowAttr[]
  ): string[] {
    if (isSelect) {
      const vulnsToSet: IVulnRowAttr[] = Array.from(
        new Set([...selectedVulnerabilities, ...vulnerabilitiesSelected])
      ).slice(0, batchLimit);
      setSelectedVulnerabilities(vulnsToSet);

      return vulnsToSet.map((vuln: IVulnRowAttr): string => vuln.id);
    }
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

    return selectedVulnerabilities.map((vuln: IVulnRowAttr): string => vuln.id);
  }

  function onSelectOneVulnerability(
    vulnerability: IVulnRowAttr,
    isSelect: boolean
  ): boolean {
    if (isSelect) {
      if (selectedVulnerabilities.length === batchLimit) {
        msgError(
          t("search_findings.tab_description.vulnBatchLimit", {
            count: batchLimit,
          })
        );

        return false;
      }
    }
    onSelectVariousVulnerabilities(isSelect, [vulnerability]);

    return true;
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

  const headers: IHeaderConfig[] = [
    {
      dataField: "where",
      formatter: vulnerabilityInfo,
      header: t("search_findings.tab_vuln.vulnTable.where"),
      headerFormatter: filterFormatter,
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
      width: "5%",
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
        pageSize={10}
        rowEvents={{ onClick: openAdditionalInfoModal }}
        search={false}
        selectionMode={isFindingReleased ? selectionMode : undefined}
        striped={true}
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
        <Modal
          headerTitle={t("search_findings.tab_description.editVuln")}
          open={isUpdateVulnOpen}
        >
          <UpdateTreatmentModal
            findingId={findingId}
            handleClearSelected={clearSelectedVulns}
            handleCloseModal={handleCloseUpdateModal}
            projectName={groupName}
            vulnerabilities={selectedVulnerabilities}
          />
        </Modal>
      ) : undefined}
      {isEditing ? (
        <Col100>
          {isFindingReleased &&
          (canUpdateVulnsTreatment || canRequestZeroRiskVuln) ? (
            <React.Fragment>
              <RowCenter>
                <TooltipWrapper
                  id={t("search_findings.tab_description.editVulnTooltip.id")}
                  message={t("search_findings.tab_description.editVulnTooltip")}
                  placement={"top"}
                >
                  <Button
                    disabled={selectedVulnerabilities.length === 0}
                    onClick={openUpdateVulnModal}
                  >
                    <FluidIcon icon={"edit"} />
                    {t("search_findings.tab_description.editVuln")}
                  </Button>
                </TooltipWrapper>
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
          <MemoryRouter
            initialEntries={["/details", "/treatments"]}
            initialIndex={0}
          >
            <TabsContainer>
              <ContentTab
                icon={"icon pe-7s-graph3"}
                id={"vulnerabilityDetailsTab"}
                link={"/details"}
                title={t("search_findings.tab_vuln.contentTab.details.title")}
                tooltip={t(
                  "search_findings.tab_vuln.contentTab.details.tooltip"
                )}
              />
              {currentRow.currentState === "open" &&
              isFindingReleased &&
              (canUpdateVulnsTreatment ||
                canRequestZeroRiskVuln ||
                canDeleteVulnsTags) ? (
                <ContentTab
                  icon={"icon pe-7s-note"}
                  id={"vulnerabilityTreatmentsTab"}
                  link={"/treatments"}
                  title={t(
                    "search_findings.tab_vuln.contentTab.treatments.title"
                  )}
                  tooltip={t(
                    "search_findings.tab_vuln.contentTab.treatments.tooltip"
                  )}
                />
              ) : undefined}
            </TabsContainer>
            <br />
            <Route path={"/details"}>
              <AdditionalInfo
                canDisplayAnalyst={canDisplayAnalyst}
                onClose={closeAdditionalInfoModal}
                vulnerability={currentRow}
              />
            </Route>
            <Route path={"/treatments"}>
              <UpdateTreatmentModal
                findingId={findingId}
                handleClearSelected={clearSelectedVulns}
                handleCloseModal={closeAdditionalInfoModal}
                projectName={groupName}
                vulnerabilities={[currentRow]}
              />
            </Route>
          </MemoryRouter>
        )}
      </Modal>
    </React.StrictMode>
  );
};
