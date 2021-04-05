import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route } from "react-router";

import { AdditionalInfo } from "./AdditionalInfo";
import { UpdateTreatmentModal } from "./UpdateDescription";
import { UploadVulnerabilities } from "./uploadFile";

import { ContentTab } from "../ContentTab";
import type { IDeleteVulnAttr } from "../DeleteVulnerability/types";
import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { deleteFormatter } from "components/DataTableNext/formatters";
import { filterFormatter } from "components/DataTableNext/headerFormatters/filterFormatter";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { FluidIcon } from "components/FluidIcon";
import { Modal } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import { DeleteVulnerabilityModal } from "scenes/Dashboard/components/DeleteVulnerability/index";
import type {
  IVulnComponentProps,
  IVulnDataTypeAttr,
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
import { vulnerabilityInfo } from "scenes/Dashboard/components/Vulnerabilities/vulnerabilityInfo";
import { Col100 } from "scenes/Dashboard/containers/ChartsGenericView/components/ChartCols";
import { RowCenter, TabsContainer } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
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

  const [selectedVulnerabilities, setSelectedVulnerabilities] = useState<
    IVulnRowAttr[]
  >([]);
  const [vulnerabilityId, setVulnerabilityId] = useState("");
  const [isUpdateVulnOpen, setUpdateVulnOpen] = useState(false);
  const [isDeleteVulnOpen, setDeleteVulnOpen] = useState(false);
  const [isAdditionalInfoOpen, setAdditionalInfoOpen] = useState(false);
  const [currentRow, updateRow] = useState<IVulnRowAttr>();

  function openAdditionalInfoModal(
    _0: React.FormEvent,
    vulnerability: IVulnRowAttr
  ): void {
    track("ViewVulnerability", { groupName });
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
        t("searchFindings.tabDescription.vulnDeleted"),
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

  useEffect(onVulnSelection, [selectedVulnerabilities, onVulnSelect]);

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
          t("searchFindings.tabDescription.vulnBatchLimit", {
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
      header: t("searchFindings.tabVuln.vulnTable.where"),
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
      header: t("searchFindings.tabDescription.action"),
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
          headerTitle={t("searchFindings.tabDescription.editVuln")}
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
                  id={t("searchFindings.tabDescription.editVulnTooltip.id")}
                  message={t("searchFindings.tabDescription.editVulnTooltip")}
                  placement={"top"}
                >
                  <Button
                    disabled={selectedVulnerabilities.length === 0}
                    onClick={openUpdateVulnModal}
                  >
                    <FluidIcon icon={"edit"} />
                    {t("searchFindings.tabDescription.editVuln")}
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
        headerTitle={t("searchFindings.tabVuln.vulnerabilityInfo")}
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
                title={t("searchFindings.tabVuln.contentTab.details.title")}
                tooltip={t("searchFindings.tabVuln.contentTab.details.tooltip")}
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
                    "searchFindings.tabVuln.contentTab.treatments.title"
                  )}
                  tooltip={t(
                    "searchFindings.tabVuln.contentTab.treatments.tooltip"
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
