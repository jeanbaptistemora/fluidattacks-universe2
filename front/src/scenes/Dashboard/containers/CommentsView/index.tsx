/* tslint:disable jsx-no-lambda jsx-no-multiline-js
 * Disabling this rules is necessary for the sake of simplicity and
 * readability of the code that binds load and post events
 * eslint quote-props: ["error", "always"]
 */

import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { InferableComponentEnhancer, lifecycle } from "recompose";
import { AnyAction } from "redux";
import { ThunkDispatch } from "redux-thunk";
import store from "../../../../store/index";
import { comments as Comments, ICommentStructure } from "../../components/Comments/index";
import * as actions from "./actions";

interface ICommentsViewProps {
  findingId: string;
  type: "comment" | "observation";
}

const enhance: InferableComponentEnhancer<{}> =
lifecycle<ICommentsViewProps, {}>({
  componentDidMount(): void {
    mixpanel.track(
      _.eq(this.props.type, "comments")
      ? "FindingComments"
      : "FindingObservations",
      {
        Organization: (window as Window & { userOrganization: string }).userOrganization,
        User: (window as Window & { userName: string }).userName,
      });
  },
});

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

const commentsView: React.FC<ICommentsViewProps> =
  (props: ICommentsViewProps): JSX.Element => (
    <React.StrictMode>
      <Comments
        id={`finding-${props.type}s`}
        onLoad={(callbackFn: ((comments: ICommentStructure[]) => void)): void => {
          loadComments(props.findingId, props.type, callbackFn);
        }}
        onPostComment={(comment: ICommentStructure, callbackFn: ((comments: ICommentStructure) => void)): void => {
          postComment(props.findingId, props.type, comment, callbackFn);
        }}
      />
    </React.StrictMode>
  );

export = enhance(commentsView);
