import { useLazyQuery, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import {
  faFileArchive,
  faFileExcel,
  faFilePdf,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import type { SortOrder } from "react-bootstrap-table-next";
import { Trans } from "react-i18next";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";

import { renderDescription } from "./description";
import { setReportType } from "./helpers";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { limitFormatter } from "components/DataTableNext/formatters";
import { useRowExpand } from "components/DataTableNext/hooks/useRowExpand";
import type {
  IFilterProps,
  IHeaderConfig,
} from "components/DataTableNext/types";
import {
  filterLastNumber,
  filterSearchText,
  filterSelect,
  filterText,
} from "components/DataTableNext/utils";
import { Modal } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import AppstoreBadge from "resources/appstore_badge.svg";
import GoogleplayBadge from "resources/googleplay_badge.svg";
import { pointStatusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import {
  GET_FINDINGS,
  REQUEST_GROUP_REPORT,
} from "scenes/Dashboard/containers/GroupFindingsView/queries";
import type {
  IFindingAttr,
  IGroupFindingsAttr,
} from "scenes/Dashboard/containers/GroupFindingsView/types";
import { formatFindings } from "scenes/Dashboard/containers/GroupFindingsView/utils";
import {
  ButtonToolbar,
  ButtonToolbarCenter,
  Col100,
  Row,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

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
  const { push } = useHistory();
  const { url } = useRouteMatch();

  // State management
  const [isReportsModalOpen, setReportsModalOpen] = useState(false);
  const openReportsModal: () => void = useCallback((): void => {
    setReportsModalOpen(true);
  }, []);
  const closeReportsModal: () => void = useCallback((): void => {
    setReportsModalOpen(false);
  }, []);

  const [requestGroupReport] = useLazyQuery(REQUEST_GROUP_REPORT, {
    onCompleted: (): void => {
      msgSuccess(
        translate.t("groupAlerts.reportRequested"),
        translate.t("groupAlerts.titleSuccess")
      );
    },
    onError: (error: ApolloError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred requesting group report", error);
    },
  });

  const [checkedItems, setCheckedItems] = useStoredState<
    Record<string, boolean>
  >(
    "tableSet",
    {
      age: false,
      lastVulnerability: true,
      locations: true,
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
  const [reattackFilter, setReattackFilter] = useState("");
  const [whereFilter, setWhereFilter] = useState("");
  const [typeFilter, setTypeFilter] = useState("");
  const [ageFilter, setAgeFilter] = useState("");
  const [lastReportFilter, setLastReportFilter] = useState("");

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
      formatter: pointStatusFormatter,
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
      visible: checkedItems.locations,
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

  const handleRequestGroupReport: (
    event: React.MouseEvent<HTMLElement>
  ) => void = (event: React.MouseEvent<HTMLElement>): void => {
    const target: HTMLElement = event.currentTarget as HTMLElement;
    const icon: SVGElement | null = target.querySelector("svg");
    if (icon !== null) {
      const reportType: string = setReportType(icon);

      track("GroupReportRequest", { reportType });

      requestGroupReport({
        variables: {
          groupName,
          reportType,
        },
      });
      setReportsModalOpen(false);
    }
  };

  const findings: IFindingAttr[] =
    data === undefined ? [] : formatFindings(data.group.findings);

  const typesArray = findings.map((find: IFindingAttr): string[] => [
    find.title,
    find.title,
  ]);
  const typesOptions = Object.fromEntries(
    _.sortBy(typesArray, (arr): string => arr[0])
  );

  const { expandedRows, handleRowExpand, handleRowExpandAll } = useRowExpand({
    rowId: "id",
    rows: findings,
    storageKey: "findingExpandedRows",
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
    setCurrentStatusFilter(event.target.value);
  }
  const filterCurrentStatusFindings: IFindingAttr[] = filterSelect(
    findings,
    currentStatusFilter,
    "state"
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

  const resultFindings: IFindingAttr[] = _.intersection(
    filterSearchtextFindings,
    filterCurrentStatusFindings,
    filterReattackFindings,
    filterWhereFindings,
    filterTypeFindings,
    filterAgeFindings,
    filterLastReportFindings
  );

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
        Closed: "Closed",
        Open: "Open",
      },
      tooltipId: "group.findings.filtersTooltips.status.id",
      tooltipMessage: "group.findings.filtersTooltips.status",
      type: "select",
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
          }
          headers={tableHeaders}
          id={"tblFindings"}
          onColumnToggle={handleChange}
          pageSize={10}
          rowEvents={{ onClick: goToFinding }}
          search={false}
          striped={true}
        />
      </TooltipWrapper>
      <Modal
        headerTitle={translate.t("group.findings.report.modalTitle")}
        onEsc={closeReportsModal}
        open={isReportsModalOpen}
      >
        <div className={"flex flex-wrap tc"}>
          <Col100>
            <Trans>
              <p>{translate.t("group.findings.report.techDescription")}</p>
            </Trans>
            <p>
              <a
                href={"https://apps.apple.com/us/app/integrates/id1470450298"}
                rel={"nofollow noopener noreferrer"}
                target={"_blank"}
              >
                <img
                  alt={"App Store"}
                  height={"40"}
                  src={AppstoreBadge}
                  width={"140"}
                />
              </a>
              <a
                href={
                  "https://play.google.com/store/apps/details?id=com.fluidattacks.integrates"
                }
                rel={"nofollow noopener noreferrer"}
                target={"_blank"}
              >
                <img
                  alt={"Google Play"}
                  height={"40"}
                  src={GoogleplayBadge}
                  width={"140"}
                />
              </a>
            </p>
            <br />
            <Row>
              <Col100>
                <ButtonToolbarCenter>
                  <TooltipWrapper
                    id={"group.findings.report.pdfTooltip.id"}
                    message={translate.t("group.findings.report.pdfTooltip")}
                  >
                    <Button
                      id={"report-pdf"}
                      // eslint-disable-next-line react/jsx-no-bind -- Needed due to nested callback
                      onClick={handleRequestGroupReport}
                    >
                      <FontAwesomeIcon icon={faFilePdf} />
                      {translate.t("group.findings.report.pdf")}
                    </Button>
                  </TooltipWrapper>
                  <TooltipWrapper
                    id={"group.findings.report.xlsTooltip.id"}
                    message={translate.t("group.findings.report.xlsTooltip")}
                  >
                    <Button
                      id={"report-excel"}
                      // eslint-disable-next-line react/jsx-no-bind -- Needed due to nested callback
                      onClick={handleRequestGroupReport}
                    >
                      <FontAwesomeIcon icon={faFileExcel} />
                      {translate.t("group.findings.report.xls")}
                    </Button>
                  </TooltipWrapper>
                  <TooltipWrapper
                    id={"group.findings.report.dataTooltip.id"}
                    message={translate.t("group.findings.report.dataTooltip")}
                  >
                    <Button
                      id={"report-zip"}
                      // eslint-disable-next-line react/jsx-no-bind -- Needed due to nested callback
                      onClick={handleRequestGroupReport}
                    >
                      <FontAwesomeIcon icon={faFileArchive} />
                      {translate.t("group.findings.report.data")}
                    </Button>
                  </TooltipWrapper>
                </ButtonToolbarCenter>
              </Col100>
            </Row>
          </Col100>
        </div>
        <hr />
        <Row>
          <Col100>
            <ButtonToolbar>
              <Button onClick={closeReportsModal}>
                {translate.t("group.findings.report.modalClose")}
              </Button>
            </ButtonToolbar>
          </Col100>
        </Row>
      </Modal>
    </React.StrictMode>
  );
};

export { GroupFindingsView };
