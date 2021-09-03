import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _, { toString } from "lodash";
import React, { useCallback, useState } from "react";
import { useParams } from "react-router-dom";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { Modal } from "components/Modal";
import { GET_EVENT_HEADER } from "scenes/Dashboard/containers/EventContent/queries";
import {
  GET_EVENT_DESCRIPTION,
  SOLVE_EVENT_MUTATION,
} from "scenes/Dashboard/containers/EventDescriptionView/queries";
import {
  ButtonToolbar,
  Col100,
  Col50,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { castAffectedComponents } from "utils/formatHelpers";
import { EditableField, FormikDateTime, FormikText } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import {
  composeValidators,
  dateTimeBeforeToday,
  numeric,
  required,
  validDatetime,
} from "utils/validations";

interface IEventDescriptionData {
  event: {
    accessibility: string;
    affectation: string;
    affectedComponents: string;
    hacker: string;
    client: string;
    detail: string;
    eventStatus: string;
    id: string;
  };
}

const EventDescriptionView: React.FC = (): JSX.Element => {
  const { eventId } = useParams<{ eventId: string }>();

  // State management
  const [isSolvingModalOpen, setSolvingModalOpen] = useState(false);
  const openSolvingModal: () => void = useCallback((): void => {
    setSolvingModalOpen(true);
  }, []);
  const closeSolvingModal: () => void = useCallback((): void => {
    setSolvingModalOpen(false);
  }, []);

  const handleErrors: (error: ApolloError) => void = useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading event description", error);
      });
    },
    []
  );

  const { data, refetch } = useQuery<IEventDescriptionData>(
    GET_EVENT_DESCRIPTION,
    {
      onError: handleErrors,
      variables: { eventId },
    }
  );

  const handleUpdateResult: () => void = (): void => {
    void refetch();
  };

  const handleUpdateError: (updateError: ApolloError) => void = (
    updateError: ApolloError
  ): void => {
    updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
      if (message === "Exception - The event has already been closed") {
        msgError(translate.t("group.events.alreadyClosed"));
      } else {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred updating event", updateError);
      }
    });
  };

  const [solveEvent, { loading: submitting }] = useMutation(
    SOLVE_EVENT_MUTATION,
    {
      onCompleted: handleUpdateResult,
      onError: handleUpdateError,
      refetchQueries: [{ query: GET_EVENT_HEADER, variables: { eventId } }],
    }
  );

  const handleSubmit: (values: Record<string, unknown>) => void = useCallback(
    (values: Record<string, unknown>): void => {
      const castValues = {
        affectation: toString(values.affectation),
        date: values.date,
      };
      void solveEvent({ variables: { eventId, ...castValues } });
      closeSolvingModal();
    },
    [eventId, closeSolvingModal, solveEvent]
  );

  const handleDescriptionSubmit: () => void = useCallback(
    (): void => undefined,
    []
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <React.Fragment>
        <Modal
          headerTitle={translate.t("searchFindings.tabSeverity.solve")}
          onEsc={closeSolvingModal}
          open={isSolvingModalOpen}
        >
          <Formik
            enableReinitialize={true}
            initialValues={{}}
            name={"solveEvent"}
            onSubmit={handleSubmit}
          >
            {({ dirty }): React.ReactNode => (
              <Form id={"solveEvent"}>
                <Row>
                  <Col50>
                    <FormGroup>
                      <ControlLabel>
                        {translate.t("group.events.description.solved.date")}
                      </ControlLabel>
                      <Field
                        component={FormikDateTime}
                        name={"date"}
                        validate={composeValidators([
                          required,
                          validDatetime,
                          dateTimeBeforeToday,
                        ])}
                      />
                    </FormGroup>
                  </Col50>
                  <Col50>
                    <FormGroup>
                      <ControlLabel>
                        {translate.t(
                          "group.events.description.solved.affectation"
                        )}
                      </ControlLabel>
                      <Field
                        component={FormikText}
                        name={"affectation"}
                        type={"number"}
                        validate={composeValidators([required, numeric])}
                      />
                    </FormGroup>
                  </Col50>
                </Row>
                <hr />
                <Row>
                  <Col100>
                    <ButtonToolbar>
                      <Button onClick={closeSolvingModal}>
                        {translate.t("confirmmodal.cancel")}
                      </Button>
                      <Button disabled={!dirty || submitting} type={"submit"}>
                        {translate.t("confirmmodal.proceed")}
                      </Button>
                    </ButtonToolbar>
                  </Col100>
                </Row>
              </Form>
            )}
          </Formik>
        </Modal>
        <Formik
          initialValues={data.event}
          name={"editEvent"}
          onSubmit={handleDescriptionSubmit}
        >
          <Form id={"editEvent"}>
            <div>
              <div>
                <Row>
                  <ButtonToolbar>
                    <Can do={"api_mutations_solve_event_mutate"}>
                      <Button
                        disabled={data.event.eventStatus === "SOLVED"}
                        onClick={openSolvingModal}
                      >
                        <FluidIcon icon={"verified"} />
                        &nbsp;
                        {translate.t("searchFindings.tabSeverity.solve")}
                      </Button>
                    </Can>
                  </ButtonToolbar>
                </Row>
                <Row>
                  <Col50>
                    <EditableField
                      alignField={"horizontalWide"}
                      component={FormikText}
                      currentValue={data.event.detail}
                      label={translate.t(
                        "searchFindings.tabEvents.description"
                      )}
                      name={"detail"}
                      renderAsEditable={false}
                      type={"text"}
                    />
                  </Col50>
                  <Col50>
                    <EditableField
                      alignField={"horizontalWide"}
                      component={FormikText}
                      currentValue={data.event.client}
                      label={translate.t("searchFindings.tabEvents.client")}
                      name={"client"}
                      renderAsEditable={false}
                      type={"text"}
                    />
                  </Col50>
                </Row>
                <Row>
                  <Col50>
                    <EditableField
                      alignField={"horizontalWide"}
                      component={FormikText}
                      currentValue={data.event.hacker}
                      label={translate.t("searchFindings.tabEvents.hacker")}
                      name={"hacker"}
                      renderAsEditable={false}
                      type={"text"}
                    />
                  </Col50>
                  <Col50>
                    <EditableField
                      alignField={"horizontalWide"}
                      component={FormikText}
                      currentValue={
                        _.isEmpty(data.event.affectation)
                          ? "-"
                          : data.event.affectation
                      }
                      label={translate.t(
                        "searchFindings.tabEvents.affectation"
                      )}
                      name={"affectation"}
                      renderAsEditable={false}
                      type={"text"}
                    />
                  </Col50>
                </Row>
                <Row>
                  {_.isEmpty(data.event.affectedComponents) ? undefined : (
                    <Col50>
                      <EditableField
                        alignField={"horizontalWide"}
                        component={FormikText}
                        currentValue={translate.t(
                          castAffectedComponents(data.event.affectedComponents)
                        )}
                        label={translate.t(
                          "searchFindings.tabEvents.affectedComponents"
                        )}
                        name={"affectedComponents"}
                        renderAsEditable={false}
                        type={"text"}
                      />
                    </Col50>
                  )}
                  <Col50>
                    <EditableField
                      alignField={"horizontalWide"}
                      component={FormikText}
                      currentValue={data.event.accessibility}
                      label={translate.t("searchFindings.tabEvents.eventIn")}
                      name={"accessibility"}
                      renderAsEditable={false}
                      type={"text"}
                    />
                  </Col50>
                </Row>
              </div>
            </div>
          </Form>
        </Formik>
      </React.Fragment>
    </React.StrictMode>
  );
};

export { EventDescriptionView };
