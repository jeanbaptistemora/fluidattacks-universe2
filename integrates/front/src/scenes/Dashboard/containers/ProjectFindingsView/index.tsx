/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import { QueryResult } from "@apollo/react-common";
import { Query } from "@apollo/react-components";
import { useLazyQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { selectFilter, textFilter } from "react-bootstrap-table2-filter";
import FontAwesome from "react-fontawesome";
import { Trans } from "react-i18next";
import { useHistory } from "react-router-dom";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { limitFormatter, statusFormatter, treatmentFormatter } from "components/DataTableNext/formatters";
import { IHeaderConfig } from "components/DataTableNext/types";
import { Modal } from "components/Modal";
import { TooltipWrapper } from "components/TooltipWrapper";
import { default as AppstoreBadge } from "resources/appstore_badge.svg";
import { default as GoogleplayBadge } from "resources/googleplay_badge.svg";
import {
  GET_FINDINGS,
  REQUEST_PROJECT_REPORT,
} from "scenes/Dashboard/containers/ProjectFindingsView/queries";
import {
  IFindingAttr,
  IProjectFindingsAttr,
  IProjectFindingsProps,
} from "scenes/Dashboard/containers/ProjectFindingsView/types";
import { formatFindings } from "scenes/Dashboard/containers/ProjectFindingsView/utils";
import { ButtonToolbar, ButtonToolbarCenter, Col100, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { useStoredState } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const projectFindingsView: React.FC<IProjectFindingsProps> = (props: IProjectFindingsProps): JSX.Element => {
  const now: Date = new Date();
  const timeSoFar: number = Date.now();
  const tzoffset: number = now.getTimezoneOffset() * 60000;
  const localIsoTime: Date = new Date(timeSoFar - tzoffset);
  const formattingDate: string = localIsoTime.toISOString();
  const currentDate: string = formattingDate.slice(0, 19);

  const { projectName } = props.match.params;
  const { push } = useHistory();

  // State management
  const [isReportsModalOpen, setReportsModalOpen] = React.useState(false);
  const openReportsModal: (() => void) = (): void => { setReportsModalOpen(true); };
  const closeReportsModal: (() => void) = (): void => { setReportsModalOpen(false); };

  const [requestProjectReport] = useLazyQuery(REQUEST_PROJECT_REPORT, {
    onCompleted: (): void => {
      msgSuccess(
        translate.t("group_alerts.report_requested"),
        translate.t("group_alerts.title_success"));
    },
    onError: (error: ApolloError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      Logger.warning("An error occurred requesting project report", error);
    },
  });

  const [checkedItems, setCheckedItems] = useStoredState<Record<string, boolean>>(
    "tableSet",
    {
      age: false,
      description: true,
      isExploitable: true,
      lastVulnerability: true,
      openAge: false,
      openVulnerabilities: true,
      remediated: false,
      severityScore: true,
      state: true,
      title: true,
      treatment: true,
      where: false,
    },
    localStorage,
  );

  const [isFilterEnabled, setFilterEnabled] = useStoredState<boolean>("findingsFilters", false);

  const selectOptionsExploitable: optionSelectFilterProps[] = [
    { value: "Yes", label: "Yes" },
    { value: "No", label: "No" },
  ];
  const selectOptionsStatus: optionSelectFilterProps[] = [
    { value: "Open", label: "Open" },
    { value: "Closed", label: "Closed" },
  ];
  const selectOptionsVerification: optionSelectFilterProps[] = [
    { value: "Pending", label: "Pending" },
    { value: "-", label: "-" },
  ];
  const selectOptionsSeverity: optionSelectFilterProps[] = [
    { value: "None", label: "None" },
    { value: "Low", label: "Low" },
    { value: "Medium", label: "Medium" },
    { value: "High", label: "High" },
    { value: "Critical", label: "Critical" },
  ];
  const restrictionSeverity: Array<{ restriction: number[]; value: string }> = [
    { restriction: [0, 0], value: "None" },
    { restriction: [0.1, 3.9], value: "Low" },
    { restriction: [4, 6.9], value: "Medium" },
    { restriction: [7, 8.9], value: "High" },
    { restriction: [9, 10], value: "Critical" },
  ];

  const handleChange: (columnName: string) => void = (columnName: string): void => {
    if (
      Object.values(checkedItems)
      .filter((val: boolean) => val)
      .length === 1 && checkedItems[columnName]
    ) {
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
  };
  const handleUpdateFilter: () => void = (): void => {
    setFilterEnabled(!isFilterEnabled);
  };

  const goToFinding: ((event: React.FormEvent<HTMLButtonElement>, rowInfo: { id: string }) => void) =
    (_0: React.FormEvent<HTMLButtonElement>, rowInfo: { id: string }): void => {
      mixpanel.track("ReadFinding");
      push(`/groups/${projectName}/vulns/${rowInfo.id}/locations`);
    };

  const handleQryResult: ((qrResult: IProjectFindingsAttr) => void) = (qrResult: IProjectFindingsAttr): void => {
    if (!_.isUndefined(qrResult)) {
      mixpanel.track("ProjectFindings");
    }
  };
  const handleQryErrors: ((error: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      Logger.warning("An error occurred loading project data", error);
    });
  };
  const onSortState: ((dataField: string, order: SortOrder) => void) =
    (dataField: string, order: SortOrder): void => {
      const newSorted: Sorted = { dataField, order };
      sessionStorage.setItem("findingSort", JSON.stringify(newSorted));
    };
  const onFilterTitle: ((filterVal: string) => void) = (filterVal: string): void => {
    sessionStorage.setItem("titleFilter", filterVal);
  };
  const onFilterWhere: ((filterVal: string) => void) = (filterVal: string): void => {
    sessionStorage.setItem("whereFilter", filterVal);
  };
  const onFilterExploitable: ((filterVal: string) => void) = (filterVal: string): void => {
    sessionStorage.setItem("exploitableFilter", filterVal);
  };
  const onFilterStatus: ((filterVal: string) => void) = (filterVal: string): void => {
    sessionStorage.setItem("statusFilter", filterVal);
  };
  const onFilterVerification: ((filterVal: string) => void) = (filterVal: string): void => {
    sessionStorage.setItem("verificationFilter", filterVal);
  };
  const onFilterSeverity: ((filterVal: string, data: IFindingAttr[]) => IFindingAttr[]) =
    (filterVal: string, data: IFindingAttr[]): IFindingAttr[] => {
      sessionStorage.setItem("severityFilter", filterVal);
      if (filterVal.length === 0) {
        return data;
      }
      const restrictions: number[] = restrictionSeverity.filter((option: { restriction: number[]; value: string }) => (
        option.value === filterVal))[0].restriction;

      return data.filter((row: IFindingAttr) => (
        row.severityScore >= restrictions[0] && row.severityScore <= restrictions[1]));
    };

  const tableHeaders: IHeaderConfig[] = [
    {
      align: "center", dataField: "age", header: "Age (days)", onSort: onSortState,
      visible: checkedItems.age, width: "5%",
    },
    {
      align: "center", dataField: "openAge", header: "Open Age (days)", onSort: onSortState,
      visible: checkedItems.openAge, width: "5%",
    },
    {
      align: "center", dataField: "lastVulnerability", header: "Last report (days)", onSort: onSortState,
      visible: checkedItems.lastVulnerability, width: "5%",
    },
    {
      align: "center", dataField: "title",
      filter: textFilter({
        defaultValue: _.get(sessionStorage, "titleFilter"),
        delay: 1000,
        onFilter: onFilterTitle,
      }),
      header: "Type", onSort: onSortState, visible: checkedItems.title, width: "11%", wrapped: true,
    },
    {
      align: "center", dataField: "description", header: "Description", onSort: onSortState,
      visible: checkedItems.description, width: "16%", wrapped: true,
    },
    {
      align: "center", dataField: "severityScore",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "severityFilter"),
        onFilter: onFilterSeverity,
        options: selectOptionsSeverity,
      }),
      header: "Severity", onSort: onSortState, visible: checkedItems.severityScore, width: "6%", wrapped: true,
    },
    {
      align: "center", dataField: "openVulnerabilities", header: "Open", onSort: onSortState,
      visible: checkedItems.openVulnerabilities, width: "6%",
    },
    {
      align: "center", dataField: "state",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "statusFilter"),
        onFilter: onFilterStatus,
        options: selectOptionsStatus,
      }),
      formatter: statusFormatter, header: "Status", onSort: onSortState, visible: checkedItems.state, width: "7%",
      wrapped: true,
    },
    {
      align: "left",
      dataField: "treatment",
      formatter: treatmentFormatter,
      header: translate.t("search_findings.tab_description.treatment.title"),
      onSort: onSortState,
      visible: checkedItems.treatment,
      width: "8%",
    },
    {
      align: "center", dataField: "remediated",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "verificationFilter"),
        onFilter: onFilterVerification,
        options: selectOptionsVerification,
      }),
      header: "Verification", onSort: onSortState, visible: checkedItems.remediated, width: "8%", wrapped: true,
    },
    {
      align: "center", dataField: "isExploitable",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "exploitableFilter"),
        onFilter: onFilterExploitable,
        options: selectOptionsExploitable,
      }),
      header: "Exploitable", onSort: onSortState, visible: checkedItems.isExploitable, width: "8%", wrapped: true,
    },
    {
      align: "center", dataField: "where",
      filter: textFilter({
        defaultValue: _.get(sessionStorage, "whereFilter"),
        delay: 1000,
        onFilter: onFilterWhere,
      }),
      formatter: limitFormatter, header: "Where", onSort: onSortState, visible: checkedItems.where, width: "8%",
      wrapped: true,
    },
  ];

  return (
    <Query query={GET_FINDINGS} variables={{ projectName }} onCompleted={handleQryResult} onError={handleQryErrors}>
      {({ data }: QueryResult<IProjectFindingsAttr>): JSX.Element => {
        if (_.isUndefined(data) || _.isEmpty(data)) {

          return <React.Fragment />;
        }

        const handleRequestProjectReport: ((event: React.MouseEvent<HTMLElement>) => void) =
        (event: React.MouseEvent<HTMLElement>): void => {
          const target: HTMLElement = event.currentTarget as HTMLElement;
          const span: HTMLSpanElement | null = target.querySelector("span");
          if (span !== null) {
            const reportType: string =
              span.className.includes("pdf")
                ? "PDF"
                : span.className.includes("excel")
                  ? "XLS"
                  : "DATA";

            requestProjectReport({variables: {
              projectName, reportType,
            }});
            setReportsModalOpen(false);
          }
        };

        return (
          <React.StrictMode>
            <Can I="backend_api_resolvers_query_report__get_url_group_report">
              <Row>
                <Col100>
                  <ButtonToolbarCenter>
                    <TooltipWrapper
                      id={"group.findings.report.btn.tooltip.id"}
                      message={translate.t("group.findings.report.btn.tooltip")}
                    >
                      <Button onClick={openReportsModal} id={"reports"}>
                        {translate.t("group.findings.report.btn.text")}
                      </Button>
                    </TooltipWrapper>
                  </ButtonToolbarCenter>
                </Col100>
              </Row>
            </Can>
            <p>{translate.t("group.findings.help_label")}</p>
            <DataTableNext
              bordered={true}
              columnToggle={true}
              csvFilename={`${projectName}-findings-${currentDate}.csv`}
              dataset={formatFindings(data.project.findings)}
              defaultSorted={JSON.parse(_.get(sessionStorage, "findingSort", "{}"))}
              exportCsv={false}
              headers={tableHeaders}
              id="tblFindings"
              isFilterEnabled={isFilterEnabled}
              pageSize={15}
              onColumnToggle={handleChange}
              onUpdateEnableFilter={handleUpdateFilter}
              rowEvents={{ onClick: goToFinding }}
              search={true}
              striped={true}
            />
              <Modal
                open={isReportsModalOpen}
                headerTitle={translate.t("group.findings.report.modal_title")}
              >
                <Row className={"tc"}>
                  <Col100>
                    <Trans>
                      <p>{translate.t("group.findings.report.tech_description")}</p>
                    </Trans>
                    <p>
                      <a
                        href="https://apps.apple.com/us/app/integrates/id1470450298"
                        rel="nofollow noopener"
                        target="_blank"
                      >
                        <img src={AppstoreBadge} width="140" height="40" />
                      </a>
                      <a
                        href="https://play.google.com/store/apps/details?id=com.fluidattacks.integrates"
                        rel="nofollow noopener"
                        target="_blank"
                      >
                        <img src={GoogleplayBadge} width="140" height="40" />
                      </a>
                    </p>
                    <br />
                    <Row>
                      <Col100>
                        <ButtonToolbarCenter>
                          <Button onClick={handleRequestProjectReport} id={"report-pdf"}>
                            <FontAwesome name="file-pdf-o" />
                              {translate.t("group.findings.report.pdf")}
                          </Button>
                          <Button onClick={handleRequestProjectReport} id={"report-excel"}>
                            <FontAwesome name="file-excel-o" />
                              {translate.t("group.findings.report.xls")}
                          </Button>
                          <Button onClick={handleRequestProjectReport} id={"report-zip"}>
                            <FontAwesome name="file-zip-o" />
                            {translate.t("group.findings.report.data")}
                          </Button>
                        </ButtonToolbarCenter>
                      </Col100>
                    </Row>
                  </Col100>
                </Row>
                <hr />
                <Row>
                  <Col100>
                    <ButtonToolbar>
                      <Button onClick={closeReportsModal}>
                        {translate.t("group.findings.report.modal_close")}
                      </Button>
                    </ButtonToolbar>
                  </Col100>
                </Row>
              </Modal>
          </React.StrictMode>
        );
      }}
    </Query>
  );
};

export { projectFindingsView as ProjectFindingsView };
