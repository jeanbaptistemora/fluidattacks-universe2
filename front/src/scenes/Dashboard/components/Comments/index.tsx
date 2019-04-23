import { default as $ } from "jquery";
/* tslint:disable-next-line no-import-side-effect
 * Disabling this rule is necessary to use the comments
 * plugin, which is currently only available for JQuery
 */
import "jquery-comments_brainkit";
import React from "react";
import { InferableComponentEnhancer, lifecycle } from "recompose";
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

export interface ICommentsProps {
  id: string;
  onLoad(callbackFn: ((comments: ICommentStructure[]) => void)): void;
  onPostComment(comment: ICommentStructure, callbackFn: ((comment: ICommentStructure) => void)): void;
}

const initializeComments: ((props: ICommentsProps) => void) = (props: ICommentsProps): void => {
  const { onLoad, onPostComment } = props;

  ($(`#${props.id}`) as JQLite & { comments({}: {}): void })
  .comments({
    defaultNavigationSortKey: "oldest",
    enableAttachments: false,
    enableEditing: false,
    enableHashtags: true,
    enablePinging: false,
    enableUpvoting: false,
    getComments: onLoad,
    postComment: onPostComment,
    roundProfilePictures: true,
    textareaRows: 2,
  });
};

const enhance: InferableComponentEnhancer<{}> =
  lifecycle<ICommentsProps, {}>({
    componentDidMount(): void {
      const props: ICommentsProps = this.props;
      initializeComments(props);
    },
    componentDidUpdate(previousProps: ICommentsProps): void {
      const props: ICommentsProps = this.props;
      if (previousProps.id !== props.id) {
        initializeComments(props);
      }
    },
  });

export const component: React.SFC<ICommentsProps> = (props: ICommentsProps): JSX.Element => (
  <React.StrictMode>
    <div id={props.id} />
  </React.StrictMode>
);

export const comments: React.SFC<ICommentsProps> = enhance(component) as React.SFC<ICommentsProps>;
