import _ from "lodash";
import moment from "moment";
import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";

import type {
  ICommentStructure,
  ILoadCallback,
  IPostCallback,
} from "scenes/Dashboard/components/Comments/types";
import { CommentEditor } from "scenes/Dashboard/components/CommentsRefac/commentEditor";
import { NestedComment } from "scenes/Dashboard/components/CommentsRefac/nestedComment";
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

interface ICommentContext {
  replying: number;
  setReplying?: React.Dispatch<React.SetStateAction<number>>;
}

const commentContext: React.Context<ICommentContext> = createContext({
  replying: 0,
});

const CommentsRefac: React.FC<ICommentsRefacProps> = (
  props: ICommentsRefacProps
): JSX.Element => {
  const { onLoad, onPostComment } = props;
  const { userEmail, userName }: IAuthContext = useContext(authContext);
  const [comments, setComments] = useState<ICommentStructure[]>([]);
  const [replying, setReplying] = useState<number>(0);

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

  const postHandler = useCallback(
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

  const rootComments: ICommentStructure[] = _.filter(comments, ["parent", 0]);

  return (
    <React.StrictMode>
      <hr />
      <CommentEditor onPost={postHandler} />
      <hr />
      <commentContext.Provider value={{ replying, setReplying }}>
        {rootComments.length > 0
          ? _.orderBy(rootComments, ["created"], ["desc"]).map(
              (comment: ICommentStructure): JSX.Element => (
                <React.Fragment key={comment.id}>
                  <NestedComment
                    comments={comments}
                    id={comment.id}
                    onPost={postHandler}
                  />
                </React.Fragment>
              )
            )
          : translate.t("comments.noComments")}
      </commentContext.Provider>
    </React.StrictMode>
  );
};

export { CommentsRefac, commentContext, ICommentContext, ICommentsRefacProps };
