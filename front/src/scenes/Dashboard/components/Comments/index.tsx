import { default as $ } from "jquery";
/* tslint:disable-next-line no-import-side-effect
 * Disabling this rule is necessary to use the comments
 * plugin, which is currently only available for JQuery
 */
import "jquery-comments_brainkit";
/* tslint:disable-next-line:no-import-side-effect no-submodule-imports
 * Disabling this two rules is necessary for
 * allowing the import of default styles that jquery-comments needs
 * to display properly even if some of them are overridden later
 */
import "jquery-comments_brainkit/css/jquery-comments.css";
import mixpanel from "mixpanel-browser";
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

  ($(`#${props.id}`) as JQuery & { comments({}: object): void })
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
      mixpanel.track(
        "ProjectComments",
        {
          Organization: (window as Window & { userOrganization: string }).userOrganization,
          User: (window as Window & { userName: string }).userName,
        });
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

export const component: React.FC<ICommentsProps> = (props: ICommentsProps): JSX.Element => (
  <React.StrictMode>
    <div id={props.id} />
  </React.StrictMode>
);

export const comments: React.FC<ICommentsProps> = enhance(component) as React.FC<ICommentsProps>;
