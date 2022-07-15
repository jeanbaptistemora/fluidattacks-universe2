import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import {
  faChartBar,
  faDownload,
  faHourglassHalf,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ExecutionResult, GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import {
  getSubscriptionFrequency,
  translateFrequency,
  translateFrequencyArrivalTime,
} from "./helpers";

import { Button } from "components/Button";
import { Dropdown } from "components/Dropdown";
import { ExternalLink } from "components/ExternalLink";
import { Gap } from "components/Layout";
import { Tooltip } from "components/Tooltip";
import {
  SUBSCRIBE_TO_ENTITY_REPORT,
  SUBSCRIPTIONS_TO_ENTITY_REPORT,
} from "scenes/Dashboard/containers/ChartsGenericView/queries";
import type {
  EntityType,
  IChartsGenericViewProps,
  ISubscriptionToEntityReport,
  ISubscriptionsToEntityReport,
} from "scenes/Dashboard/containers/ChartsGenericView/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const frequencies: string[] = ["daily", "weekly", "monthly", "never"];

const ChartsGenericViewExtras: React.FC<IChartsGenericViewProps> = ({
  entity,
  subject,
}: IChartsGenericViewProps): JSX.Element => {
  const { t } = useTranslation();
  const entityName: EntityType = entity;
  const downloadPngUrl: URL = new URL(
    "/graphics-report",
    window.location.origin
  );
  downloadPngUrl.searchParams.set("entity", entity);
  downloadPngUrl.searchParams.set(entityName, subject);

  const { data: dataSubscriptions, refetch: refetchSubscriptions } =
    useQuery<ISubscriptionsToEntityReport>(SUBSCRIPTIONS_TO_ENTITY_REPORT, {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred loading subscriptions info", error);
        });
      },
    });

  const [subscribe, { loading: loadingSubscribe }] = useMutation(
    SUBSCRIBE_TO_ENTITY_REPORT,
    {
      onError: (updateError: ApolloError): void => {
        updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred subscribing to charts", message);
        });
      },
    }
  );

  const subscribeDropdownOnSelect = useCallback(
    (key: string): void => {
      mixpanel.track(`Analytics${key === "never" ? "Uns" : "S"}ubscribe`);
      void subscribe({
        variables: {
          frequency: key.toUpperCase(),
          reportEntity: entity.toUpperCase(),
          reportSubject: subject,
        },
      }).then(
        async (
          value: ExecutionResult<{
            subscribeToEntityReport: { success: boolean };
          }>
        ): Promise<void> => {
          if (
            // eslint-disable-next-line @typescript-eslint/prefer-optional-chain
            value.data !== null &&
            value.data !== undefined &&
            value.data.subscribeToEntityReport.success
          ) {
            if (key.toLowerCase() === "never") {
              msgSuccess(
                t("analytics.sections.extras.unsubscribedSuccessfully.msg"),
                t("analytics.sections.extras.unsubscribedSuccessfully.title")
              );
            } else {
              msgSuccess(
                t("analytics.sections.extras.subscribedSuccessfully.msg"),
                t("analytics.sections.extras.subscribedSuccessfully.title")
              );
            }
            await refetchSubscriptions();
          }
        }
      );
    },
    [entity, refetchSubscriptions, subject, subscribe, t]
  );

  if (_.isUndefined(dataSubscriptions) || _.isEmpty(dataSubscriptions)) {
    return <div />;
  }

  const subscriptions: ISubscriptionToEntityReport[] =
    dataSubscriptions.me.subscriptionsToEntityReport.filter(
      (value: ISubscriptionToEntityReport): boolean =>
        value.entity.toLowerCase() === entity.toLowerCase() &&
        value.subject.toLocaleLowerCase() === subject.toLowerCase()
    );

  const subscriptionFrequency = getSubscriptionFrequency(subscriptions);

  return (
    <React.StrictMode>
      <Gap>
        <ExternalLink
          download={`charts-${entity}-${subject}.png`}
          href={downloadPngUrl.toString()}
        >
          <Button variant={"primary"}>
            <FontAwesomeIcon icon={faDownload} />
            &nbsp;
            {t("analytics.sections.extras.download")}
          </Button>
        </ExternalLink>
        <Dropdown
          button={
            <Button variant={"secondary"}>
              <FontAwesomeIcon
                icon={loadingSubscribe ? faHourglassHalf : faChartBar}
              />
              &nbsp;
              {translateFrequency(subscriptionFrequency, "statement")}
            </Button>
          }
          id={"subscribe-dropdown"}
        >
          {frequencies.map(
            (freq: string): JSX.Element => (
              <Tooltip
                id={freq}
                key={freq}
                place={"right"}
                tip={translateFrequencyArrivalTime(freq)}
              >
                <div className={"flex flex-column"}>
                  <Button
                    onClick={function fn2(): void {
                      subscribeDropdownOnSelect(freq);
                    }}
                  >
                    {translateFrequency(freq, "action")}
                  </Button>
                </div>
              </Tooltip>
            )
          )}
        </Dropdown>
      </Gap>
    </React.StrictMode>
  );
};

export { ChartsGenericViewExtras };
