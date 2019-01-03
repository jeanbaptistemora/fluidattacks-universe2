/* tslint:disable:no-any
 * Disabling this rule is necessary because the payload type may differ between
 * actions
 */
import { AxiosError, AxiosResponse } from "axios";
import { default as lodash } from "lodash";
import { Action, AnyAction, Dispatch } from "redux";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { getEnvironment, PRODUCTION_URL } from "../../utils/context";
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

export const loadDashboard: (() => void) = (): void => {
  let initialUrl: string | null = localStorage.getItem("url_inicio");
  initialUrl = lodash.isNil(initialUrl) ? "" : initialUrl;

  localStorage.removeItem("url_inicio");
  location.assign(
    getEnvironment() === "production"
      ? `${PRODUCTION_URL}/integrates/dashboard#${initialUrl}`
      : `dashboard#${initialUrl}`,
  );
};

export const loadAuthorization: ThunkActionStructure =
  (): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
    let gQry: string; gQry = `{
      login {
        authorized
        remember
      }
    }`;
    new Xhr().request(gQry, "An error ocurred resolving user authorization")
      .then((response: AxiosResponse) => {
        const { data } = response.data;

        dispatch<IActionStructure>({
          payload: {
            isAuthorized: data.login.authorized,
            isRememberEnabled: data.login.remember,
          },
          type: actionType.LOAD_AUTHORIZATION,
        });

        if (data.login.remember) {
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
