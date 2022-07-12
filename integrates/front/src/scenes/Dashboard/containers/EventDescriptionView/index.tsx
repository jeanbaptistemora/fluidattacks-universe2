import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faCheck, faPen } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import type {
  IEventDescriptionData,
  IUpdateEventSolvingReasonAttr,
} from "./types";

import { Button } from "components/Button";
import { Modal, ModalConfirm } from "components/Modal";
import { GET_EVENT_HEADER } from "scenes/Dashboard/containers/EventContent/queries";
import {
  GET_EVENT_DESCRIPTION,
  SOLVE_EVENT_MUTATION,
  UPDATE_EVENT_SOLVING_REASON_MUTATION,
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
import { EditableField, FormikDropdown, FormikText } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { composeValidators, required } from "utils/validations";

const EventDescriptionView: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { eventId } = useParams<{ eventId: string }>();

  const solvingReason: Record<string, string> = {
    AFFECTED_RESOURCE_REMOVED_FROM_SCOPE: t(
      "searchFindings.tabSeverity.common.deactivation.reason.removedFromScope"
    ),
    OTHER: t("searchFindings.tabSeverity.common.deactivation.reason.other"),
    PERMISSION_DENIED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.permissionDenied"
    ),
    PERMISSION_GRANTED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.permissionGranted"
    ),
    PROBLEM_SOLVED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.problemSolved"
    ),
    SUPPLIES_WERE_GIVEN: t(
      "searchFindings.tabSeverity.common.deactivation.reason.suppliesWereGiven"
    ),
    TOE_CHANGE_APPROVED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.toeApproved"
    ),
    TOE_WILL_REMAIN_UNCHANGED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.toeUnchanged"
    ),
  };

  // State management
  const [isSolvingModalOpen, setIsSolvingModalOpen] = useState(false);
  const [isEditingSolvingReason, setIsEditingSolvingReason] = useState(false);
  const openSolvingModal: () => void = useCallback((): void => {
    setIsSolvingModalOpen(true);
    setIsEditingSolvingReason(false);
  }, []);
  const openEditReasonModal: () => void = useCallback((): void => {
    setIsSolvingModalOpen(true);
    setIsEditingSolvingReason(true);
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
      refetchQueries: [
        { query: GET_EVENT_HEADER, variables: { eventId } },
        GET_EVENT_DESCRIPTION,
      ],
    }
  );

  const [updateEventSolvingReason] = useMutation(
    UPDATE_EVENT_SOLVING_REASON_MUTATION,
    {
      onCompleted: (mtResult: IUpdateEventSolvingReasonAttr): void => {
        if (mtResult.updateEventSolvingReason.success) {
          msgSuccess(
            t("group.events.description.alerts.editSolvingReason.success"),
            t("groupAlerts.updatedTitle")
          );
        }
      },
      onError: (error: ApolloError): void => {
        error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          switch (message) {
            case "Exception - The event has not been solved":
              msgError(
                t(
                  `group.events.description.alerts.editSolvingReason.nonSolvedEvent`
                )
              );
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning(
                "An error occurred updating the event solving reason",
                error
              );
          }
        });
      },
      refetchQueries: [GET_EVENT_DESCRIPTION],
    }
  );

  const handleSubmit: (values: Record<string, unknown>) => void = useCallback(
    (values: Record<string, unknown>): void => {
      const otherReason = values.reason === "OTHER" ? values.other : undefined;
      if (isEditingSolvingReason) {
        void updateEventSolvingReason({
          variables: {
            eventId,
            other: otherReason,
            reason: values.reason,
          },
        });
      } else {
        void solveEvent({
          variables: {
            eventId,
            other: otherReason,
            reason: values.reason,
          },
        });
      }

      closeSolvingModal();
    },
    [
      eventId,
      closeSolvingModal,
      isEditingSolvingReason,
      solveEvent,
      updateEventSolvingReason,
    ]
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
          title={
            isEditingSolvingReason
              ? t("group.events.description.editSolvingReason")
              : t("group.events.description.markAsSolved")
          }
        >
          <Formik
            enableReinitialize={true}
            initialValues={
              isEditingSolvingReason
                ? {
                    other: data.event.otherSolvingReason,
                    reason: data.event.solvingReason,
                  }
                : { other: "", reason: "" }
            }
            name={"solvingReason"}
            onSubmit={handleSubmit}
          >
            {({ dirty, values }): React.ReactNode => (
              <Form id={"solvingReason"}>
                <Row>
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
                          {solvingReason.PERMISSION_GRANTED}
                        </option>
                        <option value={"PERMISSION_DENIED"}>
                          {solvingReason.PERMISSION_DENIED}
                        </option>
                        <option value={"AFFECTED_RESOURCE_REMOVED_FROM_SCOPE"}>
                          {solvingReason.AFFECTED_RESOURCE_REMOVED_FROM_SCOPE}
                        </option>
                        <option value={"SUPPLIES_WERE_GIVEN"}>
                          {solvingReason.SUPPLIES_WERE_GIVEN}
                        </option>
                        <option value={"TOE_CHANGE_APPROVED"}>
                          {solvingReason.TOE_CHANGE_APPROVED}
                        </option>
                        <option value={"TOE_WILL_REMAIN_UNCHANGED"}>
                          {solvingReason.TOE_WILL_REMAIN_UNCHANGED}
                        </option>
                        <option value={"PROBLEM_SOLVED"}>
                          {solvingReason.PROBLEM_SOLVED}
                        </option>
                        <option value={"OTHER"}>{solvingReason.OTHER}</option>
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
                {_.isEmpty(data.event.affectedReattacks) ||
                isEditingSolvingReason ? undefined : (
                  <Row>
                    <Col100>
                      {t("group.events.description.solved.holds", {
                        length: data.event.affectedReattacks.length,
                      })}
                    </Col100>
                  </Row>
                )}
                <ModalConfirm
                  disabled={!dirty || submitting}
                  onCancel={closeSolvingModal}
                />
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
                    {data.event.eventStatus === "SOLVED" ? (
                      <Can
                        do={"api_mutations_update_event_solving_reason_mutate"}
                      >
                        <Button
                          onClick={openEditReasonModal}
                          variant={"primary"}
                        >
                          <FontAwesomeIcon icon={faPen} />
                          &nbsp;
                          {t("group.events.description.editSolvingReason")}
                        </Button>
                      </Can>
                    ) : (
                      <Can do={"api_mutations_solve_event_mutate"}>
                        <Button onClick={openSolvingModal} variant={"primary"}>
                          <FontAwesomeIcon icon={faCheck} />
                          &nbsp;
                          {t("group.events.description.markAsSolved")}
                        </Button>
                      </Can>
                    )}
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
                        currentValue={data.event.affectedComponents
                          .map((item: string): string =>
                            translate.t(castAffectedComponents(item))
                          )
                          .join(", ")}
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
                {data.event.eventStatus === "SOLVED" ? (
                  <Row>
                    {data.event.solvingReason === "OTHER" ? (
                      <Col50>
                        <EditableField
                          alignField={"horizontalWide"}
                          component={FormikText}
                          currentValue={
                            _.isNil(data.event.otherSolvingReason)
                              ? "-"
                              : _.capitalize(data.event.otherSolvingReason)
                          }
                          label={t("searchFindings.tabEvents.solvingReason")}
                          name={"otherSolvingReason"}
                          renderAsEditable={false}
                          type={"text"}
                        />
                      </Col50>
                    ) : (
                      <Col50>
                        <EditableField
                          alignField={"horizontalWide"}
                          component={FormikText}
                          currentValue={
                            _.isNil(data.event.solvingReason)
                              ? "-"
                              : solvingReason[data.event.solvingReason]
                          }
                          label={t("searchFindings.tabEvents.solvingReason")}
                          name={"solvingReason"}
                          renderAsEditable={false}
                          type={"text"}
                        />
                      </Col50>
                    )}
                  </Row>
                ) : undefined}
              </div>
            </div>
          </Form>
        </Formik>
      </React.Fragment>
    </React.StrictMode>
  );
};

export { EventDescriptionView };
