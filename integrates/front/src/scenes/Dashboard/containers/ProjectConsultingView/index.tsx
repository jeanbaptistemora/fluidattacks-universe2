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
import { ADD_PROJECT_CONSULT, GET_PROJECT_CONSULTING } from "./queries";

type IProjectConsultingViewProps = RouteComponentProps<{ projectName: string }>;

const projectConsultingView: React.FC<IProjectConsultingViewProps> =
  (props: IProjectConsultingViewProps): JSX.Element => {
  const { projectName } = props.match.params;
  const onMount: (() => void) = (): void => {
    mixpanel.track("ProjectComments", {
      User: (window as typeof window & { userName: string }).userName,
    });
  };
  React.useEffect(onMount, []);

  const handleAddConsultError: ((addCommentError: ApolloError) => void) =
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
            callbackFn(data.project.consulting.map((consult: ICommentStructure) => ({
              ...consult,
              created_by_current_user: consult.email === (window as typeof window & { userEmail: string }).userEmail,
              id: Number(consult.id),
              parent: Number(consult.parent),
            })));
          };

          return (
            <Mutation mutation={ADD_PROJECT_CONSULT} onError={handleAddConsultError}>
              {(addConsult: MutationFunction): JSX.Element => {
                const handlePost: ((consult: ICommentStructure, callbackFn: postCallback) => void) = (
                  consult: ICommentStructure, callbackFn: postCallback,
                ): void => {
                  interface IMutationResult {
                    data: {
                      addProjectConsult: {
                        commentId: string;
                        success: boolean;
                      };
                    };
                  }

                  addConsult({ variables: { projectName, ...consult } })
                    .then((mtResult: void | {}): void => {
                      const result: IMutationResult["data"] = (mtResult as IMutationResult).data;
                      if (result.addProjectConsult.success) {
                        callbackFn({ ...consult, id: Number(result.addProjectConsult.commentId) });
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

export { projectConsultingView as ProjectConsultingView };
