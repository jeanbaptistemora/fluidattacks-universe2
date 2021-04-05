import { Comment } from "antd";
import moment from "moment";
import React, { useCallback, useContext, useEffect, useState } from "react";

import { CommentEditor } from "./commentEditor";

import type {
  ICommentStructure,
  ILoadCallback,
  IPostCallback,
} from "scenes/Dashboard/components/Comments/types";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { translate } from "utils/translations/translate";

interface ICommentsRefacProps {
  onLoad: (callbackFn: ILoadCallback) => void;
  onPostComment: (
    comment: ICommentStructure,
    callbackFn: IPostCallback
  ) => void;
}

const CommentsRefac: React.FC<ICommentsRefacProps> = (
  props: ICommentsRefacProps
): JSX.Element => {
  const { onLoad, onPostComment } = props;
  const { userEmail, userName }: IAuthContext = useContext(authContext);
  const [comments, setComments] = useState<ICommentStructure[]>([]);

  const onMount: () => void = (): void => {
    onLoad((cData: ICommentStructure[]): void => {
      setComments(cData);
    });
  };
  useEffect(onMount, [onLoad]);

  const getFormattedTime = (): string => {
    const now = new Date();

    return moment(now).format("YYYY/MM/DD HH:mm:ss");
  };

  const clickHandler = useCallback(
    (editorText: string): void => {
      onPostComment(
        {
          content: editorText,
          created: getFormattedTime(),
          // eslint-disable-next-line camelcase  -- Name required by the API
          created_by_current_user: true,
          email: userEmail,
          fullname: userName,
          id: 0,
          modified: getFormattedTime(),
          parent: Number("0"),
        },
        (result: ICommentStructure): void => {
          setComments([...comments, result]);
        }
      );
    },
    [comments, onPostComment, userEmail, userName]
  );

  return (
    <React.StrictMode>
      <CommentEditor onPost={clickHandler} />
      {comments.length > 0
        ? comments.map(
            (comment: ICommentStructure): JSX.Element => (
              <React.Fragment key={comment.id}>
                <hr />
                <Comment
                  actions={[
                    <span key={"comment-nested-reply"}>
                      {translate.t("comments.reply")}
                    </span>,
                  ]}
                  author={comment.fullname}
                  content={comment.content}
                  datetime={comment.created}
                  key={comment.id}
                />
              </React.Fragment>
            )
          )
        : translate.t("comments.noComments")}
    </React.StrictMode>
  );
};

export { CommentsRefac, ICommentsRefacProps };
