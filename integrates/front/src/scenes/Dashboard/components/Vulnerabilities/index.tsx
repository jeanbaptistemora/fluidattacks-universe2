import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useEffect, useRef, useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { useTranslation } from "react-i18next";

import {
  handleDeleteVulnerabilityHelper,
  onRemoveVulnResultHelper,
  onSelectVariousVulnerabilitiesHelper,
  setColumnHelper,
  setNonSelectable,
} from "./helpers";
import { UploadVulnerabilities } from "./uploadFile";
import { AdditionalInformation } from "./VulnerabilityModal";

import type { IRemoveVulnAttr } from "../RemoveVulnerability/types";
import { DataTableNext } from "components/DataTableNext";
import { deleteFormatter } from "components/DataTableNext/formatters";
import { filterFormatter } from "components/DataTableNext/headerFormatters/filterFormatter";
import type {
  IFilterProps,
  IHeaderConfig,
  ISelectRowProps,
} from "components/DataTableNext/types";
import {
  filterDate,
  filterSearchText,
  filterSelect,
  filterText,
} from "components/DataTableNext/utils";
import { DeleteVulnerabilityModal } from "scenes/Dashboard/components/RemoveVulnerability/index";
import type {
  IVulnComponentProps,
  IVulnRowAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import {
  filterOutVulnerabilities,
  filterTreatment,
  filterTreatmentCurrentStatus,
  formatVulnerabilities,
  getNonSelectableVulnerabilitiesOnReattackIds,
  getNonSelectableVulnerabilitiesOnVerifyIds,
  getVulnerabilitiesIndex,
} from "scenes/Dashboard/components/Vulnerabilities/utils";
import { vulnerabilityInfo } from "scenes/Dashboard/components/Vulnerabilities/vulnerabilityInfo";
import { Col100 } from "scenes/Dashboard/containers/ChartsGenericView/components/ChartCols";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks";

function usePreviousProps(value: boolean): boolean {
  const ref = useRef(false);
  useEffect((): void => {
    // eslint-disable-next-line fp/no-mutation
    ref.current = value;
  });

  return ref.current;
}

export const VulnComponent: React.FC<IVulnComponentProps> = ({
  canDisplayAnalyst,
  findingId,
  findingState,
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
  const canRemoveVulnsTags: boolean = permissions.can(
    "api_mutations_remove_vulnerability_tags_mutate"
  );
  const canRequestZeroRiskVuln: boolean = permissions.can(
    "api_mutations_request_vulnerabilities_zero_risk_mutate"
  );
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "api_mutations_update_vulnerabilities_treatment_mutate"
  );
  const canRemoveVulns: boolean = permissions.can(
    "api_mutations_remove_vulnerability_mutate"
  );

  const [selectedVulnerabilities, setSelectedVulnerabilities] = useState<
    IVulnRowAttr[]
  >([]);
  const [vulnerabilityId, setVulnerabilityId] = useState("");
  const [isDeleteVulnOpen, setDeleteVulnOpen] = useState(false);
  const [isAdditionalInfoOpen, setAdditionalInfoOpen] = useState(false);
  const [currentRow, updateRow] = useState<IVulnRowAttr>();
  const previousIsEditing = usePreviousProps(isEditing);
  const previousIsRequestingReattack = usePreviousProps(isRequestingReattack);
  const previousIsVerifyingRequest = usePreviousProps(isVerifyingRequest);

  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("locationsCustomFilters", false);
  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [treatmentFilter, setTreatmentFilter] = useState("");
  const [reportDateFilter, setReportDateFilter] = useState("");
  const [tagFilter, setTagFilter] = useState("");
  const [currentStatusFilter, setCurrentStatusFilter] = useState("");
  const [treatmentCurrentStatusFilter, setTreatmentCurrentStatusFilter] =
    useState("");
  const [verificationFilter, setVerificationFilter] = useState("");

  const handleUpdateCustomFilter: () => void = useCallback((): void => {
    setCustomFilterEnabled(!isCustomFilterEnabled);
  }, [isCustomFilterEnabled, setCustomFilterEnabled]);

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
  function handleCloseDeleteModal(): void {
    setDeleteVulnOpen(false);
  }
  function onDeleteVulnResult(removeVulnResult: IRemoveVulnAttr): void {
    onRemoveVulnResultHelper(removeVulnResult, t);
    setDeleteVulnOpen(false);
  }
  function handleDeleteVulnerability(
    vulnInfo: Record<string, string> | undefined
  ): void {
    handleDeleteVulnerabilityHelper(
      vulnInfo,
      setVulnerabilityId,
      setDeleteVulnOpen
    );
  }
  function clearSelectedVulns(): void {
    setSelectedVulnerabilities([]);
  }

  function onVulnSelection(): void {
    if (previousIsRequestingReattack && !isRequestingReattack) {
      setSelectedVulnerabilities([]);
      onVulnSelect([], clearSelectedVulns);
    }
    if (previousIsVerifyingRequest && !isVerifyingRequest) {
      setSelectedVulnerabilities([]);
      onVulnSelect([], clearSelectedVulns);
    }
    if (previousIsEditing && !isEditing) {
      setSelectedVulnerabilities([]);
      onVulnSelect([], clearSelectedVulns);
    }
    if (!previousIsRequestingReattack && isRequestingReattack) {
      setSelectedVulnerabilities(
        (currentVulnerabilities: IVulnRowAttr[]): IVulnRowAttr[] => {
          const newVulnerabilities: IVulnRowAttr[] = filterOutVulnerabilities(
            currentVulnerabilities,
            vulnerabilities,
            getNonSelectableVulnerabilitiesOnReattackIds
          );
          onVulnSelect(newVulnerabilities, clearSelectedVulns);

          return newVulnerabilities;
        }
      );
    }
    if (!previousIsVerifyingRequest && isVerifyingRequest) {
      setSelectedVulnerabilities(
        (currentVulnerabilities: IVulnRowAttr[]): IVulnRowAttr[] => {
          const newVulnerabilities: IVulnRowAttr[] = filterOutVulnerabilities(
            currentVulnerabilities,
            vulnerabilities,
            getNonSelectableVulnerabilitiesOnVerifyIds
          );

          onVulnSelect(newVulnerabilities, clearSelectedVulns);

          return newVulnerabilities;
        }
      );
    }
    onVulnSelect(selectedVulnerabilities, clearSelectedVulns);
  }
  // Annotation needed as adding the dependencies creates a memory leak
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(onVulnSelection, [
    selectedVulnerabilities,
    onVulnSelect,
    isEditing,
    isRequestingReattack,
    isVerifyingRequest,
    previousIsEditing,
    previousIsRequestingReattack,
    previousIsVerifyingRequest,
  ]);

  function onSelectVariousVulnerabilities(
    isSelect: boolean,
    vulnerabilitiesSelected: IVulnRowAttr[]
  ): string[] {
    return onSelectVariousVulnerabilitiesHelper(
      isSelect,
      vulnerabilitiesSelected,
      selectedVulnerabilities,
      setSelectedVulnerabilities
    );
  }

  function onSelectOneVulnerability(
    vulnerability: IVulnRowAttr,
    isSelect: boolean
  ): boolean {
    onSelectVariousVulnerabilities(isSelect, [vulnerability]);

    return true;
  }

  const selectionMode: ISelectRowProps = {
    clickToSelect: false,
    hideSelectColumn: findingState === "closed",
    mode: "checkbox",
    nonSelectable: setNonSelectable(
      vulnerabilities,
      isRequestingReattack,
      isVerifyingRequest
    ),
    onSelect: onSelectOneVulnerability,
    onSelectAll: onSelectVariousVulnerabilities,
    selected: getVulnerabilitiesIndex(selectedVulnerabilities, vulnerabilities),
  };

  function onSortVulns(dataField: string, order: SortOrder): void {
    const newSorted = { dataField, order };
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
      visible: canRemoveVulns,
      width: "60px",
    },
  ];

  function columnHelper(): JSX.Element {
    return (
      <Col100>
        <Can do={"api_mutations_upload_file_mutate"}>
          <UploadVulnerabilities findingId={findingId} groupName={groupName} />
        </Can>
      </Col100>
    );
  }

  function setColumn(): JSX.Element | undefined {
    return setColumnHelper(true, columnHelper);
  }

  const vulnerabilitiesDataset = formatVulnerabilities(vulnerabilities);

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const filterSearchTextVulnerabilities: IVulnRowAttr[] = filterSearchText(
    vulnerabilitiesDataset,
    searchTextFilter
  );

  function onTreatmentChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    setTreatmentFilter(event.target.value);
  }
  const filterTreatmentVulnerabilities: IVulnRowAttr[] = filterTreatment(
    vulnerabilitiesDataset,
    treatmentFilter
  );
  function onReportDateChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setReportDateFilter(event.target.value);
  }
  const filterReportDateVulnerabilities: IVulnRowAttr[] = filterDate(
    vulnerabilitiesDataset,
    reportDateFilter,
    "reportDate"
  );

  function onTagChange(event: React.ChangeEvent<HTMLInputElement>): void {
    setTagFilter(event.target.value);
  }
  const filterTagVulnerabilities: IVulnRowAttr[] = filterText(
    vulnerabilitiesDataset,
    tagFilter,
    "tag"
  );

  function onStatusChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    setCurrentStatusFilter(event.target.value);
  }
  const filterCurrentStatusVulnerabilities: IVulnRowAttr[] = filterSelect(
    vulnerabilitiesDataset,
    currentStatusFilter,
    "currentState"
  );

  function onTreatmentStatusChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    setTreatmentCurrentStatusFilter(event.target.value);
  }
  const filterTreatmentCurrentStatusVulnerabilities: IVulnRowAttr[] =
    filterTreatmentCurrentStatus(
      vulnerabilitiesDataset,
      treatmentCurrentStatusFilter
    );

  function onVerificationChange(
    event: React.ChangeEvent<HTMLSelectElement>
  ): void {
    setVerificationFilter(event.target.value);
  }
  const filterVerificationVulnerabilities: IVulnRowAttr[] = filterSelect(
    vulnerabilitiesDataset,
    verificationFilter,
    "verification"
  );

  const resultVulnerabilities: IVulnRowAttr[] = _.intersection(
    filterSearchTextVulnerabilities,
    filterTreatmentCurrentStatusVulnerabilities,
    filterTreatmentVulnerabilities,
    filterCurrentStatusVulnerabilities,
    filterVerificationVulnerabilities,
    filterReportDateVulnerabilities,
    filterTagVulnerabilities
  );

  const customFiltersProps: IFilterProps[] = [
    {
      defaultValue: reportDateFilter,
      onChangeInput: onReportDateChange,
      placeholder: "Report date",
      tooltipId: "searchFindings.tabVuln.vulnTable.dateTooltip.id",
      tooltipMessage: "searchFindings.tabVuln.vulnTable.dateTooltip",
      type: "date",
    },
    {
      defaultValue: treatmentFilter,
      onChangeSelect: onTreatmentChange,
      placeholder: "Treatment",
      /* eslint-disable sort-keys */
      selectOptions: {
        NEW: "searchFindings.tabDescription.treatment.new",
        IN_PROGRESS: "searchFindings.tabDescription.treatment.inProgress",
        ACCEPTED: "searchFindings.tabDescription.treatment.accepted",
        ACCEPTED_UNDEFINED:
          "searchFindings.tabDescription.treatment.acceptedUndefined",
      },
      /* eslint-enable sort-keys */
      tooltipId: "searchFindings.tabVuln.vulnTable.treatmentsTooltip.id",
      tooltipMessage: "searchFindings.tabVuln.vulnTable.treatmentsTooltip",
      type: "select",
    },
    {
      defaultValue: verificationFilter,
      onChangeSelect: onVerificationChange,
      placeholder: "Reattacks",
      selectOptions: {
        Requested: "searchFindings.tabVuln.requested",
        Verified: "searchFindings.tabVuln.verified",
      },
      tooltipId: "searchFindings.tabVuln.vulnTable.reattacksTooltip.id",
      tooltipMessage: "searchFindings.tabVuln.vulnTable.reattacksTooltip",
      type: "select",
    },
    {
      defaultValue: currentStatusFilter,
      onChangeSelect: onStatusChange,
      placeholder: "Status",
      selectOptions: {
        closed: "searchFindings.tabVuln.closed",
        open: "searchFindings.tabVuln.open",
      },
      tooltipId: "searchFindings.tabVuln.statusTooltip.id",
      tooltipMessage: "searchFindings.tabVuln.statusTooltip",
      type: "select",
    },
    {
      defaultValue: treatmentCurrentStatusFilter,
      onChangeSelect: onTreatmentStatusChange,
      placeholder: "Treatment Acceptation",
      selectOptions: {
        false: "Accepted",
        true: "Pending",
      },
      tooltipId: "searchFindings.tabVuln.treatmentStatus.id",
      tooltipMessage: "searchFindings.tabVuln.treatmentStatus",
      type: "select",
    },
    {
      defaultValue: tagFilter,
      onChangeInput: onTagChange,
      placeholder: "searchFindings.tabVuln.searchTag",
      tooltipId: "searchFindings.tabVuln.tagTooltip.id",
      tooltipMessage: "searchFindings.tabVuln.tagTooltip",
      type: "text",
    },
  ];

  return (
    <React.StrictMode>
      <DataTableNext
        bordered={true}
        customFilters={{
          customFiltersProps,
          isCustomFilterEnabled,
          onUpdateEnableCustomFilter: handleUpdateCustomFilter,
        }}
        customSearch={{
          customSearchDefault: searchTextFilter,
          isCustomSearchEnabled: true,
          onUpdateCustomSearch: onSearchTextChange,
        }}
        dataset={resultVulnerabilities}
        defaultSorted={JSON.parse(
          _.get(sessionStorage, "vulnerabilitiesSort", "{}") as string
        )}
        exportCsv={false}
        headers={[...headers, ...(canRemoveVulns ? deleteHeader : [])]}
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
        onRemoveVulnRes={onDeleteVulnResult}
        open={isDeleteVulnOpen}
      />
      {setColumn()}
      <AdditionalInformation
        canDisplayAnalyst={canDisplayAnalyst}
        canRemoveVulnsTags={canRemoveVulnsTags}
        canRequestZeroRiskVuln={canRequestZeroRiskVuln}
        canUpdateVulnsTreatment={canUpdateVulnsTreatment}
        clearSelectedVulns={clearSelectedVulns}
        closeAdditionalInfoModal={closeAdditionalInfoModal}
        currentRow={currentRow}
        findingId={findingId}
        groupName={groupName}
        isAdditionalInfoOpen={isAdditionalInfoOpen}
        isFindingReleased={isFindingReleased}
      />
    </React.StrictMode>
  );
};
