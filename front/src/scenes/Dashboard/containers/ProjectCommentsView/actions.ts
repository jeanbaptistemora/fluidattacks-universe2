import { AxiosError, AxiosResponse } from "axios";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import Xhr from "../../../../utils/xhr";
import { ICommentStructure } from "../../components/Comments";
import { loadCallback, postCallback } from "./index";

export const loadComments: ((projectName: string, callbackFn: loadCallback) => void) = (
  projectName: string, callbackFn: loadCallback,
): void => {
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

export const postComment: ((projectName: string, comment: ICommentStructure, callbackFn: postCallback) => void) = (
  projectName: string, comment: ICommentStructure, callbackFn: postCallback,
): void => {
    let gQry: string;
    gQry = `mutation {
      addProjectComment(
        content: ${JSON.stringify(comment.content)},
        projectName: "${projectName}",
        parent: "${comment.parent}"
      ) {
        success
        commentId
      }
    }`;
    new Xhr().request(gQry, "An error occurred adding a project comment")
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
