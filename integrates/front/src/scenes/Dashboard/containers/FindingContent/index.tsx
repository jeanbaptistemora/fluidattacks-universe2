/* eslint-disable react-hooks/rules-of-hooks */
import type { ApolloError, QueryResult } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import {
  Redirect,
  Route,
  Switch,
  useHistory,
  useParams,
  useRouteMatch,
} from "react-router-dom";

import {
  handleDraftApproval,
  handleDraftApprovalError,
  handleDraftError,
  handleSuccessfulDraft,
} from "./helpers";
import { ButtonCol, Title } from "./styles";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { FindingActions } from "scenes/Dashboard/components/FindingActions";
import { FindingHeader } from "scenes/Dashboard/components/FindingHeader";
import { CommentsView } from "scenes/Dashboard/containers/CommentsView/index";
import { DescriptionView } from "scenes/Dashboard/containers/DescriptionView/index";
import { EvidenceView } from "scenes/Dashboard/containers/EvidenceView/index";
import {
  APPROVE_DRAFT_MUTATION,
  GET_FINDING_HEADER,
  REJECT_DRAFT_MUTATION,
  REMOVE_FINDING_MUTATION,
  SUBMIT_DRAFT_MUTATION,
} from "scenes/Dashboard/containers/FindingContent/queries";
import type { IHeaderQueryResult } from "scenes/Dashboard/containers/FindingContent/types";
import { MachineView } from "scenes/Dashboard/containers/MachineView/index";
import { RecordsView } from "scenes/Dashboard/containers/RecordsView/index";
import { SeverityView } from "scenes/Dashboard/containers/SeverityView/index";
import { TrackingView } from "scenes/Dashboard/containers/TrackingView/index";
import { VulnsView } from "scenes/Dashboard/containers/VulnerabilitiesView/index";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  FormGroup,
  Row,
  StickyContainer,
  TabContent,
  TabsContainer,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { Have } from "utils/authz/Have";
import { FormikDropdown } from "utils/forms/fields";
import { useTabTracking } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { composeValidators, required } from "utils/validations";

