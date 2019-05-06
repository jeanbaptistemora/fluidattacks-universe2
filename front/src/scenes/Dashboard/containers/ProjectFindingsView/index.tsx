import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, Row } from "react-bootstrap";
import FontAwesome from "react-fontawesome";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { RouteComponentProps } from "react-router";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { Button } from "../../../../components/Button";
import { dataTable as DataTable, IHeader } from "../../../../components/DataTable/index";
import { default as Modal } from "../../../../components/Modal/index";
import { formatFindings } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";
import { IDashboardState } from "../../reducer";
import { closeReportsModal, loadFindingsData, openReportsModal, ThunkDispatcher } from "./actions";
import style from "./index.css";

type IProjectFindingsBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

type IProjectFindingsStateProps = IDashboardState["findings"];

interface IProjectFindingsDispatchProps {
  onCloseReportsModal(): void;
  onLoad(): void;
  onOpenReportsModal(): void;
}

type IProjectFindingsProps = IProjectFindingsBaseProps & (IProjectFindingsStateProps & IProjectFindingsDispatchProps);

const enhance: InferableComponentEnhancer<{}> = lifecycle<IProjectFindingsProps, {}>({
  componentDidMount(): void { this.props.onLoad(); mixpanel.track("ProjectFindings"); },
});

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
    mixpanel.track("ReadFinding");
    location.hash = `#!/project/${projectName}/${rowInfo.id}/description`;
  };

  return (
    <React.StrictMode>
      <ButtonToolbar className={style.reportsBtn}>
        <Button onClick={handleOpenReportsClick}>{translate.t("project.findings.report.btn")}</Button>
      </ButtonToolbar>
      <p>{translate.t("project.findings.help_label")}</p>
      <DataTable
        dataset={formatFindings(props.dataset)}
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
};

interface IState { dashboard: IDashboardState; }
const mapStateToProps: MapStateToProps<IProjectFindingsStateProps, IProjectFindingsBaseProps, IState> =
  (state: IState): IProjectFindingsStateProps => ({
    ...state.dashboard.findings,
  });

const mapDispatchToProps: MapDispatchToProps<IProjectFindingsDispatchProps, IProjectFindingsBaseProps> =
  (dispatch: ThunkDispatcher, ownProps: IProjectFindingsBaseProps): IProjectFindingsDispatchProps => {
    const { projectName } = ownProps.match.params;

    return ({
      onCloseReportsModal: (): void => { dispatch(closeReportsModal()); },
      onLoad: (): void => { dispatch(loadFindingsData(projectName)); },
      onOpenReportsModal: (): void => { dispatch(openReportsModal()); },
    });
  };

export = connect(mapStateToProps, mapDispatchToProps)(enhance(projectFindingsView));
