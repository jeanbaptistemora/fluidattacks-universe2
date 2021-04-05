import { useMutation, useQuery } from "@apollo/react-hooks";
import type { ApolloError } from "apollo-client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useContext } from "react";
import { useParams } from "react-router";

import { Comments } from "scenes/Dashboard/components/Comments/index";
import type {
  ICommentStructure,
  ILoadCallback,
  IPostCallback,
} from "scenes/Dashboard/components/Comments/types";
import { CommentsRefac } from "scenes/Dashboard/components/CommentsRefac/index";
import {
  ADD_PROJECT_CONSULT,
  GET_PROJECT_CONSULTING,
} from "scenes/Dashboard/containers/ProjectConsultingView/queries";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IProjectConsultingData {
  project: {
    consulting: ICommentStructure[];
  };
}

const ProjectConsultingView: React.FC = (): JSX.Element => {
  const { projectName } = useParams<{ projectName: string }>();
  const { userEmail }: IAuthContext = useContext(authContext);

  const handleAddConsultError: (addCommentError: ApolloError) => void = (
    addCommentError: ApolloError
  ): void => {
    addCommentError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
      switch (message) {
        case "Exception - Comment parent is invalid":
          msgError(
            translate.t("validations.invalidCommentParent", { count: 1 })
          );
          break;
        default:
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred updating exploit", addCommentError);
      }
    });
  };

  const handleErrors: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred loading project comments", error);
    });
  };

  const { data, loading } = useQuery<IProjectConsultingData>(
    GET_PROJECT_CONSULTING,
    {
      fetchPolicy: "network-only",
      onError: handleErrors,
      variables: { projectName },
    }
  );

  const getData: (callback: ILoadCallback) => void = useCallback(
    (callbackFn: (cData: ICommentStructure[]) => void): void => {
      if (!_.isUndefined(data)) {
        callbackFn(
          data.project.consulting.map(
            (consult: ICommentStructure): ICommentStructure => ({
              ...consult,
              // eslint-disable-next-line camelcase -- It is possibly required for the API
              created_by_current_user: consult.email === userEmail,
              id: Number(consult.id),
              parent: Number(consult.parent),
            })
          )
        );
      }
    },
    [data, userEmail]
  );

  const [addConsult] = useMutation(ADD_PROJECT_CONSULT, {
    onError: handleAddConsultError,
  });

  const handlePost: (
    consult: ICommentStructure,
    callbackFn: IPostCallback
  ) => void = useCallback(
    (consult: ICommentStructure, callbackFn: IPostCallback): void => {
      interface IMutationResult {
        data: {
          addProjectConsult: {
            commentId: string;
            success: boolean;
          };
        };
      }
      track("AddGroupComment", { projectName });
      void addConsult({ variables: { projectName, ...consult } }).then(
        (mtResult: unknown | null): void => {
          const result: IMutationResult["data"] = (mtResult as IMutationResult)
            .data;
          if (result.addProjectConsult.success) {
            callbackFn({
              ...consult,
              id: Number(result.addProjectConsult.commentId),
            });
          }
        }
      );
    },
    [addConsult, projectName]
  );

  if (_.isUndefined(data) || loading) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <Comments
        id={"project-comments"}
        onLoad={getData}
        onPostComment={handlePost}
      />
      {userEmail === "integratesmanager@fluidattacks.com" ? (
        <CommentsRefac onLoad={getData} onPostComment={handlePost} />
      ) : null}
    </React.StrictMode>
  );
};

export { ProjectConsultingView };
