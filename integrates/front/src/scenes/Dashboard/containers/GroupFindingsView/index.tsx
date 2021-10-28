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
  filterText,
} from "components/DataTableNext/utils";
import { Modal } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import { GET_FINDINGS } from "scenes/Dashboard/containers/GroupFindingsView/queries";
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

  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [currentStatusFilter, setCurrentStatusFilter] = useState("");
  const [currentTreatmentFilter, setCurrentTreatmentFilter] = useState("");
  const [reattackFilter, setReattackFilter] = useState("");
  const [whereFilter, setWhereFilter] = useState("");
  const [typeFilter, setTypeFilter] = useState("");
  const [ageFilter, setAgeFilter] = useState("");
  const [lastReportFilter, setLastReportFilter] = useState("");
  const [releaseDateFilter, setReleaseDateFilter] = useState({
    max: "",
    min: "",
  });
  const [isRunning, setRunning] = useState(false);
  const [selectedFindings, setSelectedFindings] = useState<IFindingAttr[]>([]);
  const [severityFilter, setSeverityFilter] = useState({ max: "", min: "" });
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
    setSearchTextFilter(event.target.value);
  }
  const filterSearchtextFindings: IFindingAttr[] = filterSearchText(
    findings,
    searchTextFilter
  );

  function onStatusChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    setCurrentStatusFilter(event.target.value);
  }
  const filterCurrentStatusFindings: IFindingAttr[] = filterSelect(
    findings,
    currentStatusFilter,
    "state"
  );

  const onTreatmentChange: (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => void = (event: React.ChangeEvent<HTMLSelectElement>): void => {
    setCurrentTreatmentFilter(event.target.value);
  };

  const filterCurrentTreatmentFindings: IFindingAttr[] = filterSubSelectCount(
    findings,
    currentTreatmentFilter,
    "treatmentSummary"
  );

  function onReattackChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    setReattackFilter(event.target.value);
  }
  const filterReattackFindings: IFindingAttr[] = filterSelect(
    findings,
    reattackFilter,
    "remediated"
  );

  function onTypeChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    setTypeFilter(event.target.value);
  }
  const filterTypeFindings: IFindingAttr[] = filterSelect(
    findings,
    typeFilter,
    "title"
  );

  function onWhereChange(event: React.ChangeEvent<HTMLInputElement>): void {
    setWhereFilter(event.target.value);
  }
  const filterWhereFindings: IFindingAttr[] = filterText(
    findings,
    whereFilter,
    "where"
  );

  function onAgeChange(event: React.ChangeEvent<HTMLInputElement>): void {
    setAgeFilter(event.target.value);
  }
  const filterAgeFindings: IFindingAttr[] = filterLastNumber(
    findings,
    ageFilter,
    "age"
  );

  function onLastReportChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setLastReportFilter(event.target.value);
  }
  const filterLastReportFindings: IFindingAttr[] = filterLastNumber(
    findings,
    lastReportFilter,
    "lastVulnerability"
  );

  function onSeverityMinChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSeverityFilter({ ...severityFilter, min: event.target.value });
  }

  function onSeverityMaxChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSeverityFilter({ ...severityFilter, max: event.target.value });
  }

  const filterSeverityFindings: IFindingAttr[] = filterRange(
    findings,
    severityFilter,
    "severityScore"
  );

  const onReleaseDateMinChange: (
    event: React.ChangeEvent<HTMLInputElement>
  ) => void = (event: React.ChangeEvent<HTMLInputElement>): void => {
    setReleaseDateFilter({ ...releaseDateFilter, min: event.target.value });
  };

  const onReleaseDateMaxChange: (
    event: React.ChangeEvent<HTMLInputElement>
  ) => void = (event: React.ChangeEvent<HTMLInputElement>): void => {
    setReleaseDateFilter({ ...releaseDateFilter, max: event.target.value });
  };

  const filterReleaseDateFindings: IFindingAttr[] = filterDateRange(
    findings,
    releaseDateFilter,
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
      defaultValue: lastReportFilter,
      onChangeInput: onLastReportChange,
      placeholder: "Last report (last N days)",
      tooltipId: "group.findings.filtersTooltips.lastReport.id",
      tooltipMessage: "group.findings.filtersTooltips.lastReport",
      type: "number",
    },
    {
      defaultValue: typeFilter,
      onChangeSelect: onTypeChange,
      placeholder: "Type",
      selectOptions: typesOptions,
      tooltipId: "group.findings.filtersTooltips.type.id",
      tooltipMessage: "group.findings.filtersTooltips.type",
      type: "select",
    },
    {
      defaultValue: currentStatusFilter,
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
      defaultValue: currentTreatmentFilter,
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
        defaultValue: severityFilter,
        onChangeMax: onSeverityMaxChange,
        onChangeMin: onSeverityMinChange,
        step: 0.1,
      },
      tooltipId: "group.findings.filtersTooltips.severity.id",
      tooltipMessage: "group.findings.filtersTooltips.severity",
      type: "range",
    },
    {
      defaultValue: ageFilter,
      onChangeInput: onAgeChange,
      placeholder: "Age (last N days)",
      tooltipId: "group.findings.filtersTooltips.age.id",
      tooltipMessage: "group.findings.filtersTooltips.age",
      type: "number",
    },
    {
      defaultValue: whereFilter,
      onChangeInput: onWhereChange,
      placeholder: "Where",
      tooltipId: "group.findings.filtersTooltips.where.id",
      tooltipMessage: "group.findings.filtersTooltips.where",
      type: "text",
    },
    {
      defaultValue: reattackFilter,
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
        defaultValue: releaseDateFilter,
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
            customSearchDefault: searchTextFilter,
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
        hasMobileApp={true}
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
