import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { RouteComponentProps } from "react-router";
import { Comments, ICommentStructure } from "../../components/Comments/index";
import * as actions from "./actions";

type ICommentsViewProps = RouteComponentProps<{ findingId: string; type: string }>;

export type loadCallback = ((comments: ICommentStructure[]) => void);
export type postCallback = ((comments: ICommentStructure) => void);

const commentsView: React.FC<ICommentsViewProps> = (props: ICommentsViewProps): JSX.Element => {
  const { findingId, type } = props.match.params;
  const onMount: (() => void) = (): void => {
    mixpanel.track(type === "comments" ? "FindingComments" : "FindingObservations", {
      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
      User: (window as typeof window & { userName: string }).userName,
    });
  };
  React.useEffect(onMount, []);

  const handleLoad: ((callbackFn: loadCallback) => void) = (callbackFn: loadCallback): void => {
    actions.loadComments(findingId, type, callbackFn);
  };

  const handlePost: ((comment: ICommentStructure, callbackFn: postCallback) => void) = (
    comment: ICommentStructure, callbackFn: postCallback,
  ): void => {
    actions.postComment(findingId, type, comment, callbackFn);
  };

  return (
    <React.StrictMode>
      <Comments id={`finding-${type}`} onLoad={handleLoad} onPostComment={handlePost} />
    </React.StrictMode>
  );
};

export { commentsView as CommentsView };
