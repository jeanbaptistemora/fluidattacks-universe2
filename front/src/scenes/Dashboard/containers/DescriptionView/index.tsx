/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for using components with render props and
 * conditional rendering
 */

import { useMutation, useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { ApolloError } from "apollo-client";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { RouteComponentProps } from "react-router";
import { Dispatch } from "redux";
import { Field, isPristine, reset, submit } from "redux-form";
import { Can } from "../../../../utils/authz/Can";
import { authzContext } from "../../../../utils/authz/config";
import { formatCweUrl, formatFindingType, getLastTreatment } from "../../../../utils/formatHelpers";
import { dropdownField, textAreaField, textField } from "../../../../utils/forms/fields";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { numeric, required, validDraftTitle } from "../../../../utils/validations";
import { EditableField } from "../../components/EditableField";
import { GenericForm } from "../../components/GenericForm";
import { UpdateVerificationModal } from "../../components/UpdateVerificationModal";
import { VulnerabilitiesView } from "../../components/Vulnerabilities";
import { IVulnDataType } from "../../components/Vulnerabilities/types";
import { ActionButtons } from "./ActionButtons";
import { GET_FINDING_DESCRIPTION, UPDATE_DESCRIPTION_MUTATION } from "./queries";
import { TreatmentView } from "./TreatmentView";
import { IFinding, IHistoricTreatment } from "./types";

export type DescriptionViewProps = RouteComponentProps<{ findingId: string; projectName: string }>;

const descriptionView: React.FC<DescriptionViewProps> = (props: DescriptionViewProps): JSX.Element => {
  const { findingId, projectName } = props.match.params;
  const { userName, userOrganization } = window as typeof window & Dictionary<string>;
  const permissions: PureAbility<string> = useAbility(authzContext);

  // Side effects
  const onMount: (() => void) = (): void => {
    mixpanel.track("FindingDescription", { Organization: userOrganization, User: userName });
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
  const { data, refetch } = useQuery(GET_FINDING_DESCRIPTION, {
    onError: (error: ApolloError): void => {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred loading finding description", error);
    },
    variables: {
      canRetrieveAnalyst: permissions.can("backend_api_dataloaders_finding__get_analyst"),
      findingId,
      projectName,
    },
  });

  const [updateDescription] = useMutation(UPDATE_DESCRIPTION_MUTATION, {
    onCompleted: async (result: { updateDescription: { success: boolean } }): Promise<void> => {
      if (result.updateDescription.success) {
        msgSuccess(
          translate.t("proj_alerts.updated"),
          translate.t("proj_alerts.updated_title"),
        );
        await refetch();
      }
    },
    onError: (updateError: ApolloError): void => {
      msgError(translate.t("proj_alerts.error_textsad"));
      rollbar.error("An error occurred updating finding description", updateError);
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
                      component={dropdownField}
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
              <Can do="backend_api_dataloaders_finding__get_analyst">
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
                    <FormGroup>
                      <ControlLabel>
                        <b>{translate.t("search_findings.tab_description.title")}</b>
                      </ControlLabel>
                      <br />
                      <Field
                        component={textField}
                        name="title"
                        type="text"
                        validate={[required, validDraftTitle]}
                      />
                    </FormGroup>
                  </Col>
                </Row>
              ) : undefined}
            </Can>
            <Row>
              <Col md={12}>
                <Can do="backend_api_resolvers_finding__do_update_description" passThrough={true}>
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={textAreaField}
                      currentValue={dataset.description}
                      label={translate.t("search_findings.tab_description.description")}
                      name="description"
                      renderAsEditable={isEditing}
                      type="text"
                      validate={required}
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
                      component={textAreaField}
                      currentValue={dataset.requirements}
                      label={translate.t("search_findings.tab_description.requirements")}
                      name="requirements"
                      renderAsEditable={isEditing}
                      type="text"
                      validate={required}
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
                      component={textAreaField}
                      currentValue={dataset.attackVectorDesc}
                      label={translate.t("search_findings.tab_description.attack_vectors")}
                      name="attackVectorDesc"
                      renderAsEditable={isEditing}
                      type="text"
                      validate={required}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col>
              <Col md={6}>
                <Can do="backend_api_resolvers_finding__do_update_description" passThrough={true}>
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={textAreaField}
                      currentValue={dataset.affectedSystems}
                      label={translate.t("search_findings.tab_description.affected_systems")}
                      name="affectedSystems"
                      renderAsEditable={isEditing}
                      type="text"
                      validate={required}
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
                      component={textAreaField}
                      currentValue={dataset.threat}
                      label={translate.t("search_findings.tab_description.threat")}
                      name="threat"
                      renderAsEditable={isEditing}
                      type="text"
                      validate={required}
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col>
              <Col md={6}>
                <Can do="backend_api_resolvers_finding__do_update_description" passThrough={true}>
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={textField}
                      currentValue={formatCweUrl(dataset.cweUrl)}
                      label={translate.t("search_findings.tab_description.weakness")}
                      name="cweUrl"
                      renderAsEditable={isEditing}
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
                      component={textAreaField}
                      currentValue={dataset.recommendation}
                      label={translate.t("search_findings.tab_description.recommendation")}
                      name="recommendation"
                      renderAsEditable={isEditing}
                      type="text"
                      validate={required}
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
                      component={textAreaField}
                      currentValue={dataset.compromisedAttributes}
                      label={translate.t("search_findings.tab_description.compromised_attrs")}
                      name="compromisedAttributes"
                      renderAsEditable={isEditing}
                      type="text"
                      visibleWhileEditing={canEdit}
                    />
                  )}
                </Can>
              </Col>
              <Col md={6}>
                <Can do="backend_api_resolvers_finding__do_update_description" passThrough={true}>
                  {(canEdit: boolean): JSX.Element => (
                    <EditableField
                      component={textAreaField}
                      currentValue={dataset.compromisedRecords}
                      label={translate.t("search_findings.tab_description.compromised_records")}
                      name="compromisedRecords"
                      renderAsEditable={isEditing}
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
