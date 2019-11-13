import { AxiosError, AxiosResponse } from "axios";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import { ICommentStructure } from "../../components/Comments";
import { loadCallback, postCallback } from "./index";

export const loadComments: ((findingId: string, type: string, callbackFn: loadCallback) => void) = (
  findingId: string, type: string, callbackFn: loadCallback,
): void => {
    let gQry: string;
    gQry = `{
      finding(identifier: "${findingId}"){
        ${type} {
          id
          content
          created
          email
          fullname
          modified
          parent
        }
      }
    }`;
    new Xhr().request(gQry, `An error occurred getting finding ${type}s`)
      .then((response: AxiosResponse) => {
        const { data } = response.data;
        let comments: ICommentStructure[] = type === "comments"
          ? data.finding.comments
          : data.finding.observations;
        comments = comments.map((comment: ICommentStructure): ICommentStructure => ({
          ...comment,
          created_by_current_user: comment.email === (window as typeof window & { userEmail: string }).userEmail,
          id: Number(comment.id),
          parent: Number(comment.parent),
        }));

        callbackFn(comments);
      })
      .catch((error: AxiosError) => {
        if (error.response !== undefined) {
          const { errors } = error.response.data;

          msgError(translate.t("proj_alerts.error_textsad"));
          rollbar.error(error.message, errors);
        }
      });
};

export const postComment: ((
  findingId: string, type: string, comment: ICommentStructure, callbackFn: postCallback) => void
) = (findingId: string, type: string, comment: ICommentStructure, callbackFn: postCallback): void => {
    let gQry: string;
    gQry = `mutation {
      addFindingComment(
        content: ${JSON.stringify(comment.content)},
        findingId: "${findingId}",
        type: "${type.slice(0, -1)}",
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
