/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Query, QueryResult } from "react-apollo";
import { ButtonToolbar, Col, Row } from "react-bootstrap";
import FontAwesome from "react-fontawesome";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { Button } from "../../../../components/Button";
import { dataTable as DataTable, IHeader } from "../../../../components/DataTable/index";
import { default as Modal } from "../../../../components/Modal/index";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { formatFindings, handleGraphQLErrors } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";
import { IDashboardState } from "../../reducer";
import { closeReportsModal, openReportsModal, ThunkDispatcher } from "./actions";
import style from "./index.css";
import { GET_FINDINGS } from "./queries";
import { IProjectFindingsAttr, IProjectFindingsBaseProps, IProjectFindingsDispatchProps, IProjectFindingsProps,
  IProjectFindingsStateProps } from "./types";

const tableHeaders: IHeader[] = [
  { align: "center", dataField: "age", header: "Age (days)", isDate: false, isStatus: false, width: "6%" },
  {
    align: "center", dataField: "lastVulnerability", header: "Last report (days)", isDate: false, isStatus: false,
    width: "6%",
  },
  { align: "center", dataField: "type", header: "Type", isDate: false, isStatus: false, width: "10%" },
  { align: "center", dataField: "title", header: "Title", isDate: false, isStatus: false, wrapped: true, width: "15%" },
  {
    align: "center", dataField: "description", header: "Description", isDate: false, isStatus: false, width: "20%",
    wrapped: true,
  },
  { align: "center", dataField: "severityScore", header: "Severity", isDate: false, isStatus: false, width: "7%" },
  {
    align: "center", dataField: "openVulnerabilities", header: "Open Vulns.", isDate: false, isStatus: false,
    width: "6%",
  },
  { align: "center", dataField: "state", header: "Status", isDate: false, isStatus: true, width: "9%" },
  { align: "center", dataField: "treatment", header: "Treatment", isDate: false, isStatus: false, width: "11%" },
  { align: "center", dataField: "isExploitable", header: "Exploitable", isDate: false, isStatus: false, width: "10%" },
];

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
    location.hash = `#!/project/${projectName}/${rowInfo.id}/description`;
  };

  return (
    <Query query={GET_FINDINGS} variables={{ projectName }}>
      {
        ({loading, error, data}: QueryResult<IProjectFindingsAttr >): React.ReactNode => {
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
            mixpanel.track(
              "ProjectFindings",
              {
                Organization: (window as Window & { userOrganization: string }).userOrganization,
                User: (window as Window & { userName: string }).userName,
              });
            hidePreloader();

            return (
              <React.StrictMode>
                <ButtonToolbar className={style.reportsBtn}>
                  <Button onClick={handleOpenReportsClick}>{translate.t("project.findings.report.btn")}</Button>
                </ButtonToolbar>
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
                />
                <Modal
                  open={props.reportsModal.isOpen}
                  footer={modalFooter}
                  headerTitle={translate.t("project.findings.report.modal_title")}
                >
                  <Row className={style.modalContainer}>
                    <Col md={12} id="techReport">
                      <h3>{translate.t("project.findings.report.tech_title")}</h3>
                      <p>{translate.t("project.findings.report.tech_description")}</p>
                      <br />
                      <p>{translate.t("project.findings.report.tech_example")}</p>
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
