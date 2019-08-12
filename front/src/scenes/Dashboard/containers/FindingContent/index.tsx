import _ from "lodash";
import React from "react";
import { Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { NavLink, Redirect, Route, Switch } from "react-router-dom";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { Field, submit } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { ConfirmDialog } from "../../../../components/ConfirmDialog/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import { dropdownField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";
import { openConfirmDialog } from "../../actions";
import { AlertBox } from "../../components/AlertBox";
import { FindingHeader } from "../../components/FindingHeader";
import { GenericForm } from "../../components/GenericForm";
import { IDashboardState } from "../../reducer";
import { CommentsView } from "../CommentsView/index";
import { descriptionView as DescriptionView } from "../DescriptionView/index";
import { evidenceView as EvidenceView } from "../EvidenceView/index";
import { ExploitView } from "../ExploitView/index";
import { loadProjectData } from "../ProjectContent/actions";
import { RecordsView } from "../RecordsView/index";
import { severityView as SeverityView } from "../SeverityView/index";
import { trackingView as TrackingView } from "../TrackingView/index";
import {
  approveDraft, clearFindingState, deleteFinding, loadFindingData, rejectDraft, ThunkDispatcher,
} from "./actions";
import style from "./index.css";
import {
  IFindingContentBaseProps, IFindingContentDispatchProps, IFindingContentProps, IFindingContentStateProps,
} from "./types";

// tslint:disable-next-line:no-any Allows to render containers without specifying values for their redux-supplied props
const reduxProps: any = {};

const enhance: InferableComponentEnhancer<{}> = lifecycle<IFindingContentProps, {}>({
  componentDidMount(): void { this.props.onLoad(); },
  componentWillUnmount(): void { this.props.onUnmount(); },
});

const findingContent: React.FC<IFindingContentProps> = (props: IFindingContentProps): JSX.Element => {
  const { findingId, projectName } = props.match.params;
  const userRole: string =
  _.isEmpty(props.userRole) ? (window as Window & { userRole: string }).userRole : props.userRole;
  const currentUserEmail: string = (window as Window & { userEmail: string }).userEmail;
  const isDraft: boolean = _.isEmpty(props.header.reportDate);
  const hasVulns: number = props.header.openVulns + props.header.closedVulns;

  const findingStatus: string = isDraft ? "drafts" : "findings";

  const renderDescription: (() => JSX.Element) = (): JSX.Element => (
    <DescriptionView
      findingId={findingId}
      projectName={projectName}
      userRole={userRole}
      currentUserEmail={currentUserEmail}
      {...reduxProps}
    />
  );

  const renderSeverity: (() => JSX.Element) = (): JSX.Element => (
    <SeverityView findingId={findingId} canEdit={_.includes(["admin", "analyst"], userRole)} {...reduxProps} />
  );

  const renderEvidence: (() => JSX.Element) = (): JSX.Element => (
    <EvidenceView findingId={findingId} canEdit={_.includes(["admin", "analyst"], userRole)} {...reduxProps} />
  );

  const renderTracking: (() => JSX.Element) = (): JSX.Element => (
    <TrackingView findingId={findingId} hasNewVulnerabilities={true} userRole={userRole} {...reduxProps} />
  );

  const handleApprove: (() => void) = (): void => { props.onApprove(); };
  const handleReject: (() => void) = (): void => { props.onReject(); };
  const handleOpenDeleteConfirm: (() => void) = (): void => { props.openDeleteConfirm(); };
  const handleOpenRejectConfirm: (() => void) = (): void => { props.openRejectConfirm(); };
  const handleConfirmDelete: (() => void) = (): void => { props.onConfirmDelete(); };
  const handleDelete: ((values: { justification: string }) => void) = (values: { justification: string }): void => {
    props.onDelete(values.justification);
  };

  const renderActionButtons: (() => JSX.Element | undefined) = (): JSX.Element | undefined =>
    _.includes(["admin"], userRole) && isDraft ? (
      <React.Fragment>
        <Col md={2}>
          <Button block={true} bsStyle="success" onClick={handleApprove} disabled={hasVulns === 0}>
            <FluidIcon icon="verified" />&nbsp;Approve
          </Button>
        </Col>
        <Col md={2}>
          <Button block={true} bsStyle="warning" onClick={handleOpenRejectConfirm}>
            <FluidIcon icon="delete" />&nbsp;Reject
          </Button>
        </Col>
      </React.Fragment>
    ) : _.includes(["admin", "analyst"], userRole)
        ? (
          <Col md={2} mdOffset={2}>
            <Button
              block={true}
              bsStyle="warning"
              onClick={isDraft ? handleOpenRejectConfirm : handleOpenDeleteConfirm}
            >
              <FluidIcon icon="delete" />&nbsp;Delete
            </Button>
          </Col>
        ) : undefined;

  return (
    <React.StrictMode>
      <div className={style.mainContainer}>
        <Row>
          <Col md={12} sm={12}>
            <React.Fragment>
              {props.alert === undefined ? undefined : <AlertBox message={props.alert} />}
              <Row>
                <Col md={8}>
                  <h2>{props.title}</h2>
                </Col>
                {renderActionButtons()}
              </Row>
              <hr />
              <div className={style.stickyContainer}>
                <FindingHeader {...props.header} />
                <ul className={style.tabsContainer}>
                  <li id="infoItem" className={style.tab}>
                    <NavLink
                      activeClassName={style.active}
                      to={`/project/${projectName}/${findingStatus}/${findingId}/description`}
                    >
                      <i className="icon pe-7s-note2" />
                      &nbsp;{translate.t("search_findings.tab_description.tab_title")}
                    </NavLink>
                  </li>
                  <li id="cssv2Item" className={style.tab}>
                    <NavLink
                      activeClassName={style.active}
                      to={`/project/${projectName}/${findingStatus}/${findingId}/severity`}
                    >
                      <i className="icon pe-7s-calculator" />
                      &nbsp;{translate.t("search_findings.tab_severity.tab_title")}
                    </NavLink>
                  </li>
                  <li id="evidenceItem" className={style.tab}>
                    <NavLink
                      activeClassName={style.active}
                      to={`/project/${projectName}/${findingStatus}/${findingId}/evidence`}
                    >
                      <i className="icon pe-7s-photo" />
                      &nbsp;{translate.t("search_findings.tab_evidence.tab_title")}
                    </NavLink>
                  </li>
                  <li id="exploitItem" className={style.tab}>
                    <NavLink
                      activeClassName={style.active}
                      to={`/project/${projectName}/${findingStatus}/${findingId}/exploit`}
                    >
                      <i className="icon pe-7s-file" />
                      &nbsp;{translate.t("search_findings.tab_exploit.tab_title")}
                    </NavLink>
                  </li>
                  <li id="trackingItem" className={style.tab}>
                    <NavLink
                      activeClassName={style.active}
                      to={`/project/${projectName}/${findingStatus}/${findingId}/tracking`}
                    >
                      <i className="icon pe-7s-graph1" />
                      &nbsp;{translate.t("search_findings.tab_tracking.tab_title")}
                    </NavLink>
                  </li>
                  <li id="recordsItem" className={style.tab}>
                    <NavLink
                      activeClassName={style.active}
                      to={`/project/${projectName}/${findingStatus}/${findingId}/records`}
                    >
                      <i className="icon pe-7s-notebook" />
                      &nbsp;{translate.t("search_findings.tab_records.tab_title")}
                    </NavLink>
                  </li>
                  <li id="commentItem" className={style.tab}>
                    <NavLink
                      activeClassName={style.active}
                      to={`/project/${projectName}/${findingStatus}/${findingId}/comments`}
                    >
                      <i className="icon pe-7s-comment" />
                      &nbsp;{translate.t("search_findings.tab_comments.tab_title")}
                    </NavLink>
                  </li>
                  {/*tslint:disable-next-line:jsx-no-multiline-js Necessary for allowing conditional rendering here*/}
                  {_.includes(["admin", "analyst"], userRole) ?
                    <li id="observationsItem" className={style.tab}>
                      <NavLink
                        activeClassName={style.active}
                        to={`/project/${projectName}/${findingStatus}/${findingId}/observations`}
                      >
                        <i className="icon pe-7s-note" />
                        &nbsp;{translate.t("search_findings.tab_observations.tab_title")}
                      </NavLink>
                    </li>
                    : undefined}
                </ul>
              </div>

              <div className={style.tabContent}>
                <Switch>
                  <Route
                    path="/project/:projectName/:findingOrDraft(\w+)/:findingId(\d+)/description"
                    render={renderDescription}
                  />
                  <Route
                    path="/project/:projectName/:findingOrDraft(\w+)/:findingId(\d+)/severity"
                    render={renderSeverity}
                  />
                  <Route
                    path="/project/:projectName/:findingOrDraft(\w+)/:findingId(\d+)/evidence"
                    render={renderEvidence}
                  />
                  <Route
                    path="/project/:projectName/:findingOrDraft(\w+)/:findingId(\d+)/exploit"
                    component={ExploitView}
                  />
                  <Route
                    path="/project/:projectName/:findingOrDraft(\w+)/:findingId(\d+)/tracking"
                    render={renderTracking}
                  />
                  <Route
                    path="/project/:projectName/:findingOrDraft(\w+)/:findingId(\d+)/records"
                    component={RecordsView}
                  />
                  <Route
                    path="/project/:projectName/:findingOrDraft(\w+)/:findingId(\d+)/:type(comments|observations)"
                    component={CommentsView}
                  />
                  <Redirect
                    path="/project/:projectName/:findingId(\d+)/description"
                    to="/project/:projectName/:findingId(\d+)/:findingId(\d+)/description"
                  />
                  <Redirect to={`/project/:projectName/:findingOrDraft${findingStatus}/:findingId(\d+)/description`} />
                </Switch>
              </div>
            </React.Fragment>
          </Col>
        </Row>
      </div>
      <ConfirmDialog
        name="confirmDeleteFinding"
        onProceed={handleConfirmDelete}
        title={translate.t("search_findings.delete.title")}
        closeOnProceed={false}
      >
        <GenericForm name="deleteFinding" onSubmit={handleDelete}>
          <FormGroup>
            <ControlLabel>{translate.t("search_findings.delete.justif.label")}</ControlLabel>
            <Field name="justification" component={dropdownField} validate={[required]}>
              <option value="" />
              <option value="Change of evidence">{translate.t("search_findings.delete.justif.evidence_change")}</option>
              <option value="Finding has changed">{translate.t("search_findings.delete.justif.finding_change")}</option>
              <option value="It is not a Vulnerability">{translate.t("search_findings.delete.justif.not_vuln")}</option>
              <option value="It is duplicated">{translate.t("search_findings.delete.justif.duplicated")}</option>
            </Field>
          </FormGroup>
        </GenericForm>
      </ConfirmDialog>
      <ConfirmDialog name="confirmRejectDraft" onProceed={handleReject} title={translate.t("search_findings.reject")} />
    </React.StrictMode>
  );
};

interface IState { dashboard: IDashboardState; }
const mapStateToProps: MapStateToProps<IFindingContentStateProps, IFindingContentBaseProps, IState> =
  (state: IState): IFindingContentStateProps => ({
    alert: state.dashboard.finding.alert,
    header: {
      closedVulns: state.dashboard.finding.closedVulns,
      openVulns: state.dashboard.finding.openVulns,
      reportDate: state.dashboard.finding.reportDate,
      severity: state.dashboard.severity.severity,
      status: state.dashboard.finding.status,
    },
    title: state.dashboard.finding.title,
    userRole: state.dashboard.user.role,
  });

const mapDispatchToProps: MapDispatchToProps<IFindingContentDispatchProps, IFindingContentBaseProps> =
  (dispatch: ThunkDispatcher, ownProps: IFindingContentBaseProps): IFindingContentDispatchProps => {
    const { findingId, projectName } = ownProps.match.params;
    const organization: string = (window as Window & { Organization: string }).Organization;

    return ({
      onApprove: (): void => { dispatch(approveDraft(findingId)); },
      onConfirmDelete: (): void => { dispatch(submit("deleteFinding")); },
      onDelete: (justification: string): void => { dispatch(deleteFinding(findingId, projectName, justification)); },
      onLoad: (): void => {
        dispatch(loadProjectData(projectName));
        dispatch(loadFindingData(findingId, projectName, organization)); },
      onReject: (): void => { dispatch(rejectDraft(findingId, projectName)); },
      onUnmount: (): void => { dispatch(clearFindingState()); },
      openDeleteConfirm: (): void => { dispatch(openConfirmDialog("confirmDeleteFinding")); },
      openRejectConfirm: (): void => { dispatch(openConfirmDialog("confirmRejectDraft")); },
    });
  };

export = connect(mapStateToProps, mapDispatchToProps)(enhance(findingContent));
