/* eslint-disable react-hooks/rules-of-hooks */
import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { ButtonCol } from "./components/buttoncol";
import { Can } from "utils/authz/Can";
import { CommentsView } from "scenes/Dashboard/containers/CommentsView/index";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { DescriptionView } from "scenes/Dashboard/containers/DescriptionView/index";
import { Dropdown } from "utils/forms/fields";
import { EvidenceView } from "scenes/Dashboard/containers/EvidenceView/index";
import { ExploitView } from "scenes/Dashboard/containers/ExploitView/index";
import { Field } from "redux-form";
import { FindingActions } from "scenes/Dashboard/components/FindingActions";
import { FindingHeader } from "scenes/Dashboard/components/FindingHeader";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { GraphQLError } from "graphql";
import { Have } from "utils/authz/Have";
import type { IHeaderQueryResult } from "scenes/Dashboard/containers/FindingContent/types";
import { Logger } from "utils/logger";
import { Modal } from "components/Modal";
import type { PureAbility } from "@casl/ability";
import type { QueryResult } from "@apollo/react-common";
import React from "react";
import { RecordsView } from "scenes/Dashboard/containers/RecordsView/index";
import { SeverityView } from "scenes/Dashboard/containers/SeverityView/index";
import { TrackingView } from "scenes/Dashboard/containers/TrackingView/index";
import { VulnsView } from "scenes/Dashboard/containers/VulnerabilitiesView/index";
import _ from "lodash";
import { required } from "utils/validations";
import { translate } from "utils/translations/translate";
import { useAbility } from "@casl/react";
import { useTabTracking } from "utils/hooks";
import {
  APPROVE_DRAFT_MUTATION,
  DELETE_FINDING_MUTATION,
  GET_FINDING_HEADER,
  REJECT_DRAFT_MUTATION,
  SUBMIT_DRAFT_MUTATION,
} from "scenes/Dashboard/containers/FindingContent/queries";
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
import {
  Redirect,
  Route,
  Switch,
  useHistory,
  useParams,
  useRouteMatch,
} from "react-router-dom";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";
import { useMutation, useQuery } from "@apollo/react-hooks";

