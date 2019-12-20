/* tslint:disable jsx-no-lambda number-literal-format jsx-no-multiline-js
 * JSX-NO-LAMBDA: Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 *
 * JSX-NO-MULTILINE-JS: necessary for the sake of readability of the code that dynamically renders fields
 * as input or <p> depending on their state
 */

import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Mutation, MutationFn, MutationResult } from "react-apollo";
import { ButtonToolbar, Col, Row } from "react-bootstrap";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { AnyAction, Reducer } from "redux";
import { formValueSelector, submit } from "redux-form";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { Button } from "../../../../components/Button/index";
import { ConfirmDialog } from "../../../../components/ConfirmDialog";
import { FluidIcon } from "../../../../components/FluidIcon";
import store from "../../../../store/index";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { handleGraphQLErrors } from "../../../../utils/formatHelpers";
import { msgSuccess } from "../../../../utils/notifications";
import reduxWrapper from "../../../../utils/reduxWrapper";
import translate from "../../../../utils/translations/translate";
import { openConfirmDialog } from "../../actions";
import { GenericForm } from "../../components/GenericForm/index";
import { remediationModal as RemediationModal } from "../../components/RemediationModal/index";
import * as actions from "./actions";
import { renderFormFields } from "./formStructure";
import { APPROVE_ACCEPTATION } from "./queries";
import { IAcceptationApprovalAttrs } from "./types";

export interface IDescriptionViewProps {
  currentUserEmail: string;
  dataset: {
    acceptanceDate: string;
    acceptationApproval: string;
    actor: string;
    affectedSystems: string;
    analyst: string;
    attackVectorDesc: string;
    btsUrl: string;
    clientCode: string;
    clientProject: string;
    compromisedAttributes: string;
    compromisedRecords: string;
    cweUrl: string;
    description: string;
    recommendation: string;
    releaseDate: string;
    remediated: boolean;
    requirements: string;
    risk: string;
    scenario: string;
    severity?: string;
    state: string;
    subscription: string;
    tag?: string;
    threat: string;
    title: string;
    treatment: string;
    treatmentJustification: string;
    treatmentManager: string;
    type: string;
    userEmails: Array<{ email: string }>;
  };
  findingId: string;
  formValues: {
    treatment: string;
    treatmentVuln: string;
  };
  isEditing: boolean;
  isRemediationOpen: boolean;
  isTreatmentModal: boolean;
  projectName: string;
  userRole: string;
}

let remediationType: string = "request_verification";

const enhance: InferableComponentEnhancer<{}> =
  lifecycle({
    componentWillUnmount(): void { store.dispatch(actions.clearDescription()); },
    componentDidMount(): void {
      mixpanel.track(
        "FindingDescription",
        {
          Organization: (window as Window & { userOrganization: string }).userOrganization,
          User: (window as Window & { userName: string }).userName,
        });
      const { findingId, projectName, userRole } = this.props as IDescriptionViewProps;
      const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
        store.dispatch as ThunkDispatch<{}, {}, AnyAction>
      );

      thunkDispatch(actions.loadDescription(findingId, projectName, userRole));
    },
  });

const renderMarkVerifiedBtn: (() => JSX.Element) = (): JSX.Element => {
  const handleClick: (() => void) = (): void => { store.dispatch(openConfirmDialog("confirmVerify")); };

  return (
    <Button bsStyle="warning" onClick={handleClick}>
      <FluidIcon icon="verified" /> {translate.t("search_findings.tab_description.mark_verified")}
    </Button>
  );
};

const renderRequestVerifiyBtn: ((props: IDescriptionViewProps) => JSX.Element) =
  (props: IDescriptionViewProps): JSX.Element => {
    const handleClick: (() => void) = (): void => {
      remediationType = "request_verification";
      store.dispatch(actions.openRemediationMdl());
    };

    const canRequestVerification: boolean =
      props.dataset.state === "open"
      && _.includes(["CONTINUOUS", "continuous", "Continua", "Concurrente", "Si"], props.dataset.subscription)
      && !props.dataset.remediated;

    return (
      <Button
        bsStyle="success"
        disabled={!canRequestVerification}
        onClick={handleClick}
      >
        <FluidIcon icon="verified" /> {translate.t("search_findings.tab_description.request_verify")}
      </Button>
    );
  };

const renderApproveAcceptationBtn: (() => JSX.Element) = (): JSX.Element => {
  const handleClick: (() => void) = (): void => {
    remediationType = "approve_acceptation";
    store.dispatch(actions.openRemediationMdl());
  };

  return (
    <Button
      hidden={true}
      bsStyle="success"
      onClick={handleClick}
    >
      <FluidIcon icon="verified" /> Approve Acceptation
    </Button>
  );
};

const renderUpdateBtn: (() => JSX.Element) = (): JSX.Element => (
  <Button bsStyle="success" onClick={(): void => { store.dispatch(submit("editDescription")); }}>
    <FluidIcon icon="loading" /> {translate.t("search_findings.tab_description.update")}
  </Button>
);

const renderActionButtons: ((props: IDescriptionViewProps) => JSX.Element) =
  (props: IDescriptionViewProps): JSX.Element => (
    <React.Fragment>
      <ButtonToolbar className="pull-right">
        {_.includes(["customeradmin"], props.userRole) && props.dataset.acceptationApproval === "PENDING"
          ? renderApproveAcceptationBtn() : undefined}
        {_.includes(["admin", "analyst"], props.userRole) && props.dataset.remediated
          ? renderMarkVerifiedBtn() : undefined}
        {_.includes(["admin", "customer", "customeradmin"], props.userRole)
          ? renderRequestVerifiyBtn(props) : undefined}
        {props.isEditing ? renderUpdateBtn() : undefined}
        <Button bsStyle="primary" onClick={(): void => { store.dispatch(actions.editDescription()); }}>
          <FluidIcon icon="edit" /> {translate.t("search_findings.tab_description.editable")}
        </Button>
      </ButtonToolbar>
    </React.Fragment>
  );

