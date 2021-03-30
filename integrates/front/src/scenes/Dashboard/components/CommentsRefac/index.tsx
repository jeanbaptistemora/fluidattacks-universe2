import { Comment } from "antd";
import { CommentEditor } from "./commentEditor";
import { translate } from "utils/translations/translate";
import type {
  ICommentStructure,
  ILoadCallback,
  IPostCallback,
} from "scenes/Dashboard/components/Comments/types";
import React, { useEffect, useState } from "react";

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
  const [comments, setComments] = useState<ICommentStructure[]>([]);

  const onMount: () => void = (): void => {
    onLoad((cData: ICommentStructure[]): void => {
      setComments(cData);
    });
  };
  useEffect(onMount, [onLoad]);

  return (
    <React.StrictMode>
      <CommentEditor onPostComment={onPostComment} />
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
