import _ from "lodash";
import type { FC } from "react";
import React, { StrictMode, useCallback, useContext } from "react";
import { useTranslation } from "react-i18next";
import Linkify from "react-linkify";
import styled from "styled-components";

import { Button } from "components/Button";
import { Card } from "components/Card";
import { ExternalLink } from "components/ExternalLink";
import { Text } from "components/Text";
import { CommentEditor } from "scenes/Dashboard/components/Comments/components/CommentEditor";
import { commentContext } from "scenes/Dashboard/components/Comments/context";
import type {
  ICommentContext,
  ICommentStructure,
} from "scenes/Dashboard/components/Comments/types";

interface ICommentProps {
  id: number;
  comments: ICommentStructure[];
  onPost: (editorText: string) => void;
  backgroundEnabled: boolean;
  orderBy: string;
}

const CommentChildren = styled.div`
  border-left: 2px solid #8f8fa3;
  margin: 6px 0;
  padding-left: 32px;
`;

const CommentContent = styled.pre`
  font-family: "Roboto", sans-serif;
  white-space: pre-wrap;
`;

const Comment: FC<ICommentProps> = ({
  id,
  comments,
  onPost,
  backgroundEnabled,
  orderBy,
}: ICommentProps): JSX.Element => {
  const { t } = useTranslation();
  const { replying, setReplying }: ICommentContext = useContext(commentContext);

  const rootComment: ICommentStructure = _.find(comments, [
    "id",
    id,
  ]) as ICommentStructure;
  const childrenComments: ICommentStructure[] = _.filter(comments, [
    "parentComment",
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
        <ExternalLink href={href} key={key}>
          {text}
        </ExternalLink>
      );
    },
    []
  );

  return (
    <StrictMode>
      <div className={"comment"}>
        <Card>
          <div className={"flex justify-between mb2"}>
            <Text disp={"inline-block"} fw={7} size={"small"}>
              {rootComment.createdByCurrentUser ? `You` : rootComment.fullName}
            </Text>
            <Text disp={"inline-block"} size={"small"}>
              {rootComment.created}
            </Text>
          </div>
          <Text mb={2}>
            <Linkify componentDecorator={formatLinks}>
              <CommentContent>{_.trim(rootComment.content)}</CommentContent>
            </Linkify>
          </Text>
          <Button onClick={replyHandler} variant={"primary"}>
            {t("comments.reply")}
          </Button>
          {replying === rootComment.id && (
            <div className={"mt2"}>
              <CommentEditor id={id} onPost={onPost} />
            </div>
          )}
        </Card>
        <CommentChildren>
          {childrenComments.length > 0
            ? orderComments(childrenComments, orderBy).map(
                (childComment: ICommentStructure): JSX.Element => (
                  <Comment
                    backgroundEnabled={!backgroundEnabled}
                    comments={comments}
                    id={childComment.id}
                    key={childComment.id}
                    onPost={onPost}
                    orderBy={orderBy}
                  />
                )
              )
            : undefined}
        </CommentChildren>
      </div>
    </StrictMode>
  );
};

export type { ICommentProps };
export { Comment };
