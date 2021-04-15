/* eslint-disable react-hooks/rules-of-hooks */
import type { ApolloError, QueryResult } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
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
import { Field } from "redux-form";

import { ButtonCol } from "./components/buttoncol";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { FindingActions } from "scenes/Dashboard/components/FindingActions";
import { FindingHeader } from "scenes/Dashboard/components/FindingHeader";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { CommentsView } from "scenes/Dashboard/containers/CommentsView/index";
import { DescriptionView } from "scenes/Dashboard/containers/DescriptionView/index";
import { EvidenceView } from "scenes/Dashboard/containers/EvidenceView/index";
import {
  APPROVE_DRAFT_MUTATION,
  DELETE_FINDING_MUTATION,
  GET_FINDING_HEADER,
  REJECT_DRAFT_MUTATION,
  SUBMIT_DRAFT_MUTATION,
} from "scenes/Dashboard/containers/FindingContent/queries";
import type { IHeaderQueryResult } from "scenes/Dashboard/containers/FindingContent/types";
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
import { authzPermissionsContext } from "utils/authz/config";
import { Dropdown } from "utils/forms/fields";
import { useTabTracking } from "utils/hooks";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { required } from "utils/validations";

const findingContent: React.FC = (): JSX.Element => {
  const { findingId, projectName } = useParams<{
    findingId: string;
    projectName: string;
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
            translate.t("searchFindings.draftApproved"),
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
            translate.t("searchFindings.findingRejected", { findingId }),
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
            translate.t("searchFindings.findingDeleted", { findingId }),
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

  const handleDelete: (values: { justification: string }) => void = useCallback(
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
                  <ContentTab
                    icon={"icon pe-7s-comment"}
                    id={"commentItem"}
                    link={`${url}/consulting`}
                    title={translate.t("searchFindings.tabComments.tabTitle")}
                    tooltip={translate.t("searchFindings.tabComments.tooltip")}
                  />
                  <Can
                    do={"backend_api_resolvers_finding_observations_resolve"}
                  >
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
        headerTitle={translate.t("searchFindings.delete.title")}
        open={isDeleteModalOpen}
      >
        <GenericForm name={"deleteFinding"} onSubmit={handleDelete}>
          <FormGroup>
            <ControlLabel>
              {translate.t("searchFindings.delete.justif.label")}
            </ControlLabel>
            <Field
              component={Dropdown}
              name={"justification"}
              validate={[required]}
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
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};

export { findingContent as FindingContent };
