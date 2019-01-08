import { AxiosError, AxiosResponse } from "axios";
import { Dispatch } from "redux";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import { ICommentStructure } from "./index";

export interface IActionStructure {
  payload: {} | undefined;
  type: string;
}

type ThunkDispatcher = Dispatch<IActionStructure> & ThunkDispatch<{}, {}, IActionStructure>;
/* tslint:disable-next-line:no-any
 * Disabling this rule is necessary because the args
 * of an async action may differ
 */
type ThunkActionStructure = ((...args: any[]) => ThunkAction<void, {}, {}, IActionStructure>);

export const loadComments: ThunkActionStructure =
  (
    projectName: string, callbackFn: ((comments: ICommentStructure[]) => void),
  ): ThunkAction<void, {}, {}, IActionStructure> => (_: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `{
        project(projectName: "${projectName}") {
          comments
        }
      }`;
    new Xhr().request(gQry, "An error occurred getting project comments")
      .then((response: AxiosResponse) => {
        const { data } = response.data;
        callbackFn(data.project.comments);
      })
      .catch((error: AxiosError) => {
        if (error.response !== undefined) {
          const { errors } = error.response.data;

          msgError(translate.t("proj_alerts.error_textsad"));
          rollbar.error(error.message, errors);
        }
      });
  };

export const postComment: ThunkActionStructure =
  (
    projectName: string, comment: ICommentStructure, callbackFn: ((comment: ICommentStructure) => void),
  ): ThunkAction<void, {}, {}, IActionStructure> => (_: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
      addProjectComment(
        content: "${comment.content.replace(/"/g, '\\"')}",
        projectName: "${projectName}",
        parent: "${comment.parent}"
      ) {
        success
        commentId
      }
    }`;
    new Xhr().request(gQry, "An error occurred getting adding a project comment")
      .then((response: AxiosResponse) => {
        const { data } = response.data;

        if (data.addProjectComment.success) {
          comment.id = data.addProjectComment.commentId;
          callbackFn(comment);
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
