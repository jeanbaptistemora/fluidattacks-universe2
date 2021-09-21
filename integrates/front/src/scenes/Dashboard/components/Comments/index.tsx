import _ from "lodash";
import moment from "moment";
import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { CommentEditor } from "scenes/Dashboard/components/Comments/components/CommentEditor";
import { NestedComment } from "scenes/Dashboard/components/Comments/components/NestedComment";
import type {
  ICommentStructure,
  ILoadCallback,
  IPostCallback,
} from "scenes/Dashboard/components/Comments/types";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import style from "utils/forms/index.css";
import { translate } from "utils/translations/translate";

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

interface ICommentsProps {
  onLoad: (callbackFn: ILoadCallback) => void;
  onPostComment: (
    comment: ICommentStructure,
    callbackFn: IPostCallback
  ) => void;
}

interface ICommentContext {
  replying: number;
  setReplying?: React.Dispatch<React.SetStateAction<number>>;
}

const commentContext: React.Context<ICommentContext> = createContext({
  replying: 0,
});

const Comments: React.FC<ICommentsProps> = (
  props: ICommentsProps
): JSX.Element => {
  const { onLoad, onPostComment } = props;
  const { userEmail, userName }: IAuthContext = useContext(authContext);
  const [comments, setComments] = useState<ICommentStructure[]>([]);
  const [replying, setReplying] = useState<number>(0);
  const [orderBy, setOrderBy] = useState<string>("newest");

  const onMount: () => void = (): void => {
    onLoad((cData: ICommentStructure[]): void => {
      setComments(_.uniqBy(cData, "id"));
    });
  };
  useEffect(onMount, [onLoad]);

  const getFormattedTime = (): string => {
    const now = new Date();

    return moment(now).format("YYYY/MM/DD HH:mm:ss");
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
          parent: replying,
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

  const rootComments: ICommentStructure[] = _.filter(comments, ["parent", 0]);

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
            <Small>{translate.t("comments.orderBy.label")}</Small>
            <Select defaultValue={"newest"} onChange={onOrderChange}>
              <option value={"newest"}>
                {translate.t("comments.orderBy.newest")}
              </option>
              <option value={"oldest"}>
                {translate.t("comments.orderBy.oldest")}
              </option>
            </Select>
          </div>
        )}
        {rootComments.length > 0 ? (
          orderComments(rootComments, orderBy).map(
            (comment: ICommentStructure): JSX.Element => (
              <React.Fragment key={comment.id}>
                <NestedComment
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
            {translate.t("comments.noComments")}
          </div>
        )}
      </commentContext.Provider>
    </React.StrictMode>
  );
};

export { Comments, commentContext, ICommentContext, ICommentsProps };
