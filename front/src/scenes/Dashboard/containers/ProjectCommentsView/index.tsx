import React from "react";
import { RouteComponentProps } from "react-router";
import { Comments, ICommentStructure } from "../../components/Comments/index";
import { loadComments, postComment } from "./actions";

type IProjectCommentsViewProps = RouteComponentProps<{ projectName: string }>;
export type loadCallback = ((comments: ICommentStructure[]) => void);
export type postCallback = ((comments: ICommentStructure) => void);

const projectCommentsView: React.FC<IProjectCommentsViewProps> = (props: IProjectCommentsViewProps): JSX.Element => {
  const { projectName } = props.match.params;
  const handleLoad: ((callbackFn: loadCallback) => void) = (callbackFn: loadCallback): void => {
    loadComments(projectName, callbackFn);
  };

  const handlePost: ((comment: ICommentStructure, callbackFn: postCallback) => void) = (
    comment: ICommentStructure, callbackFn: postCallback,
  ): void => {
    postComment(projectName, comment, callbackFn);
  };

  return (
    <React.StrictMode>
      <Comments id="project-comments" onLoad={handleLoad} onPostComment={handlePost} />
    </React.StrictMode>
  );
};

export { projectCommentsView as ProjectCommentsView };
