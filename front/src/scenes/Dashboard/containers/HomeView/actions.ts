import { AxiosError, AxiosResponse } from "axios";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import { IDashboardState } from "../../reducer";
import * as actionTypes from "./actionTypes";

export interface IActionStructure {
  payload?: { [key: string]: string | string[] };
  type: string;
}

export type ThunkDispatcher = ThunkDispatch<{}, undefined, IActionStructure>;

type ThunkResult<T> = ThunkAction<T, {}, undefined, IActionStructure>;

export const loadProjects: (() => ThunkResult<void>) = (): ThunkResult<void> =>
  (dispatch: ThunkDispatcher): void => {
    let gQry: string; gQry = `{
      me {
        projects {
          name
          description
        }
      }
    }`;

    new Xhr().request(gQry, "An error occurred getting project list")
      .then((response: AxiosResponse) => {
        const { data } = response.data;

        dispatch({
          payload: {
            projects: data.me.projects.map((project: { name: string }) => ({
              ...project, name: project.name.toUpperCase(),
            })),
          },
          type: actionTypes.LOAD_PROJECTS,
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

export const changeProjectsDisplay: ((value: IDashboardState["user"]["displayPreference"]) => IActionStructure) =
  (value: IDashboardState["user"]["displayPreference"]): IActionStructure => ({
    payload: { value },
    type: actionTypes.CHANGE_PROJECTS_DISPLAY,
  });
