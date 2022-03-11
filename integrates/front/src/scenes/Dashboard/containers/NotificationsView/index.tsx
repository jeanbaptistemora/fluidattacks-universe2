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
  UPDATE_NOTIFICATIONS_PREFERENCES,
} from "scenes/Dashboard/containers/NotificationsView/queries";
import type {
  ISubscriptionName,
  ISubscriptionNameDataSet,
  ISubscriptionsNames,
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

  const { data: dataEnum, refetch } = useQuery<ISubscriptionsNames>(
    GET_SUBSCRIPTIONS,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(translate.t("configuration.errorText"));
          Logger.warning(
            "An error occurred loading the subscriptions info",
            error
          );
        });
      },
    }
  );

  const [updateSubscription] = useMutation(UPDATE_NOTIFICATIONS_PREFERENCES, {
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
    (notificationsPreferences: string[]): void => {
      void updateSubscription({
        variables: {
          notificationsPreferences,
        },
      });
    },
    [updateSubscription]
  );

  const subscriptions: ISubscriptionName[] =
    _.isUndefined(dataEnum) || _.isEmpty(dataEnum)
      ? []
      : dataEnum.Notifications.enumValues.map(
          (subscription: ISubscriptionName): ISubscriptionNameDataSet => {
            const listSubscription = dataEnum.me.notificationsPreferences.email;
            const isSubscribe = listSubscription.includes(subscription.name);

            function onChange(): void {
              const newListSubs = isSubscribe
                ? listSubscription.filter(
                    (sub: string): boolean => !sub.includes(subscription.name)
                  )
                : [subscription.name, ...listSubscription];
              handleSubmit(newListSubs);
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

  const exceptions = ["ACCESS_GRANTED", "GROUP_REPORT"];

  const filterByName = (subscription: ISubscriptionName): boolean =>
    !exceptions.includes(subscription.name);

  const subscriptionsFiltered = subscriptions.filter(filterByName);

  return (
    <React.StrictMode>
      <div>
        <RowCenter>
          <Col40>
            <Table
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
