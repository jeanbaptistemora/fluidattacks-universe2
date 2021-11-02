import { Comment } from "antd";
import _ from "lodash";
import React, { useCallback, useContext } from "react";
import Linkify from "react-linkify";

import { CommentEditor } from "scenes/Dashboard/components/Comments/components/CommentEditor";
import { commentContext } from "scenes/Dashboard/components/Comments/context";
import type {
  ICommentContext,
  ICommentStructure,
} from "scenes/Dashboard/components/Comments/types";
import "scenes/Dashboard/components/Comments/index.css";
import { translate } from "utils/translations/translate";

interface INestedCommentProps {
  id: number;
  comments: ICommentStructure[];
  onPost: (editorText: string) => void;
  backgroundEnabled: boolean;
  orderBy: string;
}

const NestedComment: React.FC<INestedCommentProps> = (
  props: INestedCommentProps
): JSX.Element => {
  const { id, comments, onPost, backgroundEnabled, orderBy } = props;
  const { replying, setReplying }: ICommentContext = useContext(commentContext);

  const rootComment: ICommentStructure = _.find(comments, [
    "id",
    id,
  ]) as ICommentStructure;
  const childrenComments: ICommentStructure[] = _.filter(comments, [
    "parent",
    id,
  ]);

  const orderComments = (
    unordered: ICommentStructure[],
    order: string
  ): ICommentStructure[] => {
    return order === "oldest"
      ? _.orderBy(unordered, ["created"], ["asc"])
      : _.orderBy(unordered, ["created"], ["desc"]);
  };

  const replyHandler = useCallback((): void => {
    if (!_.isUndefined(setReplying)) {
      if (replying === id) {
        setReplying(0);
      } else {
        setReplying(id);
      }
    }
  }, [id, replying, setReplying]);

  const formatLinks = useCallback(
    (href: string, text: string, key: number): React.ReactNode => {
      return (
        <a href={href} key={key} rel={"noopener noreferrer"} target={"_blank"}>
          {text}
        </a>
      );
    },
    []
  );

  return (
    <React.StrictMode>
      <div className={"comment-nested comment-no-bullets"}>
        <Comment
          actions={[
            <button
              className={"comment-reply"}
              key={"comment-reply"}
              onClick={replyHandler}
            >
              {translate.t("comments.reply")}
            </button>,
          ]}
          author={
            <span className={"comment-author"}>
              {rootComment.createdByCurrentUser
                ? `You (${rootComment.fullName})`
                : rootComment.fullName}
            </span>
          }
          content={
            <div className={"comment-content"}>
              {
                <Linkify componentDecorator={formatLinks}>
                  {_.trim(rootComment.content)}
                </Linkify>
              }
            </div>
          }
          datetime={
            <span className={"comment-datetime"}>{rootComment.created}</span>
          }
          key={rootComment.id}
        >
          {replying === rootComment.id && (
            <div className={"pa3"}>
              <CommentEditor id={id} onPost={onPost} />
            </div>
          )}
          <hr className={"bt bw1 pa0 mv0"} />
          {childrenComments.length > 0 &&
            orderComments(childrenComments, orderBy).map(
              (childComment: ICommentStructure): JSX.Element => (
                <React.Fragment key={childComment.id}>
                  <div className={"pl5"}>
                    <NestedComment
                      backgroundEnabled={!backgroundEnabled}
                      comments={comments}
                      id={childComment.id}
                      onPost={onPost}
                      orderBy={orderBy}
                    />
                  </div>
                </React.Fragment>
              )
            )}
        </Comment>
      </div>
    </React.StrictMode>
  );
};

export { NestedComment, INestedCommentProps };
