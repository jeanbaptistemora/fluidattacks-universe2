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
  ADD_FINDING_CONSULT,
  GET_FINDING_CONSULTING,
  GET_FINDING_OBSERVATIONS,
} from "scenes/Dashboard/containers/CommentsView/queries";
import type {
  ICommentStructure,
  ILoadCallback,
  IPostCallback,
} from "scenes/Dashboard/components/Comments/types";
import { Mutation, Query } from "@apollo/react-components";
import type { MutationFunction, QueryResult } from "@apollo/react-common";

const CommentsView: React.FC = (): JSX.Element => {
  const params: { findingId: string; type: string } = useParams();
  const findingId: string = params.findingId;
  const PARAM_NO_OBSERVATIONS: number = -3;
  const type: string =
    params.type === "observations"
      ? params.type.slice(0, -1)
      : params.type.slice(0, PARAM_NO_OBSERVATIONS);

  const { userEmail }: IAuthContext = React.useContext(authContext);

  const handleErrors: (error: ApolloError) => void = React.useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning(`An error occurred loading finding ${type}`, error);
      });
    },
    [type]
  );

  const handleAddCommentError: (
    addCommentError: ApolloError
  ) => void = React.useCallback(
    (addCommentError: ApolloError): void => {
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
                `An error occurred posting ${type}`,
                addCommentError
              );
          }
        }
      );
    },
    [type]
  );

  return (
    <React.StrictMode>
      <Query
        onError={handleErrors}
        query={
          type === "consult" ? GET_FINDING_CONSULTING : GET_FINDING_OBSERVATIONS
        }
        variables={{ findingId }}
      >
        {({ data, loading }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || loading) {
            return <div />;
          }
          const getData: (callback: ILoadCallback) => void = (
            callbackFn: (cData: ICommentStructure[]) => void
          ): void => {
            // Next eslint annotations needed due to the usage of any type in DB query results
            const comments: ICommentStructure[] =
              type === "consult"
                ? data.finding.consulting // eslint-disable-line @typescript-eslint/no-unsafe-member-access
                : data.finding.observations; // eslint-disable-line @typescript-eslint/no-unsafe-member-access
            callbackFn(
              comments.map(
                (comment: ICommentStructure): ICommentStructure => ({
                  ...comment,
                  created_by_current_user: comment.email === userEmail,
                  id: Number(comment.id),
                  parent: Number(comment.parent),
                })
              )
            );
          };

          return (
            <Mutation
              mutation={ADD_FINDING_CONSULT}
              onError={handleAddCommentError}
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
                      addFindingConsult: {
                        commentId: string;
                        success: boolean;
                      };
                    };
                  }
                  mixpanel.track(`Add${_.capitalize(type)}`, { findingId });
                  void addComment({
                    variables: {
                      findingId,
                      type: type.toUpperCase(),
                      ...comment,
                    },
                  }).then((mtResult: null | unknown): void => {
                    const result: IMutationResult["data"] = (mtResult as IMutationResult)
                      .data;
                    if (result.addFindingConsult.success) {
                      callbackFn({
                        ...comment,
                        id: Number(result.addFindingConsult.commentId),
                      });
                    }
                  });
                };

                return (
                  <Comments
                    id={`finding-${type}`}
                    // Next eslint annotations needed due to nested callbacks
                    onLoad={getData} // eslint-disable-line react/jsx-no-bind
                    onPostComment={handlePost} // eslint-disable-line react/jsx-no-bind
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

export { CommentsView };
