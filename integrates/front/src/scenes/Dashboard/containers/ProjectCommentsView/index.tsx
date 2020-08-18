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
import translate from "../../../../utils/translations/translate";
import { Comments, ICommentStructure, loadCallback, postCallback } from "../../components/Comments/index";
import { ADD_PROJECT_CONSULT, GET_PROJECT_CONSULTING } from "./queries";

type IProjectCommentsViewProps = RouteComponentProps<{ projectName: string }>;

const projectCommentsView: React.FC<IProjectCommentsViewProps> = (props: IProjectCommentsViewProps): JSX.Element => {
  const { projectName } = props.match.params;
  const onMount: (() => void) = (): void => {
    mixpanel.track("ProjectComments", {
      User: (window as typeof window & { userName: string }).userName,
    });
  };
  React.useEffect(onMount, []);

  const handleAddCommentError: ((addCommentError: ApolloError) => void) =
    (addCommentError: ApolloError): void => {
      addCommentError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
      switch (message) {
        case "Exception - Comment parent is invalid":
          msgError(translate.t("validations.invalidCommentParent", { count: 1 }));
          break;
        default:
          msgError(translate.t("group_alerts.error_textsad"));
          Logger.warning("An error occurred updating exploit", addCommentError);
      }
    });
  };

  const handleErrors: ((error: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      Logger.warning("An error occurred loading project comments", error);
    });
  };

  return (
    <React.StrictMode>
      <Query
        fetchPolicy="network-only"
        query={GET_PROJECT_CONSULTING}
        variables={{ projectName }}
        onError={handleErrors}
      >
        {({ data, loading }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || loading) { return <React.Fragment />; }
          const getData: ((callback: loadCallback) => void) = (
            callbackFn: (data: ICommentStructure[]) => void,
          ): void => {
            callbackFn(data.project.consulting.map((comment: ICommentStructure) => ({
              ...comment,
              created_by_current_user: comment.email === (window as typeof window & { userEmail: string }).userEmail,
              id: Number(comment.id),
              parent: Number(comment.parent),
            })));
          };

          return (
            <Mutation mutation={ADD_PROJECT_CONSULT} onError={handleAddCommentError}>
              {(addComment: MutationFunction): JSX.Element => {
                const handlePost: ((comment: ICommentStructure, callbackFn: postCallback) => void) = (
                  comment: ICommentStructure, callbackFn: postCallback,
                ): void => {
                  interface IMutationResult {
                    data: {
                      addProjectConsult: {
                        commentId: string;
                        success: boolean;
                      };
                    };
                  }

                  addComment({ variables: { projectName, ...comment } })
                    .then((mtResult: void | {}): void => {
                      const result: IMutationResult["data"] = (mtResult as IMutationResult).data;
                      if (result.addProjectConsult.success) {
                        callbackFn({ ...comment, id: Number(result.addProjectConsult.commentId) });
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
