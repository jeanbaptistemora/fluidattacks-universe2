import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useContext } from "react";
import { useTranslation } from "react-i18next";
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

interface IEventConsultingData {
  event: {
    consulting: ICommentStructure[];
  };
}

const EventCommentsView: React.FC = (): JSX.Element => {
  const { eventId } = useParams<{ eventId: string }>();
  const { userEmail }: IAuthContext = useContext(authContext);
  const { t } = useTranslation();

  const handleErrors: (error: ApolloError) => void = useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading event comments", error);
      });
    },
    [t]
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
              parentComment: Number(comment.parentComment),
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
      switch (message) {
        case "Exception - Invalid field length in form":
          msgError(t("validations.invalidFieldLength"));
          break;
        case "Exception - Comment parent is invalid":
          msgError(t("validations.invalidCommentParent", { count: 1 }));
          break;
        case "Exception - Invalid characters":
          msgError(t("validations.invalidChar"));
          break;
        default:
          msgError(t("groupAlerts.errorTextsad"));
          Logger.error(
            "An error occurred posting event comment",
            addCommentError
          );
      }
    });
  };

  const [addComment] = useMutation(ADD_EVENT_CONSULT, {
    onError: handleAddCommentError,
  });

  const handlePost = useCallback(
    async (
      comment: ICommentStructure,
      callbackFn: IPostCallback
    ): Promise<void> => {
      interface IMutationResult {
        data: {
          addEventConsult: {
            commentId: string;
            success: boolean;
          };
        };
      }
      mixpanel.track("AddEventComment", { eventId });
      await addComment({ variables: { eventId, ...comment } }).then(
        // Can also have the null type but unknown overrides it
        (mtResult: unknown): void => {
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
