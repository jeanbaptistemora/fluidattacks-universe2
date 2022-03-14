/* eslint-disable no-underscore-dangle */
import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback } from "react";

import { Card, CardBody, CardHeader } from "components/Card";
import { Col, Row } from "components/Layout";
import { SwitchButton } from "components/SwitchButton";
import {
  GET_SUBSCRIPTIONS,
  UPDATE_NOTIFICATIONS_PREFERENCES,
} from "scenes/Dashboard/containers/NotificationsView/queries";
import type {
  ISubscriptionName,
  ISubscriptionsNames,
} from "scenes/Dashboard/containers/NotificationsView/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const NotificationsView: React.FC = (): JSX.Element => {
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
          (subscription: ISubscriptionName): ISubscriptionName => {
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
                <SwitchButton
                  checked={isSubscribe}
                  id={"emailSwitch"}
                  offlabel={"Off"}
                  onChange={onChange}
                  onlabel={"On"}
                />
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
        <Row>
          {subscriptionsFiltered.map((item: ISubscriptionName): JSX.Element => {
            return (
              <Col key={item.name} large={"25"} medium={"50"} small={"50"}>
                <Card>
                  <CardHeader>{item.name}</CardHeader>
                  <CardBody>
                    <Row>
                      <Col large={"70"} medium={"70"} small={"70"}>
                        {translate.t("searchFindings.notificationTable.email")}
                      </Col>
                      <Col large={"30"} medium={"30"} small={"30"}>
                        {item.subscribeEmail}
                      </Col>
                    </Row>
                  </CardBody>
                </Card>
              </Col>
            );
          })}
        </Row>
      </div>
    </React.StrictMode>
  );
};

export { NotificationsView };
