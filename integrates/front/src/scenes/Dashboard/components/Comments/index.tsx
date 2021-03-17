import $ from "jquery";
import type { ICommentsProps } from "scenes/Dashboard/components/Comments/types";
import React, { useEffect } from "react";
import "jquery-comments_brainkit";
import "jquery-comments_brainkit/css/jquery-comments.css";

const initializeComments: (props: ICommentsProps) => void = (
  props: ICommentsProps
): void => {
  const { id, onLoad, onPostComment } = props;

  ($(`#${id}`) as JQuery & {
    comments: (options: Record<string, unknown>) => void;
  }).comments({
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

const Comments: React.FC<ICommentsProps> = (
  props: ICommentsProps
): JSX.Element => {
  const { id, onLoad, onPostComment } = props;
  const onMount: () => void = (): void => {
    initializeComments({ id, onLoad, onPostComment });
  };
  // Annotation needed for avoiding improper behaviour of callbacks
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(onMount, [id]);

  return (
    <React.StrictMode>
      <div id={id} />
    </React.StrictMode>
  );
};

export { Comments };
