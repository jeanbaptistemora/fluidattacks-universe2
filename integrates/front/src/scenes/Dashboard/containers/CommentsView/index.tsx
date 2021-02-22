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

import { Comments } from "scenes/Dashboard/components/Comments/index";
import {
  ICommentStructure,
  ILoadCallback,
  IPostCallback,
} from "scenes/Dashboard/components/Comments/types";
import {
  ADD_FINDING_CONSULT,
  GET_FINDING_CONSULTING,
  GET_FINDING_OBSERVATIONS,
} from "scenes/Dashboard/containers/CommentsView/queries";
import { authContext, IAuthContext } from "utils/auth";

import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const commentsView: React.FC = (): JSX.Element => {
  const params: { findingId: string; type: string } = useParams();
  const findingId: string = params.findingId;
  const type: string = params.type === "observations"
    ? params.type.slice(0, -1)
    : params.type.slice(0, -3);

  const { userEmail }: IAuthContext = React.useContext(authContext);

  const handleErrors: ((error: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      Logger.warning(`An error occurred loading finding ${type}`, error);
    });
  };

  return (
    <React.StrictMode>
      <Query
        query={type === "consult" ? GET_FINDING_CONSULTING : GET_FINDING_OBSERVATIONS}
        variables={{ findingId }}
        onError={handleErrors}
      >
        {({ data, loading }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || loading) { return <React.Fragment />; }
          const getData: ((callback: ILoadCallback) => void) = (
            callbackFn: (data: ICommentStructure[]) => void,
          ): void => {
            const comments: ICommentStructure[] = type === "consult"
              ? data.finding.consulting
              : data.finding.observations;
            callbackFn(comments.map((comment: ICommentStructure) => ({
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
                  Logger.warning(`An error occurred posting ${type}`, addCommentError);
              }
            });
          };

          return (
            <Mutation mutation={ADD_FINDING_CONSULT} onError={handleAddCommentError}>
              {(addComment: MutationFunction): JSX.Element => {
                const handlePost: ((comment: ICommentStructure, callbackFn: IPostCallback) => void) = (
                  comment: ICommentStructure, callbackFn: IPostCallback,
                ): void => {
                  interface IMutationResult {
                    data: {
                      addFindingConsult: {
                        commentId: string;
                        success: boolean;
                      };
                    };
                  }
                  mixpanel.track(`Add${_.capitalize(type)}`, { findingId });
                  void addComment({ variables: { findingId,
                                                 type: type.toUpperCase(),
                                                 ...comment } })
                    .then((mtResult: void | {}): void => {
                      const result: IMutationResult["data"] = (mtResult as IMutationResult).data;
                      if (result.addFindingConsult.success) {
                        callbackFn({ ...comment, id: Number(result.addFindingConsult.commentId) });
                      }
                    });
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
