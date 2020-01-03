/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React, { useState } from "react";
import { Query, QueryResult } from "react-apollo";
import { ButtonToolbar, Col, Row } from "react-bootstrap";
import { selectFilter, textFilter } from "react-bootstrap-table2-filter";
import FontAwesome from "react-fontawesome";
import { Trans } from "react-i18next";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { Button } from "../../../../components/Button";
import { statusFormatter } from "../../../../components/DataTableNext/formatters";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { IHeader } from "../../../../components/DataTableNext/types";
import { Modal } from "../../../../components/Modal/index";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { formatFindings, handleGraphQLErrors } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";
import { IDashboardState } from "../../reducer";
import { changeFilterValues, changeSortedValues, closeReportsModal, openReportsModal,
  ThunkDispatcher } from "./actions";
import { default as style } from "./index.css";
import { GET_FINDINGS } from "./queries";
import { IFindingAttr, IProjectFindingsAttr, IProjectFindingsBaseProps, IProjectFindingsDispatchProps,
  IProjectFindingsProps, IProjectFindingsStateProps } from "./types";

const projectFindingsView: React.FC<IProjectFindingsProps> = (props: IProjectFindingsProps): JSX.Element => {
  const { projectName } = props.match.params;

  const handleOpenReportsClick: (() => void) = (): void => { props.onOpenReportsModal(); };
  const handleCloseReportsClick: (() => void) = (): void => { props.onCloseReportsModal(); };
  const handleTechPdfClick: (() => void) = (): void => {
    window.open(`/integrates/pdf/en/project/${projectName}/tech/`, "_blank");
  };
  const handleTechXlsClick: (() => void) = (): void => {
    window.open(`/integrates/xls/en/project/${projectName}`, "_blank");
  };

  const tableSetStorage: (string | null) = localStorage.getItem("tableSet");

  const [checkedItems, setCheckedItems] = tableSetStorage !== null ? useState(JSON.parse(tableSetStorage)) :
    useState({
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
  const [filterValueExploitable, setFilterValueExploitable] = React.useState(props.filters.exploitable);
  const [filterValueStatus, setFilterValueStatus] = React.useState(props.filters.status);
  const [filterValueTitle, setFilterValueTitle] = React.useState(props.filters.title);
  const [filterValueVerification, setFilterValueVerification] = React.useState(props.filters.verification);
  const [filterValueWhere, setFilterValueWhere] = React.useState(props.filters.where);
  const [sortValue, setSortValue] = React.useState(props.defaultSort);
  const clearSelection: string = "_CLEAR_";

  const selectOptionsExploitable: optionSelectFilterProps[] = [
    {value: "Yes", label: "Yes"},
    {value: "No", label: "No"},
  ];
  const selectOptionsStatus: optionSelectFilterProps[] = [
    {value: "Open", label: "Open"},
    {value: "Closed", label: "Closed"},
  ];
  const selectOptionsVerification: optionSelectFilterProps[] = [
    {value: "Pending", label: "Pending"},
    {value: "-", label: "-"},
  ];

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

  const modalFooter: JSX.Element = (
    <ButtonToolbar className="pull-right">
      <Button onClick={handleCloseReportsClick}>{translate.t("project.findings.report.modal_close")}</Button>
    </ButtonToolbar>
  );

  const goToFinding: ((event: React.FormEvent<HTMLButtonElement>, rowInfo: { id: string }) => void) =
  (event: React.FormEvent<HTMLButtonElement>, rowInfo: { id: string }): void => {
    mixpanel.track(
      "ReadFinding",
      {
        Organization: (window as typeof window & { userOrganization: string }).userOrganization,
        User: (window as typeof window & { userName: string }).userName,
      });
    location.hash = `#!/project/${projectName}/findings/${rowInfo.id}/description`;
  };

  const handleQryResult: ((qrResult: IProjectFindingsAttr) => void) = (qrResult: IProjectFindingsAttr): void => {
    mixpanel.track(
      "ProjectFindings",
      {
        Organization: (window as typeof window & { userOrganization: string }).userOrganization,
        User: (window as typeof window & { userName: string }).userName,
      });
    hidePreloader();
  };
  const onSortState: ((dataField: string, order: SortOrder) => void) =
  (dataField: string, order: SortOrder): void => {
    const newSorted: Sorted = {dataField,  order};
    setSortValue(newSorted);
    props.onSort(newSorted);
  };
  const onFilterTitle: ((filterVal: string) => void) = (filterVal: string): void => {
    if (filterValueTitle !== filterVal) {
      setFilterValueTitle(filterVal);
      props.onFilter({...props.filters, title: filterVal});
    }
  };
  const clearFilterTitle: ((event: React.FormEvent<HTMLInputElement>) => void) =
  (event: React.FormEvent<HTMLInputElement>): void => {
    const inputValue: string = event.currentTarget.value;
    if (inputValue.length === 0 && filterValueTitle !== "") {
      props.onFilter({...props.filters, title: ""});
    }
  };
  const onFilterWhere: ((filterVal: string) => void) = (filterVal: string): void => {
    if (filterValueWhere !== filterVal) {
      setFilterValueWhere(filterVal);
      props.onFilter({...props.filters, where: filterVal});
    }
  };
  const clearFilterWhere: ((event: React.FormEvent<HTMLInputElement>) => void) =
  (event: React.FormEvent<HTMLInputElement>): void => {
    const inputValue: string = event.currentTarget.value;
    if (inputValue.length === 0 && filterValueWhere !== "") {
      props.onFilter({...props.filters, where: ""});
    }
  };
  const onFilterExploitable: ((filterVal: string) => void) = (filterVal: string): void => {
    if (filterValueExploitable !== filterVal && clearSelection !== filterValueExploitable) {
      setFilterValueExploitable(filterVal);
      props.onFilter({...props.filters, exploitable: filterVal});
    }
  };

  const clearFilterExploitable: ((eventInput: React.FormEvent<HTMLInputElement>) => void) =
  (eventInput: React.FormEvent<HTMLInputElement>): void => {
    const inputValue: string = eventInput.currentTarget.value;
    if (inputValue.length === 0 && filterValueExploitable !== "") {
      setFilterValueExploitable(clearSelection);
      props.onFilter({...props.filters, exploitable: ""});
    }
  };
  const onFilterStatus: ((filterVal: string) => void) = (filterVal: string): void => {
    if (filterValueStatus !== filterVal && clearSelection !== filterValueStatus) {
      setFilterValueStatus(filterVal);
      props.onFilter({...props.filters, status: filterVal});
    }
  };

  const clearFilterStatus: ((eventInput: React.FormEvent<HTMLInputElement>) => void) =
  (eventInput: React.FormEvent<HTMLInputElement>): void => {
    const inputValue: string = eventInput.currentTarget.value;
    if (inputValue.length === 0 && filterValueStatus !== "") {
      setFilterValueStatus(clearSelection);
      props.onFilter({...props.filters, status: ""});
    }
  };
  const onFilterVerification: ((filterVal: string) => void) = (filterVal: string): void => {
    if (filterValueVerification !== filterVal && clearSelection !== filterValueVerification) {
      setFilterValueVerification(filterVal);
      props.onFilter({...props.filters, verification: filterVal});
    }
  };

  const clearFilterVerification: ((eventInput: React.FormEvent<HTMLInputElement>) => void) =
  (eventInput: React.FormEvent<HTMLInputElement>): void => {
    const inputValue: string = eventInput.currentTarget.value;
    if (inputValue.length === 0 && filterValueVerification !== "") {
      setFilterValueVerification(clearSelection);
      props.onFilter({...props.filters, verification: ""});

    }
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
        defaultValue: filterValueTitle,
        delay: 1000,
        onFilter: onFilterTitle,
        onInput: clearFilterTitle,
      }),
      header: "Title", onSort: onSortState, visible: checkedItems.title, width: "11%", wrapped: true,
    },
    {
      align: "center", dataField: "description", header: "Description", onSort: onSortState,
      visible: checkedItems.description, width: "16%", wrapped: true,
    },
    {
      align: "center", dataField: "severityScore", header: "Severity", onSort: onSortState,
      visible: checkedItems.severityScore, width: "6%",
    },
    {
      align: "center", dataField: "openVulnerabilities", header: "Open Vulns.", onSort: onSortState,
      visible: checkedItems.openVulnerabilities, width: "6%",
    },
    {
      align: "center", dataField: "state",
      filter: selectFilter({
        defaultValue: filterValueStatus,
        onFilter: onFilterStatus,
        onInput: clearFilterStatus,
        options: selectOptionsStatus,
      }),
      formatter: statusFormatter, header: "Status", onSort: onSortState, visible: checkedItems.state, width: "7%",
    },
    {
      align: "center", dataField: "treatment", header: "Treatment", onSort: onSortState,
      visible: checkedItems.treatment, width: "8%", wrapped: true,
    },
    {
      align: "center", dataField: "remediated",
      filter: selectFilter({
        defaultValue: filterValueVerification,
        onFilter: onFilterVerification,
        onInput: clearFilterVerification,
        options: selectOptionsVerification,
      }),
      header: "Verification", onSort: onSortState, visible: checkedItems.remediated, width: "8%",
    },
    {
      align: "center", dataField: "isExploitable",
      filter: selectFilter({
        defaultValue: filterValueExploitable,
        onFilter: onFilterExploitable,
        onInput: clearFilterExploitable,
        options: selectOptionsExploitable,
      }),
      header: "Exploitable", onSort: onSortState, visible: checkedItems.isExploitable, width: "8%",
    },
    {
      align: "center", dataField: "where",
      filter: textFilter({
        defaultValue: filterValueWhere,
        delay: 1000,
        onFilter: onFilterWhere,
        onInput: clearFilterWhere,
      }),
      header: "Where", onSort: onSortState, visible: checkedItems.where, width: "8%", wrapped: true,
    },
  ];

  return (
    <Query query={GET_FINDINGS} variables={{ projectName }} onCompleted={handleQryResult}>
      {
        ({loading, error, data}: QueryResult<IProjectFindingsAttr>): React.ReactNode => {
          if (loading) {
            showPreloader();

            return <React.Fragment/>;
          }
          if (!_.isUndefined(error)) {
            hidePreloader();
            handleGraphQLErrors("An error occurred getting project findings", error);

            return <React.Fragment/>;
          }
          if (!_.isUndefined(data)) {
            data.project.findings = data.project.findings.map((finding: IFindingAttr) => {
              if (finding.historicTreatment.length > 0) {
                finding.treatment = finding.historicTreatment[finding.historicTreatment.length - 1].treatment;
              }

              return finding;
            });

            return (
              <React.StrictMode>
                <Row>
                  <Col md={2} mdOffset={5}>
                    <ButtonToolbar className={style.reportsBtn}>
                      <Button onClick={handleOpenReportsClick}>{translate.t("project.findings.report.btn")}</Button>
                    </ButtonToolbar>
                  </Col>
                </Row>
                <p>{translate.t("project.findings.help_label")}</p>
                <DataTableNext
                  bordered={true}
                  columnToggle={true}
                  dataset={formatFindings(data.project.findings)}
                  defaultSorted={sortValue}
                  exportCsv={true}
                  headers={tableHeaders}
                  id="tblFindings"
                  pageSize={15}
                  onColumnToggle={handleChange}
                  remote={false}
                  rowEvents={{onClick: goToFinding}}
                  search={true}
                  striped={true}
                />
                <Modal
                  open={props.reportsModal.isOpen}
                  footer={modalFooter}
                  headerTitle={translate.t("project.findings.report.modal_title")}
                >
                  <Row className={style.modalContainer}>
                    <Col md={12} id="techReport">
                      <h3>{translate.t("project.findings.report.tech_title")}</h3>
                      <Trans>
                        <p>{translate.t("project.findings.report.tech_description")}</p>
                      </Trans>
                      <br />
                      <Trans>
                        <p className={style.techExample}>{translate.t("project.findings.report.tech_example")}</p>
                      </Trans>
                      <Row>
                        <Col md={12} className={style.downloadButtonsContainer}>
                          <ButtonToolbar>
                            <Button onClick={handleTechPdfClick}>
                              <FontAwesome name="file-pdf-o" />&nbsp;PDF
                            </Button>
                            <Button onClick={handleTechXlsClick}>
                              <FontAwesome name="file-excel-o" />&nbsp;XLS
                            </Button>
                          </ButtonToolbar>
                        </Col>
                      </Row>
                    </Col>
                  </Row>
                </Modal>
              </React.StrictMode>
            );
          }
        }}
    </Query>
  );
};

interface IState { dashboard: IDashboardState; }
const mapStateToProps: MapStateToProps<IProjectFindingsStateProps, IProjectFindingsBaseProps, IState> =
  (state: IState): IProjectFindingsStateProps => ({
    ...state.dashboard.findings,
  });

const mapDispatchToProps: MapDispatchToProps<IProjectFindingsDispatchProps, IProjectFindingsBaseProps> =
  (dispatch: ThunkDispatcher, ownProps: IProjectFindingsBaseProps): IProjectFindingsDispatchProps =>
    ({
      onCloseReportsModal: (): void => { dispatch(closeReportsModal()); },
      onFilter: (newValues: {}): void => { dispatch(changeFilterValues(newValues)); },
      onOpenReportsModal: (): void => { dispatch(openReportsModal()); },
      onSort: (newValues: {}): void => { dispatch(changeSortedValues(newValues)); },
    });

export = connect(mapStateToProps, mapDispatchToProps)(projectFindingsView);
