/* tslint:disable:jsx-no-lambda
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 */
import React from "react";
import { Button, Checkbox } from "react-bootstrap";
import { AnyAction, Reducer } from "redux";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { default as Modal } from "../../../../components/Modal/index";
import store from "../../../../store/index";
import reduxWrapper from "../../../../utils/reduxWrapper";
import translate from "../../../../utils/translations/translate";
import * as actions from "../../actions";

/**
 *  CompulsoryNotice properties
 */
export interface ICompulsoryNoticeProps {
  id: string;
  open: boolean;
  rememberDecision: boolean;
  loadDashboard(): void;
}

const acceptLegal: ((arg1: ICompulsoryNoticeProps) => void) =
  (props: ICompulsoryNoticeProps): void => {
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );

    thunkDispatch(actions.acceptLegal(props));
};

const modalContent: ((arg1: ICompulsoryNoticeProps) => React.ReactNode) =
  (props: ICompulsoryNoticeProps): React.ReactNode => (
  <div>
    <p>{translate.t("legalNotice.description")}</p>
    <p title={translate.t("legalNotice.rememberCbo.tooltip")}>
      <Checkbox
        checked={props.rememberDecision}
        onClick={(): void => { store.dispatch(actions.checkRemember()); }}
      >
        {translate.t("legalNotice.rememberCbo.text")}
      </Checkbox>
    </p>
  </div>
);

const modalFooter: ((arg1: ICompulsoryNoticeProps) => React.ReactNode) =
  (props: ICompulsoryNoticeProps): React.ReactNode => (
  <Button
    bsStyle="primary"
    title={translate.t("legalNotice.acceptBtn.tooltip")}
    onClick={(): void => { acceptLegal(props); }}
  >
    {translate.t("legalNotice.acceptBtn.text")}
  </Button>
);

/**
 * CompulsoryNotice component
 */
export const component: React.StatelessComponent<ICompulsoryNoticeProps> =
  (props: ICompulsoryNoticeProps): JSX.Element => (
  <React.StrictMode>
    <Modal
      open={props.open}
      onClose={(): void => { acceptLegal(props); }}
      headerTitle={translate.t("legalNotice.title")}
      content={modalContent(props)}
      footer={modalFooter(props)}
    />
  </React.StrictMode>
);

/**
 * Export the Redux-wrapped component
 */
export const compulsoryNotice: React.SFC<ICompulsoryNoticeProps> = reduxWrapper
(
  component,
  (state: StateType<Reducer>): ICompulsoryNoticeProps => ({
    ...state.registration.legalNotice,
  }),
);
