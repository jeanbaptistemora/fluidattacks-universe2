import { AxiosError, AxiosResponse } from "axios";
import { Dispatch } from "redux";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import { ICommentStructure } from "../../components/Comments";
import { ICommentsViewProps } from "./index";

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
    findingId: string,
    type: ICommentsViewProps["type"],
    callbackFn: ((comments: ICommentStructure[]) => void),
  ): ThunkAction<void, {}, {}, IActionStructure> => (_: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `{
      finding(identifier: "${findingId}"){
        ${type}s
      }
    }`;
    new Xhr().request(gQry, `An error occurred getting finding ${type}s`)
      .then((response: AxiosResponse) => {
        const { data } = response.data;

        callbackFn(type === "comment"
          ? data.finding.comments
          : data.finding.observations);
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
    findingId: string,
    type: ICommentsViewProps["type"],
    comment: ICommentStructure, callbackFn: ((comment: ICommentStructure) => void),
  ): ThunkAction<void, {}, {}, IActionStructure> => (_: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
      addFindingComment(
        content: ${JSON.stringify(comment.content)},
        findingId: "${findingId}",
        type: "${type}",
        parent: "${comment.parent}"
      ) {
        success
        commentId
      }
    }`;
    new Xhr().request(gQry, `An error occurred adding a finding ${type}`)
      .then((response: AxiosResponse) => {
        const { data } = response.data;

        if (data.addFindingComment.success) {
          comment.id = data.addFindingComment.commentId;
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
