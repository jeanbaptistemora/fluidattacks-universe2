/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */

import { MutationFunction, MutationResult, QueryResult } from "@apollo/react-common";
import { Mutation, Query } from "@apollo/react-components";
import { ApolloError } from "apollo-client";
import _ from "lodash";
import React from "react";
import { ButtonToolbar, Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { connect, MapDispatchToProps, MapStateToProps } from "react-redux";
import { NavLink, Redirect, Route, Switch } from "react-router-dom";
import { Field, submit } from "redux-form";
import { Button } from "../../../../components/Button";
import { Modal } from "../../../../components/Modal";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { dropdownField } from "../../../../utils/forms/fields";
import { msgSuccess } from "../../../../utils/notifications";
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

  const onMount: (() => void) = (): (() => void) => {
    props.onLoad();

    return (): void => { props.onUnmount(); };
  };
  React.useEffect(onMount, []);

  const userRole: string =
    _.isEmpty(props.userRole) ? (window as typeof window & { userRole: string }).userRole : props.userRole;
  const currentUserEmail: string = (window as typeof window & { userEmail: string }).userEmail;

  const renderDescription: (() => JSX.Element) = (): JSX.Element => (
    <DescriptionView
      findingId={findingId}
      projectName={projectName}
      userRole={userRole}
      currentUserEmail={currentUserEmail}
      {...reduxProps}
    />
  );

  const canGetHistoricState: boolean = _.includes(["analyst", "admin"], props.userRole);
  const handleApprove: (() => void) = (): void => { props.onApprove(); };
  const handleReject: (() => void) = (): void => { props.onReject(); };

  const [isDeleteModalOpen, setDeleteModalOpen] = React.useState(false);
  const openDeleteModal: (() => void) = (): void => { setDeleteModalOpen(true); };
  const closeDeleteModal: (() => void) = (): void => { setDeleteModalOpen(false); };
  const handleDelete: ((values: { justification: string }) => void) = (values: { justification: string }): void => {
    props.onDelete(values.justification);
  };
  const { userOrganization } = window as typeof window & { userOrganization: string };

  return (
    <React.StrictMode>
      <div className={style.mainContainer}>
        <Row>
          <Col md={12} sm={12}>
            <React.Fragment>
              <Query query={GET_PROJECT_ALERT} variables={{ projectName, organization: userOrganization }}>
                {({ data }: QueryResult): JSX.Element => {
                  if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

                  return data.alert.status === 1 ? <AlertBox message={data.alert.message} /> : <React.Fragment />;
                }}
              </Query>
              <Query query={GET_FINDING_HEADER} variables={{ findingId, submissionField: canGetHistoricState }}>
                {({ data, refetch }: QueryResult<IHeaderQueryResult>): JSX.Element => {
                  if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

                  const handleSubmitError: ((error: ApolloError) => void) = (error: ApolloError): void => {
                    handleGraphQLErrors("An error occurred submitting draft", error);
                  };

                  const handleSubmitResult: ((result: { submitDraft: { success: boolean } }) => void) = (
                    result: { submitDraft: { success: boolean } },
                  ): void => {
                    if (result.submitDraft.success) {
                      msgSuccess(
                        translate.t("project.drafts.success_submit"),
                        translate.t("project.drafts.title_success"),
                      );
                      refetch()
                        .catch();
                    }
                  };
                  const isDraft: boolean = _.isEmpty(data.finding.releaseDate);
                  const hasVulns: boolean = _.sum([data.finding.openVulns, data.finding.closedVulns]) > 0;
                  const hasHistory: boolean = _.isEmpty(data.finding.historicState);
                  const hasSubmission: boolean = !hasHistory ?
                    (data.finding.historicState.slice(-1)[0].state === "SUBMITTED") : false;

                  return (
                    <React.Fragment>
                      <Row>
                        <Col md={8}>
                          <h2>{data.finding.title}</h2>
                        </Col>
                        <Col>
                          <Mutation
                            mutation={SUBMIT_DRAFT_MUTATION}
                            onCompleted={handleSubmitResult}
                            onError={handleSubmitError}
                          >
                            {(submitDraft: MutationFunction, submitResult: MutationResult): JSX.Element => {
                              const handleSubmitClick: (() => void) = (): void => {
                                submitDraft({ variables: { findingId } })
                                  .catch();
                              };

                              return (
                                <FindingActions
                                  isDraft={isDraft}
                                  hasVulns={hasVulns}
                                  hasSubmission={hasSubmission}
                                  loading={submitResult.loading}
                                  onApprove={handleApprove}
                                  onDelete={openDeleteModal}
                                  onReject={handleReject}
                                  onSubmit={handleSubmitClick}
                                />
                              );
                            }}
                          </Mutation>
                        </Col>
                      </Row>
                      <hr />
                      <div className={style.stickyContainer}>
                        <FindingHeader
                          openVulns={data.finding.openVulns}
                          reportDate={data.finding.releaseDate.split(" ")[0]}
                          severity={data.finding.severityScore}
                          status={data.finding.state}
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
                  );
                }}
              </Query>
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
