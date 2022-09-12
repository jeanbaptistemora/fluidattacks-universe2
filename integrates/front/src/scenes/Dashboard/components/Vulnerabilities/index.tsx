/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type {
  ColumnDef,
  ColumnFiltersState,
  InitialTableState,
  PaginationState,
  Row,
  SortingState,
  VisibilityState,
} from "@tanstack/react-table";
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
import type { FormEvent } from "react";
import { useTranslation } from "react-i18next";

import { statusFormatter } from "./Formatter";
import {
  handleDeleteVulnerabilityHelper,
  onRemoveVulnResultHelper,
  setNonSelectable,
} from "./helpers";
import { AdditionalInformation } from "./VulnerabilityModal";

import type { IRemoveVulnAttr } from "../RemoveVulnerability/types";
import { Table } from "components/TableNew";
import { deleteFormatter } from "components/TableNew/formatters/deleteFormatter";
import type { ICellHelper } from "components/TableNew/types";
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
} from "scenes/Dashboard/components/Vulnerabilities/utils";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks/useStoredState";

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
  const [columnFilters, setColumnFilters] = useStoredState<ColumnFiltersState>(
    "vulnerabilitiesTable-columnFilters",
    []
  );
  const [columnVisibility, setColumnVisibility] =
    useStoredState<VisibilityState>("vulnerabilitiesTable-visibilityState", {
      Asignees: false,
      Locations: false,
      Treatment: false,
      description: false,
      reattack: false,
      releaseDate: false,
    });
  const [pagination, setPagination] = useStoredState<PaginationState>(
    "vulnerabilitiesTable-pagination",
    {
      pageIndex: 0,
      pageSize: 10,
    }
  );
  const [sorting, setSorting] = useStoredState<SortingState>(
    "vulnerabilitiesTable-sortingState",
    []
  );
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
    rowInfo: Row<IVulnRowAttr>
  ): (event: FormEvent) => void {
    return (event: FormEvent): void => {
      if (changePermissions !== undefined) {
        changePermissions(rowInfo.original.groupName);
      }
      setCurrentRow(rowInfo.original);
      mixpanel.track("ViewVulnerability", {
        groupName: rowInfo.original.groupName,
      });
      setIsAdditionalInfoOpen(true);
      event.stopPropagation();
    };
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
  function handleDeleteVulnerability(vulnInfo: IVulnRowAttr | undefined): void {
    handleDeleteVulnerabilityHelper(
      vulnInfo as unknown as Record<string, string>,
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

  function enabledRows(row: Row<IVulnRowAttr>): boolean {
    const temp = setNonSelectable(
      vulnerabilities,
      isRequestingReattack,
      isVerifyingRequest,
      nonValidOnReattackVulnerabilities
    );

    return !temp.includes(row.index);
  }

  const findingId: string = useMemo(
    (): string => (currentRow === undefined ? "" : currentRow.findingId),
    [currentRow]
  );
  const groupName: string = useMemo(
    (): string => (currentRow === undefined ? "" : currentRow.groupName),
    [currentRow]
  );

  const columns: ColumnDef<IVulnRowAttr>[] = [
    {
      accessorKey: "where",
      enableColumnFilter: false,
      header: t("searchFindings.tabVuln.vulnTable.where"),
    },
    {
      accessorKey: "specific",
      enableColumnFilter: false,
      header: t("searchFindings.tabVuln.vulnTable.specific"),
    },
    {
      accessorKey: "currentState",
      cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element =>
        statusFormatter(cell.getValue()),
      header: t("searchFindings.tabVuln.vulnTable.status"),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "reportDate",
      header: t("searchFindings.tabVuln.vulnTable.reportDate"),
      meta: { filterType: "dateRange" },
    },
    {
      accessorKey: "verification",
      header: t("searchFindings.tabVuln.vulnTable.reattack"),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "treatment",
      header: t("searchFindings.tabVuln.vulnTable.treatment"),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "tag",
      header: t("searchFindings.tabVuln.vulnTable.tags"),
    },
    {
      accessorFn: (row: IVulnRowAttr): string => {
        return row.treatment === "ACCEPTED_UNDEFINED" &&
          row.treatmentAcceptanceStatus !== "APPROVED"
          ? "Pending"
          : "Accepted";
      },
      header: "Treatment Acceptance",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "treatmentAssigned",
      header: "Asignees",
      meta: { filterType: "select" },
    },
  ];

  const initialstate: InitialTableState = {
    columnVisibility: {
      "Treatment Acceptance": false,
      treatmentAssigned: false,
    },
  };

  const deleteColumn: ColumnDef<IVulnRowAttr>[] = [
    {
      accessorKey: "id",
      cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element =>
        deleteFormatter(cell.row.original, handleDeleteVulnerability),
      enableColumnFilter: false,
      header: t("searchFindings.tabDescription.action"),
    },
  ];

  return (
    <React.StrictMode>
      <Table
        columnFilterSetter={setColumnFilters}
        columnFilterState={columnFilters}
        columnVisibilitySetter={setColumnVisibility}
        columnVisibilityState={columnVisibility}
        columns={[...columns, ...(canRemoveVulns ? deleteColumn : [])]}
        data={formatVulnerabilities(vulnerabilities)}
        enableColumnFilters={true}
        enableRowSelection={enabledRows}
        extraButtons={
          <div className={"dib nr0 nr1-l nr1-m pt1"}>{extraButtons}</div>
        }
        id={"vulnerabilitiesTable"}
        initState={initialstate}
        onRowClick={openAdditionalInfoModal}
        paginationSetter={setPagination}
        paginationState={pagination}
        rowSelectionSetter={
          isFindingReleased &&
          !(hideSelectVulnerability === true || findingState === "closed")
            ? setSelectedVulnerabilities
            : undefined
        }
        rowSelectionState={selectedVulnerabilities}
        sortingSetter={setSorting}
        sortingState={sorting}
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
