import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { ColumnDef } from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useContext } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Col } from "components/Layout";
import { Table } from "components/Table";
import { Comments } from "scenes/Dashboard/components/Comments";
import type {
  ICommentStructure,
  ILoadCallback,
  IPostCallback,
} from "scenes/Dashboard/components/Comments/types";
import {
  ADD_GROUP_CONSULT,
  GET_GROUP_CONSULTING,
} from "scenes/Dashboard/containers/Group-Content/GroupConsultingView/queries";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { featurePreviewContext } from "utils/featurePreview";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface IGroupConsultingData {
  group: {
    consulting: ICommentStructure[];
  };
}

const GroupConsultingView: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { groupName } = useParams<{ groupName: string }>();
  const { userEmail }: IAuthContext = useContext(authContext);
  const { featurePreview } = useContext(featurePreviewContext);

  const handleAddConsultError: (addCommentError: ApolloError) => void = (
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
        default:
          msgError(t("groupAlerts.errorTextsad"));
          Logger.error("An error occurred adding comment", addCommentError);
      }
    });
  };

  const handleErrors: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(t("groupAlerts.errorTextsad"));
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
              parentComment: Number(consult.parentComment),
            })
          )
        );
      }
    },
    [data, userEmail]
  );

  const [addConsult] = useMutation(ADD_GROUP_CONSULT, {
    onError: handleAddConsultError,
    refetchQueries: [{ query: GET_GROUP_CONSULTING }, "GetGroupConsulting"],
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
      mixpanel.track("AddGroupComment", { groupName });
      void addConsult({
        variables: {
          content: consult.content,
          groupName,
          parentComment: consult.parentComment,
        },
      }).then(
        // Can also be string[] but the unknown type overrides it
        (mtResult: unknown): void => {
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
  interface IData {
    date: string;
    label: string;
    authorName: string;
  }

  const columns: ColumnDef<IData>[] = [
    {
      accessorKey: "date",
      header: "Date",
    },
    {
      accessorKey: "label",
      header: "Email",
    },
    {
      accessorKey: "authorName",
      header: "Created By",
    },
  ];

  const datasetTable: ICommentStructure[] = data.group.consulting;
  const datasetTables: IData[] = datasetTable
    .filter((comments): boolean => comments.parentComment < 1)
    .map((comment): IData => {
      return {
        authorName: comment.fullName,
        date: comment.created,
        label: comment.email,
      };
    });

  return featurePreview ? (
    <React.StrictMode>
      <div className={"flex justify-between"}>
        <Col>
          <Table columns={columns} data={datasetTables} id={"testTable"} />
        </Col>
        <Col>
          <Comments onLoad={getData} onPostComment={handlePost} />
        </Col>
      </div>
    </React.StrictMode>
  ) : (
    <React.StrictMode>
      <div>
        <Comments onLoad={getData} onPostComment={handlePost} />
      </div>
    </React.StrictMode>
  );
};

export { GroupConsultingView };
