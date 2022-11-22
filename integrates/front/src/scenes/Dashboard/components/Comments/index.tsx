/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";
import React, { useCallback, useContext, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { Comment } from "./Comment";
import { CommentEditor } from "./components/CommentEditor";
import { commentContext } from "./context";

import type {
  ICommentStructure,
  ICommentsProps,
} from "scenes/Dashboard/components/Comments/types";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import style from "utils/forms/index.css";

const Select: StyledComponent<
  "select",
  Record<string, unknown>
> = styled.select.attrs({
  className: `${style["form-control"]} black-60 border-box`,
})``;

const Small: StyledComponent<
  "small",
  Record<string, unknown>
> = styled.small.attrs({
  className: "f5 black-60 db",
})``;

export const Comments: React.FC<ICommentsProps> = ({
  onLoad,
  onPostComment,
}: ICommentsProps): JSX.Element => {
  const { t } = useTranslation();
  const { userEmail, userName }: IAuthContext = useContext(authContext);
  const [comments, setComments] = useState<ICommentStructure[]>([]);
  const [replying, setReplying] = useState<number>(0);
  const [orderBy, setOrderBy] = useState<string>("newest");

  const onMount: () => void = (): void => {
    onLoad((cData: ICommentStructure[]): void => {
      setComments(cData);
    });
  };
  useEffect(onMount, [onLoad]);

  const getFormattedTime = (): string => {
    const now = new Date();

    return `${now.toLocaleString("default", {
      year: "numeric",
    })}/${now.toLocaleString("default", {
      month: "2-digit",
    })}/${now.toLocaleString("default", {
      day: "2-digit",
    })} ${now.toLocaleString("default", {
      hour: "2-digit",
      hour12: false,
    })}:${now.toLocaleString("default", {
      minute: "2-digit",
    })}:${now.toLocaleString("default", { second: "2-digit" })}`;
  };

  const postHandler = useCallback(
    (editorText: string): void => {
      onPostComment(
        {
          content: editorText,
          created: getFormattedTime(),
          createdByCurrentUser: true,
          email: userEmail,
          fullName: userName,
          id: 0,
          modified: getFormattedTime(),
          parentComment: replying,
        },
        (result: ICommentStructure): void => {
          setComments([...comments, result]);
          setReplying(0);
        }
      );
    },
    [comments, onPostComment, replying, userEmail, userName]
  );

  const onOrderChange = useCallback(
    (event: React.ChangeEvent<HTMLSelectElement>): void => {
      setOrderBy(event.target.value);
    },
    []
  );

  const rootComments: ICommentStructure[] = _.filter(comments, [
    "parentComment",
    0,
  ]);

  const orderComments = (
    unordered: ICommentStructure[],
    order: string
  ): ICommentStructure[] => {
    return order === "oldest"
      ? _.orderBy(unordered, ["created"], ["asc"])
      : _.orderBy(unordered, ["created"], ["desc"]);
  };

  return (
    <React.StrictMode>
      <commentContext.Provider value={{ replying, setReplying }}>
        <CommentEditor id={0} onPost={postHandler} />
        {comments.length > 1 && (
          <div className={"w-25 w-50-m mb3"}>
            <Small>{t("comments.orderBy.label")}</Small>
            <Select defaultValue={"newest"} onChange={onOrderChange}>
              <option value={"newest"}>{t("comments.orderBy.newest")}</option>
              <option value={"oldest"}>{t("comments.orderBy.oldest")}</option>
            </Select>
          </div>
        )}
        {rootComments.length > 0 ? (
          orderComments(rootComments, orderBy).map(
            (comment: ICommentStructure): JSX.Element => (
              <React.Fragment key={comment.id}>
                <Comment
                  backgroundEnabled={false}
                  comments={comments}
                  id={comment.id}
                  onPost={postHandler}
                  orderBy={orderBy}
                />
              </React.Fragment>
            )
          )
        ) : (
          <div className={"w-100 f4 pa3 ba-80 tc"} id={"no-comments"}>
            {t("comments.noComments")}
          </div>
        )}
      </commentContext.Provider>
    </React.StrictMode>
  );
};
