/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */

import { QueryResult } from "@apollo/react-common";
import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";

import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import _ from "lodash";
import React from "react";
import {
  Redirect,
  Route,
  Switch,
  useHistory,
  useParams,
  useRouteMatch,
} from "react-router-dom";
import { Field } from "redux-form";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { FindingActions } from "scenes/Dashboard/components/FindingActions";
import { FindingHeader } from "scenes/Dashboard/components/FindingHeader";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { CommentsView } from "scenes/Dashboard/containers/CommentsView/index";
import { DescriptionView } from "scenes/Dashboard/containers/DescriptionView/index";
import { EvidenceView } from "scenes/Dashboard/containers/EvidenceView/index";
import { ExploitView } from "scenes/Dashboard/containers/ExploitView/index";
import {
  APPROVE_DRAFT_MUTATION, DELETE_FINDING_MUTATION, GET_FINDING_HEADER,
  REJECT_DRAFT_MUTATION, SUBMIT_DRAFT_MUTATION,
} from "scenes/Dashboard/containers/FindingContent/queries";
import { IHeaderQueryResult } from "scenes/Dashboard/containers/FindingContent/types";
import { RecordsView } from "scenes/Dashboard/containers/RecordsView/index";
import { SeverityView } from "scenes/Dashboard/containers/SeverityView/index";
import { TrackingView } from "scenes/Dashboard/containers/TrackingView/index";
import { VulnsView } from "scenes/Dashboard/containers/VulnerabilitiesView/index";
import {
  ButtonToolbar,
  Col100,
  Col60,
  ControlLabel,
  FormGroup,
  Row,
  StickyContainerFinding,
  TabContent,
  TabsContainer,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { Have } from "utils/authz/Have";
import { Dropdown } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { required } from "utils/validations";
import { ButtonCol } from "./components/buttoncol";

const findingContent: React.FC = (): JSX.Element => {
  const { findingId, projectName } = useParams<{ findingId: string; projectName: string}>();
  const { path, url } = useRouteMatch<{ path: string; url: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const groupPermissions: PureAbility<string> = useAbility(authzGroupContext);
  const { replace } = useHistory();

  // State management
  const [isDeleteModalOpen, setDeleteModalOpen] = React.useState(false);
  const openDeleteModal: (() => void) = (): void => { setDeleteModalOpen(true); };
  const closeDeleteModal: (() => void) = (): void => { setDeleteModalOpen(false); };

  // GraphQL operations
  const { data: headerData, refetch: headerRefetch }: QueryResult<IHeaderQueryResult> = useQuery(
    GET_FINDING_HEADER, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred loading finding header", error);
      });
    },
    variables: {
      canGetExploit: groupPermissions.can("has_forces"),
      canGetHistoricState: permissions.can("backend_api_resolvers_finding_historic_state_resolve"),
      findingId,
    },
  });

  const [submitDraft, { loading: submitting }] = useMutation(
    SUBMIT_DRAFT_MUTATION, {
    onCompleted: (result: { submitDraft: { success: boolean } }): void => {
      if (result.submitDraft.success) {
        msgSuccess(
          translate.t("group.drafts.success_submit"),
          translate.t("group.drafts.title_success"),
        );
        void headerRefetch();
      }
    },
    onError: (submitError: ApolloError): void => {
      submitError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        if (_.includes(message, "Exception - This draft has missing fields")) {
          msgError(translate.t("group.drafts.error_submit", {
            missingFields: message.split("fields: ")[1],
          }));
        } else if (message === "Exception - This draft has already been submitted") {
          msgError(translate.t("group_alerts.draft_already_submitted"));
          void headerRefetch();
        } else if (message === "Exception - This draft has already been approved") {
          msgError(translate.t("group_alerts.draft_already_approved"));
          void headerRefetch();
        } else {
          msgError(translate.t("group_alerts.error_textsad"));
          Logger.warning("An error occurred submitting draft", submitError);
        }
      });
    },
    variables: { findingId },
  });

  const [approveDraft, { loading: approving }] = useMutation(
    APPROVE_DRAFT_MUTATION, {
    onCompleted: (result: { approveDraft: { success: boolean } }): void => {
      if (result.approveDraft.success) {
        msgSuccess(
          translate.t("search_findings.draft_approved"),
          translate.t("group.drafts.title_success"),
        );
        void headerRefetch();
      }
    },
    onError: (approveError: ApolloError): void => {
      approveError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - This draft has already been approved":
            msgError(translate.t("group_alerts.draft_already_approved"));
            void headerRefetch();
            break;
          case "Exception - The draft has not been submitted yet":
            msgError(translate.t("group_alerts.draft_not_submitted"));
            void headerRefetch();
            break;
          case "CANT_APPROVE_FINDING_WITHOUT_VULNS":
            msgError(translate.t("group_alerts.draft_without_vulns"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("An error occurred approving draft", approveError);
        }
      });
    },
    variables: { findingId },
  });

  const [rejectDraft, { loading: rejecting }] = useMutation(
    REJECT_DRAFT_MUTATION, {
    onCompleted: (result: { rejectDraft: { success: boolean } }): void => {
      if (result.rejectDraft.success) {
        msgSuccess(
          translate.t("search_findings.finding_rejected", { findingId }),
          translate.t("group.drafts.title_success"),
        );
        void headerRefetch();
      }
    },
    onError: (rejectError: ApolloError): void => {
      rejectError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - This draft has already been approved":
            msgError(translate.t("group_alerts.draft_already_approved"));
            void headerRefetch();
            break;
          case "Exception - The draft has not been submitted yet":
            msgError(translate.t("group_alerts.draft_not_submitted"));
            void headerRefetch();
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("An error occurred rejecting draft", rejectError);
        }
      });
    },
    variables: { findingId },
  });

  const [deleteFinding, { loading: deleting }] = useMutation(
    DELETE_FINDING_MUTATION, {
    onCompleted: (result: { deleteFinding: { success: boolean } }): void => {
      if (result.deleteFinding.success) {
        msgSuccess(
          translate.t("search_findings.finding_deleted", { findingId }),
          translate.t("group.drafts.title_success"),
        );
        replace(`/groups/${projectName}/vulns`);
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred deleting finding", error);
      });
    },
  });

  const handleDelete: ((values: { justification: string }) => void) = (values: { justification: string }): void => {
    void deleteFinding({ variables: { findingId, justification: values.justification } });
  };

  if (_.isUndefined(headerData) || _.isEmpty(headerData)) { return <React.Fragment />; }

  const isDraft: boolean = _.isEmpty(headerData.finding.releaseDate);
  const hasExploit: boolean = !_.isEmpty(headerData.finding.exploit);
  const hasVulns: boolean = _.sum([headerData.finding.openVulns, headerData.finding.closedVulns]) > 0;
  const hasHistory: boolean = !_.isEmpty(headerData.finding.historicState);
  const hasSubmission: boolean = hasHistory
    ? headerData.finding.historicState.slice(-1)[0].state === "SUBMITTED"
    : false;
  const hasReleaseDate: boolean = !_.isEmpty(headerData.finding.releaseDate);

  return (
    <React.StrictMode>
      <React.Fragment>
        <Row>
          <Col100>
            <React.Fragment>
              <Row>
                <Col60>
                  <h2>{headerData.finding.title}</h2>
                </Col60>
                <ButtonCol>
                  <FindingActions
                    isDraft={isDraft}
                    hasVulns={hasVulns}
                    hasSubmission={hasSubmission}
                    loading={approving || deleting || rejecting || submitting}
                    onApprove={approveDraft}
                    onDelete={openDeleteModal}
                    onReject={rejectDraft}
                    onSubmit={submitDraft}
                  />
                </ButtonCol>
              </Row>
              <hr />
              <StickyContainerFinding>
                <FindingHeader
                  openVulns={headerData.finding.openVulns}
                  discoveryDate={hasReleaseDate ? headerData.finding.releaseDate.split(" ")[0] : "-"}
                  severity={headerData.finding.severityScore}
                  status={headerData.finding.state}
                />
                <TabsContainer>
                  <ContentTab
                    icon="icon pe-7s-menu"
                    id="vulnItem"
                    link={`${url}/locations`}
                    title={translate.t("search_findings.tab_vuln.tab_title")}
                    tooltip={translate.t("search_findings.tab_vuln.tooltip")}
                  />
                  <ContentTab
                    icon="icon pe-7s-note"
                    id="infoItem"
                    link={`${url}/description`}
                    title={translate.t("search_findings.tab_description.tab_title")}
                    tooltip={translate.t("search_findings.tab_description.tooltip")}
                  />
                  <ContentTab
                    icon="icon pe-7s-calculator"
                    id="cssv2Item"
                    link={`${url}/severity`}
                    title={translate.t("search_findings.tab_severity.tab_title")}
                    tooltip={translate.t("search_findings.tab_severity.tooltip")}
                  />
                  <ContentTab
                    icon="icon pe-7s-photo"
                    id="evidenceItem"
                    link={`${url}/evidence`}
                    title={translate.t("search_findings.tab_evidence.tab_title")}
                    tooltip={translate.t("search_findings.tab_evidence.tooltip")}
                  />
                  <Have I="has_forces">
                    { hasExploit || permissions.can("backend_api_mutations_update_evidence_mutate")
                      ? <ContentTab
                          icon="icon pe-7s-file"
                          id="exploitItem"
                          link={`${url}/exploit`}
                          title={translate.t("search_findings.tab_exploit.tab_title")}
                          tooltip={translate.t("search_findings.tab_exploit.tooltip")}
                      />
                     : undefined }
                  </Have>
                  <ContentTab
                    icon="icon pe-7s-graph1"
                    id="trackingItem"
                    link={`${url}/tracking`}
                    title={translate.t("search_findings.tab_tracking.tab_title")}
                    tooltip={translate.t("search_findings.tab_tracking.tooltip")}
                  />
                  <ContentTab
                    icon="icon pe-7s-notebook"
                    id="recordsItem"
                    link={`${url}/records`}
                    title={translate.t("search_findings.tab_records.tab_title")}
                    tooltip={translate.t("search_findings.tab_records.tooltip")}
                  />
                  <ContentTab
                    icon="icon pe-7s-comment"
                    id="commentItem"
                    link={`${url}/consulting`}
                    title={translate.t("search_findings.tab_comments.tab_title")}
                    tooltip={translate.t("search_findings.tab_comments.tooltip")}
                  />
                  <Can do="backend_api_resolvers_finding_observations_resolve">
                    <ContentTab
                      icon="icon pe-7s-note"
                      id="observationsItem"
                      link={`${url}/observations`}
                      title={translate.t("search_findings.tab_observations.tab_title")}
                      tooltip={translate.t("search_findings.tab_observations.tooltip")}
                    />
                  </Can>
                </TabsContainer>
              </StickyContainerFinding>
              <TabContent>
                <Switch>
                  <Route path={`${path}/locations`} component={VulnsView} exact={true} />
                  <Route path={`${path}/description`} component={DescriptionView} exact={true} />
                  <Route path={`${path}/severity`} component={SeverityView} exact={true} />
                  <Route path={`${path}/evidence`} component={EvidenceView} exact={true} />
                  <Route path={`${path}/exploit`} component={ExploitView} exact={true} />
                  <Route path={`${path}/tracking`} component={TrackingView} exact={true} />
                  <Route path={`${path}/records`} component={RecordsView} exact={true} />
                  <Route
                    path={`${path}/:type(consulting|observations)`}
                    component={CommentsView}
                    exact={true}
                  />
                  <Redirect to={`${path}/locations`} />
                </Switch>
              </TabContent>
            </React.Fragment>
          </Col100>
        </Row>
      </React.Fragment>
      <Modal
        open={isDeleteModalOpen}
        headerTitle={translate.t("search_findings.delete.title")}
      >
        <GenericForm name="deleteFinding" onSubmit={handleDelete}>
          <FormGroup>
            <ControlLabel>{translate.t("search_findings.delete.justif.label")}</ControlLabel>
            <Field name="justification" component={Dropdown} validate={[required]}>
              <option value="" />
              <option value="DUPLICATED">{translate.t("search_findings.delete.justif.duplicated")}</option>
              <option value="FALSE_POSITIVE">{translate.t("search_findings.delete.justif.false_positive")}</option>
              <option value="NOT_REQUIRED">{translate.t("search_findings.delete.justif.not_required")}</option>
            </Field>
          </FormGroup>
          <hr />
          <Row>
            <Col100>
              <ButtonToolbar>
                <Button onClick={closeDeleteModal}>{translate.t("confirmmodal.cancel")}</Button>
                <Button type="submit">{translate.t("confirmmodal.proceed")}</Button>
              </ButtonToolbar>
            </Col100>
          </Row>
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};

export { findingContent as FindingContent };
