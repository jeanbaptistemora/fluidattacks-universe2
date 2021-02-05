/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { MutationFunction, QueryResult } from "@apollo/react-common";
import { Mutation, Query } from "@apollo/react-components";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { useParams } from "react-router";
import {
  Comments,
  ICommentStructure,
  loadCallback,
  postCallback,
} from "scenes/Dashboard/components/Comments/index";
import {
  ADD_EVENT_CONSULT,
  GET_EVENT_CONSULTING,
} from "scenes/Dashboard/containers/EventCommentsView/queries";
import { authContext, IAuthContext } from "utils/auth";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const eventCommentsView: React.FC = (): JSX.Element => {
  const { eventId } = useParams<{eventId: string}>();
  const { userEmail }: IAuthContext = React.useContext(authContext);

  const handleErrors: ((error: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      Logger.warning("An error occurred loading event comments", error);
    });
  };

  return (
    <React.StrictMode>
      <Query fetchPolicy="network-only" query={GET_EVENT_CONSULTING} variables={{ eventId }} onError={handleErrors}>
        {({ data, loading }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || loading) { return <React.Fragment />; }
          const getData: ((callback: loadCallback) => void) = (
            callbackFn: (data: ICommentStructure[]) => void,
          ): void => {
            callbackFn(data.event.consulting.map((comment: ICommentStructure) => ({
              ...comment,
              created_by_current_user: comment.email === userEmail,
              id: Number(comment.id),
              parent: Number(comment.parent),
            })));
          };

          const handleAddCommentError: ((addCommentError: ApolloError) => void) =
            (addCommentError: ApolloError): void => {
              addCommentError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
              switch (message) {
                case "Exception - Comment parent is invalid":
                  msgError(translate.t("validations.invalidCommentParent", { count: 1 }));
                  break;
                default:
                  msgError(translate.t("group_alerts.error_textsad"));
                  Logger.warning("An error occurred posting event comment", addCommentError);
              }
            });
          };

          return (
            <Mutation mutation={ADD_EVENT_CONSULT} onError={handleAddCommentError}>
              {(addComment: MutationFunction): JSX.Element => {
                const handlePost: ((comment: ICommentStructure, callbackFn: postCallback) => void) = (
                  comment: ICommentStructure, callbackFn: postCallback,
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
                  void addComment({ variables: { eventId, ...comment } })
                    .then((mtResult: void | {}): void => {
                      const result: IMutationResult["data"] = (mtResult as IMutationResult).data;
                      if (result.addEventConsult.success) {
                        callbackFn({ ...comment, id: Number(result.addEventConsult.commentId) });
                      }
                    });
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
