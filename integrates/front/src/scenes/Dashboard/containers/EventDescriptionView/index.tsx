import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Button } from "components/Button";
import { FluidIcon } from "components/FluidIcon";
import { Modal, ModalFooter } from "components/Modal";
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
import {
  castAffectedComponents,
  formatAccessibility,
} from "utils/formatHelpers";
import {
  EditableField,
  FormikDateTime,
  FormikDropdown,
  FormikText,
} from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import {
  composeValidators,
  dateTimeBeforeToday,
  required,
  validDatetime,
} from "utils/validations";

interface IAffectedReattacks {
  findingId: string;
  where: string;
  specific: string;
}

interface IEventDescriptionData {
  event: {
    accessibility: string[];
    affectedComponents: string;
    affectedReattacks: IAffectedReattacks[];
    hacker: string;
    client: string;
    detail: string;
    eventStatus: string;
    id: string;
  };
}

const EventDescriptionView: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { eventId } = useParams<{ eventId: string }>();

  // State management
  const [isSolvingModalOpen, setIsSolvingModalOpen] = useState(false);
  const openSolvingModal: () => void = useCallback((): void => {
    setIsSolvingModalOpen(true);
  }, []);
  const closeSolvingModal: () => void = useCallback((): void => {
    setIsSolvingModalOpen(false);
  }, []);

  const handleErrors: (error: ApolloError) => void = useCallback(
    ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading event description", error);
      });
    },
    [t]
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
        msgError(t("group.events.alreadyClosed"));
      } else {
        msgError(t("groupAlerts.errorTextsad"));
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
      void solveEvent({
        variables: {
          date: values.date,
          eventId,
          other: values.other,
          reason: values.reason,
        },
      });
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
          onClose={closeSolvingModal}
          open={isSolvingModalOpen}
          title={t("searchFindings.tabSeverity.solve")}
        >
          <Formik
            enableReinitialize={true}
            initialValues={{ other: "", reason: "" }}
            name={"solveEvent"}
            onSubmit={handleSubmit}
          >
            {({ dirty, values }): React.ReactNode => (
              <Form id={"solveEvent"}>
                <Row>
                  <Col100>
                    <FormGroup>
                      <ControlLabel>
                        {t("group.events.description.solved.date")}
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
                  </Col100>
                  <Col100>
                    <FormGroup>
                      <ControlLabel>
                        {t(
                          "searchFindings.tabSeverity.common.deactivation.reason.label"
                        )}
                      </ControlLabel>
                      <Field
                        component={FormikDropdown}
                        name={"reason"}
                        validate={composeValidators([required])}
                      >
                        <option value={""} />
                        <option value={"PERMISSION_GRANTED"}>
                          {t(
                            "searchFindings.tabSeverity.common.deactivation.reason.permissionGranted"
                          )}
                        </option>
                        <option value={"PERMISSION_DENIED"}>
                          {t(
                            "searchFindings.tabSeverity.common.deactivation.reason.permissionDenied"
                          )}
                        </option>
                        <option value={"AFFECTED_RESOURCE_REMOVED_FROM_SCOPE"}>
                          {t(
                            "searchFindings.tabSeverity.common.deactivation.reason.removedFromScope"
                          )}
                        </option>
                        <option value={"SUPPLIES_WERE_GIVEN"}>
                          {t(
                            "searchFindings.tabSeverity.common.deactivation.reason.suppliesWereGiven"
                          )}
                        </option>
                        <option value={"TOE_CHANGE_APPROVED"}>
                          {t(
                            "searchFindings.tabSeverity.common.deactivation.reason.toeApproved"
                          )}
                        </option>
                        <option value={"TOE_WILL_REMAIN_UNCHANGED"}>
                          {t(
                            "searchFindings.tabSeverity.common.deactivation.reason.toeUnchanged"
                          )}
                        </option>
                        <option value={"PROBLEM_SOLVED"}>
                          {t(
                            "searchFindings.tabSeverity.common.deactivation.reason.problemSolved"
                          )}
                        </option>
                        <option value={"OTHER"}>
                          {t(
                            "searchFindings.tabSeverity.common.deactivation.reason.other"
                          )}
                        </option>
                      </Field>
                    </FormGroup>
                    {values.reason === "OTHER" ? (
                      <FormGroup>
                        <ControlLabel>
                          {t(
                            "searchFindings.tabSeverity.common.deactivation.other"
                          )}
                        </ControlLabel>
                        <Field
                          component={FormikText}
                          name={"other"}
                          validate={composeValidators([required])}
                        />
                      </FormGroup>
                    ) : undefined}
                  </Col100>
                </Row>
                {_.isEmpty(data.event.affectedReattacks) ? undefined : (
                  <Row>
                    <Col100>
                      {t("group.events.description.solved.holds", {
                        length: data.event.affectedReattacks.length,
                      })}
                    </Col100>
                  </Row>
                )}
                <ModalFooter>
                  <Button onClick={closeSolvingModal} variant={"secondary"}>
                    {t("confirmmodal.cancel")}
                  </Button>
                  <Button
                    disabled={!dirty || submitting}
                    type={"submit"}
                    variant={"primary"}
                  >
                    {t("confirmmodal.proceed")}
                  </Button>
                </ModalFooter>
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
                        variant={"primary"}
                      >
                        <FluidIcon icon={"verified"} />
                        &nbsp;
                        {t("searchFindings.tabSeverity.solve")}
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
                      label={t("searchFindings.tabEvents.description")}
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
                      label={t("searchFindings.tabEvents.client")}
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
                      label={t("searchFindings.tabEvents.hacker")}
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
                        _.isEmpty(data.event.affectedReattacks)
                          ? "0"
                          : String(data.event.affectedReattacks.length)
                      }
                      label={t("searchFindings.tabEvents.affectedReattacks")}
                      name={"affectedReattacks"}
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
                        currentValue={t(
                          castAffectedComponents(data.event.affectedComponents)
                        )}
                        label={t("searchFindings.tabEvents.affectedComponents")}
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
                      currentValue={data.event.accessibility
                        .map((item: string): string =>
                          translate.t(formatAccessibility(item))
                        )
                        .join(", ")}
                      label={t("searchFindings.tabEvents.eventIn")}
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
