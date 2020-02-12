/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { MutationFunction, QueryResult } from "@apollo/react-common";
import { Mutation, Query } from "@apollo/react-components";
import _ from "lodash";
import React from "react";
import { RouteComponentProps } from "react-router";
import { Comments, ICommentStructure, loadCallback, postCallback } from "../../components/Comments/index";
import { ADD_EVENT_COMMENT, GET_EVENT_COMMENTS } from "./queries";

type EventCommentsProps = RouteComponentProps<{ eventId: string }>;

const eventCommentsView: React.FC<EventCommentsProps> = (props: EventCommentsProps): JSX.Element => {
  const { eventId } = props.match.params;

  return (
    <React.StrictMode>
      <Query fetchPolicy="network-only" query={GET_EVENT_COMMENTS} variables={{ eventId }}>
        {({ data, loading }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || loading) { return <React.Fragment />; }
          const getData: ((callback: loadCallback) => void) = (
            callbackFn: (data: ICommentStructure[]) => void,
          ): void => {
            callbackFn(data.event.comments.map((comment: ICommentStructure) => ({
              ...comment,
              created_by_current_user: comment.email === (window as typeof window & { userEmail: string }).userEmail,
              id: Number(comment.id),
              parent: Number(comment.parent),
            })));
          };

          return (
            <Mutation mutation={ADD_EVENT_COMMENT}>
              {(addComment: MutationFunction): JSX.Element => {
                const handlePost: ((comment: ICommentStructure, callbackFn: postCallback) => void) = (
                  comment: ICommentStructure, callbackFn: postCallback,
                ): void => {
                  interface IMutationResult {
                    data: {
                      addEventComment: {
                        commentId: string;
                        success: boolean;
                      };
                    };
                  }

                  addComment({ variables: { eventId, ...comment } })
                    .then((mtResult: void | {}): void => {
                      const result: IMutationResult["data"] = (mtResult as IMutationResult).data;
                      if (result.addEventComment.success) {
                        callbackFn({ ...comment, id: Number(result.addEventComment.commentId) });
                      }
                    })
                    .catch();
                };

                return (<Comments id="event-comments" onLoad={getData} onPostComment={handlePost} />);
              }}
            </Mutation>
          );
        }}
      </Query>
    </React.StrictMode>
  );
};

export { eventCommentsView as EventCommentsView };