const findingContent: React.FC = (): JSX.Element => {
  const { findingId, groupName, organizationName } =
    useParams<{
      findingId: string;
      groupName: string;
      organizationName: string;
    }>();
  const { path, url } = useRouteMatch<{ path: string; url: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const { replace } = useHistory();

  // Side effects
  useTabTracking("Finding");

  // State management
  const [isDeleteModalOpen, setDeleteModalOpen] = useState(false);
  const openDeleteModal: () => void = useCallback((): void => {
    setDeleteModalOpen(true);
  }, []);
  const closeDeleteModal: () => void = useCallback((): void => {
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
      canGetHistoricState: permissions.can(
        "api_resolvers_finding_historic_state_resolve"
      ),
      findingId,
    },
  });

  const [submitDraft, { loading: submitting }] = useMutation(
    SUBMIT_DRAFT_MUTATION,
    {
      onCompleted: (result: { submitDraft: { success: boolean } }): void => {
        handleSuccessfulDraft(result, headerRefetch);
      },
      onError: (submitError: ApolloError): void => {
        handleDraftError(submitError, headerRefetch);
      },
      variables: { findingId },
    }
  );

  const [approveDraft, { loading: approving }] = useMutation(
    APPROVE_DRAFT_MUTATION,
    {
      onCompleted: (result: { approveDraft: { success: boolean } }): void => {
        handleDraftApproval(result, headerRefetch);
      },
      onError: (approveError: ApolloError): void => {
        handleDraftApprovalError(approveError, headerRefetch);
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
            translate.t("searchFindings.findingRejected", { findingId }),
            translate.t("group.drafts.titleSuccess")
          );
          // Exception: FP(void operator is necessary)
          // eslint-disable-next-line
          void headerRefetch(); //NOSONAR
        }
      },
      onError: (rejectError: ApolloError): void => {
        rejectError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          switch (message) {
            case "Exception - This draft has already been approved":
              msgError(translate.t("groupAlerts.draftAlreadyApproved"));
              // Exception: FP(void operator is necessary)
              // eslint-disable-next-line
              void headerRefetch(); //NOSONAR
              break;
            case "Exception - The draft has not been submitted yet":
              msgError(translate.t("groupAlerts.draftNotSubmitted"));
              // Exception: FP(void operator is necessary)
              // eslint-disable-next-line
              void headerRefetch(); //NOSONAR
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

  const [removeFinding, { loading: deleting }] = useMutation(
    REMOVE_FINDING_MUTATION,
    {
      onCompleted: (result: { removeFinding: { success: boolean } }): void => {
        if (result.removeFinding.success) {
          msgSuccess(
            translate.t("searchFindings.findingDeleted", { findingId }),
            translate.t("group.drafts.titleSuccess")
          );
          replace(`/orgs/${organizationName}/groups/${groupName}/vulns`);
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

  const handleDelete: (values: Record<string, unknown>) => void = useCallback(
    (values: Record<string, unknown>): void => {
      // Exception: FP(void operator is necessary)
      // eslint-disable-next-line
      void removeFinding({ //NOSONAR
        variables: { findingId, justification: values.justification },
      });
    },
    [removeFinding, findingId]
  );

  if (_.isUndefined(headerData) || _.isEmpty(headerData)) {
    return <div />;
  }

  const isDraft: boolean = _.isEmpty(headerData.finding.releaseDate);
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
        <div>
          <Col100>
            <React.Fragment>
              <Row>
                <Title>{headerData.finding.title}</Title>
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
              <StickyContainer>
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
                    title={translate.t("searchFindings.tabVuln.tabTitle")}
                    tooltip={translate.t("searchFindings.tabVuln.tooltip")}
                  />
                  <ContentTab
                    icon={"icon pe-7s-note"}
                    id={"infoItem"}
                    link={`${url}/description`}
                    title={translate.t(
                      "searchFindings.tabDescription.tabTitle"
                    )}
                    tooltip={translate.t(
                      "searchFindings.tabDescription.tooltip"
                    )}
                  />
                  <ContentTab
                    icon={"icon pe-7s-calculator"}
                    id={"cssv2Item"}
                    link={`${url}/severity`}
                    title={translate.t("searchFindings.tabSeverity.tabTitle")}
                    tooltip={translate.t("searchFindings.tabSeverity.tooltip")}
                  />
                  <ContentTab
                    icon={"icon pe-7s-photo"}
                    id={"evidenceItem"}
                    link={`${url}/evidence`}
                    title={translate.t("searchFindings.tabEvidence.tabTitle")}
                    tooltip={translate.t("searchFindings.tabEvidence.tooltip")}
                  />
                  <ContentTab
                    icon={"icon pe-7s-graph1"}
                    id={"trackingItem"}
                    link={`${url}/tracking`}
                    title={translate.t("searchFindings.tabTracking.tabTitle")}
                    tooltip={translate.t("searchFindings.tabTracking.tooltip")}
                  />
                  <ContentTab
                    icon={"icon pe-7s-notebook"}
                    id={"recordsItem"}
                    link={`${url}/records`}
                    title={translate.t("searchFindings.tabRecords.tabTitle")}
                    tooltip={translate.t("searchFindings.tabRecords.tooltip")}
                  />
                  <Can do={"api_resolvers_finding_machine_jobs_resolve"}>
                    <ContentTab
                      icon={"icon pe-7s-rocket"}
                      id={"machineItem"}
                      link={`${url}/machine`}
                      title={translate.t("searchFindings.tabMachine.tabTitle")}
                      tooltip={translate.t("searchFindings.tabMachine.tooltip")}
                    />
                  </Can>
                  <Have I={"has_squad"}>
                    <Can
                      do={"api_resolvers_finding_new_consulting_new_resolve"}
                    >
                      <ContentTab
                        icon={"icon pe-7s-comment"}
                        id={"commentItem"}
                        link={`${url}/consulting`}
                        title={translate.t(
                          "searchFindings.tabComments.tabTitle"
                        )}
                        tooltip={translate.t(
                          "searchFindings.tabComments.tooltip"
                        )}
                      />
                    </Can>
                  </Have>
                  <Can do={"api_resolvers_finding_observations_resolve"}>
                    <ContentTab
                      icon={"icon pe-7s-note"}
                      id={"observationsItem"}
                      link={`${url}/observations`}
                      title={translate.t(
                        "searchFindings.tabObservations.tabTitle"
                      )}
                      tooltip={translate.t(
                        "searchFindings.tabObservations.tooltip"
                      )}
                    />
                  </Can>
                </TabsContainer>
              </StickyContainer>
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
                    component={MachineView}
                    exact={true}
                    path={`${path}/machine`}
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
        </div>
      </div>
      <Modal
        headerTitle={translate.t("searchFindings.delete.title")}
        onEsc={closeDeleteModal}
        open={isDeleteModalOpen}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{}}
          name={"removeFinding"}
          onSubmit={handleDelete}
        >
          <Form id={"removeFinding"}>
            <FormGroup>
              <ControlLabel>
                {translate.t("searchFindings.delete.justif.label")}
              </ControlLabel>
              <Field
                component={FormikDropdown}
                name={"justification"}
                validate={composeValidators([required])}
              >
                <option value={""} />
                <option value={"DUPLICATED"}>
                  {translate.t("searchFindings.delete.justif.duplicated")}
                </option>
                <option value={"FALSE_POSITIVE"}>
                  {translate.t("searchFindings.delete.justif.falsePositive")}
                </option>
                <option value={"NOT_REQUIRED"}>
                  {translate.t("searchFindings.delete.justif.notRequired")}
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
          </Form>
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { findingContent as FindingContent };
