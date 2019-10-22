/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React, { useState } from "react";
import { Query, QueryResult } from "react-apollo";
import { ButtonToolbar, Checkbox, Col, Glyphicon, Row } from "react-bootstrap";
import FontAwesome from "react-fontawesome";
import { Trans } from "react-i18next";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { Button } from "../../../../components/Button";
import { dataTable as DataTable, IHeader } from "../../../../components/DataTable/index";
import { Modal } from "../../../../components/Modal/index";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { formatFindings, handleGraphQLErrors } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";
import { IDashboardState } from "../../reducer";
import { closeReportsModal, openReportsModal, ThunkDispatcher } from "./actions";
import style from "./index.css";
import { GET_FINDINGS } from "./queries";
import { IProjectFindingsAttr, IProjectFindingsBaseProps, IProjectFindingsDispatchProps, IProjectFindingsProps,
  IProjectFindingsStateProps } from "./types";

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

  const handleChange: (event: React.FormEvent<Checkbox>) => void = (event: React.FormEvent<Checkbox>): void => {
    const target: HTMLInputElement = event.target as HTMLInputElement;
    setCheckedItems({
      ...checkedItems,
      [target.name]: target.checked,
    });
  };

  const [hidden, setHidden] = useState(false);

  const handleOpenTableSetClick: () => void = (): void => {
    setHidden(true);
  };

  const handleCloseTableSetClick: () => void = (): void => {
    localStorage.setItem("tableSet", JSON.stringify(checkedItems));
    setHidden(false);
  };

  const tableModalFooter: JSX.Element = (
    <ButtonToolbar className="pull-right">
      <Button onClick={handleCloseTableSetClick}>{translate.t("project.findings.report.modal_close")}</Button>
    </ButtonToolbar>
  );

  const modalFooter: JSX.Element = (
    <ButtonToolbar className="pull-right">
      <Button onClick={handleCloseReportsClick}>{translate.t("project.findings.report.modal_close")}</Button>
    </ButtonToolbar>
  );

  const goToFinding: ((rowInfo: { id: string }) => void) = (rowInfo: { id: string }): void => {
    mixpanel.track(
      "ReadFinding",
      {
        Organization: (window as Window & { userOrganization: string }).userOrganization,
        User: (window as Window & { userName: string }).userName,
      });
    location.hash = `#!/project/${projectName}/findings/${rowInfo.id}/description`;
  };

  const handleQryResult: ((qrResult: IProjectFindingsAttr) => void) = (qrResult: IProjectFindingsAttr): void => {
    mixpanel.track(
      "ProjectFindings",
      {
        Organization: (window as Window & { userOrganization: string }).userOrganization,
        User: (window as Window & { userName: string }).userName,
      });
    hidePreloader();
  };

  const tableHeaders: IHeader[] = [
    {
      align: "center", dataField: "age", header: "Age (days)",
      isDate: false, isStatus: false, visible: checkedItems.age, width: "5%",
    },
    {
      align: "center", dataField: "lastVulnerability", header: "Last report (days)",
      isDate: false, isStatus: false, visible: checkedItems.lastVulnerability,
      width: "5%",
    },
    {
      align: "center", dataField: "title", header: "Title",
      isDate: false, isStatus: false, visible: checkedItems.title, width: "11%", wrapped: true,
    },
    {
      align: "center", dataField: "description", header: "Description",
      isDate: false, isStatus: false, visible: checkedItems.description, width: "16%", wrapped: true,
    },
    {
      align: "center", dataField: "severityScore", header: "Severity",
      isDate: false, isStatus: false, visible: checkedItems.severityScore, width: "6%",
    },
    {
      align: "center", dataField: "openVulnerabilities", header: "Open Vulns.",
      isDate: false, isStatus: false, visible: checkedItems.openVulnerabilities, width: "6%",
    },
    {
      align: "center", dataField: "state", header: "Status", isDate: false,
      isStatus: true, visible: checkedItems.state, width: "7%",
    },
    {
      align: "center", dataField: "treatment", header: "Treatment",
      isDate: false, isStatus: false, visible: checkedItems.treatment, width: "8%",
    },
    {
      align: "center", dataField: "remediated", header: "Remediated",
      isDate: false, isStatus: false, visible: checkedItems.remediated, width: "8%",
    },
    {
      align: "center", dataField: "isExploitable", header: "Exploitable",
      isDate: false, isStatus: false, visible: checkedItems.isExploitable, width: "8%",
    },
    {
      align: "center", dataField: "where", header: "Where",
      isDate: false, isStatus: false, visible: checkedItems.where, width: "8%", wrapped: true,
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

            return (
              <React.StrictMode>
                <Row>
                  <Col md={12} >
                      <Col mdOffset={2} md={4} sm={6}>
                        <ButtonToolbar className={style.tableBtn}>
                          <Button onClick={handleOpenTableSetClick}>
                            <Glyphicon glyph="glyphicon glyphicon-cog" />&nbsp;
                            {translate.t("project.findings.tableSet.btn")}
                          </Button>
                        </ButtonToolbar>
                      </Col>
                    <Col  md={3} sm={6}>
                      <ButtonToolbar className={style.reportsBtn}>
                        <Button onClick={handleOpenReportsClick}>{translate.t("project.findings.report.btn")}</Button>
                      </ButtonToolbar>
                    </Col>
                  </Col>
                </Row>
                <p>{translate.t("project.findings.help_label")}</p>
                <DataTable
                  dataset={formatFindings(data.project.findings)}
                  enableRowSelection={false}
                  exportCsv={true}
                  headers={tableHeaders}
                  id="tblFindings"
                  onClickRow={goToFinding}
                  pageSize={15}
                  search={true}
                  selectionMode="none"
                />
                <Modal
                  open={hidden}
                  footer={tableModalFooter}
                  headerTitle={translate.t("project.findings.tableSet.modal_title")}
                >
                  <Col mdOffset={5} className={style.tableModalContainer}>
                    {tableHeaders.map((item: IHeader) => (
                      <div>
                        <Checkbox
                          name={item.dataField}
                          checked={item.visible}
                          onChange={handleChange}
                        >{item.header}
                        </Checkbox>
                      </div>
                    ))}
                  </Col>
                </Modal>
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
      onOpenReportsModal: (): void => { dispatch(openReportsModal()); },
    });

export = connect(mapStateToProps, mapDispatchToProps)(projectFindingsView);
