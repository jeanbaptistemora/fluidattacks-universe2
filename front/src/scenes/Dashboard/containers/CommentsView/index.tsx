import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { RouteComponentProps } from "react-router";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { comments as Comments, ICommentStructure } from "../../components/Comments/index";
import * as actions from "./actions";

type ICommentsViewProps = RouteComponentProps<{ findingId: string; type: string }>;

export type loadCallback = ((comments: ICommentStructure[]) => void);
export type postCallback = ((comments: ICommentStructure) => void);

const enhance: InferableComponentEnhancer<{}> = lifecycle<ICommentsViewProps, {}>({
  componentDidMount(): void {
    const { type } = this.props.match.params;
    mixpanel.track(type === "comments" ? "FindingComments" : "FindingObservations", {
      Organization: (window as Window & { userOrganization: string }).userOrganization,
      User: (window as Window & { userName: string }).userName,
    });
  },
});

const commentsView: React.FC<ICommentsViewProps> = (props: ICommentsViewProps): JSX.Element => {
  const { findingId, type } = props.match.params;

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

const commentsComponent: React.ComponentType<ICommentsViewProps> = enhance(commentsView);

export { commentsComponent as CommentsView };
