import { AxiosError, AxiosResponse } from "axios";
import { Action, AnyAction, Dispatch } from "redux";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import * as actionTypes from "./actionTypes";
import { IEventsViewProps } from "./index";

export interface IActionStructure {
  /* tslint:disable-next-line:no-any
   * Disabling this rule is necessary because the payload
   * type may differ between actions
   */
  payload: any;
  type: string;
}

type ThunkDispatcher = Dispatch<Action> & ThunkDispatch<{}, {}, AnyAction>;
/* tslint:disable-next-line:no-any
 * Disabling this rule is necessary because args of an async action may differ
 */
type ThunkActionStructure = ((...args: any[]) => ThunkAction<void, {}, {}, AnyAction>);

export const loadEvents: ThunkActionStructure =
  (projectName: IEventsViewProps["projectName"]): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `{
        events (projectName: "${projectName}") {
          eventDate,
          detail,
          id,
          projectName,
          eventStatus,
          eventType
        }
    }`;
      new Xhr().request(gQry, "An error occurred getting eventualities")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          dispatch({
            payload: {
              events: data.events,
            },
            type: actionTypes.LOAD_EVENTS,
          });
        })
        .catch((error: AxiosError) => {
          if (error.response !== undefined) {
            const { errors } = error.response.data;
            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error(error.message, errors);
          }
        });
    };
