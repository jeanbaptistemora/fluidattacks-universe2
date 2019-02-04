/* tslint:disable jsx-no-lambda number-literal-format jsx-no-multiline-js
 * JSX-NO-LAMBDA: Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 *
 * JSX-NO-MULTILINE-JS: necessary for the sake of readability of the code that dynamically renders fields
 * as input or <p> depending on their state
 */

import _ from "lodash";
import React from "react";
import { Button, Col, Glyphicon, Row } from "react-bootstrap";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { AnyAction, Reducer } from "redux";
import { formValueSelector, submit } from "redux-form";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { confirmDialog as ConfirmDialog } from "../../../../components/ConfirmDialog";
import store from "../../../../store/index";
import reduxWrapper from "../../../../utils/reduxWrapper";
import translate from "../../../../utils/translations/translate";
import { GenericForm } from "../../components/GenericForm/index";
import { remediationModal as RemediationModal } from "../../components/RemediationModal/index";
import * as actions from "./actions";
import { getFormStructure } from "./formStructure";

export interface IDescriptionViewProps {
  dataset: {
    actor: string;
    affectedSystems: string;
    attackVector: string;
    btsUrl: string;
    compromisedAttributes: string;
    compromisedRecords: string;
    cweUrl: string;
    description: string;
    kbUrl: string;
    recommendation: string;
    releaseDate: string;
    remediated: boolean;
    reportLevel: string;
    requirements: string;
    scenario: string;
    state: string;
    subscription: string;
    threat: string;
    title: string;
    treatment: string;
    treatmentJustification: string;
    treatmentManager: string;
    userEmails: Array<{ email: string }>;
  };
  findingId: string;
  formValues: { treatment: string };
  isEditing: boolean;
  isMdlConfirmOpen: boolean;
  isRemediationOpen: boolean;
  projectName: string;
  userRole: string;
}

const enhance: InferableComponentEnhancer<{}> =
  lifecycle({
    componentWillUnmount(): void { store.dispatch(actions.clearDescription()); },
    componentDidMount(): void {
      const { findingId, projectName, userRole } = this.props as IDescriptionViewProps;
      const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
        store.dispatch as ThunkDispatch<{}, {}, AnyAction>
      );

      thunkDispatch(actions.loadDescription(findingId, projectName, userRole));
    },
  });

const renderMarkVerifiedBtn: (() => JSX.Element) = (): JSX.Element => (
  <Row style={{ paddingTop: "10px" }}>
    <Col md={2} mdOffset={10} xs={6} sm={6}>
      <Button bsStyle="warning" block={true} onClick={(): void => { store.dispatch(actions.openConfirmMdl()); }}>
        <Glyphicon glyph="ok" /> {translate.t("search_findings.tab_description.mark_verified")}
      </Button>
    </Col>
  </Row>
);

const renderRequestVerifiyBtn: ((props: IDescriptionViewProps) => JSX.Element) =
  (props: IDescriptionViewProps): JSX.Element => {
    const canRequestVerification: boolean =
      props.dataset.state === "Abierto"
      && _.includes(["continuous", "Continua", "Concurrente", "Si"], props.dataset.subscription)
      && props.dataset.treatment !== "Asumido";

    return (
      <Row style={{ paddingTop: "10px" }}>
        <Col md={2} mdOffset={10} xs={6} sm={6}>
          <Button
            bsStyle="success"
            block={true}
            disabled={!canRequestVerification}
            onClick={(): void => { store.dispatch(actions.openRemediationMdl()); }}
          >
            <Glyphicon glyph="ok" /> {translate.t("search_findings.tab_description.request_verify")}
          </Button>
        </Col>
      </Row>
    );
  };

const renderUpdateBtn: (() => JSX.Element) = (): JSX.Element => (
  <Button bsStyle="success" block={true} onClick={(): void => { store.dispatch(submit("editDescription")); }}>
    <Glyphicon glyph="repeat" /> {translate.t("search_findings.tab_description.update")}
  </Button>
);

const renderEditBtn: (() => JSX.Element) = (): JSX.Element => (
  <Col md={2} xs={6} sm={6}>
    <Button bsStyle="primary" block={true} onClick={(): void => { store.dispatch(actions.editDescription()); }}>
      <Glyphicon glyph="edit" /> {translate.t("search_findings.tab_description.editable")}
    </Button>
  </Col>
);

const renderActionButtons: ((props: IDescriptionViewProps) => JSX.Element) =
  (props: IDescriptionViewProps): JSX.Element => (
    <React.Fragment>
      <Col md={12} sm={12} xs={12}>
        <Row style={{ paddingTop: "10px" }}>
          <Col md={2} mdOffset={8} xs={6} sm={6}>
            {_.includes(["admin", "analyst"], props.userRole) && props.isEditing ? renderUpdateBtn() : undefined}
          </Col>
          {renderEditBtn()}
        </Row>
        {_.includes(["admin", "analyst"], props.userRole) && props.dataset.remediated
          ? renderMarkVerifiedBtn() : undefined}
        {_.includes(["admin", "customer"], props.userRole) ? renderRequestVerifiyBtn(props) : undefined}
      </Col>
    </React.Fragment>
  );

const updateDescription: ((values: IDescriptionViewProps["dataset"], userRole: string, findingId: string) => void) =
  (values: IDescriptionViewProps["dataset"], userRole: string, findingId: string): void => {
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );

    if (_.includes(["admin", "analyst"], userRole)) {
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
          form="editDescription"
          formStructure={getFormStructure(props)}
          initialValues={props.dataset}
          onSubmit={(values: {}): void => {
            updateDescription(values as IDescriptionViewProps["dataset"], props.userRole, props.findingId);
          }}
        />
        <Row style={{ paddingTop: "10px" }}>
          {props.isEditing && _.includes(["customer", "customeradmin"], props.userRole) ? renderUpdateBtn() : undefined}
        </Row>
      </Col>
    </React.Fragment>
  );

export const component: React.SFC<IDescriptionViewProps> =
  (props: IDescriptionViewProps): JSX.Element => (
    <React.StrictMode>
      <Row>
        <React.Fragment>
          {renderForm(props)}
          <RemediationModal
            isOpen={props.isRemediationOpen}
            onClose={(): void => { store.dispatch(actions.closeRemediationMdl()); }}
            onSubmit={(values: { treatmentJustification: string }): void => {
              const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
                store.dispatch as ThunkDispatch<{}, {}, AnyAction>
              );
              thunkDispatch(actions.requestVerification(props.findingId, values.treatmentJustification));
            }}
          />
          <ConfirmDialog
            open={props.isMdlConfirmOpen}
            title={translate.t("confirmmodal.title_generic")}
            onProceed={(): void => {
              const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
                store.dispatch as ThunkDispatch<{}, {}, AnyAction>
              );
              thunkDispatch(actions.verifyFinding(props.findingId));
            }}
            onCancel={(): void => { store.dispatch(actions.closeConfirmMdl()); }}
          />
        </React.Fragment>
      </Row>
    </React.StrictMode>
  );

const fieldSelector: ((state: {}, ...fields: string[]) => string) = formValueSelector("editDescription");

export const descriptionView: React.ComponentType<IDescriptionViewProps> = reduxWrapper(
  enhance(component) as React.SFC<IDescriptionViewProps>,
  (state: StateType<Reducer>): IDescriptionViewProps => ({
    ...state.dashboard.description,
    formValues: { treatment: fieldSelector(state, "treatment") },
    isMdlConfirmOpen: state.dashboard.isMdlConfirmOpen,
  }),
);
