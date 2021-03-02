import type { ApolloError } from "apollo-client";
import { Comments } from "scenes/Dashboard/components/Comments/index";
import type { GraphQLError } from "graphql";
import type { IAuthContext } from "utils/auth";
import { Logger } from "utils/logger";
import React from "react";
import _ from "lodash";
import { authContext } from "utils/auth";
import mixpanel from "mixpanel-browser";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { useParams } from "react-router";
import {
  ADD_EVENT_CONSULT,
  GET_EVENT_CONSULTING,
} from "scenes/Dashboard/containers/EventCommentsView/queries";
import type {
  ICommentStructure,
  ILoadCallback,
  IPostCallback,
} from "scenes/Dashboard/components/Comments/types";
import { Mutation, Query } from "@apollo/react-components";
import type { MutationFunction, QueryResult } from "@apollo/react-common";

const EventCommentsView: React.FC = (): JSX.Element => {
  const { eventId } = useParams<{ eventId: string }>();
  const { userEmail }: IAuthContext = React.useContext(authContext);

  const handleErrors: (error: ApolloError) => void = React.useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred loading event comments", error);
      });
    },
    []
  );

  return (
    <React.StrictMode>
      <Query
        fetchPolicy={"network-only"}
        onError={handleErrors}
        query={GET_EVENT_CONSULTING}
        variables={{ eventId }}
      >
        {({ data, loading }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || loading) {
            return <div />;
          }
          const getData: (callback: ILoadCallback) => void = (
            callbackFn: (cData: ICommentStructure[]) => void
          ): void => {
            callbackFn(
              // Next eslint annotations needed due to the usage of any type in DB query results
              // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
              data.event.consulting.map(
                (comment: ICommentStructure): ICommentStructure => ({
                  ...comment,
                  created_by_current_user: comment.email === userEmail,
                  id: Number(comment.id),
                  parent: Number(comment.parent),
                })
              )
            );
          };

          const handleAddCommentError: (
            addCommentError: ApolloError
          ) => void = (addCommentError: ApolloError): void => {
            addCommentError.graphQLErrors.forEach(
              ({ message }: GraphQLError): void => {
                switch (message) {
                  case "Exception - Comment parent is invalid":
                    msgError(
                      translate.t("validations.invalidCommentParent", {
                        count: 1,
                      })
                    );
                    break;
                  default:
                    msgError(translate.t("group_alerts.error_textsad"));
                    Logger.warning(
                      "An error occurred posting event comment",
                      addCommentError
                    );
                }
              }
            );
          };

          return (
            <Mutation
              mutation={ADD_EVENT_CONSULT}
              onError={handleAddCommentError} // eslint-disable-line react/jsx-no-bind -- Annotation needed due to nested callback
            >
              {(addComment: MutationFunction): JSX.Element => {
                const handlePost: (
                  comment: ICommentStructure,
                  callbackFn: IPostCallback
                ) => void = (
                  comment: ICommentStructure,
                  callbackFn: IPostCallback
                ): void => {
                  interface IMutationResult {
                    data: {
                      addEventConsult: {
                        commentId: string;
                        success: boolean;
                      };
                    };
                  }
                  mixpanel.track("AddEventComment", { eventId });
                  void addComment({ variables: { eventId, ...comment } }).then(
                    (mtResult: unknown | null): void => {
                      const result: IMutationResult["data"] = (mtResult as IMutationResult)
                        .data;
                      if (result.addEventConsult.success) {
                        callbackFn({
                          ...comment,
                          id: Number(result.addEventConsult.commentId),
                        });
                      }
                    }
                  );
                };

                return (
                  <Comments
                    id={"event-comments"}
                    onLoad={getData} // eslint-disable-line react/jsx-no-bind -- Annotation needed due to nested callback
                    onPostComment={handlePost} // eslint-disable-line react/jsx-no-bind -- Annotation needed due to nested callback
                  />
                );
              }}
            </Mutation>
          );
        }}
      </Query>
    </React.StrictMode>
  );
};

export { EventCommentsView };
