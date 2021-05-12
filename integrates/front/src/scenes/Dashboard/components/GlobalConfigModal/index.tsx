import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { SwitchButton } from "components/SwitchButton";
import { TooltipWrapper } from "components/TooltipWrapper";
import {
  SUBSCRIBE_TO_ENTITY_REPORT,
  SUBSCRIPTIONS_TO_ENTITY_REPORT,
} from "scenes/Dashboard/components/GlobalConfigModal/queries";
import type { ISubscriptionsToEntityReport } from "scenes/Dashboard/components/GlobalConfigModal/types";
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
    (values: { digest: boolean }): void => {
      void subscribe({
        variables: {
          frequency: values.digest ? "DAILY" : "NEVER",
          reportEntity: "DIGEST",
          reportSubject: "ALL_GROUPS",
        },
      });
      setDigestSubscription(values.digest);
    },
    [subscribe, setDigestSubscription]
  );

  if (_.isUndefined(dataSubscriptions) || _.isEmpty(dataSubscriptions)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <Modal headerTitle={translate.t("configuration.title")} open={open}>
        <Formik
          enableReinitialize={true}
          initialValues={{
            digest: isDigestEnabled,
          }}
          name={"config"}
          onSubmit={onSubmitChange}
        >
          {({ values, dirty, setFieldValue }): JSX.Element => {
            function onHandleDigestChange(): void {
              setFieldValue("digest", !values.digest);
            }

            return (
              <Form>
                <Row>
                  <Col100>
                    <TooltipWrapper
                      id={"config.digest"}
                      message={translate.t("configuration.digest.tooltip")}
                      placement={"top"}
                    >
                      <FormGroup>
                        <div
                          className={"flex justify-between w-100 items-center"}
                        >
                          <ControlLabel>
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
                      </FormGroup>
                    </TooltipWrapper>
                  </Col100>
                </Row>
                <hr />
                <Row>
                  <Col100>
                    <ButtonToolbar>
                      <Button id={"config-close"} onClick={onClose}>
                        {translate.t("configuration.close")}
                      </Button>
                      <Button
                        disabled={!dirty || loading}
                        id={"config-confirm"}
                        type={"submit"}
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
