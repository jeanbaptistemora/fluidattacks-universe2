/* eslint-disable no-underscore-dangle */
/* eslint-disable react/forbid-component-props */
import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback } from "react";

import { Card } from "components/Card";
import { Col, Row } from "components/Layout";
import { NumberInput } from "components/NumberInput";
import { Switch } from "components/Switch";
import { Tooltip } from "components/Tooltip";
import {
  GET_SUBSCRIPTIONS,
  UPDATE_NOTIFICATIONS_PREFERENCES,
} from "scenes/Dashboard/containers/NotificationsView/queries";
import type {
  INotificationsPreferences,
  ISubscriptionName,
  ISubscriptionsNames,
} from "scenes/Dashboard/containers/NotificationsView/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const { t } = translate;

const NotificationsView: React.FC = (): JSX.Element => {
  const { data: dataEnum, refetch } = useQuery<ISubscriptionsNames>(
    GET_SUBSCRIPTIONS,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("configuration.errorText"));
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
        msgError(t("configuration.errorText"));
        Logger.warning(
          "An error occurred changing the subscriptions info",
          message
        );
      });
    },
  });

  const handleSubmit = useCallback(
    (email: string[], severity: number, sms: string[]): void => {
      void updateSubscription({
        variables: {
          email,
          severity,
          sms,
        },
      });
    },
    [updateSubscription]
  );

  const onChangeSeverity = useCallback(
    (
      listSubscription: INotificationsPreferences
    ): ((newValue: number | undefined) => void) => {
      return (newValue: number | undefined): void => {
        if (!_.isUndefined(newValue)) {
          handleSubmit(listSubscription.email, newValue, listSubscription.sms);
        }
      };
    },
    [handleSubmit]
  );

  const subscriptions: ISubscriptionName[] =
    _.isUndefined(dataEnum) || _.isEmpty(dataEnum)
      ? []
      : dataEnum.Notifications.enumValues.map(
          (subscription: ISubscriptionName): ISubscriptionName => {
            const listSubscription = dataEnum.me.notificationsPreferences;
            const severity =
              dataEnum.me.notificationsPreferences.parameters.minSeverity;

            const isSubscribe = (sub: string[] | string): boolean =>
              sub.includes(subscription.name);

            const newListSubs = (listSub: string[]): string[] =>
              isSubscribe(listSub)
                ? listSub.filter((sub: string): boolean => !isSubscribe(sub))
                : [subscription.name, ...listSub];

            const onChangeMail = (listSub: string[]): (() => void) => {
              const newListMail = (): void => {
                const newListEmailSubs = newListSubs(listSub);
                handleSubmit(newListEmailSubs, severity, listSubscription.sms);
              };

              return newListMail;
            };

            const onChangeSms = (listSub: string[]): (() => void) => {
              const newListSms = (): void => {
                const newListSmsSubs = newListSubs(listSub);
                handleSubmit(listSubscription.email, severity, newListSmsSubs);
              };

              return newListSms;
            };

            return {
              minSeverity: (
                <NumberInput
                  autoUpdate={true}
                  decimalPlaces={1}
                  defaultValue={severity}
                  max={10}
                  min={0}
                  onEnter={onChangeSeverity(listSubscription)}
                />
              ),
              name: t(`searchFindings.enumValues.${subscription.name}.name`),
              subscribeEmail: (
                <Switch
                  checked={isSubscribe(listSubscription.email)}
                  label={{ off: "", on: "" }}
                  onChange={onChangeMail(listSubscription.email)}
                />
              ),
              subscribeSms: (
                <Switch
                  checked={isSubscribe(listSubscription.sms)}
                  label={{ off: "", on: "" }}
                  onChange={onChangeSms(listSubscription.sms)}
                />
              ),
              tooltip: t(
                `searchFindings.enumValues.${subscription.name}.tooltip`
              ),
            };
          }
        );

  const defaultExceptions = ["ACCESS_GRANTED", "GROUP_REPORT"];

  const exceptions =
    _.isUndefined(dataEnum) || _.isEmpty(dataEnum)
      ? defaultExceptions
      : [
          ...defaultExceptions,
          dataEnum.me.userEmail.endsWith("@fluidattacks.com")
            ? undefined
            : "Draft updates",
        ];

  const filterByName = (subscription: ISubscriptionName): boolean =>
    !exceptions.includes(subscription.name);

  const subscriptionsFiltered = subscriptions.filter(filterByName);

  return (
    <React.StrictMode>
      <Row>
        {subscriptionsFiltered.map(
          (item: ISubscriptionName): JSX.Element => (
            <React.Fragment key={item.name}>
              <Col lg={25} md={50} sm={100}>
                <Tooltip
                  id={`${item.name.toLowerCase().replace(" ", "_")}_tooltip`}
                  tip={item.tooltip}
                >
                  <Card title={item.name}>
                    <div className={"flex justify-between mt1"}>
                      {t("searchFindings.notificationTable.email")}
                      {item.subscribeEmail}
                    </div>
                    <div className={"flex justify-between mt1"}>
                      {t("searchFindings.notificationTable.sms")}
                      {item.subscribeSms}
                    </div>
                  </Card>
                </Tooltip>
              </Col>
              {item.name ===
                t("searchFindings.enumValues.VULNERABILITY_REPORT.name") && (
                <Col key={item.name} lg={25} md={50} sm={100}>
                  <Tooltip
                    id={`${t(
                      "searchFindings.notificationTable.parameters.minimumSeverity.name"
                    )
                      .toLowerCase()
                      .replace(" ", "_")}_tooltip`}
                    tip={t(
                      "searchFindings.notificationTable.parameters.minimumSeverity.tooltip"
                    )}
                  >
                    <Card
                      title={t(
                        "searchFindings.notificationTable.parameters.minimumSeverity.name"
                      )}
                    >
                      <div className={"flex justify-between mt1"}>
                        {item.minSeverity}
                      </div>
                    </Card>
                  </Tooltip>
                </Col>
              )}
            </React.Fragment>
          )
        )}
      </Row>
    </React.StrictMode>
  );
};

export { NotificationsView };
