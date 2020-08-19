/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for using components with render props and
 * conditional rendering
 */

import { useMutation, useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router";
import { Dispatch } from "redux";
import { Field, isPristine, reset, submit } from "redux-form";
import { ConfigurableValidator } from "revalidate";
import { TooltipWrapper } from "../../../../components/TooltipWrapper/index";
import { Can } from "../../../../utils/authz/Can";
import { authzPermissionsContext } from "../../../../utils/authz/config";
import { Dropdown, Text, TextArea } from "../../../../utils/forms/fields";
import { Logger } from "../../../../utils/logger";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import { translate } from "../../../../utils/translations/translate";
import { maxLength, numeric, required, validDraftTitle, validTextField } from "../../../../utils/validations";
import { EditableField } from "../../components/EditableField";
import { GenericForm } from "../../components/GenericForm";
import { UpdateVerificationModal } from "../../components/UpdateVerificationModal";
import { VulnerabilitiesView } from "../../components/Vulnerabilities";
import { IVulnDataType } from "../../components/Vulnerabilities/types";
import { ActionButtons } from "./ActionButtons";
import { GET_FINDING_DESCRIPTION, UPDATE_DESCRIPTION_MUTATION } from "./queries";
import { TreatmentView } from "./TreatmentView";
import { IFinding, IFindingDescriptionData, IFindingDescriptionVars, IHistoricTreatment } from "./types";
import {
  formatCompromisedRecords, formatCweUrl, formatFindingType, getLastTreatment,
} from "./utils";

const maxTitleLength: ConfigurableValidator = maxLength(90);
const maxDescriptionLength: ConfigurableValidator = maxLength(500);
const maxRequirementsLength: ConfigurableValidator = maxLength(500);
const maxImpactsLength: ConfigurableValidator = maxLength(300);
const maxAffectedSystemsLength: ConfigurableValidator = maxLength(200);
const maxThreatLength: ConfigurableValidator = maxLength(300);
const maxRecommendationLength: ConfigurableValidator = maxLength(300);
const maxCompromisedAttributesLength: ConfigurableValidator = maxLength(200);

const descriptionView: React.FC = (): JSX.Element => {
  const { findingId, projectName } = useParams<{ findingId: string; projectName: string }>();
  const { userName } = window as typeof window & Dictionary<string>;
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  // Side effects
  const onMount: (() => void) = (): void => {
    mixpanel.track("FindingDescription", { User: userName });
  };
  React.useEffect(onMount, []);

  // State management
  const dispatch: Dispatch = useDispatch();

  const isDescriptionPristine: boolean = useSelector((state: {}) =>
    isPristine("editDescription")(state));
  const isTreatmentPristine: boolean = useSelector((state: {}) =>
    isPristine("editTreatment")(state));

  const [isEditing, setEditing] = React.useState(false);
  const toggleEdit: (() => void) = (): void => {
    if (!isDescriptionPristine) {
      dispatch(reset("editDescription"));
    }
    if (!isTreatmentPristine) {
      dispatch(reset("editTreatment"));
    }
    setEditing(!isEditing);
  };

  const [approvalModalConfig, setApprovalModalConfig] = React.useState({ open: false, type: "" });
  const openApproveModal: (() => void) = (): void => {
    setApprovalModalConfig({ open: true, type: "APPROVED" });
  };
  const openRejectModal: (() => void) = (): void => {
    setApprovalModalConfig({ open: true, type: "REJECTED" });
  };
  const closeApprovalModal: (() => void) = (): void => {
    setApprovalModalConfig({ open: false, type: "" });
  };

  type verificationFn = (
    vulnerabilities: IVulnDataType[], type: "request" | "verify", clearSelected: () => void,
  ) => void;
  const [remediationModalConfig, setRemediationModalConfig] = React.useState<{
    open: boolean;
    type: "request" | "verify";
    vulnerabilities: IVulnDataType[];
    clearSelected(): void;
  }>({
    clearSelected: (): void => undefined,
    open: false,
    type: "request",
    vulnerabilities: [],
  });
  const openRemediationModal: verificationFn = (
    vulnerabilities: IVulnDataType[], type: "request" | "verify", clearSelected: () => void,
  ): void => {
    setRemediationModalConfig({ open: true, type, vulnerabilities, clearSelected });
  };
  const closeRemediationModal: (() => void) = (): void => {
    setRemediationModalConfig({
      clearSelected: (): void => undefined,
      open: false,
      type: "request",
      vulnerabilities: [],
    });
  };

  const [isRequestingVerify, setRequestingVerify] = React.useState(false);
  const toggleRequestVerify: (() => void) = (): void => {
    setRequestingVerify(!isRequestingVerify);
  };

  const [isVerifying, setVerifying] = React.useState(false);
  const toggleVerify: (() => void) = (): void => {
    setVerifying(!isVerifying);
  };

  // GraphQL operations
  const { data, refetch } = useQuery<IFindingDescriptionData, IFindingDescriptionVars>(GET_FINDING_DESCRIPTION, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred loading finding description", error);
      });
    },
    variables: {
      canRetrieveAnalyst: permissions.can("backend_api_resolvers_finding__get_analyst"),
      findingId,
      projectName,
    },
  });

  const [updateDescription] = useMutation(UPDATE_DESCRIPTION_MUTATION, {
    onCompleted: async (result: { updateDescription: { success: boolean } }): Promise<void> => {
      if (result.updateDescription.success) {
        msgSuccess(
          translate.t("group_alerts.updated"),
          translate.t("group_alerts.updated_title"),
        );
        await refetch();
      }
    },
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Invalid field in form":
            msgError(translate.t("validations.invalidValueInField"));
            break;
          case "Exception - Invalid characters":
            msgError(translate.t("validations.invalid_char"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("An error occurred updating treatment", updateError);
        }
      });
    },
  });

  const handleDescriptionSubmit: ((values: Dictionary<string>) => Promise<void>) = async (
    values: Dictionary<string>,
  ): Promise<void> => {
    setEditing(false);
    await updateDescription({
      variables: {
        ...values,
        compromisedRecords: Number(values.compromisedRecords),
        findingId,
      },
    });
  };

  const handleSubmit: (() => void) = (): void => {
    if (!isDescriptionPristine) {
      dispatch(submit("editDescription"));
    }
    if (!isTreatmentPristine) {
      dispatch(submit("editTreatment"));
    }
  };

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  const dataset: IFinding = data.finding;
  const lastTreatment: IHistoricTreatment = getLastTreatment(dataset.historicTreatment);

  return (
    <React.StrictMode>
      <ActionButtons
        isEditing={isEditing}
        isPristine={isDescriptionPristine && isTreatmentPristine}
        isRemediated={dataset.newRemediated}
        isRequestingVerify={isRequestingVerify}
        isVerified={dataset.verified}
        isVerifying={isVerifying}
        lastTreatment={lastTreatment}
        onApproveAcceptation={openApproveModal}
        onEdit={toggleEdit}
        onRejectAcceptation={openRejectModal}
        onRequestVerify={toggleRequestVerify}
        onUpdate={handleSubmit}
        onVerify={toggleVerify}
        state={dataset.state}
        subscription={data.project.subscription}
      />
      <br />
      <GenericForm name="editDescription" initialValues={dataset} onSubmit={handleDescriptionSubmit}>
        <React.Fragment>
          <React.Fragment>
            <Row>
              <Col md={6}>
                <Can do="backend_api_resolvers_finding__do_update_description" passThrough={true}>
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={Dropdown}
                      currentValue={formatFindingType(dataset.type)}
                      label={translate.t("search_findings.tab_description.type.title")}
                      name="type"
                      renderAsEditable={isEditing}
                      validate={required}
                      visibleWhileEditing={canEdit}
                    >
                      <option value="" />
                      <option value="SECURITY">{translate.t("search_findings.tab_description.type.security")}</option>
                      <option value="HYGIENE">{translate.t("search_findings.tab_description.type.hygiene")}</option>
                    </EditableField>
                  )}
                </Can>
              </Col>
              <Can do="backend_api_resolvers_finding__get_analyst">
                <Col md={6}>
                  <FormGroup>
                    <ControlLabel>
                      <b>{translate.t("search_findings.tab_description.analyst")}</b>
                    </ControlLabel>
                    <p>{dataset.analyst}</p>
                  </FormGroup>
                </Col>
              </Can>
            </Row>
            <Can do="backend_api_resolvers_finding__do_update_description">
              {isEditing ? (
                <Row>
                  <Col md={12}>
                    <TooltipWrapper
                      message={translate.t("search_findings.tab_description.title.tooltip")}
                    >
                      <FormGroup>
                        <ControlLabel>
                          <b>{translate.t("search_findings.tab_description.title.text")}</b>
                        </ControlLabel>
                        <br />
                        <Field
                          component={Text}
                          name="title"
                          type="text"
                          validate={[required, validDraftTitle, validTextField, maxTitleLength]}
                        />
                      </FormGroup>
                    </TooltipWrapper>
                  </Col>
                </Row>
              ) : undefined}
            </Can>
            <Row>
              <Col md={12}>
                <Can do="backend_api_resolvers_finding__do_update_description" passThrough={true}>
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
                      currentValue={dataset.description}
                      label={translate.t("search_findings.tab_description.description.text")}
                      name="description"
                      renderAsEditable={isEditing}
                      tooltip={translate.t("search_findings.tab_description.description.tooltip")}
                      type="text"
                      validate={[required, validTextField, maxDescriptionLength]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col>
            </Row>
            <Row>
              <Col md={12}>
                <Can do="backend_api_resolvers_finding__do_update_description" passThrough={true}>
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
                      currentValue={dataset.requirements}
                      label={translate.t("search_findings.tab_description.requirements.text")}
                      name="requirements"
                      renderAsEditable={isEditing}
                      tooltip={translate.t("search_findings.tab_description.requirements.tooltip")}
                      type="text"
                      validate={[required, validTextField, maxRequirementsLength]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col>
            </Row>
            <Row>
              <Col md={12}>
                <FormGroup>
                  <ControlLabel>
                    <b>{translate.t("search_findings.tab_description.where")}</b>
                  </ControlLabel>
                  <br />
                  <VulnerabilitiesView
                    btsUrl={dataset.btsUrl}
                    editMode={isEditing}
                    findingId={findingId}
                    isRequestVerification={isRequestingVerify}
                    isVerifyRequest={isVerifying}
                    lastTreatment={lastTreatment}
                    projectName={projectName}
                    separatedRow={true}
                    state="open"
                    verificationFn={openRemediationModal}
                  />
                </FormGroup>
              </Col>
            </Row>
            <Row>
              <Col md={6}>
                <Can do="backend_api_resolvers_finding__do_update_description" passThrough={true}>
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
                      currentValue={dataset.attackVectorDesc}
                      label={translate.t("search_findings.tab_description.attack_vectors.text")}
                      name="attackVectorDesc"
                      renderAsEditable={isEditing}
                      tooltip={translate.t("search_findings.tab_description.attack_vectors.tooltip")}
                      type="text"
                      validate={[required, validTextField, maxImpactsLength]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col>
              <Col md={6}>
                <Can do="backend_api_resolvers_finding__do_update_description" passThrough={true}>
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
                      currentValue={dataset.affectedSystems}
                      label={translate.t("search_findings.tab_description.affected_systems.text")}
                      name="affectedSystems"
                      renderAsEditable={isEditing}
                      tooltip={translate.t("search_findings.tab_description.affected_systems.tooltip")}
                      type="text"
                      validate={[required, validTextField, maxAffectedSystemsLength]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col>
            </Row>
            <Row>
              <Col md={6}>
                <Can do="backend_api_resolvers_finding__do_update_description" passThrough={true}>
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
                      currentValue={dataset.threat}
                      label={translate.t("search_findings.tab_description.threat.text")}
                      name="threat"
                      renderAsEditable={isEditing}
                      tooltip={translate.t("search_findings.tab_description.threat.tooltip")}
                      type="text"
                      validate={[required, validTextField, maxThreatLength]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col>
              <Col md={6}>
                <Can do="backend_api_resolvers_finding__do_update_description" passThrough={true}>
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
                      currentValue={formatCweUrl(dataset.cweUrl)}
                      label={translate.t("search_findings.tab_description.weakness.text")}
                      name="cweUrl"
                      renderAsEditable={isEditing}
                      tooltip={translate.t("search_findings.tab_description.weakness.tooltip")}
                      type="number"
                      validate={[required, numeric]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col>
            </Row>
            <Row>
              <Col md={12}>
                <Can do="backend_api_resolvers_finding__do_update_description" passThrough={true}>
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
                      currentValue={dataset.recommendation}
                      label={translate.t("search_findings.tab_description.recommendation.text")}
                      name="recommendation"
                      renderAsEditable={isEditing}
                      tooltip={translate.t("search_findings.tab_description.recommendation.tooltip")}
                      type="text"
                      validate={[required, validTextField, maxRecommendationLength]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col>
            </Row>
            <Row>
              <Col md={6}>
                <Can do="backend_api_resolvers_finding__do_update_description" passThrough={true}>
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
                      currentValue={dataset.compromisedAttributes}
                      label={translate.t("search_findings.tab_description.compromised_attrs.text")}
                      name="compromisedAttributes"
                      renderAsEditable={isEditing}
                      tooltip={translate.t("search_findings.tab_description.compromised_attrs.tooltip")}
                      type="text"
                      validate={[validTextField, maxCompromisedAttributesLength]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col>
              <Col md={6}>
                <Can do="backend_api_resolvers_finding__do_update_description" passThrough={true}>
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={TextArea}
                      currentValue={formatCompromisedRecords(dataset.compromisedRecords)}
                      label={translate.t("search_findings.tab_description.compromised_records.text")}
                      name="compromisedRecords"
                      renderAsEditable={isEditing}
                      tooltip={translate.t("search_findings.tab_description.compromised_records.tooltip")}
                      type="number"
                      validate={[required, numeric]}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col>
            </Row>
          </React.Fragment>
        </React.Fragment>
      </GenericForm>
      <TreatmentView
        approvalModalConfig={approvalModalConfig}
        findingId={findingId}
        isEditing={isEditing}
        onCloseApproval={closeApprovalModal}
        projectName={projectName}
        setEditing={setEditing}
      />
      {remediationModalConfig.open ? (
        <UpdateVerificationModal
          clearSelected={_.get(remediationModalConfig, "clearSelected")}
          findingId={findingId}
          handleCloseModal={closeRemediationModal}
          isOpen={true}
          refetchData={refetch}
          remediationType={remediationModalConfig.type}
          setRequestState={toggleRequestVerify}
          setVerifyState={toggleVerify}
          vulns={remediationModalConfig.vulnerabilities}
        />
      ) : undefined}
    </React.StrictMode>
  );
};

export { descriptionView as DescriptionView };
