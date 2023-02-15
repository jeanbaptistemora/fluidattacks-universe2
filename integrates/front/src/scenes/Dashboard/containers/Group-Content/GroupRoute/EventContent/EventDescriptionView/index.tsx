import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { Fragment, useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";
import { object, string } from "yup";

import { ActionButtons } from "./ActionButtons";
import type {
  IDescriptionFormValues,
  IEventDescriptionData,
  IRejectEventSolutionResultAttr,
  IUpdateEventAttr,
} from "./types";

import { Input, Select } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import { RemediationModal } from "scenes/Dashboard/components/RemediationModal";
import {
  GET_EVENT_DESCRIPTION,
  REJECT_EVENT_SOLUTION_MUTATION,
  SOLVE_EVENT_MUTATION,
  UPDATE_EVENT_MUTATION,
} from "scenes/Dashboard/containers/Group-Content/GroupRoute/EventContent/EventDescriptionView/queries";
import { GET_EVENT_HEADER } from "scenes/Dashboard/containers/Group-Content/GroupRoute/EventContent/queries";
import {
  Col100,
  Col50,
  ControlLabel,
  EditableFieldTitle50,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { authzPermissionsContext } from "utils/authz/config";
import { castEventType } from "utils/formatHelpers";
import { EditableField, FormikDropdown, FormikText } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { composeValidators, required } from "utils/validations";

const EventDescriptionView: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { eventId } = useParams<{ eventId: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateEvent: boolean = permissions.can(
    "api_mutations_update_event_mutate"
  );

  const solvingReasons: Record<string, string> = {
    ACCESS_GRANTED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.accessGranted"
    ),
    AFFECTED_RESOURCE_REMOVED_FROM_SCOPE: t(
      "searchFindings.tabSeverity.common.deactivation.reason.removedFromScope"
    ),
    CLONED_SUCCESSFULLY: t(
      "searchFindings.tabSeverity.common.deactivation.reason.clonedSuccessfully"
    ),
    CREDENTIALS_ARE_WORKING_NOW: t(
      "searchFindings.tabSeverity.common.deactivation.reason.credentialsAreWorkingNow"
    ),
    DATA_UPDATED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.dataUpdated"
    ),
    ENVIRONMENT_IS_WORKING_NOW: t(
      "searchFindings.tabSeverity.common.deactivation.reason.environmentIsWorkingNow"
    ),
    INSTALLER_IS_WORKING_NOW: t(
      "searchFindings.tabSeverity.common.deactivation.reason.installerIsWorkingNow"
    ),
    IS_OK_TO_RESUME: t(
      "searchFindings.tabSeverity.common.deactivation.reason.isOkToResume"
    ),
    NEW_CREDENTIALS_PROVIDED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.newCredentialsProvided"
    ),
    NEW_ENVIRONMENT_PROVIDED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.newEnvironmentProvided"
    ),
    OTHER: t("searchFindings.tabSeverity.common.deactivation.reason.other"),
    PERMISSION_DENIED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.permissionDenied"
    ),
    PERMISSION_GRANTED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.permissionGranted"
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
  const allSolvingReasons: Record<string, string> = {
    ...solvingReasons,
    PROBLEM_SOLVED: t(
      "searchFindings.tabSeverity.common.deactivation.reason.problemSolved"
    ),
  };
  const solutionReasonByEventType: Record<string, string[]> = {
    AUTHORIZATION_SPECIAL_ATTACK: ["PERMISSION_DENIED", "PERMISSION_GRANTED"],
    CLIENT_CANCELS_PROJECT_MILESTONE: ["OTHER"],
    CLIENT_EXPLICITLY_SUSPENDS_PROJECT: [
      "IS_OK_TO_RESUME",
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "OTHER",
    ],
    CLONING_ISSUES: [
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "CLONED_SUCCESSFULLY",
    ],
    CREDENTIAL_ISSUES: [
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "CREDENTIALS_ARE_WORKING_NOW",
      "NEW_CREDENTIALS_PROVIDED",
    ],
    DATA_UPDATE_REQUIRED: [
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "DATA_UPDATED",
      "OTHER",
    ],
    ENVIRONMENT_ISSUES: [
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "ENVIRONMENT_IS_WORKING_NOW",
      "NEW_ENVIRONMENT_PROVIDED",
    ],
    INSTALLER_ISSUES: [
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "INSTALLER_IS_WORKING_NOW",
      "OTHER",
    ],
    MISSING_SUPPLIES: [
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "SUPPLIES_WERE_GIVEN",
      "OTHER",
    ],
    NETWORK_ACCESS_ISSUES: [
      "PERMISSION_GRANTED",
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "OTHER",
    ],
    OTHER: ["OTHER"],
    REMOTE_ACCESS_ISSUES: [
      "ACCESS_GRANTED",
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "OTHER",
    ],
    TOE_DIFFERS_APPROVED: ["TOE_CHANGE_APPROVED", "TOE_WILL_REMAIN_UNCHANGED"],
    VPN_ISSUES: [
      "ACCESS_GRANTED",
      "AFFECTED_RESOURCE_REMOVED_FROM_SCOPE",
      "OTHER",
    ],
  };

  // State management
  const [isSolvingModalOpen, setIsSolvingModalOpen] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const openSolvingModal: () => void = useCallback((): void => {
    setIsSolvingModalOpen(true);
  }, []);
  const closeSolvingModal: () => void = useCallback((): void => {
    setIsSolvingModalOpen(false);
  }, []);
  const toggleEdit: () => void = useCallback((): void => {
    setIsEditing(!isEditing);
  }, [isEditing]);

  const [isRejectSolutionModalOpen, setIsRejectSolutionModalOpen] =
    useState(false);
  const openRejectSolutionModal: () => void = useCallback((): void => {
    setIsRejectSolutionModalOpen(true);
  }, []);
  const closeRejectSolutionModal: () => void = useCallback((): void => {
    setIsRejectSolutionModalOpen(false);
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

  const [rejectSolution] = useMutation(REJECT_EVENT_SOLUTION_MUTATION, {
    onCompleted: (mtResult: IRejectEventSolutionResultAttr): void => {
      if (mtResult.rejectEventSolution.success) {
        msgSuccess(
          t("group.events.description.alerts.rejectSolution.success"),
          t("groupAlerts.updatedTitle")
        );
        setIsRejectSolutionModalOpen(false);
      }
    },
    onError: (error: ApolloError): void => {
      error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Event not found":
            msgError(
              t(
                `group.events.description.alerts.editSolvingReason.eventNotFound`
              )
            );
            break;
          case "Exception - The event verification has not been requested":
            msgError(
              t(
                "group.events.description.alerts.rejectSolution.nonRequestedVerification"
              )
            );
            break;
          case "Exception - The event has already been closed":
            msgError(t("group.events.alreadyClosed"));
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.warning(
              "An error occurred rejecting the event solution",
              error
            );
        }
      });
    },
    refetchQueries: [GET_EVENT_HEADER, GET_EVENT_DESCRIPTION],
  });

  const [updateEvent] = useMutation(UPDATE_EVENT_MUTATION, {
    onCompleted: (mtResult: IUpdateEventAttr): void => {
      if (mtResult.updateEvent.success) {
        msgSuccess(
          t("group.events.description.alerts.editEvent.success"),
          t("groupAlerts.updatedTitle")
        );
        setIsEditing(false);
      }
    },
    onError: (error: ApolloError): void => {
      error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Exception - Event not found":
            msgError(
              t(`group.events.description.alerts.editEvent.eventNotFound`)
            );
            break;
          case "Exception - The event has not been solved":
            msgError(
              t(`group.events.description.alerts.editEvent.nonSolvedEvent`)
            );
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.warning("An error occurred updating the event", error);
        }
      });
    },
    refetchQueries: [GET_EVENT_DESCRIPTION],
  });

  const handleRejectSolution: (values: Record<string, unknown>) => void =
    useCallback(
      (values: Record<string, unknown>): void => {
        void rejectSolution({
          variables: {
            comments: values.treatmentJustification,
            eventId,
          },
        });
        closeRejectSolutionModal();
      },
      [eventId, closeRejectSolutionModal, rejectSolution]
    );

  const handleSubmit: (values: Record<string, unknown>) => void = useCallback(
    (values: Record<string, unknown>): void => {
      const otherReason = values.reason === "OTHER" ? values.other : undefined;
      void solveEvent({
        variables: {
          eventId,
          other: otherReason,
          reason: values.reason,
        },
      });
      closeSolvingModal();
    },
    [eventId, closeSolvingModal, solveEvent]
  );

  const handleDescriptionSubmit: (values: IDescriptionFormValues) => void =
    useCallback(
      (values: IDescriptionFormValues): void => {
        const otherSolvingReason =
          values.solvingReason === "OTHER"
            ? values.otherSolvingReason
            : undefined;

        if (!_.isUndefined(data)) {
          void updateEvent({
            variables: {
              eventId,
              eventType: values.eventType,
              otherSolvingReason,
              solvingReason: values.solvingReason,
            },
          });
        }
      },
      [data, eventId, updateEvent]
    );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const editValidations = object().shape({
    otherSolvingReason: string().when("solvingReason", {
      is: "OTHER",
      otherwise: string().nullable(),
      then: string().nullable().required(t("validations.required")),
    }),
    solvingReason: string().when("eventStatus", {
      is: "SOLVED",
      otherwise: string().nullable(),
      then: string().nullable().required(t("validations.required")),
    }),
  });

  return (
    <React.StrictMode>
      <React.Fragment>
        {isRejectSolutionModalOpen ? (
          <RemediationModal
            isLoading={false}
            isOpen={true}
            maxJustificationLength={20000}
            message={t(
              "group.events.description.rejectSolution.modal.observations"
            )}
            onClose={closeRejectSolutionModal}
            onSubmit={handleRejectSolution}
            title={t("group.events.description.rejectSolution.modal.title")}
          />
        ) : undefined}
        <Modal
          onClose={closeSolvingModal}
          open={isSolvingModalOpen}
          title={t("group.events.description.markAsSolved")}
        >
          <Formik
            enableReinitialize={true}
            initialValues={{ other: "", reason: "" }}
            name={"solvingReason"}
            onSubmit={handleSubmit}
          >
            {({ dirty, values }): React.ReactNode => (
              <Form id={"solvingReason"}>
                <Row>
                  <Col100>
                    <FormGroup>
                      <Select
                        label={t(
                          "searchFindings.tabSeverity.common.deactivation.reason.label"
                        )}
                        name={"reason"}
                        validate={composeValidators([required])}
                      >
                        <option value={""} />
                        {_.map(
                          solutionReasonByEventType[data.event.eventType],
                          (reasonValue: string): JSX.Element => (
                            <option value={reasonValue}>
                              {solvingReasons[reasonValue]}
                            </option>
                          )
                        )}
                      </Select>
                    </FormGroup>
                    {values.reason === "OTHER" ? (
                      <FormGroup>
                        <Input
                          label={t(
                            "searchFindings.tabSeverity.common.deactivation.other"
                          )}
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
                <ModalConfirm
                  disabled={!dirty || submitting}
                  onCancel={closeSolvingModal}
                />
              </Form>
            )}
          </Formik>
        </Modal>
        <Formik
          enableReinitialize={true}
          initialValues={data.event}
          name={"editEvent"}
          onSubmit={handleDescriptionSubmit}
          validationSchema={editValidations}
        >
          {({ values, dirty, setFieldValue }): React.ReactNode => {
            if (
              !_.isNull(values.solvingReason) &&
              !_.isEmpty(values.solvingReason) &&
              !_.isEmpty(values.eventType) &&
              !solutionReasonByEventType[values.eventType].includes(
                values.solvingReason
              )
            ) {
              setFieldValue("solvingReason", "");
            }

            return (
              <Form id={"editEvent"}>
                <div>
                  <div>
                    <ActionButtons
                      eventStatus={values.eventStatus}
                      isDirtyForm={dirty}
                      isEditing={isEditing}
                      onEdit={toggleEdit}
                      openRejectSolutionModal={openRejectSolutionModal}
                      openSolvingModal={openSolvingModal}
                    />
                    <br />
                    {isEditing && canUpdateEvent ? (
                      <Row>
                        <Col50>
                          <Row>
                            <EditableFieldTitle50>
                              <ControlLabel>
                                <b>{t("searchFindings.tabEvents.type")} </b>
                              </ControlLabel>
                            </EditableFieldTitle50>
                            <Col50>
                              <Select name={"eventType"} validate={required}>
                                <option value={""} />
                                <option value={"AUTHORIZATION_SPECIAL_ATTACK"}>
                                  {t(
                                    castEventType(
                                      "AUTHORIZATION_SPECIAL_ATTACK"
                                    )
                                  )}
                                </option>
                                <option
                                  value={"CLIENT_EXPLICITLY_SUSPENDS_PROJECT"}
                                >
                                  {t(
                                    castEventType(
                                      "CLIENT_EXPLICITLY_SUSPENDS_PROJECT"
                                    )
                                  )}
                                </option>
                                <option value={"CLONING_ISSUES"}>
                                  {t(castEventType("CLONING_ISSUES"))}
                                </option>
                                <option value={"CREDENTIAL_ISSUES"}>
                                  {t(castEventType("CREDENTIAL_ISSUES"))}
                                </option>
                                <option value={"DATA_UPDATE_REQUIRED"}>
                                  {t(castEventType("DATA_UPDATE_REQUIRED"))}
                                </option>
                                <option value={"ENVIRONMENT_ISSUES"}>
                                  {t(castEventType("ENVIRONMENT_ISSUES"))}
                                </option>
                                <option value={"INSTALLER_ISSUES"}>
                                  {t(castEventType("INSTALLER_ISSUES"))}
                                </option>
                                <option value={"MISSING_SUPPLIES"}>
                                  {t(castEventType("MISSING_SUPPLIES"))}
                                </option>
                                <option value={"NETWORK_ACCESS_ISSUES"}>
                                  {t(castEventType("NETWORK_ACCESS_ISSUES"))}
                                </option>
                                <option value={"OTHER"}>
                                  {t(castEventType("OTHER"))}
                                </option>
                                <option value={"REMOTE_ACCESS_ISSUES"}>
                                  {t(castEventType("REMOTE_ACCESS_ISSUES"))}
                                </option>
                                <option value={"TOE_DIFFERS_APPROVED"}>
                                  {t(castEventType("TOE_DIFFERS_APPROVED"))}
                                </option>
                                <option value={"VPN_ISSUES"}>
                                  {t(castEventType("VPN_ISSUES"))}
                                </option>
                              </Select>
                            </Col50>
                          </Row>
                        </Col50>
                      </Row>
                    ) : undefined}
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
                          label={t(
                            "searchFindings.tabEvents.affectedReattacks"
                          )}
                          name={"affectedReattacks"}
                          renderAsEditable={false}
                          type={"text"}
                        />
                      </Col50>
                    </Row>
                    {data.event.eventStatus === "SOLVED" ? (
                      isEditing ? (
                        canUpdateEvent ? (
                          <Row>
                            <Col50>
                              <Row>
                                <EditableFieldTitle50>
                                  <ControlLabel>
                                    <b>
                                      {t(
                                        "searchFindings.tabEvents.solvingReason"
                                      )}{" "}
                                    </b>
                                  </ControlLabel>
                                </EditableFieldTitle50>
                                <Col50>
                                  <Field
                                    component={FormikDropdown}
                                    name={"solvingReason"}
                                    validate={composeValidators([required])}
                                  >
                                    <option value={""} />
                                    {_.map(
                                      solutionReasonByEventType[
                                        values.eventType
                                      ],
                                      (reasonValue: string): JSX.Element => (
                                        <option value={reasonValue}>
                                          {solvingReasons[reasonValue]}
                                        </option>
                                      )
                                    )}
                                  </Field>
                                  {values.solvingReason === "OTHER" ? (
                                    <Fragment>
                                      <br />
                                      <EditableField
                                        component={FormikText}
                                        currentValue={
                                          _.isNil(data.event.otherSolvingReason)
                                            ? ""
                                            : data.event.otherSolvingReason
                                        }
                                        label={t(
                                          "searchFindings.tabSeverity.common.deactivation.other"
                                        )}
                                        name={"otherSolvingReason"}
                                        renderAsEditable={isEditing}
                                        type={"text"}
                                      />
                                    </Fragment>
                                  ) : undefined}
                                </Col50>
                              </Row>
                            </Col50>
                          </Row>
                        ) : undefined
                      ) : (
                        <Row>
                          {data.event.solvingReason === "OTHER" ? (
                            <Col50>
                              <EditableField
                                alignField={"horizontalWide"}
                                component={FormikText}
                                currentValue={
                                  _.isNil(data.event.otherSolvingReason)
                                    ? "-"
                                    : _.capitalize(
                                        data.event.otherSolvingReason
                                      )
                                }
                                label={t(
                                  "searchFindings.tabEvents.solvingReason"
                                )}
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
                                    : allSolvingReasons[
                                        data.event.solvingReason
                                      ]
                                }
                                label={t(
                                  "searchFindings.tabEvents.solvingReason"
                                )}
                                name={"solvingReason"}
                                renderAsEditable={false}
                                type={"text"}
                              />
                            </Col50>
                          )}
                          <Col50>
                            <EditableField
                              alignField={"horizontalWide"}
                              component={FormikText}
                              currentValue={
                                _.isNil(data.event.closingDate)
                                  ? "-"
                                  : data.event.closingDate
                              }
                              label={t("searchFindings.tabEvents.dateClosed")}
                              name={"dateClosed"}
                              renderAsEditable={false}
                              type={"text"}
                            />
                          </Col50>
                        </Row>
                      )
                    ) : undefined}
                  </div>
                </div>
              </Form>
            );
          }}
        </Formik>
      </React.Fragment>
    </React.StrictMode>
  );
};

export { EventDescriptionView };
