/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */

import { QueryResult } from "@apollo/react-common";
import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { ButtonToolbar, Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { NavLink, Redirect, Route, Switch } from "react-router-dom";
import { Field, submit } from "redux-form";
import { Button } from "../../../../components/Button";
import { Modal } from "../../../../components/Modal";
import { dropdownField } from "../../../../utils/forms/fields";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";
import { AlertBox } from "../../components/AlertBox";
import { FindingActions } from "../../components/FindingActions";
import { FindingHeader } from "../../components/FindingHeader";
import { GenericForm } from "../../components/GenericForm";
import { IDashboardState } from "../../reducer";
import { CommentsView } from "../CommentsView/index";
import { descriptionView as DescriptionView } from "../DescriptionView/index";
import { EvidenceView } from "../EvidenceView/index";
import { ExploitView } from "../ExploitView/index";
import { loadProjectData } from "../ProjectContent/actions";
import { GET_PROJECT_ALERT } from "../ProjectContent/queries";
import { RecordsView } from "../RecordsView/index";
import { SeverityView } from "../SeverityView/index";
import { TrackingView } from "../TrackingView/index";
import {
  approveDraft, clearFindingState, deleteFinding, rejectDraft, ThunkDispatcher,
} from "./actions";
import { default as style } from "./index.css";
import { GET_FINDING_HEADER, SUBMIT_DRAFT_MUTATION } from "./queries";
import {
  IFindingContentBaseProps, IFindingContentDispatchProps, IFindingContentProps,
  IFindingContentStateProps, IHeaderQueryResult,
} from "./types";

// tslint:disable-next-line:no-any Allows to render containers without specifying values for their redux-supplied props
const reduxProps: any = {};

const findingContent: React.FC<IFindingContentProps> = (props: IFindingContentProps): JSX.Element => {
  const { findingId, projectName } = props.match.params;
  const { userEmail, userOrganization, userRole } = window as typeof window & Dictionary<string>;

  // Side effects
  const onMount: (() => void) = (): (() => void) => {
    props.onLoad();

    return (): void => { props.onUnmount(); };
  };
  React.useEffect(onMount, []);

  const renderDescription: (() => JSX.Element) = (): JSX.Element => (
    <DescriptionView
      findingId={findingId}
      projectName={projectName}
      userRole={_.isEmpty(props.userRole) ? userRole : props.userRole}
      currentUserEmail={userEmail}
      {...reduxProps}
    />
  );

  // State management
  const canGetHistoricState: boolean = _.includes(["analyst", "admin"], props.userRole);
  const handleApprove: (() => void) = (): void => { props.onApprove(); };
  const handleReject: (() => void) = (): void => { props.onReject(); };

  const [isDeleteModalOpen, setDeleteModalOpen] = React.useState(false);
  const openDeleteModal: (() => void) = (): void => { setDeleteModalOpen(true); };
  const closeDeleteModal: (() => void) = (): void => { setDeleteModalOpen(false); };
  const handleDelete: ((values: { justification: string }) => void) = (values: { justification: string }): void => {
    props.onDelete(values.justification);
  };

  // GraphQL operations
  const { data: alertData }: QueryResult = useQuery(
    GET_PROJECT_ALERT, {
    variables: { projectName, organization: userOrganization },
  });
  const { data: headerData, refetch: headerRefetch }: QueryResult<IHeaderQueryResult> = useQuery(
    GET_FINDING_HEADER, {
    variables: { findingId, submissionField: canGetHistoricState },
  });

  const [submitDraft, { loading: submitting }] = useMutation(
    SUBMIT_DRAFT_MUTATION, {
    onCompleted: (result: { submitDraft: { success: boolean } }): void => {
      if (result.submitDraft.success) {
        msgSuccess(
          translate.t("project.drafts.success_submit"),
          translate.t("project.drafts.title_success"),
        );
        headerRefetch()
          .catch();
      }
    },
    onError: (submitError: ApolloError): void => {
      submitError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        if (_.includes(message, "Exception - This draft has missing fields")) {
          msgError(translate.t("project.drafts.error_submit", {
            missingFields: message.split("fields: ")[1],
          }));
        } else {
          msgError(translate.t("proj_alerts.error_textsad"));
          rollbar.error("An error occurred updating event evidence", submitError);
        }
      });
    },
    variables: { findingId },
  });

  if (_.isUndefined(headerData) || _.isEmpty(headerData)) { return <React.Fragment />; }

  const isDraft: boolean = _.isEmpty(headerData.finding.releaseDate);
  const hasVulns: boolean = _.sum([headerData.finding.openVulns, headerData.finding.closedVulns]) > 0;
  const hasHistory: boolean = !_.isEmpty(headerData.finding.historicState);
  const hasSubmission: boolean = hasHistory
    ? headerData.finding.historicState.slice(-1)[0].state === "SUBMITTED"
    : false;

  return (
    <React.StrictMode>
      <div className={style.mainContainer}>
        <Row>
          <Col md={12} sm={12}>
            <React.Fragment>
              {_.isUndefined(alertData) || _.isEmpty(alertData) || alertData.alert.status === 0
                ? <React.Fragment />
                : <AlertBox message={alertData.alert.message} />}
                    <React.Fragment>
                      <Row>
                        <Col md={8}>
                          <h2>{headerData.finding.title}</h2>
                        </Col>
                        <Col>
                                <FindingActions
                                  isDraft={isDraft}
                                  hasVulns={hasVulns}
                                  hasSubmission={hasSubmission}
                                  loading={submitting}
                                  onApprove={handleApprove}
                                  onDelete={openDeleteModal}
                                  onReject={handleReject}
                                  onSubmit={submitDraft}
                                />
                        </Col>
                      </Row>
                      <hr />
                      <div className={style.stickyContainer}>
                        <FindingHeader
                          openVulns={headerData.finding.openVulns}
                          reportDate={headerData.finding.releaseDate.split(" ")[0]}
                          severity={headerData.finding.severityScore}
                          status={headerData.finding.state}
                        />
                        <ul className={style.tabsContainer}>
                          <li id="infoItem" className={style.tab}>
                            <NavLink activeClassName={style.active} to={`${props.match.url}/description`}>
                              <i className="icon pe-7s-note2" />
                              &nbsp;{translate.t("search_findings.tab_description.tab_title")}
                            </NavLink>
                          </li>
                          <li id="cssv2Item" className={style.tab}>
                            <NavLink activeClassName={style.active} to={`${props.match.url}/severity`}>
                              <i className="icon pe-7s-calculator" />
                              &nbsp;{translate.t("search_findings.tab_severity.tab_title")}
                            </NavLink>
                          </li>
                          <li id="evidenceItem" className={style.tab}>
                            <NavLink activeClassName={style.active} to={`${props.match.url}/evidence`}>
                              <i className="icon pe-7s-photo" />
                              &nbsp;{translate.t("search_findings.tab_evidence.tab_title")}
                            </NavLink>
                          </li>
                          <li id="exploitItem" className={style.tab}>
                            <NavLink activeClassName={style.active} to={`${props.match.url}/exploit`}>
                              <i className="icon pe-7s-file" />
                              &nbsp;{translate.t("search_findings.tab_exploit.tab_title")}
                            </NavLink>
                          </li>
                          <li id="trackingItem" className={style.tab}>
                            <NavLink activeClassName={style.active} to={`${props.match.url}/tracking`}>
                              <i className="icon pe-7s-graph1" />
                              &nbsp;{translate.t("search_findings.tab_tracking.tab_title")}
                            </NavLink>
                          </li>
                          <li id="recordsItem" className={style.tab}>
                            <NavLink activeClassName={style.active} to={`${props.match.url}/records`}>
                              <i className="icon pe-7s-notebook" />
                              &nbsp;{translate.t("search_findings.tab_records.tab_title")}
                            </NavLink>
                          </li>
                          <li id="commentItem" className={style.tab}>
                            <NavLink activeClassName={style.active} to={`${props.match.url}/comments`}>
                              <i className="icon pe-7s-comment" />
                              &nbsp;{translate.t("search_findings.tab_comments.tab_title")}
                            </NavLink>
                          </li>
                          {_.includes(["admin", "analyst"], userRole) ?
                            <li id="observationsItem" className={style.tab}>
                              <NavLink activeClassName={style.active} to={`${props.match.url}/observations`}>
                                <i className="icon pe-7s-note" />
                                &nbsp;{translate.t("search_findings.tab_observations.tab_title")}
                              </NavLink>
                            </li>
                            : undefined}
                        </ul>
                      </div>
                    </React.Fragment>
              <div className={style.tabContent}>
                <Switch>
                  <Route path={`${props.match.path}/description`} render={renderDescription} exact={true} />
                  <Route path={`${props.match.path}/severity`} component={SeverityView} exact={true} />
                  <Route path={`${props.match.path}/evidence`} component={EvidenceView} exact={true} />
                  <Route path={`${props.match.path}/exploit`} component={ExploitView} exact={true} />
                  <Route path={`${props.match.path}/tracking`} component={TrackingView} exact={true} />
                  <Route path={`${props.match.path}/records`} component={RecordsView} exact={true} />
                  <Route
                    path={`${props.match.path}/:type(comments|observations)`}
                    component={CommentsView}
                    exact={true}
                  />
                  <Redirect to={`${props.match.path}/description`} />
                </Switch>
              </div>
            </React.Fragment>
          </Col>
        </Row>
      </div>
      <Modal
        open={isDeleteModalOpen}
        footer={<div />}
        headerTitle={translate.t("search_findings.delete.title")}
      >
        <GenericForm name="deleteFinding" onSubmit={handleDelete}>
          <FormGroup>
            <ControlLabel>{translate.t("search_findings.delete.justif.label")}</ControlLabel>
            <Field name="justification" component={dropdownField} validate={[required]}>
              <option value="" />
              <option value="DUPLICATED">{translate.t("search_findings.delete.justif.duplicated")}</option>
              <option value="FALSE_POSITIVE">{translate.t("search_findings.delete.justif.false_positive")}</option>
              <option value="NOT_REQUIRED">{translate.t("search_findings.delete.justif.not_required")}</option>
            </Field>
          </FormGroup>
          <ButtonToolbar className="pull-right">
            <Button onClick={closeDeleteModal}>{translate.t("confirmmodal.cancel")}</Button>
            <Button type="submit">{translate.t("confirmmodal.proceed")}</Button>
          </ButtonToolbar>
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};

interface IState { dashboard: IDashboardState; }
const mapStateToProps: MapStateToProps<IFindingContentStateProps, IFindingContentBaseProps, IState> =
  (state: IState): IFindingContentStateProps => ({
    userRole: state.dashboard.user.role,
  });

const mapDispatchToProps: MapDispatchToProps<IFindingContentDispatchProps, IFindingContentBaseProps> =
  (dispatch: ThunkDispatcher, ownProps: IFindingContentBaseProps): IFindingContentDispatchProps => {
    const { findingId, projectName } = ownProps.match.params;

    return ({
      onApprove: (): void => { dispatch(approveDraft(findingId)); },
      onConfirmDelete: (): void => { dispatch(submit("deleteFinding")); },
      onDelete: (justification: string): void => { dispatch(deleteFinding(findingId, projectName, justification)); },
      onLoad: (): void => { dispatch(loadProjectData(projectName)); },
      onReject: (): void => { dispatch(rejectDraft(findingId, projectName)); },
      onUnmount: (): void => { dispatch(clearFindingState()); },
    });
  };

export = connect(mapStateToProps, mapDispatchToProps)(findingContent);
