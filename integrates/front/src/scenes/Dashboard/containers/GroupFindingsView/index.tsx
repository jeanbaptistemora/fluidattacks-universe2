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
import { DataTableNext } from "components/DataTableNext";
import { limitFormatter } from "components/DataTableNext/formatters";
import { useRowExpand } from "components/DataTableNext/hooks/useRowExpand";
import type {
  IFilterProps,
  IHeaderConfig,
} from "components/DataTableNext/types";
import {
  filterDateRange,
  filterLastNumber,
  filterRange,
  filterSearchText,
  filterSelect,
  filterSubSelectCount,
  filterWhere,
} from "components/DataTableNext/utils";
import { Modal } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  GET_FINDINGS,
  GET_HAS_MOBILE_APP,
} from "scenes/Dashboard/containers/GroupFindingsView/queries";
import { ReportsModal } from "scenes/Dashboard/containers/GroupFindingsView/reportsModal";
import type {
  IFindingAttr,
  IGroupFindingsAttr,
} from "scenes/Dashboard/containers/GroupFindingsView/types";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { FormikDropdown } from "utils/forms/fields";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { composeValidators, required } from "utils/validations";

interface IDataResult {
  me: {
    hasMobileApp: boolean;
  };
}

interface IFilterSet {
  age: string;
  currentStatus: string;
  currentTreatment: string;
  lastReport: string;
  reattack: string;
  releaseDate: { max: string; min: string };
  searchText: string;
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
  const [filterTable, setFilterTable] = useStoredState<IFilterSet>(
    "filterGroupFindingsTableSet",
    {
      age: "",
      currentStatus: "open",
      currentTreatment: "",
      lastReport: "",
      reattack: "",
      releaseDate: { max: "", min: "" },
      searchText: "",
      severity: { max: "", min: "" },
      type: "",
      where: "",
    },
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
        alert(translate.t("validations.columns"));
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
    [checkedItems, setCheckedItems]
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
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading group data", error);
      });
    },
    []
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
      align: "center",
      dataField: "lastVulnerability",
      header: "Last report",
      onSort: onSortState,
      visible: checkedItems.lastVulnerability,
    },
    {
      align: "center",
      dataField: "title",
      header: "Type",
      onSort: onSortState,
      visible: checkedItems.title,
      wrapped: true,
    },
    {
      align: "left",
      dataField: "state",
      formatter: formatState,
      header: "Status",
      onSort: onSortState,
      visible: checkedItems.state,
      width: "80px",
      wrapped: true,
    },
    {
      align: "center",
      dataField: "severityScore",
      header: "Severity",
      onSort: onSortState,
      visible: checkedItems.severityScore,
      wrapped: true,
    },
    {
      align: "center",
      dataField: "age",
      header: "Age",
      onSort: onSortState,
      visible: checkedItems.age,
    },
    {
      align: "center",
      dataField: "openVulnerabilities",
      header: "Locations",
      onSort: onSortState,
      visible: checkedItems.openVulnerabilities,
    },
    {
      align: "center",
      dataField: "where",
      formatter: limitFormatter,
      header: "Where",
      onSort: onSortState,
      visible: checkedItems.where,
      wrapped: true,
    },
    {
      align: "center",
      dataField: "remediated",
      header: "Reattack",
      onSort: onSortState,
      visible: checkedItems.remediated,
      wrapped: true,
    },
  ];

  const { data } = useQuery<IGroupFindingsAttr>(GET_FINDINGS, {
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
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred getting user info", error);
    },
  });

  const findings: IFindingAttr[] =
    data === undefined ? [] : formatFindings(data.group.findings);

  const typesArray = findings.map((find: IFindingAttr): string[] => [
    find.title,
    find.title,
  ]);
  const typesOptions = Object.fromEntries(
    _.sortBy(typesArray, (arr): string => arr[0])
  );

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    event.persist();
    setFilterTable(
      (value): IFilterSet => ({
        ...value,
        searchText: event.target.value,
      })
    );
  }
  const filterSearchtextFindings: IFindingAttr[] = filterSearchText(
    findings,
    filterTable.searchText
  );

  function onStatusChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterTable(
      (value): IFilterSet => ({
        ...value,
        currentStatus: event.target.value,
      })
    );
  }
  const filterCurrentStatusFindings: IFindingAttr[] = filterSelect(
    findings,
    filterTable.currentStatus,
    "state"
  );

  const onTreatmentChange: (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => void = (event: React.ChangeEvent<HTMLSelectElement>): void => {
    event.persist();
    setFilterTable(
      (value): IFilterSet => ({
        ...value,
        currentTreatment: event.target.value,
      })
    );
  };

  const filterCurrentTreatmentFindings: IFindingAttr[] = filterSubSelectCount(
    findings,
    filterTable.currentTreatment,
    "treatmentSummary"
  );

  function onReattackChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterTable(
      (value): IFilterSet => ({ ...value, reattack: event.target.value })
    );
  }
  const filterReattackFindings: IFindingAttr[] = filterSelect(
    findings,
    filterTable.reattack,
    "remediated"
  );

  function onTypeChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterTable(
      (value): IFilterSet => ({ ...value, type: event.target.value })
    );
  }
  const filterTypeFindings: IFindingAttr[] = filterSelect(
    findings,
    filterTable.type,
    "title"
  );

  function onWhereChange(event: React.ChangeEvent<HTMLInputElement>): void {
    event.persist();
    setFilterTable(
      (value): IFilterSet => ({
        ...value,
        where: event.target.value,
      })
    );
  }
  const filterWhereFindings: IFindingAttr[] = filterWhere(
    findings,
    filterTable.where,
    "vulnerabilities"
  );

  function onAgeChange(event: React.ChangeEvent<HTMLInputElement>): void {
    event.persist();
    setFilterTable(
      (value): IFilterSet => ({ ...value, age: event.target.value })
    );
  }
  const filterAgeFindings: IFindingAttr[] = filterLastNumber(
    findings,
    filterTable.age,
    "age"
  );

  function onLastReportChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    event.persist();
    setFilterTable(
      (value): IFilterSet => ({ ...value, lastReport: event.target.value })
    );
  }
  const filterLastReportFindings: IFindingAttr[] = filterLastNumber(
    findings,
    filterTable.lastReport,
    "lastVulnerability"
  );

  function onSeverityMinChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    event.persist();
    setFilterTable(
      (value): IFilterSet => ({
        ...value,
        severity: { ...value.severity, min: event.currentTarget.value },
      })
    );
  }

  function onSeverityMaxChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    event.persist();
    setFilterTable(
      (value): IFilterSet => ({
        ...value,
        severity: { ...value.severity, max: event.currentTarget.value },
      })
    );
  }

  const filterSeverityFindings: IFindingAttr[] = filterRange(
    findings,
    filterTable.severity,
    "severityScore"
  );

  const onReleaseDateMinChange: (
    event: React.ChangeEvent<HTMLInputElement>
  ) => void = (event: React.ChangeEvent<HTMLInputElement>): void => {
    event.persist();
    setFilterTable(
      (value): IFilterSet => ({
        ...value,
        releaseDate: { ...value.releaseDate, min: event.currentTarget.value },
      })
    );
  };

  const onReleaseDateMaxChange: (
    event: React.ChangeEvent<HTMLInputElement>
  ) => void = (event: React.ChangeEvent<HTMLInputElement>): void => {
    event.persist();
    setFilterTable(
      (value): IFilterSet => ({
        ...value,
        releaseDate: { ...value.releaseDate, max: event.currentTarget.value },
      })
    );
  };

  const filterReleaseDateFindings: IFindingAttr[] = filterDateRange(
    findings,
    filterTable.releaseDate,
    "releaseDate"
  );

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
          msgError(translate.t("groupAlerts.errorTextsad"));
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
        translate.t("searchFindings.findingsDeleted"),
        translate.t("group.drafts.titleSuccess")
      );
      replace(`groups/${groupName}/vulns`);
      handleCloseModal();
    }
  };

  const handleRemoveFinding = async (justification: unknown): Promise<void> => {
    if (selectedFindings.length === 0) {
      msgError(translate.t("searchFindings.tabResources.noSelection"));
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
      defaultValue: filterTable.lastReport,
      onChangeInput: onLastReportChange,
      placeholder: "Last report (last N days)",
      tooltipId: "group.findings.filtersTooltips.lastReport.id",
      tooltipMessage: "group.findings.filtersTooltips.lastReport",
      type: "number",
    },
    {
      defaultValue: filterTable.type,
      onChangeSelect: onTypeChange,
      placeholder: "Type",
      selectOptions: typesOptions,
      tooltipId: "group.findings.filtersTooltips.type.id",
      tooltipMessage: "group.findings.filtersTooltips.type",
      type: "select",
    },
    {
      defaultValue: filterTable.currentStatus,
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
      defaultValue: filterTable.currentTreatment,
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
        defaultValue: filterTable.severity,
        onChangeMax: onSeverityMaxChange,
        onChangeMin: onSeverityMinChange,
        step: 0.1,
      },
      tooltipId: "group.findings.filtersTooltips.severity.id",
      tooltipMessage: "group.findings.filtersTooltips.severity",
      type: "range",
    },
    {
      defaultValue: filterTable.age,
      onChangeInput: onAgeChange,
      placeholder: "Age (last N days)",
      tooltipId: "group.findings.filtersTooltips.age.id",
      tooltipMessage: "group.findings.filtersTooltips.age",
      type: "number",
    },
    {
      defaultValue: filterTable.where,
      onChangeInput: onWhereChange,
      placeholder: "Where",
      tooltipId: "group.findings.filtersTooltips.where.id",
      tooltipMessage: "group.findings.filtersTooltips.where",
      type: "text",
    },
    {
      defaultValue: filterTable.reattack,
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
        defaultValue: filterTable.releaseDate,
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
      <TooltipWrapper
        id={"group.findings.help"}
        message={translate.t("group.findings.helpLabel")}
      >
        <DataTableNext
          bordered={true}
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
            customSearchDefault: filterTable.searchText,
            isCustomSearchEnabled: true,
            onUpdateCustomSearch: onSearchTextChange,
          }}
          dataset={resultFindings}
          defaultSorted={JSON.parse(_.get(sessionStorage, "findingSort", "{}"))}
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
                  message={translate.t("group.findings.report.btn.tooltip")}
                >
                  <Button id={"reports"} onClick={openReportsModal}>
                    {translate.t("group.findings.report.btn.text")}
                  </Button>
                </TooltipWrapper>
              </Can>
              <Can do={"api_mutations_remove_finding_mutate"}>
                <TooltipWrapper
                  displayClass={"dib"}
                  id={"searchFindings.delete.btn.tooltip"}
                  message={translate.t("searchFindings.delete.btn.tooltip")}
                >
                  <Button
                    disabled={selectedFindings.length === 0 || deleting}
                    onClick={openDeleteModal}
                  >
                    <FontAwesomeIcon icon={faTrashAlt} />
                    &nbsp;{translate.t("searchFindings.delete.btn.text")}
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
          striped={true}
        />
      </TooltipWrapper>
      <ReportsModal
        hasMobileApp={hasMobileApp}
        isOpen={isReportsModalOpen}
        onClose={closeReportsModal}
      />
      <Modal
        headerTitle={translate.t("searchFindings.delete.title")}
        onEsc={closeDeleteModal}
        open={isDeleteModalOpen}
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
                {translate.t("searchFindings.delete.justif.label")}
              </ControlLabel>
              <Field
                component={FormikDropdown}
                name={"justification"}
                validate={composeValidators([required])}
              >
                <option value={""} />
                <option value={"DUPLICATED"}>
                  {translate.t("searchFindings.delete.justif.duplicated")}
                </option>
                <option value={"FALSE_POSITIVE"}>
                  {translate.t("searchFindings.delete.justif.falsePositive")}
                </option>
                <option value={"NOT_REQUIRED"}>
                  {translate.t("searchFindings.delete.justif.notRequired")}
                </option>
              </Field>
            </FormGroup>
            <hr />
            <Row>
              <Col100>
                <ButtonToolbar>
                  <Button onClick={closeDeleteModal}>
                    {translate.t("confirmmodal.cancel")}
                  </Button>
                  <Button disabled={isRunning} type={"submit"}>
                    {translate.t("confirmmodal.proceed")}
                  </Button>
                </ButtonToolbar>
              </Col100>
            </Row>
          </Form>
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { GroupFindingsView };
