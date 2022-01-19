import { useApolloClient, useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { FormikTouched } from "formik";
import { Form, useFormikContext } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useContext, useEffect, useRef, useState } from "react";

import { AcceptanceDateField } from "./AcceptanceDateField";
import { AcceptanceUserField } from "./AcceptanceUserField";
import { AssignedField } from "./AssignedField";
import { ExternalBtsField } from "./ExternalBtsField";
import {
  dataTreatmentTrackHelper,
  deleteTagVulnHelper,
  getAreAllMutationValid,
  getResults,
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
import { UpdateDescriptionContext } from "../VulnerabilityModal/context";
import { Button } from "components/Button";
import { mergedAssigned } from "scenes/Dashboard/components/Navbar/Tasks/utils";
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
import {
  GET_FINDING_AND_GROUP_INFO,
  GET_FINDING_VULNS,
} from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { AssignedVulnerabilitiesContext } from "scenes/Dashboard/context";
import { GET_VULNS_GROUPS } from "scenes/Dashboard/queries";
import type { IGetVulnsGroups } from "scenes/Dashboard/types";
import { ButtonToolbar, Col100, Col50, Row } from "styles/styledComponents";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

function usePreviousPristine(value: boolean): boolean {
  const ref = useRef(false);
  useEffect((): void => {
    // eslint-disable-next-line fp/no-mutation
    ref.current = value;
  });

  return ref.current;
}

const UpdateTreatmentModal: React.FC<IUpdateTreatmentModalProps> = ({
  findingId,
  groupName,
  vulnerabilities,
  handleClearSelected,
  handleCloseModal,
  setConfigFn,
}: IUpdateTreatmentModalProps): JSX.Element => {
  const { userEmail }: IAuthContext = useContext(authContext);
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRetrieveZeroRisk: boolean = permissions.can(
    "api_resolvers_finding_zero_risk_resolve"
  );
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
  const [isRunning, setRunning] = useState(false);
  const [treatment, setTreatment] = useContext(UpdateDescriptionContext);
  const [, setAllData] = useContext(AssignedVulnerabilitiesContext);
  const client = useApolloClient();

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
      refetchQueries: [
        {
          query: GET_FINDING_AND_GROUP_INFO,
          variables: {
            findingId,
            groupName,
          },
        },
        {
          query: GET_FINDING_VULNS,
          variables: {
            canRetrieveZeroRisk,
            findingId,
          },
        },
      ],
    });

  const [sendNotification] = useMutation<ISendNotificationResultAttr>(
    SEND_ASSIGNED_NOTIFICATION,
    {
      onCompleted: ({
        sendAssignedNotification,
      }: ISendNotificationResultAttr): void => {
        if (sendAssignedNotification.success) {
          msgSuccess(
            translate.t(
              "searchFindings.tabDescription.notification.emailNotificationText"
            ),
            translate.t(
              "searchFindings.tabDescription.notification.emailNotificationTitle"
            )
          );
        }
      },
      onError: (updateError: ApolloError): void => {
        updateError.graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(
            translate.t(
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
    },
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred deleting vulnerabilities tags",
          error
        );
      });
    },
    refetchQueries: [
      {
        query: GET_FINDING_AND_GROUP_INFO,
        variables: {
          findingId,
          groupName,
        },
      },
      {
        query: GET_FINDING_VULNS,
        variables: {
          canRetrieveZeroRisk,
          findingId,
        },
      },
    ],
  });

  const updateAssigned = async (): Promise<void> => {
    const groupData = await client.query<IGetVulnsGroups>({
      errorPolicy: "all",
      fetchPolicy: "network-only",
      query: GET_VULNS_GROUPS,
      variables: { groupName },
    });

    setAllData((current: IGetVulnsGroups[]): IGetVulnsGroups[] =>
      Array.from(
        new Set(
          mergedAssigned(current, [
            _.isUndefined(groupData.errors) && _.isEmpty(groupData.errors)
              ? groupData.data
              : {
                  group: {
                    name: _.isUndefined(groupName) ? "" : groupName,
                    vulnerabilitiesAssigned: [],
                  },
                },
          ])
        )
      )
    );
  };

  const handleUpdateVulnTreatment = async (
    dataTreatment: IUpdateTreatmentVulnerabilityForm,
    isEditPristineP: boolean,
    isTreatmentPristineP: boolean
  ): Promise<void> => {
    if (vulnerabilities.length === 0) {
      msgError(translate.t("searchFindings.tabResources.noSelection"));
    } else {
      dataTreatmentTrackHelper(dataTreatment);
      try {
        setRunning(true);
        const results = await getResults(
          updateVuln,
          vulnerabilities,
          dataTreatment,
          findingId,
          isEditPristineP,
          isTreatmentPristineP
        );

        const areAllMutationValid = getAreAllMutationValid(results);

        validMutationsHelper(
          handleCloseModal,
          areAllMutationValid,
          vulnerabilities
        );

        if (!isTreatmentPristineP) {
          await sendNotification({
            variables: {
              findingId,
              vulnerabilities: vulnerabilities.map(({ id }): string => id),
            },
          });
        }
      } catch (updateError: unknown) {
        handleUpdateVulnTreatmentError(updateError);
      } finally {
        setRunning(false);
        if (permissions.can("valid_assigned")) {
          await updateAssigned();
        }
      }
    }
  };

  const { submitForm } = useFormikContext<IUpdateTreatmentVulnerabilityForm>();

  async function handleDeletion(tag: string): Promise<void> {
    await deleteTagVuln({
      variables: {
        findingId,
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
      onCompleted: async (
        requestZeroRiskVulnResult: IRequestVulnZeroRiskResultAttr
      ): Promise<void> => {
        requestZeroRiskHelper(
          handleClearSelected,
          handleCloseModal,
          requestZeroRiskVulnResult
        );
        if (permissions.can("valid_assigned")) {
          await updateAssigned();
        }
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        handleRequestZeroRiskError(graphQLErrors);
      },
      refetchQueries: [
        {
          query: GET_FINDING_AND_GROUP_INFO,
          variables: {
            findingId,
            groupName,
          },
        },
        {
          query: GET_FINDING_VULNS,
          variables: {
            canRetrieveZeroRisk,
            findingId,
          },
        },
        {
          query: GET_FINDING_HEADER,
          variables: {
            canGetHistoricState,
            findingId,
          },
        },
      ],
    }
  );

  const userEmails: string[] =
    _.isUndefined(data) || _.isEmpty(data) || numberOfGroups > 1
      ? [userEmail]
      : data.group.stakeholders
          .filter(
            (stakeholder: IStakeholderAttr): boolean =>
              stakeholder.invitationState === "CONFIRMED"
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
      <hr />
      <Row>
        <Col100>
          <ButtonToolbar>
            <Button onClick={handleCloseModal}>
              {translate.t("group.findings.report.modalClose")}
            </Button>
            {canRequestZeroRiskVuln || canUpdateVulnsTreatment ? (
              <Button
                disabled={
                  requestingZeroRisk ||
                  updatingVuln ||
                  deletingTag ||
                  isRunning ||
                  (isEditPristine && isTreatmentPristine)
                }
                onClick={submitForm}
              >
                {translate.t("confirmmodal.proceed")}
              </Button>
            ) : undefined}
          </ButtonToolbar>
        </Col100>
      </Row>
    </React.StrictMode>
  );
};

export { UpdateTreatmentModal };
