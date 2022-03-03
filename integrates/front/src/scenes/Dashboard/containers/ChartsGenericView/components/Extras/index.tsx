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
import { track } from "mixpanel-browser";
import React from "react";

import {
  getSubscriptionFrequency,
  translateFrequency,
  translateFrequencyArrivalTime,
} from "./helpers";

import { Button } from "components/Button";
import { DropdownButton, MenuItem } from "components/DropdownButton";
import { ExternalLink } from "components/ExternalLink";
import { TooltipWrapper } from "components/TooltipWrapper";
import styles from "scenes/Dashboard/containers/ChartsGenericView/index.css";
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
import {
  ButtonToolbarCenter,
  Col100,
  Container,
  Panel,
  PanelBody,
  Row,
} from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const frequencies: string[] = ["daily", "weekly", "monthly", "never"];

const ChartsGenericViewExtras: React.FC<IChartsGenericViewProps> = (
  props: IChartsGenericViewProps
): JSX.Element => {
  const { entity, subject } = props;

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
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred loading subscriptions info", error);
        });
      },
    });

  const [subscribe, { loading: loadingSubscribe }] = useMutation(
    SUBSCRIBE_TO_ENTITY_REPORT,
    {
      onError: (updateError: ApolloError): void => {
        updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred subscribing to charts", message);
        });
      },
    }
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

  const subscribeDropdownOnSelect: (key: string) => void = (
    key: string
  ): void => {
    track(`Analytics${key === "never" ? "Uns" : "S"}ubscribe`);
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
              translate.t(
                "analytics.sections.extras.unsubscribedSuccessfully.msg"
              ),
              translate.t(
                "analytics.sections.extras.unsubscribedSuccessfully.title"
              )
            );
          } else {
            msgSuccess(
              translate.t(
                "analytics.sections.extras.subscribedSuccessfully.msg"
              ),
              translate.t(
                "analytics.sections.extras.subscribedSuccessfully.title"
              )
            );
          }
          await refetchSubscriptions();
        }
      }
    );
  };

  const subscriptionFrequency = getSubscriptionFrequency(subscriptions);

  return (
    <React.StrictMode>
      <Container>
        <Row>
          <Col100>
            <Panel>
              <PanelBody>
                <div className={styles.toolbarWrapper}>
                  <div className={styles.toolbarCentered}>
                    <ButtonToolbarCenter>
                      <ExternalLink
                        // eslint-disable-next-line react/forbid-component-props
                        className={"mr2"}
                        download={`charts-${entity}-${subject}.png`}
                        href={downloadPngUrl.toString()}
                      >
                        <Button variant={"secondary"}>
                          <FontAwesomeIcon icon={faDownload} />
                          &nbsp;
                          {translate.t("analytics.sections.extras.download")}
                        </Button>
                      </ExternalLink>
                      <DropdownButton
                        content={
                          <div className={"tc"}>
                            {loadingSubscribe ? (
                              <FontAwesomeIcon icon={faHourglassHalf} />
                            ) : (
                              <FontAwesomeIcon icon={faChartBar} />
                            )}
                            {`   ${translateFrequency(
                              subscriptionFrequency,
                              "statement"
                            )}`}
                          </div>
                        }
                        id={"subscribe-dropdown"}
                        items={frequencies.map(
                          (freq: string): JSX.Element => (
                            <TooltipWrapper
                              id={freq}
                              key={freq}
                              message={translateFrequencyArrivalTime(freq)}
                              placement={"right"}
                            >
                              <MenuItem
                                eventKey={freq}
                                itemContent={
                                  <span>
                                    {translateFrequency(freq, "action")}
                                  </span>
                                }
                                key={freq}
                                // eslint-disable-next-line react/jsx-no-bind
                                onClick={subscribeDropdownOnSelect}
                              />
                            </TooltipWrapper>
                          )
                        )}
                        scrollInto={false}
                      />
                    </ButtonToolbarCenter>
                  </div>
                </div>
              </PanelBody>
            </Panel>
          </Col100>
        </Row>
        <div className={styles.separatorTitleFromCharts} />
      </Container>
    </React.StrictMode>
  );
};

export { ChartsGenericViewExtras };
