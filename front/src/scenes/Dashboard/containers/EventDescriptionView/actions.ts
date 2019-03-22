import { AxiosError, AxiosResponse } from "axios";
import { Action, Dispatch } from "redux";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import * as actionTypes from "./actionTypes";
import { IEventDescriptionViewProps } from "./index";

export interface IActionStructure {
  /* tslint:disable-next-line:no-any
   * Disabling this rule is necessary because the payload
   * type may differ between actions
   */
  payload: any;
  type: string;
}

type ThunkDispatcher = Dispatch<IActionStructure> & ThunkDispatch<{}, {}, IActionStructure>;
/* tslint:disable-next-line:no-any
 * Disabling this rule is necessary because args of an async action may differ
 */
type ThunkActionStructure = ((...args: any[]) => ThunkAction<void, {}, {}, IActionStructure>);

export const editEvent: (() => IActionStructure) =
  (): IActionStructure => ({
    payload: undefined,
    type: actionTypes.CHANGE_EVENT_EDITABLE,
  });

export const loadEvent: ThunkActionStructure =
  (eventId: IEventDescriptionViewProps["eventId"]): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `{
           event (identifier: "${eventId}") {
             accessibility,
             affectation,
             affectedComponents,
             analyst,
             client,
             clientProject,
             eventDate,
             detail,
             evidence,
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
              event: data.event,
            },
            type: actionTypes.LOAD_EVENT,
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

export const updateEvent: ThunkActionStructure =
  (values: IEventDescriptionViewProps["eventData"]): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
      let gQry: string;
      gQry = `mutation {
        updateEvent(eventId: "${values.id}", affectation: "${values.affectation}"){
          success
          event {
            accessibility,
            affectation,
            affectedComponents,
            analyst,
            client,
            clientProject,
            eventDate,
            detail,
            evidence,
            id,
            projectName,
            eventStatus,
            eventType
          }
        }
      }`;
      new Xhr().request(gQry, "An error occurred updating event")
        .then((response: AxiosResponse) => {
          const { data } = response.data;
          if (data.updateEvent.success) {
            dispatch({
              payload: {
              event: data.updateEvent.event,
              },
              type: actionTypes.LOAD_EVENT,
            });
            dispatch(editEvent());
            msgSuccess(
              translate.t("proj_alerts.updated"),
              translate.t("proj_alerts.updated_title"),
            );
          } else {
            msgError(translate.t("proj_alerts.error_textsad"));
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
