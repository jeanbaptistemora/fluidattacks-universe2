import { useMutation, useQuery } from "@apollo/react-hooks";
import { faChartBar, faDownload, faHourglassHalf } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { ApolloError } from "apollo-client";
import { ExecutionResult, GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";

import { Badge } from "components/Badge";
import { Button } from "components/Button";
import { DropdownButton, MenuItem } from "components/DropdownButton";
import { TooltipWrapper } from "components/TooltipWrapper";
import mixpanel from "mixpanel-browser";
import styles from "scenes/Dashboard/containers/ChartsGenericView/index.css";
import {
  SUBSCRIBE_TO_ENTITY_REPORT,
  SUBSCRIPTIONS_TO_ENTITY_REPORT,
} from "scenes/Dashboard/containers/ChartsGenericView/queries";
import {
  EntityType,
  IChartsGenericViewProps,
  ISubscriptionsToEntityReport,
  ISubscriptionToEntityReport,
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

const frequencies: string[] = [
  "daily",
  "weekly",
  "monthly",
  "never",
];

const translateFrequency: (freq: string, kind: "action" | "statement") => string =
(freq: string, kind: "action" | "statement"): string => (
  translate.t(`analytics.sections.extras.frequencies.${kind}.${freq}`)
);

const translateFrequencyArrivalTime: (freq: string) => string =
(freq: string): string => (
  translate.t(`analytics.sections.extras.frequenciesArrivalTime.${freq}`)
);

const chartsGenericViewExtras: React.FC<IChartsGenericViewProps> = (props: IChartsGenericViewProps): JSX.Element => {
  const { entity, subject } = props;

  const entityName: EntityType = entity;
  const downloadPngUrl: URL = new URL("/graphics-report", window.location.origin);
  downloadPngUrl.searchParams.set("entity", entity);
  downloadPngUrl.searchParams.set(entityName, subject);

  const { data: dataSubscriptions, refetch: refetchSubscriptions } =
    useQuery<ISubscriptionsToEntityReport>(SUBSCRIPTIONS_TO_ENTITY_REPORT, {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(translate.t("group_alerts.error_textsad"));
          Logger.warning("An error occurred loading subscriptions info", error);
        });
      },
    });

  const [subscribe, { loading: loadingSubscribe }] = useMutation(SUBSCRIBE_TO_ENTITY_REPORT, {
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred subscribing to charts", message);
      });
    },
  });

  if (_.isUndefined(dataSubscriptions) || _.isEmpty(dataSubscriptions)) {
    return <React.Fragment />;
  }

  const subscriptions: ISubscriptionToEntityReport[] =
    dataSubscriptions.me.subscriptionsToEntityReport.filter(
      (value: ISubscriptionToEntityReport) => (
        value.entity.toLowerCase() === entity.toLowerCase()
        && value.subject.toLocaleLowerCase() === subject.toLowerCase()
      ),
    );

  const subscribeDropdownOnSelect: (key: string) => void =
    (key: string): void => {
      mixpanel.track(`Analytics${key === "never" ? "Uns" : "S"}ubscribe`);
      subscribe({
        variables: {
          frequency: key.toUpperCase(),
          reportEntity: entity.toUpperCase(),
          reportSubject: subject,
        },
      })
      .then(async (value: ExecutionResult<{ subscribeToEntityReport: { success: boolean } }>) => {
        if (
          value.data !== null
          && value.data !== undefined
          && value.data.subscribeToEntityReport.success
        ) {
          if (key.toLowerCase() === "never") {
            msgSuccess(
              translate.t("analytics.sections.extras.unsubscribedSuccessfully.msg"),
              translate.t("analytics.sections.extras.unsubscribedSuccessfully.title"),
            );
          } else {
            msgSuccess(
              translate.t("analytics.sections.extras.subscribedSuccessfully.msg"),
              translate.t("analytics.sections.extras.subscribedSuccessfully.title"),
            );
          }
          await refetchSubscriptions();
        }
      });
    };

  const subscriptionFrequency: string =
    _.isEmpty(subscriptions) ? "never" : subscriptions[0].frequency.toLowerCase();

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
                      <a
                        download={`charts-${entity}-${subject}.png`}
                        href={downloadPngUrl.toString()}
                        className={"mr2"}
                      >
                        <Button
                          className={"pv3"}
                        >
                          <FontAwesomeIcon icon={faDownload} />
                            {translate.t("analytics.sections.extras.download")}
                          <Badge>pro</Badge>
                        </Button>
                      </a>
                      <DropdownButton
                        id="subscribe-dropdown"
                        width={"suscribeDropdownBtn"}
                        content={
                          <React.Fragment>
                            <div className={"tc"}>
                              {loadingSubscribe
                                ? <FontAwesomeIcon icon={faHourglassHalf} />
                                : <FontAwesomeIcon icon={faChartBar} />}
                              {`   ${translateFrequency(subscriptionFrequency, "statement")}`}
                              <Badge>pro</Badge>
                            </div>
                          </React.Fragment>
                        }
                        items={
                          frequencies.map((freq: string): JSX.Element => (
                            <TooltipWrapper
                              id={freq}
                              key={freq}
                              message={translateFrequencyArrivalTime(freq)}
                              placement="right"
                            >
                              <MenuItem
                                eventKey={freq}
                                key={freq}
                                onClick={subscribeDropdownOnSelect}
                                itemContent={
                                  <React.Fragment>
                                      <span>
                                        {translateFrequency(freq, "action")}
                                      </span>
                                  </React.Fragment>
                                }
                              />
                            </TooltipWrapper>

                        ))}
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

export { chartsGenericViewExtras as ChartsGenericViewExtras };
