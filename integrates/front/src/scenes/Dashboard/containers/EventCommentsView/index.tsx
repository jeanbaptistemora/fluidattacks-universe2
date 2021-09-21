import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useContext } from "react";
import { useParams } from "react-router-dom";

import { Comments } from "scenes/Dashboard/components/Comments";
import type {
  ICommentStructure,
  ILoadCallback,
  IPostCallback,
} from "scenes/Dashboard/components/Comments/types";
import {
  ADD_EVENT_CONSULT,
  GET_EVENT_CONSULTING,
} from "scenes/Dashboard/containers/EventCommentsView/queries";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IEventConsultingData {
  event: {
    consulting: ICommentStructure[];
  };
}

const EventCommentsView: React.FC = (): JSX.Element => {
  const { eventId } = useParams<{ eventId: string }>();
  const { userEmail }: IAuthContext = useContext(authContext);

  const handleErrors: (error: ApolloError) => void = useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading event comments", error);
      });
    },
    []
  );

  const { data, loading } = useQuery<IEventConsultingData>(
    GET_EVENT_CONSULTING,
    {
      fetchPolicy: "network-only",
      onError: handleErrors,
      variables: { eventId },
    }
  );

  const getData: (callback: ILoadCallback) => void = useCallback(
    (callbackFn: (cData: ICommentStructure[]) => void): void => {
      if (!_.isUndefined(data)) {
        callbackFn(
          data.event.consulting.map(
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
    [data, userEmail]
  );

  const handleAddCommentError: (addCommentError: ApolloError) => void = (
    addCommentError: ApolloError
  ): void => {
    addCommentError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
      if (message === "Exception - Comment parent is invalid") {
        msgError(
          translate.t("validations.invalidCommentParent", {
            count: 1,
          })
        );
      } else {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred posting event comment",
          addCommentError
        );
      }
    });
  };

  const [addComment] = useMutation(ADD_EVENT_CONSULT, {
    onError: handleAddCommentError,
  });

  const handlePost: (
    comment: ICommentStructure,
    callbackFn: IPostCallback
  ) => void = useCallback(
    (comment: ICommentStructure, callbackFn: IPostCallback): void => {
      interface IMutationResult {
        data: {
          addEventConsult: {
            commentId: string;
            success: boolean;
          };
        };
      }
      track("AddEventComment", { eventId });
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
    },
    [addComment, eventId]
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

export { EventCommentsView };
