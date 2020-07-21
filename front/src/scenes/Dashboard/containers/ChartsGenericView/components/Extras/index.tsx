import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { ExecutionResult, GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import {
  ButtonToolbar,
  Col,
  Glyphicon,
  Grid,
  MenuItem,
  Panel,
  Row,
} from "react-bootstrap";
import { Badge } from "../../../../../../components/Badge";
import { Button } from "../../../../../../components/Button";
import { DropdownButton } from "../../../../../../components/DropdownButton";
import { TooltipWrapper } from "../../../../../../components/TooltipWrapper";
import { msgError, msgSuccess } from "../../../../../../utils/notifications";
import rollbar from "../../../../../../utils/rollbar";
import translate from "../../../../../../utils/translations/translate";
import styles from "../../index.css";
import {
  SUBSCRIBE_TO_ENTITY_REPORT,
  SUBSCRIPTIONS_TO_ENTITY_REPORT,
} from "../../queries";
import {
  IChartsGenericViewProps,
  ISubscriptionsToEntityReport,
  ISubscriptionToEntityReport,
} from "../../types";

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

  const downloadPngUrl: URL = new URL("/integrates/graphics-report", window.location.origin);
  downloadPngUrl.searchParams.set("entity", entity);
  downloadPngUrl.searchParams.set(entity, subject);

  const { data: dataSubscriptions, refetch: refetchSubscriptions } =
    useQuery<ISubscriptionsToEntityReport>(SUBSCRIPTIONS_TO_ENTITY_REPORT, {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(translate.t("group_alerts.error_textsad"));
          rollbar.error("An error occurred loading subscriptions info", error);
        });
      },
    });

  const [subscribe, { loading: loadingSubscribe }] = useMutation(SUBSCRIBE_TO_ENTITY_REPORT, {
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        rollbar.error("An error occurred subscribing to charts", message);
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
      <Grid fluid={true}>
        <Row>
          <Col md={12}>
            <Panel>
              <Panel.Body>
                <div className={styles.toolbarWrapper}>
                  <div className={styles.toolbarCentered}>
                    <ButtonToolbar block={true} justified={true}>
                      <Button
                        bsSize="large"
                        download={`charts-${entity}-${subject}.png`}
                        href={downloadPngUrl.toString()}
                      >
                        <Glyphicon glyph="save" /> {translate.t("analytics.sections.extras.download")}
                      </Button>
                      <DropdownButton
                        bsSize="large"
                        id="subscribe-dropdown"
                        onSelect={subscribeDropdownOnSelect}
                        title={
                          <React.Fragment>
                            {loadingSubscribe
                              ? <Glyphicon glyph="hourglass" />
                              : <Glyphicon glyph="stats" />}
                            {`   ${translateFrequency(subscriptionFrequency, "statement")}`}
                            <Badge>PLUS+</Badge>
                          </React.Fragment>
                        }
                      >
                        {frequencies.map((freq: string): JSX.Element => (
                          <MenuItem
                            eventKey={freq.toUpperCase()}
                            key={freq}
                          >
                            <TooltipWrapper
                              message={translateFrequencyArrivalTime(freq)}
                              placement="right"
                            >
                              <span>
                                {translateFrequency(freq, "action")}
                              </span>
                            </TooltipWrapper>
                          </MenuItem>
                        ))}
                      </DropdownButton>
                    </ButtonToolbar>
                  </div>
                </div>
              </Panel.Body>
            </Panel>
          </Col>
        </Row>
        <div className={styles.separatorTitleFromCharts} />
      </Grid>
    </React.StrictMode>
  );
};

export { chartsGenericViewExtras as ChartsGenericViewExtras };
