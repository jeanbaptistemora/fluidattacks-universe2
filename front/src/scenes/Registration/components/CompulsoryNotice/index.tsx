/* tslint:disable:jsx-no-lambda
 * JSX-NO-LAMBDA: Disabling this rule is necessary because it is not possible
 * to call functions with props as params from the JSX element definition
 * without using lambda expressions () => {}
 */
import { AxiosResponse } from "axios";
import React from "react";
import { Button, Checkbox } from "react-bootstrap";
import { Reducer } from "redux";
import { StateType } from "typesafe-actions";
import { default as Modal } from "../../../../components/Modal/index";
import store from "../../../../store/index";
import reduxWrapper from "../../../../utils/reduxWrapper";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import * as actions from "../../actions";
/**
 *  CompulsoryNotice properties
 */
interface ICompulsoryNoticeProps {
  id: string;
  open: boolean;
  rememberDecision: boolean;
  loadDashboard(): void;
}

const acceptLegal: ((arg1: ICompulsoryNoticeProps) => void) =
  (props: ICompulsoryNoticeProps): void => {
    let getLoginInfoQry: string;
    getLoginInfoQry = `{
      login{
        authorized
      }
    }`;
    new Xhr().request(getLoginInfoQry, "An error ocurred resolving user authorization")
    .then((authorizationResp: AxiosResponse) => {
      /* tslint:disable-next-line:no-any
       * Disabling here is necessary because TypeScript relies
       * on its JS base for functions like JSON.parse whose type is 'any'
       */
      const authorizedRespData: any = JSON.parse(JSON.stringify(authorizationResp.data)).data;
      if (authorizedRespData.login.authorized) {
        let acceptLegalQry: string;
        acceptLegalQry = `mutation {
          acceptLegal(remember:${props.rememberDecision}){
            success
          }
        }`;
        new Xhr().request(acceptLegalQry, "An error ocurred updating legal acceptance status")
        .then((acceptResponse: AxiosResponse) => {
          // tslint:disable-next-line:no-any
          const acceptRespData: any = JSON.parse(JSON.stringify(acceptResponse.data)).data;

          if (acceptRespData.acceptLegal.success) {
            props.loadDashboard();
          }
        })
        .catch((error: string) => {
          rollbar.error(error);
        });
      }
    })
    .catch((error: string) => {
      rollbar.error(error);
    });
};

const mapStateToProps: ((arg1: StateType<Reducer>) => ICompulsoryNoticeProps) =
  (state: StateType<Reducer>): ICompulsoryNoticeProps => ({
    ...state,
    open: state.registration.legalNotice.open,
    rememberDecision: state.registration.legalNotice.rememberDecision,
});

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
export const compulsoryNotice: React.StatelessComponent<ICompulsoryNoticeProps> = reduxWrapper
(
  component,
  mapStateToProps,
);
