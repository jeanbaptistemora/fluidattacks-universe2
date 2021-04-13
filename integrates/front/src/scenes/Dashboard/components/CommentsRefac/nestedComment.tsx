import { Comment } from "antd";
import _ from "lodash";
import React, { useCallback, useContext } from "react";

import { CommentEditor } from "./commentEditor";

import type { ICommentStructure } from "scenes/Dashboard/components/Comments/types";
import type { ICommentContext } from "scenes/Dashboard/components/CommentsRefac/index";
import { commentContext } from "scenes/Dashboard/components/CommentsRefac/index";
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
      <div style={{ borderStyle: "solid", margin: "10px", padding: "10px" }}>
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
          content={rootComment.content}
          datetime={rootComment.created}
          key={rootComment.id}
        >
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
          {replying === rootComment.id && <CommentEditor onPost={onPost} />}
        </Comment>
      </div>
    </React.StrictMode>
  );
};

export { NestedComment, INestedCommentProps };
