import { Comment } from "antd";
import _ from "lodash";
import React, { useCallback, useContext } from "react";

import type { ICommentStructure } from "scenes/Dashboard/components/Comments/types";
import { CommentEditor } from "scenes/Dashboard/components/CommentsRefac/commentEditor";
import type { ICommentContext } from "scenes/Dashboard/components/CommentsRefac/index";
import { commentContext } from "scenes/Dashboard/components/CommentsRefac/index";
import "scenes/Dashboard/components/CommentsRefac/index.css";
import { translate } from "utils/translations/translate";

interface INestedCommentProps {
  id: number;
  comments: ICommentStructure[];
  onPost: (editorText: string) => void;
}

const NestedComment: React.FC<INestedCommentProps> = (
  props: INestedCommentProps
): JSX.Element => {
  const { id, comments, onPost } = props;
  const { replying, setReplying }: ICommentContext = useContext(commentContext);

  const rootComment: ICommentStructure = _.find(comments, [
    "id",
    id,
  ]) as ICommentStructure;
  const childrenComments: ICommentStructure[] = _.filter(comments, [
    "parent",
    id,
  ]);

  const replyHandler = useCallback((): void => {
    if (!_.isUndefined(setReplying)) {
      if (replying === id) {
        setReplying(0);
      } else {
        setReplying(id);
      }
    }
  }, [id, replying, setReplying]);

  return (
    <React.StrictMode>
      <div className={"comment-nested"}>
        <Comment
          actions={[
            <button key={"comment-nested-reply"} onClick={replyHandler}>
              {translate.t("comments.reply")}
            </button>,
          ]}
          author={
            rootComment.created_by_current_user
              ? `You (${rootComment.fullname})`
              : rootComment.fullname
          }
          content={<p>{rootComment.content}</p>}
          datetime={rootComment.created}
          key={rootComment.id}
        >
          {replying === rootComment.id && <CommentEditor onPost={onPost} />}
          {childrenComments.length > 0 &&
            childrenComments.map(
              (childComment: ICommentStructure): JSX.Element => (
                <React.Fragment key={childComment.id}>
                  <NestedComment
                    comments={comments}
                    id={childComment.id}
                    onPost={onPost}
                  />
                </React.Fragment>
              )
            )}
        </Comment>
      </div>
    </React.StrictMode>
  );
};

export { NestedComment, INestedCommentProps };
