import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, {
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { useTranslation } from "react-i18next";

import { statusFormatter } from "./Formatter";
import {
  handleDeleteVulnerabilityHelper,
  onRemoveVulnResultHelper,
  onSelectVariousVulnerabilitiesHelper,
  setNonSelectable,
} from "./helpers";
import { AdditionalInformation } from "./VulnerabilityModal";

import type { IRemoveVulnAttr } from "../RemoveVulnerability/types";
import { Table } from "components/Table";
import { deleteFormatter } from "components/Table/formatters";
import type { IHeaderConfig, ISelectRowProps } from "components/Table/types";
import { DeleteVulnerabilityModal } from "scenes/Dashboard/components/RemoveVulnerability/index";
import type {
  IVulnComponentProps,
  IVulnRowAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import {
  filterOutVulnerabilities,
  formatVulnerabilities,
  getNonSelectableVulnerabilitiesOnReattackIds,
  getNonSelectableVulnerabilitiesOnVerifyIds,
  getVulnerabilitiesIndex,
} from "scenes/Dashboard/components/Vulnerabilities/utils";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";

function usePreviousProps(value: boolean): boolean {
  const ref = useRef(false);
  useEffect((): void => {
    // eslint-disable-next-line fp/no-mutation
    ref.current = value;
  });

  return ref.current;
}

export const VulnComponent: React.FC<IVulnComponentProps> = ({
  canDisplayHacker,
  changePermissions,
  clearFiltersButton,
  customFilters,
  customSearch,
  extraButtons,
  findingState,
  hideSelectVulnerability,
  isEditing,
  isFindingReleased,
  isRequestingReattack,
  isVerifyingRequest,
  refetchData,
  nonValidOnReattackVulnerabilities,
  vulnerabilities,
  onVulnSelect,
}: IVulnComponentProps): JSX.Element => {
  const { t } = useTranslation();
  const attributes: PureAbility<string> = useContext(authzGroupContext);
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
  const canRemoveVulns: boolean =
    permissions.can("api_mutations_remove_vulnerability_mutate") &&
    attributes.can("can_report_vulnerabilities");

  const [selectedVulnerabilities, setSelectedVulnerabilities] = useState<
    IVulnRowAttr[]
  >([]);
  const [vulnerabilityId, setVulnerabilityId] = useState("");
  const [isDeleteVulnOpen, setIsDeleteVulnOpen] = useState(false);
  const [isAdditionalInfoOpen, setIsAdditionalInfoOpen] = useState(false);
  const [currentRow, setCurrentRow] = useState<IVulnRowAttr>();
  const previousIsEditing = usePreviousProps(isEditing);
  const previousIsRequestingReattack = usePreviousProps(isRequestingReattack);
  const previousIsVerifyingRequest = usePreviousProps(isVerifyingRequest);

  function openAdditionalInfoModal(
    _0: React.FormEvent,
    vulnerability: IVulnRowAttr
  ): void {
    if (changePermissions !== undefined) {
      changePermissions(vulnerability.groupName);
    }
    setCurrentRow(vulnerability);
    mixpanel.track("ViewVulnerability", { groupName: vulnerability.groupName });
    setIsAdditionalInfoOpen(true);
  }
  const closeAdditionalInfoModal: () => void = useCallback((): void => {
    setIsAdditionalInfoOpen(false);
  }, []);
  const handleCloseDeleteModal: () => void = useCallback((): void => {
    setIsDeleteVulnOpen(false);
  }, []);
  function onDeleteVulnResult(removeVulnResult: IRemoveVulnAttr): void {
    refetchData();
    onRemoveVulnResultHelper(removeVulnResult, t);
    setIsDeleteVulnOpen(false);
  }
  function handleDeleteVulnerability(
    vulnInfo: Record<string, string> | undefined
  ): void {
    handleDeleteVulnerabilityHelper(
      vulnInfo,
      setVulnerabilityId,
      setIsDeleteVulnOpen,
      setCurrentRow,
      vulnerabilities
    );
  }
  const clearSelectedVulns: () => void = useCallback((): void => {
    setSelectedVulnerabilities([]);
  }, []);

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
          const nonValidIds =
            nonValidOnReattackVulnerabilities === undefined
              ? []
              : nonValidOnReattackVulnerabilities.map(
                  (vulnerability: IVulnRowAttr): string => vulnerability.id
                );
          const newVulnerabilities: IVulnRowAttr[] = filterOutVulnerabilities(
            currentVulnerabilities,
            vulnerabilities,
            getNonSelectableVulnerabilitiesOnReattackIds
          ).filter(
            (vuln: IVulnRowAttr): boolean => !nonValidIds.includes(vuln.id)
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
    hideSelectColumn:
      hideSelectVulnerability === true || findingState === "closed",
    mode: "checkbox",
    nonSelectable: setNonSelectable(
      vulnerabilities,
      isRequestingReattack,
      isVerifyingRequest,
      nonValidOnReattackVulnerabilities
    ),
    onSelect: onSelectOneVulnerability,
    onSelectAll: onSelectVariousVulnerabilities,
    selected: getVulnerabilitiesIndex(selectedVulnerabilities, vulnerabilities),
  };

  function onSortVulns(dataField: string, order: SortOrder): void {
    const newSorted = { dataField, order };
    sessionStorage.setItem("vulnerabilitiesSort", JSON.stringify(newSorted));
  }

  const findingId: string = useMemo(
    (): string => (currentRow === undefined ? "" : currentRow.findingId),
    [currentRow]
  );
  const groupName: string = useMemo(
    (): string => (currentRow === undefined ? "" : currentRow.groupName),
    [currentRow]
  );

  const headers: IHeaderConfig[] = [
    {
      dataField: "where",
      header: t("searchFindings.tabVuln.vulnTable.where"),
      onSort: onSortVulns,
    },
    {
      dataField: "specific",
      header: t("searchFindings.tabVuln.vulnTable.specific"),
      onSort: onSortVulns,
    },
    {
      dataField: "currentState",
      formatter: statusFormatter,
      header: t("searchFindings.tabVuln.vulnTable.status"),
      onSort: onSortVulns,
    },
    {
      dataField: "reportDate",
      header: t("searchFindings.tabVuln.vulnTable.reportDate"),
      onSort: onSortVulns,
    },
    {
      dataField: "verification",
      header: t("searchFindings.tabVuln.vulnTable.reattack"),
      onSort: onSortVulns,
    },
    {
      dataField: "treatment",
      header: t("searchFindings.tabVuln.vulnTable.treatment"),
      onSort: onSortVulns,
    },
    {
      dataField: "tag",
      header: t("searchFindings.tabVuln.vulnTable.tags"),
      onSort: onSortVulns,
    },
  ];
  const deleteHeader: IHeaderConfig[] = [
    {
      dataField: "id",
      deleteFunction: handleDeleteVulnerability,
      formatter: deleteFormatter,
      header: t("searchFindings.tabDescription.action"),
      visible: canRemoveVulns,
      width: "60px",
    },
  ];
  const sortPreference = sessionStorage.getItem("vulnerabilitiesSort");

  return (
    <React.StrictMode>
      <Table
        clearFiltersButton={clearFiltersButton}
        customFilters={customFilters}
        customSearch={customSearch}
        dataset={formatVulnerabilities(vulnerabilities)}
        defaultSorted={
          sortPreference === null ? undefined : JSON.parse(sortPreference)
        }
        exportCsv={false}
        extraButtonsRight={
          <div className={"dib nr0 nr1-l nr1-m pt1"}>{extraButtons}</div>
        }
        headers={[...headers, ...(canRemoveVulns ? deleteHeader : [])]}
        id={"vulnerabilitiesTable"}
        pageSize={10}
        rowEvents={{ onClick: openAdditionalInfoModal }}
        search={false}
        selectionMode={isFindingReleased ? selectionMode : undefined}
      />
      <DeleteVulnerabilityModal
        findingId={findingId}
        id={vulnerabilityId}
        onClose={handleCloseDeleteModal}
        onRemoveVulnRes={onDeleteVulnResult}
        open={isDeleteVulnOpen}
      />
      {currentRow ? (
        <AdditionalInformation
          canDisplayHacker={canDisplayHacker}
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
          refetchData={refetchData}
        />
      ) : undefined}
    </React.StrictMode>
  );
};
