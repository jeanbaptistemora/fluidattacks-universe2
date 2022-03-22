import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { useTranslation } from "react-i18next";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";

import { renderDescription } from "./description";
import {
  formatFindings,
  formatState,
  getAreAllMutationValid,
  getFindingsIndex,
  getResults,
  handleRemoveFindingsError,
  onSelectVariousFindingsHelper,
} from "./utils";

import { REMOVE_FINDING_MUTATION } from "../FindingContent/queries";
import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { Table } from "components/Table";
import { limitFormatter } from "components/Table/formatters";
import { tooltipFormatter } from "components/Table/headerFormatters/tooltipFormatter";
import { useRowExpand } from "components/Table/hooks/useRowExpand";
import type { IFilterProps, IHeaderConfig } from "components/Table/types";
import {
  filterDateRange,
  filterLastNumber,
  filterRange,
  filterSearchText,
  filterSelect,
  filterSubSelectCount,
  filterWhere,
} from "components/Table/utils";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  GET_FINDINGS,
  GET_GROUP_VULNS,
  GET_HAS_MOBILE_APP,
} from "scenes/Dashboard/containers/GroupFindingsView/queries";
import { ReportsModal } from "scenes/Dashboard/containers/GroupFindingsView/reportsModal";
import type {
  IFindingAttr,
  IGroupFindingsAttr,
} from "scenes/Dashboard/containers/GroupFindingsView/types";
import { ControlLabel, FormGroup, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { FormikDropdown } from "utils/forms/fields";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { composeValidators, required } from "utils/validations";

interface IDataResult {
  me: {
    hasMobileApp: boolean;
  };
}

interface IFilterSet {
  age: string;
  currentTreatment: string;
  lastReport: string;
  reattack: string;
  releaseDate: { max: string; min: string };
  severity: { max: string; min: string };
  type: string;
  where: string;
}
const GroupFindingsView: React.FC = (): JSX.Element => {
  const TIMEZONE_OFFSET = 60000;
  const FORMATTING_DATE_INDEX = 19;

  const now: Date = new Date();
  const timeSoFar: number = Date.now();
  const tzoffset: number = now.getTimezoneOffset() * TIMEZONE_OFFSET;
  const localIsoTime: Date = new Date(timeSoFar - tzoffset);
  const formattingDate: string = localIsoTime.toISOString();
  const currentDate: string = formattingDate.slice(0, FORMATTING_DATE_INDEX);

  const { groupName } = useParams<{ groupName: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const { push, replace } = useHistory();
  const { url } = useRouteMatch();
  const { t } = useTranslation();

  // State management
  const [isReportsModalOpen, setReportsModalOpen] = useState(false);
  const openReportsModal: () => void = useCallback((): void => {
    setReportsModalOpen(true);
  }, []);
  const closeReportsModal: () => void = useCallback((): void => {
    setReportsModalOpen(false);
  }, []);
  const [hasMobileApp, setHasMobileApp] = useState(false);

  const [checkedItems, setCheckedItems] = useStoredState<
    Record<string, boolean>
  >(
    "tableSet",
    {
      age: false,
      lastVulnerability: true,
      openVulnerabilities: true,
      remediated: false,
      severityScore: true,
      state: true,
      title: true,
      where: false,
    },
    localStorage
  );

  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("findingsCustomFilters", false);
  const [isRunning, setRunning] = useState(false);
  const [selectedFindings, setSelectedFindings] = useState<IFindingAttr[]>([]);

  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [filterGroupFindingsTable, setFilterGroupFindingsTable] =
    useStoredState<IFilterSet>(
      "filterGroupFindingsTableSet",
      {
        age: "",
        currentTreatment: "",
        lastReport: "",
        reattack: "",
        releaseDate: { max: "", min: "" },
        severity: { max: "", min: "" },
        type: "",
        where: "",
      },
      localStorage
    );
  const [
    filterGroupFindingsCurrentStatus,
    setFilterGroupFindingsCurrentStatus,
  ] = useStoredState<Record<string, string>>(
    "groupFindingsCurrentStatus",
    { currentStatus: "open" },
    localStorage
  );
  const [isDeleteModalOpen, setDeleteModalOpen] = useState(false);
  const openDeleteModal: () => void = useCallback((): void => {
    setDeleteModalOpen(true);
  }, []);
  const closeDeleteModal: () => void = useCallback((): void => {
    setDeleteModalOpen(false);
  }, []);

  const handleChange: (columnName: string) => void = useCallback(
    (columnName: string): void => {
      if (
        Object.values(checkedItems).filter((val: boolean): boolean => val)
          .length === 1 &&
        checkedItems[columnName]
      ) {
        // eslint-disable-next-line no-alert
        alert(t("validations.columns"));
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
    },
    [checkedItems, setCheckedItems, t]
  );

  const handleUpdateCustomFilter: () => void = useCallback((): void => {
    setCustomFilterEnabled(!isCustomFilterEnabled);
  }, [isCustomFilterEnabled, setCustomFilterEnabled]);

  const goToFinding: (
    event: React.FormEvent<HTMLButtonElement>,
    rowInfo: { id: string }
  ) => void = (
    _0: React.FormEvent<HTMLButtonElement>,
    rowInfo: { id: string }
  ): void => {
    push(`${url}/${rowInfo.id}/locations`);
  };

  const handleQryErrors: (error: ApolloError) => void = useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading group data", error);
      });
    },
    [t]
  );

  const onSortState: (dataField: string, order: SortOrder) => void = (
    dataField: string,
    order: SortOrder
  ): void => {
    const newSorted = { dataField, order };
    sessionStorage.setItem("findingSort", JSON.stringify(newSorted));
  };

  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "title",
      header: "Type",
      headerFormatter: tooltipFormatter,
      onSort: onSortState,
      tooltipDataField: t("group.findings.headersTooltips.type"),
      visible: checkedItems.title,
      wrapped: true,
    },
    {
      dataField: "lastVulnerability",
      formatter: (value: number): string =>
        t("group.findings.description.value", { count: value }),
      header: "Last report",
      headerFormatter: tooltipFormatter,
      onSort: onSortState,
      tooltipDataField: t("group.findings.headersTooltips.lastReport"),
      visible: checkedItems.lastVulnerability,
      wrapped: true,
    },
    {
      dataField: "state",
      formatter: formatState,
      header: "Status",
      headerFormatter: tooltipFormatter,
      onSort: onSortState,
      tooltipDataField: t("group.findings.headersTooltips.status"),
      visible: checkedItems.state,
      width: "80px",
      wrapped: true,
    },
    {
      dataField: "severityScore",
      header: "Severity",
      headerFormatter: tooltipFormatter,
      onSort: onSortState,
      tooltipDataField: t("group.findings.headersTooltips.severity"),
      visible: checkedItems.severityScore,
      wrapped: true,
    },
    {
      dataField: "openVulnerabilities",
      header: "Vulnerabilities",
      headerFormatter: tooltipFormatter,
      onSort: onSortState,
      tooltipDataField: t("group.findings.headersTooltips.locations"),
      visible: checkedItems.openVulnerabilities,
      wrapped: true,
    },
    {
      dataField: "where",
      formatter: limitFormatter,
      header: "Locations",
      headerFormatter: tooltipFormatter,
      onSort: onSortState,
      tooltipDataField: t("group.findings.headersTooltips.where"),
      visible: checkedItems.where,
      wrapped: true,
    },
    {
      dataField: "remediated",
      header: "Reattack",
      headerFormatter: tooltipFormatter,
      onSort: onSortState,
      tooltipDataField: t("group.findings.headersTooltips.reattack"),
      visible: checkedItems.remediated,
      wrapped: true,
    },
  ];

  const { data } = useQuery<IGroupFindingsAttr>(GET_FINDINGS, {
    fetchPolicy: "cache-first",
    onError: handleQryErrors,
    variables: { groupName },
  });

  const { data: vulnsData } = useQuery<IGroupFindingsAttr>(GET_GROUP_VULNS, {
    fetchPolicy: "cache-first",
    onError: handleQryErrors,
    variables: { groupName },
  });

  const { data: userData } = useQuery<IDataResult>(GET_HAS_MOBILE_APP, {
    fetchPolicy: "no-cache",
    onCompleted: (): void => {
      if (userData?.me.hasMobileApp ?? false) {
        setHasMobileApp(true);
      }
    },
    onError: (error: ApolloError): void => {
      msgError(t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred getting user info", error);
    },
  });

  const findings: IFindingAttr[] =
    data === undefined
      ? []
      : formatFindings(_.merge({}, data.group, vulnsData?.group).findings);

  const typesArray = findings.map((find: IFindingAttr): string[] => [
    find.title,
    find.title,
  ]);
  const typesOptions = Object.fromEntries(
    _.sortBy(typesArray, (arr): string => arr[0])
  );

  const initialSort: string = JSON.stringify({
    dataField: "severityScore",
    order: "desc",
  });

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const filterSearchtextFindings: IFindingAttr[] = filterSearchText(
    findings,
    searchTextFilter
  );

  function onStatusChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterGroupFindingsCurrentStatus(
      (value): Record<string, string> => ({
        ...value,
        currentStatus: event.target.value,
      })
    );
  }
  const filterCurrentStatusFindings: IFindingAttr[] = filterSelect(
    findings,
    filterGroupFindingsCurrentStatus.currentStatus,
    "state"
  );

  const onTreatmentChange: (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => void = (event: React.ChangeEvent<HTMLSelectElement>): void => {
    event.persist();
    setFilterGroupFindingsTable(
      (value): IFilterSet => ({
        ...value,
        currentTreatment: event.target.value,
      })
    );
  };

  const filterCurrentTreatmentFindings: IFindingAttr[] = filterSubSelectCount(
    findings,
    filterGroupFindingsTable.currentTreatment,
    "treatmentSummary"
  );

  function onReattackChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterGroupFindingsTable(
      (value): IFilterSet => ({ ...value, reattack: event.target.value })
    );
  }
  const filterReattackFindings: IFindingAttr[] = filterSelect(
    findings,
    filterGroupFindingsTable.reattack,
    "remediated"
  );

  function onTypeChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterGroupFindingsTable(
      (value): IFilterSet => ({ ...value, type: event.target.value })
    );
  }
  const filterTypeFindings: IFindingAttr[] = filterSelect(
    findings,
    filterGroupFindingsTable.type,
    "title"
  );

  function onWhereChange(event: React.ChangeEvent<HTMLInputElement>): void {
    event.persist();
    setFilterGroupFindingsTable(
      (value): IFilterSet => ({
        ...value,
        where: event.target.value,
      })
    );
  }
  const filterWhereFindings: IFindingAttr[] = filterWhere(
    findings,
    filterGroupFindingsTable.where
  );

  function onAgeChange(event: React.ChangeEvent<HTMLInputElement>): void {
    event.persist();
    setFilterGroupFindingsTable(
      (value): IFilterSet => ({ ...value, age: event.target.value })
    );
  }
  const filterAgeFindings: IFindingAttr[] = filterLastNumber(
    findings,
    filterGroupFindingsTable.age,
    "age"
  );

  function onLastReportChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    event.persist();
    setFilterGroupFindingsTable(
      (value): IFilterSet => ({ ...value, lastReport: event.target.value })
    );
  }
  const filterLastReportFindings: IFindingAttr[] = filterLastNumber(
    findings,
    filterGroupFindingsTable.lastReport,
    "lastVulnerability"
  );

  function onSeverityMinChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    event.persist();
    setFilterGroupFindingsTable(
      (value): IFilterSet => ({
        ...value,
        severity: { ...value.severity, min: event.target.value },
      })
    );
  }

  function onSeverityMaxChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    event.persist();
    setFilterGroupFindingsTable(
      (value): IFilterSet => ({
        ...value,
        severity: { ...value.severity, max: event.target.value },
      })
    );
  }

  const filterSeverityFindings: IFindingAttr[] = filterRange(
    findings,
    filterGroupFindingsTable.severity,
    "severityScore"
  );

  const onReleaseDateMinChange: (
    event: React.ChangeEvent<HTMLInputElement>
  ) => void = (event: React.ChangeEvent<HTMLInputElement>): void => {
    event.persist();
    setFilterGroupFindingsTable(
      (value): IFilterSet => ({
        ...value,
        releaseDate: { ...value.releaseDate, min: event.target.value },
      })
    );
  };

  const onReleaseDateMaxChange: (
    event: React.ChangeEvent<HTMLInputElement>
  ) => void = (event: React.ChangeEvent<HTMLInputElement>): void => {
    event.persist();
    setFilterGroupFindingsTable(
      (value): IFilterSet => ({
        ...value,
        releaseDate: { ...value.releaseDate, max: event.target.value },
      })
    );
  };

  const filterReleaseDateFindings: IFindingAttr[] = filterDateRange(
    findings,
    filterGroupFindingsTable.releaseDate,
    "releaseDate"
  );

  function clearFilters(): void {
    setFilterGroupFindingsCurrentStatus(
      (): Record<string, string> => ({
        currentStatus: "open",
      })
    );
    setFilterGroupFindingsTable(
      (): IFilterSet => ({
        age: "",
        currentTreatment: "",
        lastReport: "",
        reattack: "",
        releaseDate: { max: "", min: "" },
        severity: { max: "", min: "" },
        type: "",
        where: "",
      })
    );
    setSearchTextFilter("");
  }

  const resultFindings: IFindingAttr[] = _.intersection(
    filterSearchtextFindings,
    filterCurrentStatusFindings,
    filterCurrentTreatmentFindings,
    filterReattackFindings,
    filterReleaseDateFindings,
    filterWhereFindings,
    filterTypeFindings,
    filterAgeFindings,
    filterLastReportFindings,
    filterSeverityFindings
  );

  const { expandedRows, handleRowExpand, handleRowExpandAll } = useRowExpand({
    rowId: "id",
    rows: resultFindings,
    storageKey: "findingExpandedRows",
  });

  const [removeFinding, { loading: deleting }] = useMutation(
    REMOVE_FINDING_MUTATION,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred deleting finding", error);
        });
      },
    }
  );

  const validMutationsHelper = (
    handleCloseModal: () => void,
    areAllMutationValid: boolean[]
  ): void => {
    if (areAllMutationValid.every(Boolean)) {
      msgSuccess(
        t("searchFindings.findingsDeleted"),
        t("group.drafts.titleSuccess")
      );
      replace(`groups/${groupName}/vulns`);
      handleCloseModal();
    }
  };

  const handleRemoveFinding = async (justification: unknown): Promise<void> => {
    if (selectedFindings.length === 0) {
      msgError(t("searchFindings.tabResources.noSelection"));
    } else {
      try {
        const results = await getResults(
          removeFinding,
          selectedFindings,
          justification
        );
        const areAllMutationValid = getAreAllMutationValid(results);
        validMutationsHelper(closeDeleteModal, areAllMutationValid);
      } catch (updateError: unknown) {
        handleRemoveFindingsError(updateError);
      } finally {
        setRunning(false);
      }
    }
  };

  function handleDelete(values: Record<string, unknown>): void {
    void handleRemoveFinding(values.justification);
  }

  function onSelectVariousFindings(
    isSelect: boolean,
    findingsSelected: IFindingAttr[]
  ): string[] {
    return onSelectVariousFindingsHelper(
      isSelect,
      findingsSelected,
      selectedFindings,
      setSelectedFindings
    );
  }

  function onSelectOneFinding(
    finding: IFindingAttr,
    isSelect: boolean
  ): boolean {
    onSelectVariousFindings(isSelect, [finding]);

    return true;
  }

  const customFilters: IFilterProps[] = [
    {
      defaultValue: filterGroupFindingsTable.lastReport,
      onChangeInput: onLastReportChange,
      placeholder: "Last report (last N days)",
      tooltipId: "group.findings.filtersTooltips.lastReport.id",
      tooltipMessage: "group.findings.filtersTooltips.lastReport",
      type: "number",
    },
    {
      defaultValue: filterGroupFindingsTable.type,
      onChangeSelect: onTypeChange,
      placeholder: "Type",
      selectOptions: typesOptions,
      tooltipId: "group.findings.filtersTooltips.type.id",
      tooltipMessage: "group.findings.filtersTooltips.type",
      type: "select",
    },
    {
      defaultValue: filterGroupFindingsCurrentStatus.currentStatus,
      onChangeSelect: onStatusChange,
      placeholder: "Status",
      selectOptions: {
        closed: "Closed",
        open: "Open",
      },
      tooltipId: "group.findings.filtersTooltips.status.id",
      tooltipMessage: "group.findings.filtersTooltips.status",
      type: "select",
    },
    {
      defaultValue: filterGroupFindingsTable.currentTreatment,
      onChangeSelect: onTreatmentChange,
      placeholder: "Treatment",
      selectOptions: {
        accepted: "Temporarily Accepted",
        acceptedUndefined: "Permanently Accepted",
        inProgress: "In Progress",
        new: "New",
      },
      tooltipId: "group.findings.filtersTooltips.treatment.id",
      tooltipMessage: "group.findings.filtersTooltips.treatment",
      type: "select",
    },
    {
      defaultValue: "",
      placeholder: "Severity (range)",
      rangeProps: {
        defaultValue: filterGroupFindingsTable.severity,
        onChangeMax: onSeverityMaxChange,
        onChangeMin: onSeverityMinChange,
        step: 0.1,
      },
      tooltipId: "group.findings.filtersTooltips.severity.id",
      tooltipMessage: "group.findings.filtersTooltips.severity",
      type: "range",
    },
    {
      defaultValue: filterGroupFindingsTable.age,
      onChangeInput: onAgeChange,
      placeholder: "Age (last N days)",
      tooltipId: "group.findings.filtersTooltips.age.id",
      tooltipMessage: "group.findings.filtersTooltips.age",
      type: "number",
    },
    {
      defaultValue: filterGroupFindingsTable.where,
      onChangeInput: onWhereChange,
      placeholder: "Where",
      tooltipId: "group.findings.filtersTooltips.where.id",
      tooltipMessage: "group.findings.filtersTooltips.where",
      type: "text",
    },
    {
      defaultValue: filterGroupFindingsTable.reattack,
      onChangeSelect: onReattackChange,
      placeholder: "Reattack",
      selectOptions: {
        "-": "-",
        Pending: "Pending",
      },
      tooltipId: "group.findings.filtersTooltips.reattack.id",
      tooltipMessage: "group.findings.filtersTooltips.reattack",
      type: "select",
    },
    {
      defaultValue: "",
      placeholder: "Release date (Range)",
      rangeProps: {
        defaultValue: filterGroupFindingsTable.releaseDate,
        onChangeMax: onReleaseDateMaxChange,
        onChangeMin: onReleaseDateMinChange,
      },
      tooltipId: "group.findings.filtersTooltips.releaseDate.id",
      tooltipMessage: "group.findings.filtersTooltips.releaseDate",
      type: "dateRange",
    },
  ];

  return (
    <React.StrictMode>
      <Table
        clearFiltersButton={clearFilters}
        columnToggle={true}
        csvFilename={`${groupName}-findings-${currentDate}.csv`}
        customFilters={{
          customFiltersProps: customFilters,
          isCustomFilterEnabled,
          onUpdateEnableCustomFilter: handleUpdateCustomFilter,
          resultSize: {
            current: resultFindings.length,
            total: findings.length,
          },
        }}
        customSearch={{
          customSearchDefault: searchTextFilter,
          isCustomSearchEnabled: true,
          onUpdateCustomSearch: onSearchTextChange,
          position: "right",
        }}
        dataset={resultFindings}
        defaultSorted={JSON.parse(
          _.get(sessionStorage, "findingSort", initialSort)
        )}
        expandRow={{
          expandByColumnOnly: true,
          expanded: expandedRows,
          onExpand: handleRowExpand,
          onExpandAll: handleRowExpandAll,
          renderer: renderDescription,
          showExpandColumn: true,
        }}
        exportCsv={false}
        extraButtons={
          <Row>
            <Can I={"api_resolvers_query_report__get_url_group_report"}>
              <TooltipWrapper
                id={"group.findings.report.btn.tooltip.id"}
                message={t("group.findings.report.btn.tooltip")}
              >
                <Button
                  id={"reports"}
                  onClick={openReportsModal}
                  variant={"secondary"}
                >
                  {t("group.findings.report.btn.text")}
                </Button>
              </TooltipWrapper>
            </Can>
            <Can do={"api_mutations_remove_finding_mutate"}>
              <TooltipWrapper
                displayClass={"dib"}
                id={"searchFindings.delete.btn.tooltip"}
                message={t("searchFindings.delete.btn.tooltip")}
              >
                <Button
                  disabled={selectedFindings.length === 0 || deleting}
                  onClick={openDeleteModal}
                  variant={"secondary"}
                >
                  <FontAwesomeIcon icon={faTrashAlt} />
                  &nbsp;{t("searchFindings.delete.btn.text")}
                </Button>
              </TooltipWrapper>
            </Can>
          </Row>
        }
        headers={tableHeaders}
        id={"tblFindings"}
        onColumnToggle={handleChange}
        pageSize={10}
        rowEvents={{ onClick: goToFinding }}
        search={false}
        selectionMode={{
          clickToSelect: false,
          hideSelectColumn: permissions.cannot(
            "api_mutations_remove_finding_mutate"
          ),
          mode: "checkbox",
          onSelect: onSelectOneFinding,
          onSelectAll: onSelectVariousFindings,
          selected: getFindingsIndex(selectedFindings, resultFindings),
        }}
      />
      <ReportsModal
        hasMobileApp={hasMobileApp}
        isOpen={isReportsModalOpen}
        onClose={closeReportsModal}
      />
      <Modal
        onClose={closeDeleteModal}
        open={isDeleteModalOpen}
        title={t("searchFindings.delete.title")}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{}}
          name={"removeFinding"}
          onSubmit={handleDelete}
        >
          <Form id={"removeFinding"}>
            <FormGroup>
              <ControlLabel>
                {t("searchFindings.delete.justif.label")}
              </ControlLabel>
              <Field
                component={FormikDropdown}
                name={"justification"}
                validate={composeValidators([required])}
              >
                <option value={""} />
                <option value={"DUPLICATED"}>
                  {t("searchFindings.delete.justif.duplicated")}
                </option>
                <option value={"FALSE_POSITIVE"}>
                  {t("searchFindings.delete.justif.falsePositive")}
                </option>
                <option value={"NOT_REQUIRED"}>
                  {t("searchFindings.delete.justif.notRequired")}
                </option>
              </Field>
            </FormGroup>
            <ModalFooter>
              <Button onClick={closeDeleteModal} variant={"secondary"}>
                {t("confirmmodal.cancel")}
              </Button>
              <Button disabled={isRunning} type={"submit"} variant={"primary"}>
                {t("confirmmodal.proceed")}
              </Button>
            </ModalFooter>
          </Form>
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { GroupFindingsView };