const updateDescription: ((values: IDescriptionViewProps["dataset"], userRole: string, findingId: string) => void) =
  (values: IDescriptionViewProps["dataset"], userRole: string, findingId: string): void => {
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );

    if (_.includes(["admin", "analyst"], userRole)) {
      mixpanel.track(
        "UpdateFindingDescript",
        {
          Organization: (window as Window & { userOrganization: string }).userOrganization,
          User: (window as Window & { userName: string }).userName,
        });
      thunkDispatch(actions.updateDescription(findingId, values));
    } else {
      thunkDispatch(actions.updateTreatment(findingId, values));
    }
  };

const renderForm: ((props: IDescriptionViewProps) => JSX.Element) =
  (props: IDescriptionViewProps): JSX.Element => (
    <React.Fragment>
      <Col md={12} sm={12} xs={12}>
        <Row>{renderActionButtons(props)}</Row>
        <GenericForm
          name="editDescription"
          initialValues={props.dataset}
          onSubmit={(values: IDescriptionViewProps["dataset"]): void => {
            updateDescription(values, props.userRole, props.findingId);
          }}
        >
          {renderFormFields(props)}
        </GenericForm>
      </Col>
    </React.Fragment>
  );

export const component: ((props: IDescriptionViewProps) => JSX.Element) =
  (props: IDescriptionViewProps): JSX.Element => {

    const handleMtApproveAcceptation: ((mtResult: IAcceptationApprovalAttrs) => void) =
      (mtResult: IAcceptationApprovalAttrs): void => {
      if (!_.isUndefined(mtResult)) {
        if (mtResult.approveAcceptation.success) {
          mixpanel.track(
            "ApproveAcceptation",
            {
              Organization: (window as Window & { userOrganization: string }).userOrganization,
              User: (window as Window & { userName: string }).userName,
            });
          msgSuccess(
            translate.t("proj_alerts.verified_success"),
            translate.t("proj_alerts.updated_title"),
          );
        }
      }
    };

    return(
      <Mutation mutation={APPROVE_ACCEPTATION} onCompleted={handleMtApproveAcceptation}>
        { (approveAcceptation: MutationFn<IAcceptationApprovalAttrs, {
            findingId: string; observations: string; projectName: string; }>,
           mutationRes: MutationResult): React.ReactNode => {
          if (mutationRes.loading) {
            showPreloader();
          }
          if (!_.isUndefined(mutationRes.error)) {
            hidePreloader();
            handleGraphQLErrors("An error occurred approving acceptation", mutationRes.error);

            return <React.Fragment/>;
          }

          const handleApproveAcceptation: ((observations: string) => void) =
            (observations: string): void => {
            approveAcceptation({ variables: { findingId: props.findingId,
                                              observations,
                                              projectName: props.projectName }})
              .catch();
          };

          return(
            <React.StrictMode>
              <Row>
                <React.Fragment>
                  {renderForm(props)}
                  <RemediationModal
                    additionalInfo={
                      remediationType === "approve_acceptation" ?
                      `${props.dataset.compromisedRecords} vulnerabilities will be assumed`
                      : undefined
                    }
                    isOpen={props.isRemediationOpen}
                    message={
                      remediationType === "request_verification" ?
                      translate.t("search_findings.tab_description.remediation_modal.justification")
                      : translate.t("search_findings.tab_description.remediation_modal.observations")
                    }
                    onClose={(): void => { store.dispatch(actions.closeRemediationMdl()); }}
                    onSubmit={(values: { treatmentJustification: string }): void => {
                      const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
                        store.dispatch as ThunkDispatch<{}, {}, AnyAction>
                      );
                      if (remediationType === "request_verification") {
                        thunkDispatch(actions.requestVerification(props.findingId, values.treatmentJustification));
                      } else {
                        handleApproveAcceptation(values.treatmentJustification);
                      }
                    }}
                  />
                  <ConfirmDialog
                    name="confirmVerify"
                    title={translate.t("confirmmodal.title_generic")}
                    onProceed={(): void => {
                      const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
                        store.dispatch as ThunkDispatch<{}, {}, AnyAction>
                      );
                      thunkDispatch(actions.verifyFinding(props.findingId));
                    }}
                  />
                </React.Fragment>
              </Row>
            </React.StrictMode>
          );
        }}
      </Mutation>
    );
  };

const fieldSelector: ((state: {}, ...fields: string[]) => string) = formValueSelector("editDescription");
const fieldSelectorVuln: ((state: {}, ...fields: string[]) => string) = formValueSelector("editTreatmentVulnerability");

export const descriptionView: React.ComponentType<IDescriptionViewProps> = reduxWrapper(
  enhance(component) as React.FC<IDescriptionViewProps>,
  (state: StateType<Reducer>): IDescriptionViewProps => ({
    ...state.dashboard.description,
    formValues: {
      treatment: fieldSelector(state, "treatment"),
      treatmentVuln: fieldSelectorVuln(state, "treatment"),
    },
    isMdlConfirmOpen: state.dashboard.isMdlConfirmOpen,
  }),
);
