import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { FormikTouched } from "formik";
import { Form, useFormikContext } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useContext, useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import { AcceptanceDateField } from "./AcceptanceDateField";
import { AcceptanceUserField } from "./AcceptanceUserField";
import { AssignedField } from "./AssignedField";
import { ExternalBtsField } from "./ExternalBtsField";
import {
  dataTreatmentTrackHelper,
  deleteTagVulnHelper,
  getAllNotifications,
  getAllResults,
  getAreAllChunckedMutationValid,
  getAreAllNotificationValid,
  handleRequestZeroRiskError,
  handleUpdateVulnTreatmentError,
  hasNewVulnsAlert,
  isTheFormPristine,
  requestZeroRiskHelper,
  tagReminderAlert,
  treatmentChangeAlert,
  validMutationsHelper,
} from "./helpers";
import { JustificationField } from "./JustificationField";
import { SeverityField } from "./SeverityField";
import { TagField } from "./TagField";
import { TreatmentField } from "./TreatmentField";

import { GET_FINDING_HEADER } from "../../../containers/FindingContent/queries";
import { GET_ME_VULNERABILITIES_ASSIGNED_IDS } from "../../Navbar/Tasks/queries";
import { UpdateDescriptionContext } from "../VulnerabilityModal/context";
import { ModalConfirm } from "components/Modal";
import { GET_GROUP_USERS } from "scenes/Dashboard/components/Vulnerabilities/queries";
import type {
  IUpdateTreatmentVulnerabilityForm,
  IVulnDataTypeAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import {
  REMOVE_TAGS_MUTATION,
  REQUEST_VULNS_ZERO_RISK,
  SEND_ASSIGNED_NOTIFICATION,
  UPDATE_DESCRIPTION_MUTATION,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/queries";
import type {
  IGroupUsersAttr,
  IRemoveTagAttr,
  IRemoveTagResultAttr,
  IRequestVulnZeroRiskResultAttr,
  ISendNotificationResultAttr,
  IStakeholderAttr,
  IUpdateTreatmentModalProps,
  IUpdateVulnDescriptionResultAttr,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/types";
import {
  groupLastHistoricTreatment,
  groupVulnLevel,
  hasNewTreatment,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import { GET_FINDING_LOCATIONS } from "scenes/Dashboard/containers/GroupFindingsView/loaders/Locations/queries";
import { GET_ME_VULNERABILITIES_ASSIGNED } from "scenes/Dashboard/containers/Tasks/Vulnerabilities/queries";
import { GET_FINDING_AND_GROUP_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { Col100, Col50, Row } from "styles/styledComponents";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

function usePreviousPristine(value: boolean): boolean {
  const ref = useRef(false);
  useEffect((): void => {
    // eslint-disable-next-line fp/no-mutation
    ref.current = value;
  });

  return ref.current;
}

const UpdateTreatmentModal: React.FC<IUpdateTreatmentModalProps> = ({
  groupName,
  vulnerabilities,
  handleClearSelected,
  handleCloseModal,
  refetchData,
  setConfigFn,
}: IUpdateTreatmentModalProps): JSX.Element => {
  const { t } = useTranslation();
  const { userEmail }: IAuthContext = useContext(authContext);
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canGetHistoricState: boolean = permissions.can(
    "api_resolvers_finding_historic_state_resolve"
  );
  const canRequestZeroRiskVuln: boolean = permissions.can(
    "api_mutations_request_vulnerabilities_zero_risk_mutate"
  );
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "api_mutations_update_vulnerabilities_treatment_mutate"
  );
  const canDeleteVulnsTags: boolean = permissions.can(
    "api_mutations_remove_vulnerability_tags_mutate"
  );
  const [isRunning, setIsRunning] = useState(false);
  const [treatment, setTreatment] = useContext(UpdateDescriptionContext);

  const {
    dirty,
    touched,
    initialValues,
    values: formValues,
    setTouched,
    setValues,
  } = useFormikContext<IUpdateTreatmentVulnerabilityForm>();

  function getDiff(
    initValues: Dictionary<unknown>,
    values: Dictionary<unknown>
  ): string[] {
    return _.reduce(
      initValues,
      (result: string[], value: unknown, key: string): string[] => {
        return _.isEqual(value, values[key]) ? result : result.concat(key);
      },
      []
    );
  }

  const diffs: string[] = getDiff(
    initialValues as unknown as Dictionary<unknown>,
    formValues as unknown as Dictionary<unknown>
  );
  const isEditPristine: boolean =
    diffs.filter((diff: string): boolean =>
      ["externalBugTrackingSystem", "tag", "severity"].includes(diff)
    ).length === 0;
  const isTreatmentValuesPristine: boolean =
    diffs.filter((diff: string): boolean =>
      ["acceptanceDate", "treatment", "assigned"].includes(diff)
    ).length === 0;
  const isTreatmentPristine = isTheFormPristine(
    isTreatmentValuesPristine,
    formValues,
    vulnerabilities
  );
  const isPreviousEditPristine = usePreviousPristine(isEditPristine);
  const isPreviousTreatmentPristine = usePreviousPristine(isTreatmentPristine);

  const [updateVuln, { loading: updatingVuln }] =
    useMutation<IUpdateVulnDescriptionResultAttr>(UPDATE_DESCRIPTION_MUTATION, {
      onCompleted: (result: IUpdateVulnDescriptionResultAttr): void => {
        if (
          !_.isUndefined(result.updateVulnerabilitiesTreatment) &&
          result.updateVulnerabilitiesTreatment.success
        ) {
          refetchData();
        }
      },
      refetchQueries: [
        GET_ME_VULNERABILITIES_ASSIGNED,
        GET_ME_VULNERABILITIES_ASSIGNED_IDS,
      ],
    });

  const [sendNotification] = useMutation<ISendNotificationResultAttr>(
    SEND_ASSIGNED_NOTIFICATION,
    {
      onError: (updateError: ApolloError): void => {
        updateError.graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(
            t(
              "searchFindings.tabDescription.notification.emailNotificationError"
            )
          );
          Logger.warning("An error occurred sending the notification", error);
        });
      },
    }
  );

  const numberOfGroups: number = Array.from(
    new Set(
      vulnerabilities.map(
        (vulnerability: IVulnDataTypeAttr): string => vulnerability.groupName
      )
    )
  ).length;

  const { data } = useQuery<IGroupUsersAttr>(GET_GROUP_USERS, {
    skip:
      permissions.cannot("api_resolvers_group_stakeholders_resolve") ||
      numberOfGroups > 1,
    variables: {
      groupName,
    },
  });

  const [deleteTagVuln, { loading: deletingTag }] = useMutation<
    IRemoveTagResultAttr,
    IRemoveTagAttr
  >(REMOVE_TAGS_MUTATION, {
    onCompleted: (result: IRemoveTagResultAttr): void => {
      deleteTagVulnHelper(result);
      refetchData();
    },
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred deleting vulnerabilities tags",
          error
        );
      });
    },
    refetchQueries: [
      GET_ME_VULNERABILITIES_ASSIGNED,
      GET_ME_VULNERABILITIES_ASSIGNED_IDS,
    ],
  });

  const handleUpdateVulnTreatment = async (
    dataTreatment: IUpdateTreatmentVulnerabilityForm,
    isEditPristineP: boolean,
    isTreatmentPristineP: boolean
  ): Promise<void> => {
    if (vulnerabilities.length === 0) {
      msgError(t("searchFindings.tabResources.noSelection"));
    } else {
      dataTreatmentTrackHelper(dataTreatment);
      try {
        setIsRunning(true);
        const results = await getAllResults(
          updateVuln,
          vulnerabilities,
          dataTreatment,
          isEditPristineP,
          isTreatmentPristineP
        );

        const areAllMutationValid = getAreAllChunckedMutationValid(results);

        validMutationsHelper(
          handleCloseModal,
          areAllMutationValid,
          dataTreatment,
          vulnerabilities,
          isTreatmentPristineP
        );

        if (!isTreatmentPristineP) {
          const notificationsResults = await getAllNotifications(
            sendNotification,
            vulnerabilities
          );
          const areAllNotificationValid =
            getAreAllNotificationValid(notificationsResults);
          if (areAllNotificationValid.every(Boolean)) {
            msgSuccess(
              t(
                "searchFindings.tabDescription.notification.emailNotificationText"
              ),
              t(
                "searchFindings.tabDescription.notification.emailNotificationTitle"
              )
            );
          }
        }
      } catch (updateError: unknown) {
        handleUpdateVulnTreatmentError(updateError);
      } finally {
        setIsRunning(false);
      }
    }
  };

  const { submitForm } = useFormikContext<IUpdateTreatmentVulnerabilityForm>();

  async function handleDeletion(tag: string): Promise<void> {
    await deleteTagVuln({
      variables: {
        findingId: vulnerabilities[0].findingId,
        tag,
        vulnerabilities: vulnerabilities.map(
          (vuln: IVulnDataTypeAttr): string => vuln.id
        ),
      },
    });
  }

  const [requestZeroRisk, { loading: requestingZeroRisk }] = useMutation(
    REQUEST_VULNS_ZERO_RISK,
    {
      onCompleted: (
        requestZeroRiskVulnResult: IRequestVulnZeroRiskResultAttr
      ): void => {
        requestZeroRiskHelper(
          handleClearSelected,
          handleCloseModal,
          refetchData,
          requestZeroRiskVulnResult
        );
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        handleRequestZeroRiskError(graphQLErrors);
      },
      refetchQueries: [
        {
          query: GET_FINDING_AND_GROUP_INFO,
          variables: {
            findingId: vulnerabilities[0].findingId,
          },
        },
        {
          query: GET_FINDING_HEADER,
          variables: {
            canGetHistoricState,
            findingId: vulnerabilities[0].findingId,
          },
        },
        {
          query: GET_FINDING_LOCATIONS,
          variables: {
            findingId: vulnerabilities[0].findingId,
          },
        },
        GET_ME_VULNERABILITIES_ASSIGNED,
        GET_ME_VULNERABILITIES_ASSIGNED_IDS,
      ],
    }
  );

  const userEmails: string[] =
    _.isUndefined(data) || _.isEmpty(data) || numberOfGroups > 1
      ? [userEmail]
      : data.group.stakeholders
          .filter(
            (stakeholder: IStakeholderAttr): boolean =>
              stakeholder.invitationState === "REGISTERED"
          )
          .map((stakeholder: IStakeholderAttr): string => stakeholder.email);

  const lastTreatment: IHistoricTreatment = {
    ...groupLastHistoricTreatment(vulnerabilities),
    justification: "",
  };

  const hasNewVulns: boolean = hasNewTreatment(vulnerabilities);

  const isInProgressSelected: boolean = formValues.treatment === "IN_PROGRESS";
  const isAcceptedSelected: boolean = formValues.treatment === "ACCEPTED";
  const isAcceptedUndefinedSelected: boolean =
    formValues.treatment === "ACCEPTED_UNDEFINED";

  function isEmpty(formObject: IUpdateTreatmentVulnerabilityForm): boolean {
    return _.values(formObject).every(
      (objectValue: string | null | undefined): boolean =>
        _.isEmpty(objectValue)
    );
  }

  useEffect((): void => {
    setConfigFn(
      requestZeroRisk,
      handleUpdateVulnTreatment,
      isEditPristine,
      isTreatmentPristine
    );
    const valuesDifferences: string[] = getDiff(
      treatment as unknown as Dictionary<unknown>,
      formValues as unknown as Dictionary<unknown>
    );
    const isTouched: boolean = valuesDifferences.some(
      (field: string): boolean => Boolean(_.keys(touched).includes(field))
    );
    if (isEmpty(treatment) && !_.isEmpty(initialValues)) {
      setTreatment(initialValues);
    } else if (
      (!isEditPristine || !isTreatmentPristine) &&
      valuesDifferences.length > 0
    ) {
      setTreatment(formValues);
    } else if (isEditPristine && isTreatmentPristine) {
      if (isTouched) {
        setTreatment(initialValues);
        setValues(initialValues);
        setTouched({});
      } else if (
        !dirty &&
        isPreviousEditPristine &&
        isPreviousTreatmentPristine
      ) {
        if (valuesDifferences.length > 0) {
          setValues(treatment);
          setTouched(
            (
              valuesDifferences as (keyof IUpdateTreatmentVulnerabilityForm)[]
            ).reduce(
              (
                previousValue: FormikTouched<IUpdateTreatmentVulnerabilityForm>,
                currentValue: keyof IUpdateTreatmentVulnerabilityForm
              ): FormikTouched<IUpdateTreatmentVulnerabilityForm> => (
                // eslint-disable-next-line fp/no-mutation, no-sequences
                (previousValue[currentValue] = true), previousValue
              ),
              {}
            )
          );
        }
      }
    }
    // Annotation needed as adding the dependencies creates a memory leak
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    isEditPristine,
    isTreatmentPristine,
    isPreviousEditPristine,
    isPreviousTreatmentPristine,
    requestZeroRisk,
    setConfigFn,
    formValues,
    dirty,
    touched,
  ]);

  return (
    <React.StrictMode>
      <Form>
        <div className={"flex flex-wrap pt3"}>
          <Col50>
            <TreatmentField
              isTreatmentPristine={isTreatmentPristine}
              lastTreatment={lastTreatment}
            />
          </Col50>
          <Col50>
            <AssignedField
              isAcceptedSelected={isAcceptedSelected}
              isAcceptedUndefinedSelected={isAcceptedUndefinedSelected}
              isInProgressSelected={isInProgressSelected}
              lastTreatment={lastTreatment}
              userEmails={userEmails}
            />
          </Col50>
        </div>
        <Row>
          <Col50>
            <AcceptanceUserField
              isAcceptedSelected={isAcceptedSelected}
              isAcceptedUndefinedSelected={isAcceptedUndefinedSelected}
              isInProgressSelected={isInProgressSelected}
              lastTreatment={lastTreatment}
            />
          </Col50>
        </Row>
        <Row>
          <Col100>
            <JustificationField
              isTreatmentPristine={isTreatmentPristine}
              lastTreatment={lastTreatment}
            />
          </Col100>
        </Row>
        <Row>
          <Col50>
            <AcceptanceDateField
              isAcceptedSelected={isAcceptedSelected}
              lastTreatment={lastTreatment}
            />
          </Col50>
        </Row>
        <Row>
          <Col100>
            <ExternalBtsField
              hasNewVulnSelected={hasNewVulns}
              isAcceptedSelected={isAcceptedSelected}
              isAcceptedUndefinedSelected={isAcceptedUndefinedSelected}
              isInProgressSelected={isInProgressSelected}
              vulnerabilities={vulnerabilities}
            />
          </Col100>
        </Row>
        <Row>
          <Col100>
            <TagField
              handleDeletion={handleDeletion}
              hasNewVulnSelected={hasNewVulns}
              isAcceptedSelected={isAcceptedSelected}
              isAcceptedUndefinedSelected={isAcceptedUndefinedSelected}
              isInProgressSelected={isInProgressSelected}
            />
          </Col100>
        </Row>
        {(isAcceptedSelected ||
          isAcceptedUndefinedSelected ||
          isInProgressSelected ||
          !hasNewVulns) &&
        canUpdateVulnsTreatment &&
        canDeleteVulnsTags ? (
          <React.StrictMode>
            {tagReminderAlert(isTreatmentPristine)}
          </React.StrictMode>
        ) : undefined}
        <Row>
          <Col50>
            <SeverityField
              hasNewVulnSelected={hasNewVulns}
              isAcceptedSelected={isAcceptedSelected}
              isAcceptedUndefinedSelected={isAcceptedUndefinedSelected}
              isInProgressSelected={isInProgressSelected}
              level={groupVulnLevel(vulnerabilities)}
            />
          </Col50>
        </Row>
      </Form>
      {treatmentChangeAlert(isTreatmentPristine)}
      {hasNewVulnsAlert(
        vulnerabilities,
        hasNewVulns,
        isAcceptedSelected,
        isAcceptedUndefinedSelected,
        isInProgressSelected
      )}
      {canRequestZeroRiskVuln || canUpdateVulnsTreatment ? (
        <ModalConfirm
          disabled={
            requestingZeroRisk ||
            updatingVuln ||
            deletingTag ||
            isRunning ||
            (isEditPristine && isTreatmentPristine)
          }
          onCancel={handleCloseModal}
          onConfirm={submitForm}
          txtCancel={t("group.findings.report.modalClose")}
        />
      ) : undefined}
    </React.StrictMode>
  );
};

export { UpdateTreatmentModal };
