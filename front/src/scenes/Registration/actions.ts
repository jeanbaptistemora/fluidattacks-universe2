/* tslint:disable:no-any
 * Disabling this rule is necessary because the payload type may differ between
 * actions
 */
import { AxiosError, AxiosResponse } from "axios";
import _ from "lodash";
import { Action, AnyAction, Dispatch } from "redux";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError } from "../../utils/notifications";
import rollbar from "../../utils/rollbar";
import translate from "../../utils/translations/translate";
import Xhr from "../../utils/xhr";
import * as actionType from "./actionTypes";

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

export const loadDashboard: (() => void) = (): void => {
  let initialUrl: string | null = localStorage.getItem("url_inicio");
  initialUrl = _.isEmpty(initialUrl) ? "!/home" : initialUrl;

  localStorage.removeItem("url_inicio");
  location.assign(`/integrates/dashboard#${initialUrl}`);
};

export const acceptLegal: ThunkActionStructure =
  (rememberValue: boolean): ThunkAction<void, {}, {}, Action> => (_0: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
      acceptLegal(remember:${rememberValue}){
        success
      }
    }`;
    new Xhr().request(gQry, "An error ocurred updating legal acceptance status")
    .then((response: AxiosResponse) => {
      const { data } = response.data;

      if (data.acceptLegal.success) {
        loadDashboard();
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

export const loadAuthorization: ThunkActionStructure =
  (): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
    let gQry: string; gQry = `{
      me {
        authorized
        remember
      }
    }`;
    new Xhr().request(gQry, "An error ocurred resolving user authorization")
      .then((response: AxiosResponse) => {
        const { data } = response.data;

        dispatch<IActionStructure>({
          payload: {
            isAuthorized: data.me.authorized,
            isRememberEnabled: data.me.remember,
          },
          type: actionType.LOAD_AUTHORIZATION,
        });

        if (data.me.remember) {
          loadDashboard();
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
