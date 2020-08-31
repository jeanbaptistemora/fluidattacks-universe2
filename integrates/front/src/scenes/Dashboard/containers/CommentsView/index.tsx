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
import { RouteComponentProps } from "react-router";
import { Logger } from "../../../../utils/logger";
import { msgError } from "../../../../utils/notifications";
import { translate } from "../../../../utils/translations/translate";
import { Comments, ICommentStructure, loadCallback, postCallback } from "../../components/Comments/index";
import { ADD_FINDING_CONSULT, GET_FINDING_CONSULTING, GET_FINDING_OBSERVATIONS } from "./queries";

type ICommentsViewProps = RouteComponentProps<{ findingId: string; type: string }>;

const commentsView: React.FC<ICommentsViewProps> = (props: ICommentsViewProps): JSX.Element => {
  const findingId: string = props.match.params.findingId;
  let type: string = props.match.params.type;
  type = type === "observations" ? type.slice(0, -1) : type.slice(0, -3);

  const onMount: (() => void) = (): void => {
    mixpanel.track(type === "consult" ? "FindingComments" : "FindingObservations", {
      User: (window as typeof window & { userName: string }).userName,
    });
  };
  React.useEffect(onMount, []);

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
          const getData: ((callback: loadCallback) => void) = (
            callbackFn: (data: ICommentStructure[]) => void,
          ): void => {
            const comments: ICommentStructure[] = type === "consult"
              ? data.finding.consulting
              : data.finding.observations;
            callbackFn(comments.map((comment: ICommentStructure) => ({
              ...comment,
              created_by_current_user: comment.email === (window as typeof window & { userEmail: string }).userEmail,
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
                const handlePost: ((comment: ICommentStructure, callbackFn: postCallback) => void) = (
                  comment: ICommentStructure, callbackFn: postCallback,
                ): void => {
                  interface IMutationResult {
                    data: {
                      addFindingConsult: {
                        commentId: string;
                        success: boolean;
                      };
                    };
                  }

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
