/* eslint-disable no-underscore-dangle */
import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback } from "react";

import { Table } from "components/Table";
import type { IHeaderConfig } from "components/Table/types";
import {
  GET_SUBSCRIPTIONS,
  SUBSCRIBE_TO_ENTITY_REPORT,
  SUBSCRIPTIONS_TO_ENTITY_REPORT,
} from "scenes/Dashboard/containers/NotificationsView/queries";
import type {
  ISubscriptionName,
  ISubscriptionNameDataSet,
  ISubscriptionToEntityReport,
  ISubscriptionsNames,
  ISubscriptionsToEntityReport,
} from "scenes/Dashboard/containers/NotificationsView/types";
import { Col40, RowCenter } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const NotificationsView: React.FC = (): JSX.Element => {
  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "name",
      header: translate.t("searchFindings.notificationTable.notification"),
      width: "99%",
    },
    {
      dataField: "subscribeEmail",
      header: translate.t("searchFindings.notificationTable.email"),
      width: "1%",
    },
  ];

  const { data: dataEnum } = useQuery<ISubscriptionsNames>(GET_SUBSCRIPTIONS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("configuration.errorText"));
        Logger.warning(
          "An error occurred loading the subscriptions info",
          error
        );
      });
    },
  });

  const { data: dataSubscriptions, refetch } =
    useQuery<ISubscriptionsToEntityReport>(SUBSCRIPTIONS_TO_ENTITY_REPORT, {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(translate.t("configuration.errorText"));
          Logger.warning(
            "An error occurred loading the subscriptions info",
            error
          );
        });
      },
    });

  const [subscribe] = useMutation(SUBSCRIBE_TO_ENTITY_REPORT, {
    onCompleted: (): void => {
      void refetch();
    },
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        msgError(translate.t("configuration.errorText"));
        Logger.warning(
          "An error occurred changing the subscriptions info",
          message
        );
      });
    },
  });

  const handleSubmit = useCallback(
    (entityName: string, isSubscribe: boolean): void => {
      void subscribe({
        variables: {
          frequency: isSubscribe ? "DAILY" : "NEVER",
          reportEntity: entityName,
          reportSubject: "ALL_GROUPS",
        },
      });
    },
    [subscribe]
  );

  const subscriptionsToEntity: ISubscriptionToEntityReport[] =
    _.isUndefined(dataSubscriptions) || _.isEmpty(dataSubscriptions)
      ? []
      : dataSubscriptions.me.subscriptionsToEntityReport;

  const subscriptions: ISubscriptionName[] =
    _.isUndefined(dataEnum) || _.isEmpty(dataEnum)
      ? []
      : dataEnum.__type.enumValues.map(
          (subscription: ISubscriptionName): ISubscriptionNameDataSet => {
            const isSubscribe =
              _.size(
                _.filter(subscriptionsToEntity, {
                  entity: subscription.name,
                })
              ) > 0;
            function onChange(): void {
              handleSubmit(subscription.name, !isSubscribe);
            }

            return {
              name: translate.t(
                `searchFindings.enumValues.${subscription.name}`
              ),
              subscribeEmail: (
                <Col40>
                  <input
                    checked={isSubscribe}
                    onChange={onChange}
                    type={"checkbox"}
                  />
                </Col40>
              ),
            };
          }
        );

  const exceptions = ["GROUP", "ORGANIZATION", "PORTFOLIO"];

  const filterByName = (subscription: ISubscriptionName): boolean =>
    !exceptions.includes(subscription.name);

  const subscriptionsFiltered = subscriptions.filter(filterByName);

  return (
    <React.StrictMode>
      <div>
        <RowCenter>
          <Col40>
            <Table
              bordered={true}
              dataset={subscriptionsFiltered}
              exportCsv={false}
              headers={tableHeaders}
              id={"tblNotifications"}
              pageSize={10}
              search={false}
            />
          </Col40>
        </RowCenter>
      </div>
    </React.StrictMode>
  );
};

export { NotificationsView };
