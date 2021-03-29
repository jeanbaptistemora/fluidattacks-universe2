import { Comment } from "antd";
import type { ICommentStructure } from "scenes/Dashboard/components/Comments/types";
import React from "react";

interface ICommentsRefacProps {
  comments: ICommentStructure[];
}

const CommentsRefac: React.FC<ICommentsRefacProps> = (
  props: ICommentsRefacProps
): JSX.Element => {
  const { comments } = props;

  return (
    <React.StrictMode>
      {comments.map(
        (comment: ICommentStructure): JSX.Element => (
          <Comment
            actions={[<span key={"comment-nested-reply"}>{"Reply"}</span>]}
            author={comment.fullname}
            content={comment.content}
            key={comment.id}
          />
        )
      )}
    </React.StrictMode>
  );
};

export { CommentsRefac, ICommentsRefacProps };
