import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { Can } from "utils/authz/Can";
import { EditableField } from "scenes/Dashboard/components/EditableField";
import { Field } from "redux-form";
import { FluidIcon } from "components/FluidIcon";
import { GET_EVENT_HEADER } from "scenes/Dashboard/containers/EventContent/queries";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { GraphQLError } from "graphql";
import type { InjectedFormProps } from "redux-form";
import { Logger } from "utils/logger";
import { Modal } from "components/Modal";
import React from "react";
import _ from "lodash";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { useParams } from "react-router";
import {
  ButtonToolbar,
  Col100,
  Col50,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { DateTime, Text } from "utils/forms/fields";
import {
  GET_EVENT_DESCRIPTION,
  SOLVE_EVENT_MUTATION,
} from "scenes/Dashboard/containers/EventDescriptionView/queries";
import {
  dateTimeBeforeToday,
  numeric,
  required,
  validDatetime,
} from "utils/validations";
import { useMutation, useQuery } from "@apollo/react-hooks";

interface IEventDescriptionData {
  event: {
    accessibility: string;
    affectation: string;
    affectedComponents: string;
    analyst: string;
    client: string;
    detail: string;
    eventStatus: string;
    id: string;
  };
}

const EventDescriptionView: React.FC = (): JSX.Element => {
  const { eventId } = useParams<{ eventId: string }>();

  // State management
  const [isSolvingModalOpen, setSolvingModalOpen] = React.useState(false);
  const openSolvingModal: () => void = React.useCallback((): void => {
    setSolvingModalOpen(true);
  }, []);
  const closeSolvingModal: () => void = React.useCallback((): void => {
    setSolvingModalOpen(false);
  }, []);

  const handleErrors: (error: ApolloError) => void = React.useCallback(
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
      switch (message) {
        case "Exception - The event has already been closed":
          msgError(translate.t("group.events.alreadyClosed"));
          break;
        default:
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

  const handleSubmit: (
    values: Record<string, unknown>
  ) => void = React.useCallback(
    (values: Record<string, unknown>): void => {
      void solveEvent({ variables: { eventId, ...values } });
      closeSolvingModal();
    },
    [eventId, closeSolvingModal, solveEvent]
  );

  const handleDescriptionSubmit: () => void = React.useCallback(
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
          headerTitle={translate.t("search_findings.tab_severity.solve")}
          open={isSolvingModalOpen}
        >
          <GenericForm name={"solveEvent"} onSubmit={handleSubmit}>
            {({ pristine }: InjectedFormProps): React.ReactNode => (
              <React.Fragment>
                <Row>
                  <Col50>
                    <FormGroup>
                      <ControlLabel>
                        {translate.t("group.events.description.solved.date")}
                      </ControlLabel>
                      <Field
                        component={DateTime}
                        name={"date"}
                        validate={[
                          required,
                          validDatetime,
                          dateTimeBeforeToday,
                        ]}
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
                        component={Text}
                        name={"affectation"}
                        type={"number"}
                        validate={[required, numeric]}
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
                      <Button disabled={pristine || submitting} type={"submit"}>
                        {translate.t("confirmmodal.proceed")}
                      </Button>
                    </ButtonToolbar>
                  </Col100>
                </Row>
              </React.Fragment>
            )}
          </GenericForm>
        </Modal>
        <GenericForm
          initialValues={data.event}
          name={"editEvent"}
          onSubmit={handleDescriptionSubmit}
        >
          <div>
            <div>
              <Row>
                <ButtonToolbar>
                  <Can do={"backend_api_mutations_solve_event_mutate"}>
                    <Button
                      disabled={data.event.eventStatus === "SOLVED"}
                      onClick={openSolvingModal}
                    >
                      <FluidIcon icon={"verified"} />
                      &nbsp;
                      {translate.t("search_findings.tab_severity.solve")}
                    </Button>
                  </Can>
                </ButtonToolbar>
              </Row>
              <Row>
                <Col50>
                  <EditableField
                    alignField={"horizontalWide"}
                    component={Text}
                    currentValue={data.event.detail}
                    label={translate.t("search_findings.tabEvents.description")}
                    name={"detail"}
                    renderAsEditable={false}
                    type={"text"}
                  />
                </Col50>
                <Col50>
                  <EditableField
                    alignField={"horizontalWide"}
                    component={Text}
                    currentValue={data.event.client}
                    label={translate.t("search_findings.tabEvents.client")}
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
                    component={Text}
                    currentValue={data.event.analyst}
                    label={translate.t("search_findings.tabEvents.analyst")}
                    name={"analyst"}
                    renderAsEditable={false}
                    type={"text"}
                  />
                </Col50>
                <Col50>
                  <EditableField
                    alignField={"horizontalWide"}
                    component={Text}
                    currentValue={
                      _.isEmpty(data.event.affectation)
                        ? "-"
                        : data.event.affectation
                    }
                    label={translate.t("search_findings.tabEvents.affectation")}
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
                      component={Text}
                      currentValue={data.event.affectedComponents}
                      label={translate.t(
                        "search_findings.tabEvents.affectedComponents"
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
                    component={Text}
                    currentValue={data.event.accessibility}
                    label={translate.t("search_findings.tabEvents.eventIn")}
                    name={"accessibility"}
                    renderAsEditable={false}
                    type={"text"}
                  />
                </Col50>
              </Row>
            </div>
          </div>
        </GenericForm>
      </React.Fragment>
    </React.StrictMode>
  );
};

export { EventDescriptionView };
