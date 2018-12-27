/* tslint:disable jsx-no-lambda jsx-no-multiline-js
 * Disabling this rules is necessary for the sake of simplicity and
 * readability of the code that binds load and post events
 */

import React from "react";
import { AnyAction } from "redux";
import { ThunkDispatch } from "redux-thunk";
import store from "../../../../store/index";
import { comments as Comments } from "../../components/Comments/index";
import * as actions from "./actions";

export interface IProjectCommentsViewProps {
  projectName: string;
}

export interface ICommentStructure {
  content: string;
  created: string;
  created_by_current_user: boolean;
  email: string;
  fullname: string;
  id: number;
  modified: string;
  parent: number;
}

const loadComments: ((projectName: string, callbackFn: ((comments: ICommentStructure[]) => void)) => void) =
  (projectName: string, callbackFn: ((comments: ICommentStructure[]) => void)): void => {
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );

    thunkDispatch(actions.loadComments(projectName, callbackFn));
  };

const postComment: (
  (projectName: string, comment: ICommentStructure, callbackFn: ((comment: ICommentStructure) => void)) => void) =
  (projectName: string, comment: ICommentStructure, callbackFn: ((comment: ICommentStructure) => void)): void => {
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );

    thunkDispatch(actions.postComment(projectName, comment, callbackFn));
  };

export const projectCommentsView: React.SFC<IProjectCommentsViewProps> =
  (props: IProjectCommentsViewProps): JSX.Element => (
    <React.StrictMode>
      <Comments
        id="project-comments"
        onLoad={(callbackFn: ((comments: {}) => void)): void => {
          loadComments(props.projectName, callbackFn);
        }}
        onPostComment={(comment: {}, callbackFn: ((comments: {}) => void)): void => {
          postComment(props.projectName, comment as ICommentStructure, callbackFn);
        }}
      />
    </React.StrictMode>
  );
