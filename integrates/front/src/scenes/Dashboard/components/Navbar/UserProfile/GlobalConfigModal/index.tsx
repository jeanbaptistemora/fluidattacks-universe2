import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useState } from "react";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { SwitchButton } from "components/SwitchButton";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  SUBSCRIBE_TO_ENTITY_REPORT,
  SUBSCRIPTIONS_TO_ENTITY_REPORT,
} from "scenes/Dashboard/components/Navbar/UserProfile/GlobalConfigModal/queries";
import type { ISubscriptionsToEntityReport } from "scenes/Dashboard/components/Navbar/UserProfile/GlobalConfigModal/types";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IGlobalConfigModalProps {
  open: boolean;
  onClose: () => void;
}

const GlobalConfigModal: React.FC<IGlobalConfigModalProps> = (
  props: IGlobalConfigModalProps
): JSX.Element => {
  const { onClose, open } = props;
  const [isDigestEnabled, setDigestSubscription] = useState(false);
  const [isCommentsEnabled, setCommentsSubscription] = useState(false);

  const { data: dataSubscriptions } = useQuery<ISubscriptionsToEntityReport>(
    SUBSCRIPTIONS_TO_ENTITY_REPORT,
    {
      onCompleted: (result: ISubscriptionsToEntityReport): void => {
        setDigestSubscription(
          _.size(
            _.filter(result.me.subscriptionsToEntityReport, {
              entity: "DIGEST",
            })
          ) > 0
        );
        setCommentsSubscription(
          _.size(
            _.filter(result.me.subscriptionsToEntityReport, {
              entity: "COMMENTS",
            })
          ) > 0
        );
      },
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

  const [subscribe, { loading }] = useMutation(SUBSCRIBE_TO_ENTITY_REPORT, {
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

  const onSubmitChange = useCallback(
    (values: { digest: boolean; comments: boolean }): void => {
      if (values.digest !== isDigestEnabled) {
        void subscribe({
          variables: {
            frequency: values.digest ? "DAILY" : "NEVER",
            reportEntity: "DIGEST",
            reportSubject: "ALL_GROUPS",
          },
        });
        setDigestSubscription(values.digest);
        if (values.digest) {
          track("DailyDigestSubscribe");
        } else {
          track("DailyDigestUnsubscribe");
        }
      }
      if (values.comments !== isCommentsEnabled) {
        void subscribe({
          variables: {
            frequency: values.comments ? "DAILY" : "NEVER",
            reportEntity: "COMMENTS",
            reportSubject: "ALL_GROUPS",
          },
        });
        if (values.comments) {
          track("ConfigCommentsSubscribe");
        } else {
          track("ConfigCommentsUnsubscribe");
        }
        setCommentsSubscription(values.comments);
      }
    },
    [isDigestEnabled, isCommentsEnabled, subscribe]
  );

  if (_.isUndefined(dataSubscriptions) || _.isEmpty(dataSubscriptions)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t("configuration.title")}
        onClose={onClose}
        open={open}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{
            comments: isCommentsEnabled,
            digest: isDigestEnabled,
          }}
          name={"config"}
          onSubmit={onSubmitChange}
        >
          {({ values, dirty, setFieldValue }): JSX.Element => {
            function onHandleDigestChange(): void {
              setFieldValue("digest", !values.digest);
            }
            function onHandleCommentsChange(): void {
              setFieldValue("comments", !values.comments);
            }

            return (
              <Form>
                <Row>
                  <Col100>
                    <FormGroup>
                      <TooltipWrapper
                        id={"config.digest.tooltip"}
                        message={translate.t("configuration.digest.tooltip")}
                        placement={"top"}
                      >
                        <div
                          className={"flex justify-between w-100 items-center"}
                        >
                          <ControlLabel id={"config-digest-label"}>
                            {translate.t("configuration.digest.label")}
                          </ControlLabel>
                          <span className={"fr w-40"}>
                            <SwitchButton
                              checked={values.digest}
                              disabled={false}
                              name={"config-digest-switch"}
                              offlabel={translate.t(
                                "configuration.digest.unsubscribed"
                              )}
                              onChange={onHandleDigestChange}
                              onlabel={translate.t(
                                "configuration.digest.subscribed"
                              )}
                            />
                          </span>
                        </div>
                      </TooltipWrapper>
                      <br />
                      <TooltipWrapper
                        id={"config.comments.tooltip"}
                        message={translate.t("configuration.comments.tooltip")}
                        placement={"top"}
                      >
                        <div
                          className={"flex justify-between w-100 items-center"}
                        >
                          <ControlLabel id={"config-comments-label"}>
                            {translate.t("configuration.comments.label")}
                          </ControlLabel>
                          <span className={"fr w-40"}>
                            <SwitchButton
                              checked={values.comments}
                              disabled={false}
                              name={"config-comments-switch"}
                              offlabel={translate.t(
                                "configuration.comments.unsubscribed"
                              )}
                              onChange={onHandleCommentsChange}
                              onlabel={translate.t(
                                "configuration.comments.subscribed"
                              )}
                            />
                          </span>
                        </div>
                      </TooltipWrapper>
                    </FormGroup>
                  </Col100>
                </Row>
                <hr />
                <Row>
                  <Col100>
                    <ButtonToolbar>
                      <Button
                        id={"config-close"}
                        onClick={onClose}
                        variant={"secondary"}
                      >
                        {translate.t("configuration.close")}
                      </Button>
                      <Button
                        disabled={!dirty || loading}
                        id={"config-confirm"}
                        type={"submit"}
                        variant={"primary"}
                      >
                        {translate.t("configuration.confirm")}
                      </Button>
                    </ButtonToolbar>
                  </Col100>
                </Row>
              </Form>
            );
          }}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { IGlobalConfigModalProps, GlobalConfigModal };
