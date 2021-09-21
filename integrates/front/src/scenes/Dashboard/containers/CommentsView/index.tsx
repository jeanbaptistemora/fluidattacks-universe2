import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useContext } from "react";
import { useParams } from "react-router-dom";

import { handleAddCommentErrorHelper } from "./helpers";

import { Comments } from "scenes/Dashboard/components/Comments";
import type {
  ICommentStructure,
  ILoadCallback,
  IPostCallback,
} from "scenes/Dashboard/components/Comments/types";
import {
  ADD_FINDING_CONSULT,
  GET_FINDING_CONSULTING,
  GET_FINDING_OBSERVATIONS,
} from "scenes/Dashboard/containers/CommentsView/queries";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

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

  const handleAddCommentError: (addCommentError: ApolloError) => void =
    useCallback(
      (addCommentError: ApolloError): void => {
        handleAddCommentErrorHelper(addCommentError, type);
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
              createdByCurrentUser: comment.email === userEmail,
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
      <div>
        <Comments onLoad={getData} onPostComment={handlePost} />
      </div>
    </React.StrictMode>
  );
};

export { CommentsView };
