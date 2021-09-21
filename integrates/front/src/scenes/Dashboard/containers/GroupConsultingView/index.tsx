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
  ADD_GROUP_CONSULT,
  GET_GROUP_CONSULTING,
} from "scenes/Dashboard/containers/GroupConsultingView/queries";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IGroupConsultingData {
  group: {
    consulting: ICommentStructure[];
  };
}

const GroupConsultingView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const { userEmail }: IAuthContext = useContext(authContext);

  const handleAddConsultError: (addCommentError: ApolloError) => void = (
    addCommentError: ApolloError
  ): void => {
    addCommentError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
      if (message === "Exception - Comment parent is invalid") {
        msgError(translate.t("validations.invalidCommentParent", { count: 1 }));
      } else {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.error("An error occurred adding comment", addCommentError);
      }
    });
  };

  const handleErrors: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred loading group comments", error);
    });
  };

  const { data, loading } = useQuery<IGroupConsultingData>(
    GET_GROUP_CONSULTING,
    {
      fetchPolicy: "network-only",
      onError: handleErrors,
      variables: { groupName },
    }
  );

  const getData: (callback: ILoadCallback) => void = useCallback(
    (callbackFn: (cData: ICommentStructure[]) => void): void => {
      if (!_.isUndefined(data)) {
        callbackFn(
          data.group.consulting.map(
            (consult: ICommentStructure): ICommentStructure => ({
              ...consult,
              createdByCurrentUser: consult.email === userEmail,
              id: Number(consult.id),
              parent: Number(consult.parent),
            })
          )
        );
      }
    },
    [data, userEmail]
  );

  const [addConsult] = useMutation(ADD_GROUP_CONSULT, {
    onError: handleAddConsultError,
  });

  const handlePost: (
    consult: ICommentStructure,
    callbackFn: IPostCallback
  ) => void = useCallback(
    (consult: ICommentStructure, callbackFn: IPostCallback): void => {
      interface IMutationResult {
        data: {
          addGroupConsult: {
            commentId: string;
            success: boolean;
          };
        };
      }
      track("AddGroupComment", { groupName });
      void addConsult({ variables: { groupName, ...consult } }).then(
        (mtResult: unknown | null): void => {
          const result: IMutationResult["data"] = (mtResult as IMutationResult)
            .data;
          if (result.addGroupConsult.success) {
            callbackFn({
              ...consult,
              id: Number(result.addGroupConsult.commentId),
            });
          }
        }
      );
    },
    [addConsult, groupName]
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

export { GroupConsultingView };
