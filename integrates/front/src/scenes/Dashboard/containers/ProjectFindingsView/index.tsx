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
import type {
  SortOrder,
  TableColumnFilterProps,
} from "react-bootstrap-table-next";
import { selectFilter, textFilter } from "react-bootstrap-table2-filter";
import { Trans } from "react-i18next";
import { useHistory, useParams, useRouteMatch } from "react-router-dom";

import { renderDescription } from "./description";
import { renderExpandIcon, renderHeaderExpandIcon } from "./expandIcon";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import {
  limitFormatter,
  statusFormatter,
} from "components/DataTableNext/formatters";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Modal } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import AppstoreBadge from "resources/appstore_badge.svg";
import GoogleplayBadge from "resources/googleplay_badge.svg";
import {
  GET_FINDINGS,
  REQUEST_PROJECT_REPORT,
} from "scenes/Dashboard/containers/ProjectFindingsView/queries";
import type { IProjectFindingsAttr } from "scenes/Dashboard/containers/ProjectFindingsView/types";
import { formatFindings } from "scenes/Dashboard/containers/ProjectFindingsView/utils";
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

const ProjectFindingsView: React.FC = (): JSX.Element => {
  const TIMEZONE_OFFSET = 60000;
  const FORMATTING_DATE_INDEX = 19;

  const now: Date = new Date();
  const timeSoFar: number = Date.now();
  const tzoffset: number = now.getTimezoneOffset() * TIMEZONE_OFFSET;
  const localIsoTime: Date = new Date(timeSoFar - tzoffset);
  const formattingDate: string = localIsoTime.toISOString();
  const currentDate: string = formattingDate.slice(0, FORMATTING_DATE_INDEX);

  const { projectName } = useParams<{ projectName: string }>();
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

  const [requestProjectReport] = useLazyQuery(REQUEST_PROJECT_REPORT, {
    onCompleted: (): void => {
      msgSuccess(
        translate.t("groupAlerts.reportRequested"),
        translate.t("groupAlerts.titleSuccess")
      );
    },
    onError: (error: ApolloError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred requesting project report", error);
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

  const [isFilterEnabled, setFilterEnabled] = useStoredState<boolean>(
    "findingsFilters",
    false
  );

  const selectOptionsStatus = { Closed: "Closed", Open: "Open" };
  const selectOptionsVerification = { "-": "-", Pending: "Pending" };

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
  const handleUpdateFilter: () => void = useCallback((): void => {
    setFilterEnabled(!isFilterEnabled);
  }, [isFilterEnabled, setFilterEnabled]);

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
        Logger.warning("An error occurred loading project data", error);
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
  const onFilterWhere: TableColumnFilterProps["onFilter"] = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("whereFilter", filterVal);
  };
  const onFilterStatus: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("statusFilter", filterVal);
  };
  const onFilterVerification: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("verificationFilter", filterVal);
  };

  const tableHeaders: IHeaderConfig[] = [
    {
      align: "center",
      dataField: "lastVulnerability",
      header: "Last report (days)",
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
      align: "center",
      dataField: "state",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "statusFilter"),
        onFilter: onFilterStatus,
        options: selectOptionsStatus,
      }),
      formatter: statusFormatter,
      header: "Status",
      onSort: onSortState,
      visible: checkedItems.state,
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
      header: "Age (days)",
      onSort: onSortState,
      visible: checkedItems.age,
    },
    {
      align: "center",
      dataField: "locations",
      header: "Locations",
      onSort: onSortState,
      visible: checkedItems.locations,
    },
    {
      align: "center",
      dataField: "where",
      filter: textFilter({
        defaultValue: _.get(sessionStorage, "whereFilter"),
        delay: 1000,
        onFilter: onFilterWhere,
      }),
      formatter: limitFormatter,
      header: "Where",
      onSort: onSortState,
      visible: checkedItems.where,
      wrapped: true,
    },
    {
      align: "center",
      dataField: "remediated",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "verificationFilter"),
        onFilter: onFilterVerification,
        options: selectOptionsVerification,
      }),
      header: "Reattack",
      onSort: onSortState,
      visible: checkedItems.remediated,
      wrapped: true,
    },
  ];

  const { data } = useQuery<IProjectFindingsAttr>(GET_FINDINGS, {
    onError: handleQryErrors,
    variables: { projectName },
  });

  function setReportType(icon: SVGElement): string {
    if (
      (icon.attributes.getNamedItem("data-icon")?.value as string).includes(
        "pdf"
      )
    ) {
      return "PDF";
    }

    return (icon.attributes.getNamedItem("data-icon")
      ?.value as string).includes("excel")
      ? "XLS"
      : "DATA";
  }

  const handleRequestProjectReport: (
    event: React.MouseEvent<HTMLElement>
  ) => void = (event: React.MouseEvent<HTMLElement>): void => {
    const target: HTMLElement = event.currentTarget as HTMLElement;
    const icon: SVGElement | null = target.querySelector("svg");
    if (icon !== null) {
      const reportType: string = setReportType(icon);

      track("GroupReportRequest", { reportType });

      requestProjectReport({
        variables: {
          projectName,
          reportType,
        },
      });
      setReportsModalOpen(false);
    }
  };

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <TooltipWrapper
        id={"group.findings.help"}
        message={translate.t("group.findings.helpLabel")}
      >
        <DataTableNext
          bordered={true}
          columnToggle={true}
          csvFilename={`${projectName}-findings-${currentDate}.csv`}
          dataset={formatFindings(data.project.findings)}
          defaultSorted={JSON.parse(_.get(sessionStorage, "findingSort", "{}"))}
          expandRow={{
            expandByColumnOnly: true,
            expandColumnRenderer: renderExpandIcon,
            expandHeaderColumnRenderer: renderHeaderExpandIcon,
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
          isFilterEnabled={isFilterEnabled}
          onColumnToggle={handleChange}
          onUpdateEnableFilter={handleUpdateFilter}
          pageSize={10}
          rowEvents={{ onClick: goToFinding }}
          search={true}
          striped={true}
        />
      </TooltipWrapper>
      <Modal
        headerTitle={translate.t("group.findings.report.modalTitle")}
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
                      onClick={handleRequestProjectReport}
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
                      onClick={handleRequestProjectReport}
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
                      onClick={handleRequestProjectReport}
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

export { ProjectFindingsView };
