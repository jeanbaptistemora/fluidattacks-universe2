import React from "react";
import { InferableComponentEnhancer, lifecycle } from "recompose";

export interface ICommentsProps {
  id: string;
  onLoad(callbackFn: ((dataset: Map<string, string>) => void)): void;
  onPostComment(
    data: { [key: string]: string },
    callbackFn: ((commentData: { [key: string]: string }) => void),
  ): void;
}

/* tslint:disable-next-line no-any
 * Disabling this rule is necessary to use the comments
 * plugin, which is currently only available for JQuery
 */
declare var $: any;

const initializeComments: ((props: ICommentsProps) => void) = (props: ICommentsProps): void => {
  $(`#${props.id}`)
  .comments({
    defaultNavigationSortKey: "oldest",
    enableAttachments: false,
    enableEditing: false,
    enableHashtags: true,
    enablePinging: false,
    enableUpvoting: false,
    getComments(callbackFn: (dataset: Map<string, string>) => void): void {
      props.onLoad(callbackFn);
    },
    postComment(data: { [key: string]: string }, callbackFn: (data: { [key: string]: string }) => void): void {
      props.onPostComment(data, callbackFn);
    },
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
