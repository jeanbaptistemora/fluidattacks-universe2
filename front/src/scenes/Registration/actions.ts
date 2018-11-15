/* tslint:disable:no-any
 * Disabling this rule is necessary because the payload type may differ between
 * actions
 */
import { AxiosError, AxiosResponse } from "axios";
import { Action, AnyAction, Dispatch } from "redux";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError } from "../../utils/notifications";
import rollbar from "../../utils/rollbar";
import translate from "../../utils/translations/translate";
import Xhr from "../../utils/xhr";
import * as actionType from "./actionTypes";
import { ICompulsoryNoticeProps } from "./components/CompulsoryNotice";

export interface IActionStructure {
  payload: any;
  type: string;
}

type RegistrationAction = ((...args: any[]) => IActionStructure);
type ThunkDispatcher = Dispatch<Action> & ThunkDispatch<{}, {}, AnyAction>;
type ThunkActionStructure = ((...args: any[]) => ThunkAction<void, {}, {}, AnyAction>);

export const checkRemember: RegistrationAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.CHECK_REMEMBER,
});

export const acceptLegal: ThunkActionStructure =
  (
    props: ICompulsoryNoticeProps,
  ): ThunkAction<void, {}, {}, Action> => (_: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
      acceptLegal(remember:${props.rememberDecision}){
        success
      }
    }`;
    new Xhr().request(gQry, "An error ocurred updating legal acceptance status")
    .then((response: AxiosResponse) => {
      const { data } = response.data;

      if (data.acceptLegal.success) {
        props.loadDashboard();
      }
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(error.message, errors);
      }
    });
};
