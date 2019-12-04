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
import React from "react";

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

  ($(`#${props.id}`) as JQuery & { comments({ }: object): void }).comments({
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

const comments: React.FC<ICommentsProps> = (props: ICommentsProps): JSX.Element => {
  const onMount: (() => void) = (): void => {
    initializeComments(props);
  };
  React.useEffect(onMount, [props.id]);

  return (
    <React.StrictMode>
      <div id={props.id} />
    </React.StrictMode>
  );
};

export { comments as Comments };
