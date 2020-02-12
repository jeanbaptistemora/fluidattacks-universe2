/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { MutationFunction, QueryResult } from "@apollo/react-common";
import { Mutation, Query } from "@apollo/react-components";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { RouteComponentProps } from "react-router";
import { Comments, ICommentStructure, loadCallback, postCallback } from "../../components/Comments/index";
import { ADD_PROJECT_COMMENT, GET_PROJECT_COMMENTS } from "./queries";

type IProjectCommentsViewProps = RouteComponentProps<{ projectName: string }>;

const projectCommentsView: React.FC<IProjectCommentsViewProps> = (props: IProjectCommentsViewProps): JSX.Element => {
  const { projectName } = props.match.params;
  const onMount: (() => void) = (): void => {
    mixpanel.track("ProjectComments", {
      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
      User: (window as typeof window & { userName: string }).userName,
    });
  };
  React.useEffect(onMount, []);

  return (
    <React.StrictMode>
      <Query fetchPolicy="network-only" query={GET_PROJECT_COMMENTS} variables={{ projectName }}>
        {({ data, loading }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || loading) { return <React.Fragment />; }
          const getData: ((callback: loadCallback) => void) = (
            callbackFn: (data: ICommentStructure[]) => void,
          ): void => {
            callbackFn(data.project.comments.map((comment: ICommentStructure) => ({
              ...comment,
              created_by_current_user: comment.email === (window as typeof window & { userEmail: string }).userEmail,
              id: Number(comment.id),
              parent: Number(comment.parent),
            })));
          };

          return (
            <Mutation mutation={ADD_PROJECT_COMMENT}>
              {(addComment: MutationFunction): JSX.Element => {
                const handlePost: ((comment: ICommentStructure, callbackFn: postCallback) => void) = (
                  comment: ICommentStructure, callbackFn: postCallback,
                ): void => {
                  interface IMutationResult {
                    data: {
                      addProjectComment: {
                        commentId: string;
                        success: boolean;
                      };
                    };
                  }

                  addComment({ variables: { projectName, ...comment } })
                    .then((mtResult: void | {}): void => {
                      const result: IMutationResult["data"] = (mtResult as IMutationResult).data;
                      if (result.addProjectComment.success) {
                        callbackFn({ ...comment, id: Number(result.addProjectComment.commentId) });
                      }
                    })
                    .catch();
                };

                return (<Comments id="project-comments" onLoad={getData} onPostComment={handlePost} />);
              }}
            </Mutation>
          );
        }}
      </Query>
    </React.StrictMode>
  );
};

export { projectCommentsView as ProjectCommentsView };
