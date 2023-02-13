import type { ApolloError, QueryResult } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useContext, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  Redirect,
  Route,
  Switch,
  useHistory,
  useLocation,
  useParams,
  useRouteMatch,
} from "react-router-dom";

import {
  handleDraftApproval,
  handleDraftApprovalError,
  handleDraftError,
  handleSuccessfulDraft,
} from "./helpers";
import { FindingOverview } from "./overview";
import { ButtonCol, Title, TitleContainer } from "./styles";

import type { IGroupFindingsAttr } from "../Group-Content/GroupFindingsView/types";
import { Select } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import { Tab, Tabs } from "components/Tabs";
import { EventBar } from "scenes/Dashboard/components/EventBar";
import { FindingActions } from "scenes/Dashboard/components/FindingActions";
import { RejectDraftModal } from "scenes/Dashboard/components/RejectDraftModal";
import { CommentsView } from "scenes/Dashboard/containers/Finding-Content/CommentsView/index";
import { DescriptionView } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/index";
import { EvidenceView } from "scenes/Dashboard/containers/Finding-Content/EvidenceView/index";
import { MachineView } from "scenes/Dashboard/containers/Finding-Content/MachineView/index";
import {
  APPROVE_DRAFT_MUTATION,
  GET_FINDING_HEADER,
  REJECT_DRAFT_MUTATION,
  REMOVE_FINDING_MUTATION,
  SUBMIT_DRAFT_MUTATION,
} from "scenes/Dashboard/containers/Finding-Content/queries";
import { RecordsView } from "scenes/Dashboard/containers/Finding-Content/RecordsView/index";
import { SeverityView } from "scenes/Dashboard/containers/Finding-Content/SeverityView/index";
import { TrackingView } from "scenes/Dashboard/containers/Finding-Content/TrackingView/index";
import type { IHeaderQueryResult } from "scenes/Dashboard/containers/Finding-Content/types";
import { VulnsView } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/index";
import { GET_DRAFTS_AND_FINDING_TITLES } from "scenes/Dashboard/containers/Group-Content/GroupDraftsView/queries";
import { GET_FINDINGS } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/queries";
import { FormGroup, TabContent } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { Have } from "utils/authz/Have";
import { featurePreviewContext } from "utils/featurePreview";
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
  const { featurePreview } = useContext(featurePreviewContext);
  const { t } = useTranslation();
  const { path, url } = useRouteMatch<{ path: string; url: string }>();
  const { pathname } = useLocation();
  const { replace } = useHistory();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  // Side effects
  useTabTracking("Finding");

  // State management
  const [isRejectModalOpen, setIsRejectModalOpen] = useState(false);
  const openRejectModal: () => void = useCallback((): void => {
    setIsRejectModalOpen(true);
  }, []);
  const closeRejectModal: () => void = useCallback((): void => {
    setIsRejectModalOpen(false);
  }, []);

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
      canRetrieveHacker: permissions.can(
        "api_resolvers_finding_hacker_resolve"
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
      refetchQueries: [
        { query: GET_DRAFTS_AND_FINDING_TITLES, variables: { groupName } },
        { query: GET_FINDINGS, variables: { groupName } },
      ],
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
            case "Exception - Invalid characters":
              msgError(t("validations.invalidChar"));
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

  const handleReject = useCallback(
    async (values: {
      reasons: string[];
      other: string | null;
    }): Promise<void> => {
      const otherReasons = values.reasons.includes("OTHER") ? values.other : "";
      await rejectDraft({
        variables: { findingId, other: otherReasons, reasons: values.reasons },
      });
      closeRejectModal();
    },
    [closeRejectModal, rejectDraft, findingId]
  );

  const handleDelete = useCallback(
    async (values: Record<string, unknown>): Promise<void> => {
      await removeFinding({
        variables: { findingId, justification: values.justification },
      });
    },
    [removeFinding, findingId]
  );

  useEffect((): void => {
    if (!_.isUndefined(headerData) && !_.isEmpty(headerData)) {
      const [currentTab] = pathname.split("/").slice(-1);
      if (_.isEmpty(headerData.finding.releaseDate)) {
        const properPath: string = `/orgs/${organizationName}/groups/${groupName}/drafts/${findingId}`;
        if (properPath !== url) {
          replace(`${properPath}/${currentTab}`);
        }
      } else {
        const properPath: string = `/orgs/${organizationName}/groups/${groupName}/vulns/${findingId}`;
        if (properPath !== url) {
          replace(`${properPath}/${currentTab}`);
        }
      }
    }
  }, [
    findingId,
    groupName,
    headerData,
    organizationName,
    pathname,
    replace,
    url,
  ]);

  const handleQryErrors: (error: ApolloError) => void = useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading group data", error);
      });
    },
    [t]
  );

  const { data } = useQuery<IGroupFindingsAttr>(GET_FINDINGS, {
    fetchPolicy: "cache-first",
    onError: handleQryErrors,
    variables: { groupName },
  });

  const groupCVSSF = data?.group.findings
    .filter((find): boolean => find.status === "VULNERABLE")
    .reduce(
      (sum, finding): number => sum + 4 ** (finding.severityScore - 4),
      0
    );

  if (_.isUndefined(headerData) || _.isEmpty(headerData)) {
    return <div />;
  }

  const isDraft: boolean = _.isEmpty(headerData.finding.releaseDate);
  const hasVulns: boolean =
    _.sum([headerData.finding.openVulns, headerData.finding.closedVulns]) > 0;
  const hasSubmission: boolean =
    headerData.finding.currentState === "SUBMITTED";

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
                      onReject={openRejectModal}
                      onSubmit={submitDraft}
                    />
                  </Have>
                </ButtonCol>
              </TitleContainer>
              <div>
                <FindingOverview
                  discoveryDate={
                    headerData.finding.releaseDate?.split(" ")[0] ?? "-"
                  }
                  estRemediationTime={calculateEstRemediationTime()}
                  groupCVSSF={groupCVSSF ?? 0}
                  openVulns={headerData.finding.openVulns}
                  severity={headerData.finding.severityScore}
                  status={headerData.finding.status}
                />
                <br />
                <Tabs>
                  {featurePreview ? undefined : (
                    <Tab
                      id={"vulnItem"}
                      link={`${url}/locations`}
                      tooltip={t("searchFindings.tabVuln.tooltip")}
                    >
                      {t("searchFindings.tabVuln.tabTitle")}
                    </Tab>
                  )}
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
                  {headerData.finding.hacker === "machine@fluidattacks.com" ? (
                    <Can do={"api_resolvers_finding_machine_jobs_resolve"}>
                      <Tab
                        id={"machineItem"}
                        link={`${url}/machine`}
                        tooltip={t("searchFindings.tabMachine.tooltip")}
                      >
                        {t("searchFindings.tabMachine.tabTitle")}
                      </Tab>
                    </Can>
                  ) : undefined}
                  {isDraft ? undefined : (
                    <Can do={"api_resolvers_finding_consulting_resolve"}>
                      <Tab
                        id={"commentItem"}
                        link={`${url}/consulting`}
                        tooltip={t("searchFindings.tabComments.tooltip")}
                      >
                        {t("searchFindings.tabComments.tabTitle")}
                      </Tab>
                    </Can>
                  )}
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
              <Select
                label={t("searchFindings.delete.justif.label")}
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
              </Select>
            </FormGroup>
            <ModalConfirm onCancel={closeDeleteModal} />
          </Form>
        </Formik>
      </Modal>
      <RejectDraftModal
        isOpen={isRejectModalOpen}
        onClose={closeRejectModal}
        onSubmit={handleReject}
      />
    </React.StrictMode>
  );
};

export { FindingContent };
