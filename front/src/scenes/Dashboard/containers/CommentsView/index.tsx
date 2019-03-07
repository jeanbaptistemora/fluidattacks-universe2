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

export interface ICommentsViewProps {
  findingId: string;
  type: "comment" | "observation";
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

const loadComments: ((projectName: string, type: ICommentsViewProps["type"],
                      callbackFn: ((comments: ICommentStructure[]) => void)) => void) =
  (projectName: string, type: ICommentsViewProps["type"],
   callbackFn: ((comments: ICommentStructure[]) => void)): void => {
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );

    thunkDispatch(actions.loadComments(projectName, type, callbackFn));
  };

const postComment: ((projectName: string, type: ICommentsViewProps["type"],
                     comment: ICommentStructure, callbackFn: ((comment: ICommentStructure) => void)) => void) =
  (projectName: string, type: ICommentsViewProps["type"],
   comment: ICommentStructure, callbackFn: ((comment: ICommentStructure) => void)): void => {
    const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
      store.dispatch as ThunkDispatch<{}, {}, AnyAction>
    );

    thunkDispatch(actions.postComment(projectName, type, comment, callbackFn));
  };

export const commentsView: React.SFC<ICommentsViewProps> =
  (props: ICommentsViewProps): JSX.Element => (
    <React.StrictMode>
      <Comments
        id={`finding-${props.type}s`}
        onLoad={(callbackFn: ((comments: {}) => void)): void => {
          loadComments(props.findingId, props.type, callbackFn);
        }}
        onPostComment={(comment: {}, callbackFn: ((comments: {}) => void)): void => {
          postComment(props.findingId, props.type, comment as ICommentStructure, callbackFn);
        }}
      />
    </React.StrictMode>
  );
