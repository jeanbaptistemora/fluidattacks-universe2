import type { ApolloError, QueryResult } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
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
import { ButtonCol, Title, TitleContainer } from "./styles";

import { Modal, ModalConfirm } from "components/Modal";
import { Tab, Tabs } from "components/Tabs";
import { EventBar } from "scenes/Dashboard/components/EventBar";
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
import { ControlLabel, FormGroup, TabContent } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { Have } from "utils/authz/Have";
import { FormikDropdown } from "utils/forms/fields";
import { useTabTracking } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { composeValidators, required } from "utils/validations";

const FindingContent: React.FC = (): JSX.Element => {
  const { findingId, groupName, organizationName } = useParams<{
    findingId: string;
    groupName: string;
    organizationName: string;
  }>();
  const { t } = useTranslation();
  const { path, url } = useRouteMatch<{ path: string; url: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const { replace } = useHistory();

  // Side effects
  useTabTracking("Finding");

  // State management
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const openDeleteModal: () => void = useCallback((): void => {
    setIsDeleteModalOpen(true);
  }, []);
  const closeDeleteModal: () => void = useCallback((): void => {
    setIsDeleteModalOpen(false);
  }, []);

  // GraphQL operations
  const {
    data: headerData,
    refetch: headerRefetch,
  }: QueryResult<IHeaderQueryResult> = useQuery(GET_FINDING_HEADER, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
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
      onCompleted: async (result: {
        rejectDraft: { success: boolean };
      }): Promise<void> => {
        if (result.rejectDraft.success) {
          msgSuccess(
            t("searchFindings.findingRejected", { findingId }),
            t("group.drafts.titleSuccess")
          );
          await headerRefetch();
        }
      },
      onError: (rejectError: ApolloError): void => {
        rejectError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          switch (message) {
            case "Exception - This draft has already been approved":
              msgError(t("groupAlerts.draftAlreadyApproved"));
              // Exception: FP(void operator is necessary)
              // eslint-disable-next-line
              void headerRefetch(); //NOSONAR
              break;
            case "Exception - The draft has not been submitted yet":
              msgError(t("groupAlerts.draftNotSubmitted"));
              // Exception: FP(void operator is necessary)
              // eslint-disable-next-line
              void headerRefetch(); //NOSONAR
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred rejecting draft", rejectError);
          }
        });
      },
      // Temporary dummy value for reason while the proper selection is added
      variables: { findingId, reason: "WRITING" },
    }
  );

  const [removeFinding, { loading: deleting }] = useMutation(
    REMOVE_FINDING_MUTATION,
    {
      onCompleted: (result: { removeFinding: { success: boolean } }): void => {
        if (result.removeFinding.success) {
          msgSuccess(
            t("searchFindings.findingDeleted", { findingId }),
            t("group.drafts.titleSuccess")
          );
          replace(`/orgs/${organizationName}/groups/${groupName}/vulns`);
        }
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred deleting finding", error);
        });
      },
    }
  );

  const handleDelete = useCallback(
    async (values: Record<string, unknown>): Promise<void> => {
      await removeFinding({
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

  const calculateEstRemediationTime = (): string => {
    if (_.isNil(headerData.finding.minTimeToRemediate)) {
      return "Unknown";
    }
    const minutesInAnHour = 60;
    const rawHours =
      (headerData.finding.minTimeToRemediate * headerData.finding.openVulns) /
      minutesInAnHour;

    if (rawHours === 0) {
      return "None";
    } else if (Number.isInteger(rawHours)) {
      return `${rawHours.toFixed(0)}h`;
    }

    return `${rawHours.toFixed(1)}h`;
  };

  return (
    <React.StrictMode>
      <div>
        <div>
          <div>
            <div>
              <EventBar organizationName={organizationName} />
              <TitleContainer>
                <Title>{headerData.finding.title}</Title>
                <ButtonCol>
                  <Have I={"can_report_vulnerabilities"}>
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
                  </Have>
                </ButtonCol>
              </TitleContainer>
              <div>
                <FindingHeader
                  discoveryDate={
                    headerData.finding.releaseDate?.split(" ")[0] ?? "-"
                  }
                  estRemediationTime={calculateEstRemediationTime()}
                  openVulns={headerData.finding.openVulns}
                  severity={headerData.finding.severityScore}
                  status={headerData.finding.state}
                />
                <Tabs>
                  <Tab
                    id={"vulnItem"}
                    link={`${url}/locations`}
                    tooltip={t("searchFindings.tabVuln.tooltip")}
                  >
                    {t("searchFindings.tabVuln.tabTitle")}
                  </Tab>
                  <Tab
                    id={"infoItem"}
                    link={`${url}/description`}
                    tooltip={t("searchFindings.tabDescription.tooltip")}
                  >
                    {t("searchFindings.tabDescription.tabTitle")}
                  </Tab>
                  <Tab
                    id={"cssv2Item"}
                    link={`${url}/severity`}
                    tooltip={t("searchFindings.tabSeverity.tooltip")}
                  >
                    {t("searchFindings.tabSeverity.tabTitle")}
                  </Tab>
                  <Tab
                    id={"evidenceItem"}
                    link={`${url}/evidence`}
                    tooltip={t("searchFindings.tabEvidence.tooltip")}
                  >
                    {t("searchFindings.tabEvidence.tabTitle")}
                  </Tab>
                  <Tab
                    id={"trackingItem"}
                    link={`${url}/tracking`}
                    tooltip={t("searchFindings.tabTracking.tooltip")}
                  >
                    {t("searchFindings.tabTracking.tabTitle")}
                  </Tab>
                  <Tab
                    id={"recordsItem"}
                    link={`${url}/records`}
                    tooltip={t("searchFindings.tabRecords.tooltip")}
                  >
                    {t("searchFindings.tabRecords.tabTitle")}
                  </Tab>
                  <Can do={"api_resolvers_finding_machine_jobs_resolve"}>
                    <Tab
                      id={"machineItem"}
                      link={`${url}/machine`}
                      tooltip={t("searchFindings.tabMachine.tooltip")}
                    >
                      {t("searchFindings.tabMachine.tabTitle")}
                    </Tab>
                  </Can>
                  <Have I={"has_squad"}>
                    <Can do={"api_resolvers_finding_consulting_resolve"}>
                      <Tab
                        id={"commentItem"}
                        link={`${url}/consulting`}
                        tooltip={t("searchFindings.tabComments.tooltip")}
                      >
                        {t("searchFindings.tabComments.tabTitle")}
                      </Tab>
                    </Can>
                  </Have>
                  <Can do={"api_resolvers_finding_observations_resolve"}>
                    <Tab
                      id={"observationsItem"}
                      link={`${url}/observations`}
                      tooltip={t("searchFindings.tabObservations.tooltip")}
                    >
                      {t("searchFindings.tabObservations.tabTitle")}
                    </Tab>
                  </Can>
                </Tabs>
              </div>
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
            </div>
          </div>
        </div>
      </div>
      <Modal
        onClose={closeDeleteModal}
        open={isDeleteModalOpen}
        title={t("searchFindings.delete.title")}
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
                {t("searchFindings.delete.justif.label")}
              </ControlLabel>
              <Field
                component={FormikDropdown}
                name={"justification"}
                validate={composeValidators([required])}
              >
                <option value={""} />
                <option value={"DUPLICATED"}>
                  {t("searchFindings.delete.justif.duplicated")}
                </option>
                <option value={"FALSE_POSITIVE"}>
                  {t("searchFindings.delete.justif.falsePositive")}
                </option>
                <option value={"NOT_REQUIRED"}>
                  {t("searchFindings.delete.justif.notRequired")}
                </option>
              </Field>
            </FormGroup>
            <ModalConfirm onCancel={closeDeleteModal} />
          </Form>
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { FindingContent };