const findingContent: React.FC = (): JSX.Element => {
  const { findingId, projectName } = useParams<{
    findingId: string;
    projectName: string;
  }>();
  const { path, url } = useRouteMatch<{ path: string; url: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const groupPermissions: PureAbility<string> = useAbility(authzGroupContext);
  const { replace } = useHistory();

  // Side effects
  useTabTracking("Finding");

  // State management
  const [isDeleteModalOpen, setDeleteModalOpen] = React.useState(false);
  const openDeleteModal: () => void = React.useCallback((): void => {
    setDeleteModalOpen(true);
  }, []);
  const closeDeleteModal: () => void = React.useCallback((): void => {
    setDeleteModalOpen(false);
  }, []);

  // GraphQL operations
  const {
    data: headerData,
    refetch: headerRefetch,
  }: QueryResult<IHeaderQueryResult> = useQuery(GET_FINDING_HEADER, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading finding header", error);
      });
    },
    variables: {
      canGetExploit: groupPermissions.can("has_forces"),
      canGetHistoricState: permissions.can(
        "backend_api_resolvers_finding_historic_state_resolve"
      ),
      findingId,
    },
  });

  const [submitDraft, { loading: submitting }] = useMutation(
    SUBMIT_DRAFT_MUTATION,
    {
      onCompleted: (result: { submitDraft: { success: boolean } }): void => {
        if (result.submitDraft.success) {
          msgSuccess(
            translate.t("group.drafts.successSubmit"),
            translate.t("group.drafts.titleSuccess")
          );
          void headerRefetch();
        }
      },
      onError: (submitError: ApolloError): void => {
        submitError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          if (
            _.includes(message, "Exception - This draft has missing fields")
          ) {
            msgError(
              translate.t("group.drafts.errorSubmit", {
                missingFields: message.split("fields: ")[1],
              })
            );
          } else if (
            message === "Exception - This draft has already been submitted"
          ) {
            msgError(translate.t("groupAlerts.draftAlreadySubmitted"));
            void headerRefetch();
          } else if (
            message === "Exception - This draft has already been approved"
          ) {
            msgError(translate.t("groupAlerts.draftAlreadyApproved"));
            void headerRefetch();
          } else {
            msgError(translate.t("groupAlerts.errorTextsad"));
            Logger.warning("An error occurred submitting draft", submitError);
          }
        });
      },
      variables: { findingId },
    }
  );

  const [approveDraft, { loading: approving }] = useMutation(
    APPROVE_DRAFT_MUTATION,
    {
      onCompleted: (result: { approveDraft: { success: boolean } }): void => {
        if (result.approveDraft.success) {
          msgSuccess(
            translate.t("search_findings.draftApproved"),
            translate.t("group.drafts.titleSuccess")
          );
          void headerRefetch();
        }
      },
      onError: (approveError: ApolloError): void => {
        approveError.graphQLErrors.forEach(
          ({ message }: GraphQLError): void => {
            switch (message) {
              case "Exception - This draft has already been approved":
                msgError(translate.t("groupAlerts.draftAlreadyApproved"));
                void headerRefetch();
                break;
              case "Exception - The draft has not been submitted yet":
                msgError(translate.t("groupAlerts.draftNotSubmitted"));
                void headerRefetch();
                break;
              case "CANT_APPROVE_FINDING_WITHOUT_VULNS":
                msgError(translate.t("groupAlerts.draftWithoutVulns"));
                break;
              default:
                msgError(translate.t("groupAlerts.errorTextsad"));
                Logger.warning(
                  "An error occurred approving draft",
                  approveError
                );
            }
          }
        );
      },
      variables: { findingId },
    }
  );

  const [rejectDraft, { loading: rejecting }] = useMutation(
    REJECT_DRAFT_MUTATION,
    {
      onCompleted: (result: { rejectDraft: { success: boolean } }): void => {
        if (result.rejectDraft.success) {
          msgSuccess(
            translate.t("search_findings.findingRejected", { findingId }),
            translate.t("group.drafts.titleSuccess")
          );
          void headerRefetch();
        }
      },
      onError: (rejectError: ApolloError): void => {
        rejectError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          switch (message) {
            case "Exception - This draft has already been approved":
              msgError(translate.t("groupAlerts.draftAlreadyApproved"));
              void headerRefetch();
              break;
            case "Exception - The draft has not been submitted yet":
              msgError(translate.t("groupAlerts.draftNotSubmitted"));
              void headerRefetch();
              break;
            default:
              msgError(translate.t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred rejecting draft", rejectError);
          }
        });
      },
      variables: { findingId },
    }
  );

  const [deleteFinding, { loading: deleting }] = useMutation(
    DELETE_FINDING_MUTATION,
    {
      onCompleted: (result: { deleteFinding: { success: boolean } }): void => {
        if (result.deleteFinding.success) {
          msgSuccess(
            translate.t("search_findings.findingDeleted", { findingId }),
            translate.t("group.drafts.titleSuccess")
          );
          replace(`/groups/${projectName}/vulns`);
        }
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred deleting finding", error);
        });
      },
    }
  );

  const handleDelete: (values: {
    justification: string;
  }) => void = React.useCallback(
    (values: { justification: string }): void => {
      void deleteFinding({
        variables: { findingId, justification: values.justification },
      });
    },
    [deleteFinding, findingId]
  );

  if (_.isUndefined(headerData) || _.isEmpty(headerData)) {
    return <div />;
  }

  const isDraft: boolean = _.isEmpty(headerData.finding.releaseDate);
  const hasExploit: boolean = !_.isEmpty(headerData.finding.exploit);
  const hasVulns: boolean =
    _.sum([headerData.finding.openVulns, headerData.finding.closedVulns]) > 0;
  const hasHistory: boolean = !_.isEmpty(headerData.finding.historicState);
  const hasSubmission: boolean = hasHistory
    ? headerData.finding.historicState.slice(-1)[0].state === "SUBMITTED"
    : false;
  const hasReleaseDate: boolean = !_.isEmpty(headerData.finding.releaseDate);

  return (
    <React.StrictMode>
      <div>
        <Row>
          <Col100>
            <React.Fragment>
              <Row>
                <Col60>
                  <h1>{headerData.finding.title}</h1>
                </Col60>
                <ButtonCol>
                  <FindingActions
                    hasSubmission={hasSubmission}
                    hasVulns={hasVulns}
                    isDraft={isDraft}
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
                  discoveryDate={
                    hasReleaseDate
                      ? headerData.finding.releaseDate.split(" ")[0]
                      : "-"
                  }
                  openVulns={headerData.finding.openVulns}
                  severity={headerData.finding.severityScore}
                  status={headerData.finding.state}
                />
                <TabsContainer>
                  <ContentTab
                    icon={"icon pe-7s-menu"}
                    id={"vulnItem"}
                    link={`${url}/locations`}
                    title={translate.t("search_findings.tab_vuln.tabTitle")}
                    tooltip={translate.t("search_findings.tab_vuln.tooltip")}
                  />
                  <ContentTab
                    icon={"icon pe-7s-note"}
                    id={"infoItem"}
                    link={`${url}/description`}
                    title={translate.t(
                      "search_findings.tabDescription.tabTitle"
                    )}
                    tooltip={translate.t(
                      "search_findings.tabDescription.tooltip"
                    )}
                  />
                  <ContentTab
                    icon={"icon pe-7s-calculator"}
                    id={"cssv2Item"}
                    link={`${url}/severity`}
                    title={translate.t("search_findings.tab_severity.tabTitle")}
                    tooltip={translate.t(
                      "search_findings.tab_severity.tooltip"
                    )}
                  />
                  <ContentTab
                    icon={"icon pe-7s-photo"}
                    id={"evidenceItem"}
                    link={`${url}/evidence`}
                    title={translate.t("search_findings.tab_evidence.tabTitle")}
                    tooltip={translate.t(
                      "search_findings.tab_evidence.tooltip"
                    )}
                  />
                  <Have I={"has_forces"}>
                    {hasExploit ||
                    permissions.can(
                      "backend_api_mutations_update_evidence_mutate"
                    ) ? (
                      <ContentTab
                        icon={"icon pe-7s-file"}
                        id={"exploitItem"}
                        link={`${url}/exploit`}
                        title={translate.t(
                          "search_findings.tab_exploit.tabTitle"
                        )}
                        tooltip={translate.t(
                          "search_findings.tab_exploit.tooltip"
                        )}
                      />
                    ) : undefined}
                  </Have>
                  <ContentTab
                    icon={"icon pe-7s-graph1"}
                    id={"trackingItem"}
                    link={`${url}/tracking`}
                    title={translate.t("search_findings.tab_tracking.tabTitle")}
                    tooltip={translate.t(
                      "search_findings.tab_tracking.tooltip"
                    )}
                  />
                  <ContentTab
                    icon={"icon pe-7s-notebook"}
                    id={"recordsItem"}
                    link={`${url}/records`}
                    title={translate.t("search_findings.tabRecords.tabTitle")}
                    tooltip={translate.t("search_findings.tabRecords.tooltip")}
                  />
                  <ContentTab
                    icon={"icon pe-7s-comment"}
                    id={"commentItem"}
                    link={`${url}/consulting`}
                    title={translate.t("search_findings.tabComments.tabTitle")}
                    tooltip={translate.t("search_findings.tabComments.tooltip")}
                  />
                  <Can
                    do={"backend_api_resolvers_finding_observations_resolve"}
                  >
                    <ContentTab
                      icon={"icon pe-7s-note"}
                      id={"observationsItem"}
                      link={`${url}/observations`}
                      title={translate.t(
                        "search_findings.tabObservations.tabTitle"
                      )}
                      tooltip={translate.t(
                        "search_findings.tabObservations.tooltip"
                      )}
                    />
                  </Can>
                </TabsContainer>
              </StickyContainerFinding>
              <TabContent>
                <Switch>
                  <Route
                    component={VulnsView}
                    exact={true}
                    path={`${path}/locations`}
                  />
                  <Route
                    component={DescriptionView}
                    exact={true}
                    path={`${path}/description`}
                  />
                  <Route
                    component={SeverityView}
                    exact={true}
                    path={`${path}/severity`}
                  />
                  <Route
                    component={EvidenceView}
                    exact={true}
                    path={`${path}/evidence`}
                  />
                  <Route
                    component={ExploitView}
                    exact={true}
                    path={`${path}/exploit`}
                  />
                  <Route
                    component={TrackingView}
                    exact={true}
                    path={`${path}/tracking`}
                  />
                  <Route
                    component={RecordsView}
                    exact={true}
                    path={`${path}/records`}
                  />
                  <Route
                    component={CommentsView}
                    exact={true}
                    path={`${path}/:type(consulting|observations)`}
                  />
                  <Redirect to={`${path}/locations`} />
                </Switch>
              </TabContent>
            </React.Fragment>
          </Col100>
        </Row>
      </div>
      <Modal
        headerTitle={translate.t("search_findings.delete.title")}
        open={isDeleteModalOpen}
      >
        <GenericForm name={"deleteFinding"} onSubmit={handleDelete}>
          <FormGroup>
            <ControlLabel>
              {translate.t("search_findings.delete.justif.label")}
            </ControlLabel>
            <Field
              component={Dropdown}
              name={"justification"}
              validate={[required]}
            >
              <option value={""} />
              <option value={"DUPLICATED"}>
                {translate.t("search_findings.delete.justif.duplicated")}
              </option>
              <option value={"FALSE_POSITIVE"}>
                {translate.t("search_findings.delete.justif.falsePositive")}
              </option>
              <option value={"NOT_REQUIRED"}>
                {translate.t("search_findings.delete.justif.notRequired")}
              </option>
            </Field>
          </FormGroup>
          <hr />
          <Row>
            <Col100>
              <ButtonToolbar>
                <Button onClick={closeDeleteModal}>
                  {translate.t("confirmmodal.cancel")}
                </Button>
                <Button type={"submit"}>
                  {translate.t("confirmmodal.proceed")}
                </Button>
              </ButtonToolbar>
            </Col100>
          </Row>
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};

export { findingContent as FindingContent };
