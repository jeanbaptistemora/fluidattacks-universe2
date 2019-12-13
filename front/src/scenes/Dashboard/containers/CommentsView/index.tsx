/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Mutation, MutationFn, Query, QueryResult } from "react-apollo";
import { RouteComponentProps } from "react-router";
import { Comments, ICommentStructure, loadCallback, postCallback } from "../../components/Comments/index";
import { ADD_FINDING_COMMENT, GET_FINDING_COMMENTS, GET_FINDING_OBSERVATIONS } from "./queries";

type ICommentsViewProps = RouteComponentProps<{ findingId: string; type: string }>;

const commentsView: React.FC<ICommentsViewProps> = (props: ICommentsViewProps): JSX.Element => {
  const { findingId, type } = props.match.params;
  const onMount: (() => void) = (): void => {
    mixpanel.track(type === "comments" ? "FindingComments" : "FindingObservations", {
      Organization: (window as typeof window & { userOrganization: string }).userOrganization,
      User: (window as typeof window & { userName: string }).userName,
    });
  };
  React.useEffect(onMount, []);

  return (
    <React.StrictMode>
      <Query
        fetchPolicy="network-only"
        query={type === "comments" ? GET_FINDING_COMMENTS : GET_FINDING_OBSERVATIONS}
        variables={{ findingId }}
      >
        {({ data, loading }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || loading) { return <React.Fragment />; }
          const getData: ((callback: loadCallback) => void) = (
            callbackFn: (data: ICommentStructure[]) => void,
          ): void => {
            const comments: ICommentStructure[] = type === "comments"
              ? data.finding.comments
              : data.finding.observations;
            callbackFn(comments.map((comment: ICommentStructure) => ({
              ...comment,
              created_by_current_user: comment.email === (window as typeof window & { userEmail: string }).userEmail,
              id: Number(comment.id),
              parent: Number(comment.parent),
            })));
          };

          return (
            <Mutation mutation={ADD_FINDING_COMMENT}>
              {(addComment: MutationFn): React.ReactNode => {
                const handlePost: ((comment: ICommentStructure, callbackFn: postCallback) => void) = (
                  comment: ICommentStructure, callbackFn: postCallback,
                ): void => {
                  interface IMutationResult {
                    data: {
                      addFindingComment: {
                        commentId: string;
                        success: boolean;
                      };
                    };
                  }

                  addComment({ variables: { findingId, type: type.slice(0, -1), ...comment } })
                    .then((mtResult: void | {}): void => {
                      const result: IMutationResult["data"] = (mtResult as IMutationResult).data;
                      if (result.addFindingComment.success) {
                        callbackFn({ ...comment, id: Number(result.addFindingComment.commentId) });
                      }
                    })
                    .catch();
                };

                return (<Comments id={`finding-${type}`} onLoad={getData} onPostComment={handlePost} />);
              }}
            </Mutation>
          );
        }}
      </Query>
    </React.StrictMode>
  );
};

export { commentsView as CommentsView };
