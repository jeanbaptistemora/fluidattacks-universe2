import React from "react";
import { connect, ConnectedComponentClass, MapDispatchToProps } from "react-redux";
import { RouteComponentProps } from "react-router";
import { comments as Comments, ICommentStructure } from "../../components/Comments/index";
import { loadComments, postComment, ThunkDispatcher } from "./actions";

type IProjectCommentsBaseProps = Pick<RouteComponentProps<{ projectName: string }>, "match">;

interface IProjectCommentsDispatchProps {
  onLoad(callbackFn: ((comments: ICommentStructure[]) => void)): void;
  onPostComment(comment: ICommentStructure, callbackFn: ((comment: ICommentStructure) => void)): void;
}

export type IProjectCommentsViewProps = IProjectCommentsBaseProps & IProjectCommentsDispatchProps;

const projectCommentsView: React.FC<IProjectCommentsViewProps> = (props: IProjectCommentsViewProps): JSX.Element => {
  const handleLoad: ((callbackFn: ((comments: ICommentStructure[]) => void)) => void) =
    (callbackFn: ((comments: ICommentStructure[]) => void)): void => {
      props.onLoad(callbackFn);
    };

  const handlePost: ((comment: ICommentStructure, callbackFn: ((comments: ICommentStructure) => void)) => void) =
    (comment: ICommentStructure, callbackFn: ((comments: ICommentStructure) => void)): void => {
      props.onPostComment(comment, callbackFn);
    };

  return (
    <React.StrictMode>
      <Comments id="project-comments" onLoad={handleLoad} onPostComment={handlePost} />
    </React.StrictMode>
  );
};

const mapStateToProps: undefined = undefined;

const mapDispatchToProps: MapDispatchToProps<IProjectCommentsDispatchProps, IProjectCommentsBaseProps> =
  (dispatch: ThunkDispatcher, ownProps: IProjectCommentsBaseProps): IProjectCommentsDispatchProps => {
    const { projectName } = ownProps.match.params;

    return ({
      onLoad: (callbackFn: ((comments: ICommentStructure[]) => void)): void => {
        dispatch(loadComments(projectName, callbackFn));
      },
      onPostComment: (comment: ICommentStructure, callbackFn: ((comments: ICommentStructure) => void)): void => {
        dispatch(postComment(projectName, comment, callbackFn));
      },
    });
  };

const connectedProjectCommentsView:
  ConnectedComponentClass<React.FunctionComponent<IProjectCommentsViewProps>, IProjectCommentsBaseProps> =
    connect(mapStateToProps, mapDispatchToProps)(projectCommentsView);
export { connectedProjectCommentsView as ProjectCommentsView };
