/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import { QueryResult } from "@apollo/react-common";
import { Query } from "@apollo/react-components";
import { useMutation } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Button as ButtonType, ButtonToolbar, Col, Row } from "react-bootstrap";
import { selectFilter, textFilter } from "react-bootstrap-table2-filter";
import FontAwesome from "react-fontawesome";
import { Trans } from "react-i18next";
import { Button } from "../../../../components/Button";
import { limitFormatter, statusFormatter } from "../../../../components/DataTableNext/formatters";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeader } from "../../../../components/DataTableNext/types";
import { Modal } from "../../../../components/Modal/index";
import { formatFindings, formatTreatment, handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { useStoredState } from "../../../../utils/hooks";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { default as style } from "./index.css";
import { GET_FINDINGS, REQUEST_PROJECT_REPORT } from "./queries";
import { IFindingAttr, IProjectFindingsAttr, IProjectFindingsProps } from "./types";

const projectFindingsView: React.FC<IProjectFindingsProps> = (props: IProjectFindingsProps): JSX.Element => {
  const { projectName } = props.match.params;
  const { userName, userOrganization } = window as typeof window & Dictionary<string>;

  // State management
  const [isReportsModalOpen, setReportsModalOpen] = React.useState(false);
  const openReportsModal: (() => void) = (): void => { setReportsModalOpen(true); };
  const closeReportsModal: (() => void) = (): void => { setReportsModalOpen(false); };

  const [requestProjectReport] = useMutation(REQUEST_PROJECT_REPORT, {
    onCompleted: (): void => {
      msgSuccess(
        translate.t("proj_alerts.report_requested"),
        translate.t("proj_alerts.title_success"));
    },
    onError: (error: ApolloError): void => {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred requesting project report", error);
    },
  });

  const tableSetStorage: (string | null) = localStorage.getItem("tableSet");

  const [checkedItems, setCheckedItems] = React.useState(tableSetStorage !== null ? JSON.parse(tableSetStorage) : {
    age: false,
    description: true,
    isExploitable: true,
    lastVulnerability: true,
    openVulnerabilities: true,
    remediated: false,
    severityScore: true,
    state: true,
    title: true,
    treatment: true,
    where: false,
  });
  const [isFilterEnabled, setFilterEnabled] = useStoredState<boolean>("findingsFilters", false);

  const selectOptionsExploitable: optionSelectFilterProps[] = [
    { value: "Yes", label: "Yes" },
    { value: "No", label: "No" },
  ];
  const selectOptionsStatus: optionSelectFilterProps[] = [
    { value: "Open", label: "Open" },
    { value: "Closed", label: "Closed" },
  ];
  const selectOptionsTreatment: optionSelectFilterProps[] = [
    { value: "Temporarily accepted", label: "Temporarily accepted" },
    { value: "In progress", label: "In progress" },
    { value: "Eternally accepted", label: "Eternally accepted" },
    { value: "Eternally accepted (Pending approval)", label: "Eternally accepted (Pending approval)" },
    { value: "New", label: "New" },
    { value: "-", label: "-" },
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
  const [optionTreatment, setOptionTreatment] =
    React.useState<optionSelectFilterProps[]>(selectOptionsTreatment);

  const handleChange: (columnName: string) => void = (columnName: string): void => {
    setCheckedItems({
      ...checkedItems,
      [columnName]: !checkedItems[columnName],
    });
    localStorage.setItem("tableSet", JSON.stringify({
      ...checkedItems,
      [columnName]: !checkedItems[columnName],
    }));
  };
  const handleUpdateFilter: () => void = (): void => {
    setFilterEnabled(!isFilterEnabled);
  };

  const goToFinding: ((event: React.FormEvent<HTMLButtonElement>, rowInfo: { id: string }) => void) =
    (event: React.FormEvent<HTMLButtonElement>, rowInfo: { id: string }): void => {
      mixpanel.track("ReadFinding", { Organization: userOrganization, User: userName });
      location.hash = `#!/project/${projectName}/findings/${rowInfo.id}/description`;
    };

  const handleQryResult: ((qrResult: IProjectFindingsAttr) => void) = (qrResult: IProjectFindingsAttr): void => {
    let findingOptions: string[] = Array.from(new Set(qrResult.project.findings.map(
      (finding: { treatment: string }) => finding.treatment)));
    findingOptions = findingOptions.map((option: string) => translate.t(formatTreatment(option, "open")));
    const filterOptions: optionSelectFilterProps[] = selectOptionsTreatment.filter(
      (option: optionSelectFilterProps) => (_.includes(findingOptions, option.value)));
    setOptionTreatment(filterOptions);
    mixpanel.track("ProjectFindings", { Organization: userOrganization, User: userName });
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
  const onFilterTreatment: ((filterVal: string) => void) =
    (filterVal: string): void => {
      sessionStorage.setItem("treatmentFilter", filterVal);
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

  const tableHeaders: IHeader[] = [
    {
      align: "center", dataField: "age", header: "Age (days)", onSort: onSortState,
      visible: checkedItems.age, width: "5%",
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
      header: "Title", onSort: onSortState, visible: checkedItems.title, width: "11%", wrapped: true,
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
      header: "Severity", onSort: onSortState, visible: checkedItems.severityScore, width: "6%",
    },
    {
      align: "center", dataField: "openVulnerabilities", header: "Open Vulns.", onSort: onSortState,
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
    },
    {
      align: "center", dataField: "treatment",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "treatmentFilter"),
        onFilter: onFilterTreatment,
        options: optionTreatment,
      }),
      header: "Treatment", onSort: onSortState, visible: checkedItems.treatment, width: "8%", wrapped: true,
    },
    {
      align: "center", dataField: "remediated",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "verificationFilter"),
        onFilter: onFilterVerification,
        options: selectOptionsVerification,
      }),
      header: "Verification", onSort: onSortState, visible: checkedItems.remediated, width: "8%",
    },
    {
      align: "center", dataField: "isExploitable",
      filter: selectFilter({
        defaultValue: _.get(sessionStorage, "exploitableFilter"),
        onFilter: onFilterExploitable,
        options: selectOptionsExploitable,
      }),
      header: "Exploitable", onSort: onSortState, visible: checkedItems.isExploitable, width: "8%",
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
    <Query query={GET_FINDINGS} variables={{ projectName }} onCompleted={handleQryResult}>
      {({ error, data }: QueryResult<IProjectFindingsAttr>): JSX.Element => {
        if (_.isUndefined(data) || _.isEmpty(data)) {

          return <React.Fragment />;
        }
        if (!_.isUndefined(error)) {
          handleGraphQLErrors("An error occurred getting project findings", error);

          return <React.Fragment />;
        }

        data.project.findings = data.project.findings.map((finding: IFindingAttr) => {
          if (finding.historicTreatment.length > 0) {
            finding.treatment = finding.historicTreatment[finding.historicTreatment.length - 1].treatment;
            const acceptationApproval: string | undefined =
              _.get(finding.historicTreatment[finding.historicTreatment.length - 1], "acceptance_status");
            if (acceptationApproval !== undefined && acceptationApproval === "SUBMITTED") {
              finding.treatment += " pending";
            }
          }

          return finding;
        });

        const handleRequestProjectReport: ((event: React.MouseEvent<HTMLElement | ButtonType>) => void) =
        (event: React.MouseEvent<HTMLElement | ButtonType>): void => {
          const target: HTMLElement = event.currentTarget as HTMLElement;
          const span: HTMLSpanElement | null = target.querySelector("span");
          if (span !== null) {
            const reportType: string = span.className
                                           .includes("pdf") ? "PDF" : "XLS";
            requestProjectReport({variables: {
              projectName, reportType,
            }})
            .catch();
          }
        };

        return (
          <React.StrictMode>
            <Row>
              <Col md={2} mdOffset={5}>
                <ButtonToolbar className={style.reportsBtn}>
                  <Button onClick={openReportsModal}>{translate.t("project.findings.report.btn")}</Button>
                </ButtonToolbar>
              </Col>
            </Row>
            <p>{translate.t("project.findings.help_label")}</p>
            <DataTableNext
              bordered={true}
              columnToggle={true}
              dataset={formatFindings(data.project.findings)}
              defaultSorted={JSON.parse(_.get(sessionStorage, "findingSort", "{}"))}
              exportCsv={true}
              headers={tableHeaders}
              id="tblFindings"
              isFilterEnabled={isFilterEnabled}
              pageSize={15}
              onColumnToggle={handleChange}
              onUpdateEnableFilter={handleUpdateFilter}
              remote={false}
              rowEvents={{ onClick: goToFinding }}
              search={true}
              striped={true}
            />
              <Modal
                open={isReportsModalOpen}
                footer={<div />}
                headerTitle={translate.t("project.findings.report.modal_title")}
              >
                <Row className={style.modalContainer}>
                  <Col md={12} id="techReport">
                    <h3>{translate.t("project.findings.report.tech_title")}</h3>
                    <Trans>
                      <p>{translate.t("project.findings.report.tech_description")}</p>
                    </Trans>
                    <br />
                    <Row>
                      <Col md={12} className={style.downloadButtonsContainer}>
                        <ButtonToolbar>
                          <Button onClick={handleRequestProjectReport}>
                            <FontAwesome name="file-pdf-o" />&nbsp;PDF
                              </Button>
                          <Button onClick={handleRequestProjectReport}>
                            <FontAwesome name="file-excel-o" />&nbsp;XLS
                              </Button>
                        </ButtonToolbar>
                      </Col>
                    </Row>
                  </Col>
                </Row>
                <ButtonToolbar className="pull-right">
                  <Button onClick={closeReportsModal}>
                    {translate.t("project.findings.report.modal_close")}
                  </Button>
                </ButtonToolbar>
              </Modal>
          </React.StrictMode>
        );
      }}
    </Query>
  );
};

export { projectFindingsView as ProjectFindingsView };
