import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { Form, useFormikContext } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useContext, useEffect, useState } from "react";

import { AcceptanceDateField } from "./AcceptanceDateField";
import { AcceptationUserField } from "./AcceptationUserField";
import { ExternalBtsField } from "./ExternalBtsField";
import {
  dataTreatmentTrackHelper,
  deleteTagVulnHelper,
  getAreAllMutationValid,
  getResults,
  handleRequestZeroRiskError,
  handleUpdateTreatmentVulnError,
  hasNewVulnsAlert,
  isTheFormPristine,
  requestZeroRiskHelper,
  treatmentChangeAlert,
  validMutationsHelper,
} from "./helpers";
import { JustificationField } from "./JustificationField";
import { SeverityField } from "./SeverityField";
import { TagField } from "./TagField";
import { TreatmentField } from "./TreatmentField";
import { TreatmentManagerField } from "./TreatmentManagerField";

import { GET_FINDING_HEADER } from "../../../containers/FindingContent/queries";
import { UpdateDescriptionContext } from "../VulnerabilityModal/context";
import { Button } from "components/Button";
import { GET_GROUP_USERS } from "scenes/Dashboard/components/Vulnerabilities/queries";
import type {
  IUpdateTreatmentVulnerabilityForm,
  IVulnDataTypeAttr,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import {
  REMOVE_TAGS_MUTATION,
  REQUEST_ZERO_RISK_VULN,
  UPDATE_DESCRIPTION_MUTATION,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/queries";
import type {
  IGroupUsersAttr,
  IRemoveTagAttr,
  IRemoveTagResultAttr,
  IRequestZeroRiskVulnResultAttr,
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
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { ButtonToolbar, Col100, Col50, Row } from "styles/styledComponents";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

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
  const canRetrieveAnalyst: boolean = permissions.can(
    "api_resolvers_vulnerability_analyst_resolve"
  );
  const canRetrieveZeroRisk: boolean = permissions.can(
    "api_resolvers_finding_zero_risk_resolve"
  );
  const canGetHistoricState: boolean = permissions.can(
    "api_resolvers_finding_historic_state_resolve"
  );
  const canRequestZeroRiskVuln: boolean = permissions.can(
    "api_mutations_request_zero_risk_vulnerabilities_mutate"
  );
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "api_mutations_update_vulnerabilities_treatment_mutate"
  );
  const [isRunning, setRunning] = useState(false);
  const [treatment, setTreatment] = useContext(UpdateDescriptionContext);

  const {
    initialValues,
    values: formValues,
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
      ["externalBts", "tag", "severity"].includes(diff)
    ).length === 0;
  const isTreatmentValuesPristine: boolean =
    diffs.filter((diff: string): boolean =>
      ["acceptanceDate", "treatment", "treatmentManager"].includes(diff)
    ).length === 0;
  const isTreatmentPristine = isTheFormPristine(
    isTreatmentValuesPristine,
    formValues,
    vulnerabilities
  );

  const [updateVuln, { loading: updatingVuln }] =
    useMutation<IUpdateVulnDescriptionResultAttr>(UPDATE_DESCRIPTION_MUTATION, {
      refetchQueries: [
        {
          query: GET_FINDING_VULN_INFO,
          variables: {
            canRetrieveAnalyst,
            canRetrieveZeroRisk,
            findingId,
            groupName,
          },
        },
      ],
    });

  const { data } = useQuery<IGroupUsersAttr>(GET_GROUP_USERS, {
    skip: permissions.cannot("api_resolvers_group_stakeholders_resolve"),
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
        Logger.warning("An error occurred deleting vulnerabilities", error);
      });
    },
    refetchQueries: [
      {
        query: GET_FINDING_VULN_INFO,
        variables: {
          canRetrieveAnalyst,
          canRetrieveZeroRisk,
          findingId,
          groupName,
        },
      },
    ],
  });

  const handleUpdateTreatmentVuln = async (
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
      } catch (updateError: unknown) {
        handleUpdateTreatmentVulnError(updateError);
      } finally {
        setRunning(false);
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
    REQUEST_ZERO_RISK_VULN,
    {
      onCompleted: (
        requestZeroRiskVulnResult: IRequestZeroRiskVulnResultAttr
      ): void => {
        requestZeroRiskHelper(
          handleClearSelected,
          handleCloseModal,
          requestZeroRiskVulnResult
        );
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        handleRequestZeroRiskError(graphQLErrors);
      },
      refetchQueries: [
        {
          query: GET_FINDING_VULN_INFO,
          variables: {
            canRetrieveAnalyst,
            canRetrieveZeroRisk,
            findingId,
            groupName,
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
    _.isUndefined(data) || _.isEmpty(data)
      ? [userEmail]
      : data.group.stakeholders.map(
          (stakeholder: IStakeholderAttr): string => stakeholder.email
        );

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
      (objectValue: string | undefined): boolean =>
        objectValue === undefined || objectValue === ""
    );
  }

  useEffect((): void => {
    setConfigFn(
      requestZeroRisk,
      handleUpdateTreatmentVuln,
      isEditPristine,
      isTreatmentPristine
    );
    if (isEmpty(treatment) && !_.isEmpty(initialValues)) {
      setTreatment(initialValues);
    } else if (
      (!isEditPristine || !isTreatmentPristine) &&
      getDiff(
        treatment as unknown as Dictionary<unknown>,
        formValues as unknown as Dictionary<unknown>
      ).length > 0
    ) {
      setTreatment(formValues);
    } else if (isEditPristine && isTreatmentPristine) {
      setValues(treatment);
    }
    // Annotation needed as adding the dependencies creates a memory leak
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    isEditPristine,
    isTreatmentPristine,
    requestZeroRisk,
    setConfigFn,
    formValues,
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
            <AcceptationUserField
              isAcceptedSelected={isAcceptedSelected}
              isAcceptedUndefinedSelected={isAcceptedUndefinedSelected}
              isInProgressSelected={isInProgressSelected}
              lastTreatment={lastTreatment}
            />
          </Col50>
        </div>
        <Row>
          <Col50>
            <TreatmentManagerField
              isInProgressSelected={isInProgressSelected}
              lastTreatment={lastTreatment}
              userEmails={userEmails}
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
