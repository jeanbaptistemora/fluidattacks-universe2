import type { ApolloError } from "apollo-client";
import { Comments } from "scenes/Dashboard/components/Comments/index";
import type { GraphQLError } from "graphql";
import type { IAuthContext } from "utils/auth";
import { Logger } from "utils/logger";
import _ from "lodash";
import { authContext } from "utils/auth";
import { msgError } from "utils/notifications";
import { track } from "mixpanel-browser";
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
import React, { useCallback, useContext } from "react";
import { useMutation, useQuery } from "@apollo/react-hooks";

interface ICommentsData {
  finding: {
    consulting: ICommentStructure[];
    observations: ICommentStructure[];
  };
}

const CommentsView: React.FC = (): JSX.Element => {
  const params: { findingId: string; type: string } = useParams();
  const { findingId } = params;
  const PARAM_NO_OBSERVATIONS: number = -3;
  const type: string =
    params.type === "observations"
      ? params.type.slice(0, -1)
      : params.type.slice(0, PARAM_NO_OBSERVATIONS);

  const { userEmail }: IAuthContext = useContext(authContext);

  const handleErrors: (error: ApolloError) => void = useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(`An error occurred loading finding ${type}`, error);
      });
    },
    [type]
  );

  const handleAddCommentError: (
    addCommentError: ApolloError
  ) => void = useCallback(
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
              msgError(translate.t("groupAlerts.errorTextsad"));
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

  const { data, loading } = useQuery<ICommentsData>(
    type === "consult" ? GET_FINDING_CONSULTING : GET_FINDING_OBSERVATIONS,
    {
      onError: handleErrors,
      variables: { findingId },
    }
  );

  const getData: (callback: ILoadCallback) => void = useCallback(
    (callbackFn: (cData: ICommentStructure[]) => void): void => {
      if (!_.isUndefined(data)) {
        const comments: ICommentStructure[] =
          type === "consult"
            ? data.finding.consulting
            : data.finding.observations;
        callbackFn(
          comments.map(
            (comment: ICommentStructure): ICommentStructure => ({
              ...comment,
              // eslint-disable-next-line camelcase -- It is possibly required for the API
              created_by_current_user: comment.email === userEmail,
              id: Number(comment.id),
              parent: Number(comment.parent),
            })
          )
        );
      }
    },
    [data, type, userEmail]
  );

  const [addComment] = useMutation(ADD_FINDING_CONSULT, {
    onError: handleAddCommentError,
  });

  const handlePost: (
    comment: ICommentStructure,
    callbackFn: IPostCallback
  ) => void = useCallback(
    (comment: ICommentStructure, callbackFn: IPostCallback): void => {
      interface IMutationResult {
        data: {
          addFindingConsult: {
            commentId: string;
            success: boolean;
          };
        };
      }
      track(`Add${_.capitalize(type)}`, { findingId });
      void addComment({
        variables: {
          findingId,
          type: type.toUpperCase(),
          ...comment,
        },
      }).then((mtResult: unknown | null): void => {
        const result: IMutationResult["data"] = (mtResult as IMutationResult)
          .data;
        if (result.addFindingConsult.success) {
          callbackFn({
            ...comment,
            id: Number(result.addFindingConsult.commentId),
          });
        }
      });
    },
    [addComment, findingId, type]
  );

  if (_.isUndefined(data) || loading) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <Comments
        id={`finding-${type}`}
        onLoad={getData}
        onPostComment={handlePost}
      />
    </React.StrictMode>
  );
};

export { CommentsView };
