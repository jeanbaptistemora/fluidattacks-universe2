import { AcceptedUndefinedTable } from "./AcceptedUndefinedTable";
import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import type { Dispatch } from "redux";
import { GET_FINDING_HEADER } from "../../FindingContent/queries";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { GraphQLError } from "graphql";
import { JustificationField } from "./JustificationField";
import { Logger } from "utils/logger";
import { Modal } from "components/Modal";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { TreatmentField } from "./TreatmentField";
import { ZeroRiskConfirmationTable } from "./ZeroRiskConfirmationTable";
import { ZeroRiskRejectionTable } from "./ZeroRiskRejectionTable";
import _ from "lodash";
import { translate } from "utils/translations/translate";
import { useAbility } from "@casl/react";
import { useMutation } from "@apollo/react-hooks";
import { ButtonToolbar, Col100, Col50, Row } from "styles/styledComponents";
import {
  CONFIRM_ZERO_RISK_VULN,
  HANDLE_VULNS_ACCEPTATION,
  REJECT_ZERO_RISK_VULN,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/queries";
import type {
  IConfirmZeroRiskVulnResultAttr,
  IHandleVulnsAcceptationModalProps,
  IHandleVulnsAcceptationResultAttr,
  IRejectZeroRiskVulnResultAttr,
  IVulnDataAttr,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/types";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { formValueSelector, submit } from "redux-form";
import {
  getRequestedZeroRiskVulns,
  getVulnsPendingOfAcceptation,
} from "../utils";
import { msgError, msgSuccess } from "utils/notifications";
import { useDispatch, useSelector } from "react-redux";

const HandleAcceptationModal: React.FC<IHandleVulnsAcceptationModalProps> = (
  props: IHandleVulnsAcceptationModalProps
): JSX.Element => {
  const { findingId, groupName, vulns, handleCloseModal, refetchData } = props;

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canGetHistoricState: boolean = permissions.can(
    "backend_api_resolvers_finding_historic_state_resolve"
  );
  const canRetrieveAnalyst: boolean = permissions.can(
    "backend_api_resolvers_vulnerability_analyst_resolve"
  );
  const canRetrieveZeroRisk: boolean = permissions.can(
    "backend_api_resolvers_finding_zero_risk_resolve"
  );
  const groupPermissions: PureAbility<string> = useAbility(authzGroupContext);
  const canGetExploit: boolean = groupPermissions.can("has_forces");
  const canHandleVulnsAcceptation: boolean = permissions.can(
    "backend_api_mutations_handle_vulns_acceptation_mutate"
  );
  const canConfirmZeroRiskVuln: boolean = permissions.can(
    "backend_api_mutations_confirm_zero_risk_vuln_mutate"
  );

  const dispatch: Dispatch = useDispatch();

  const [acceptationVulns, setAcceptationVulns] = React.useState<
    IVulnDataAttr[]
  >([]);
  const [acceptedVulns, setAcceptedVulns] = React.useState<IVulnDataAttr[]>([]);
  const [rejectedVulns, setRejectedVulns] = React.useState<IVulnDataAttr[]>([]);
  const [hasAcceptedVulns, setHasAcceptedVulns] = React.useState<boolean>(
    false
  );
  const [hasRejectedVulns, setHasRejectedVulns] = React.useState<boolean>(
    false
  );

  const formValues: Dictionary<string> = useSelector(
    (state: Record<string, unknown>): Dictionary<string> =>
      // It is necessary since formValueSelector returns an any type
      // eslint-disable-next-line @typescript-eslint/no-unsafe-return
      formValueSelector("updateTreatmentAcceptation")(state, "treatment", "")
  );

  const isAcceptedUndefinedSelected: boolean =
    formValues.treatment === "ACCEPTED_UNDEFINED";
  const isConfirmZeroRiskSelected: boolean =
    formValues.treatment === "CONFIRM_ZERO_RISK";
  const isRejectZeroRiskSelected: boolean =
    formValues.treatment === "REJECT_ZERO_RISK";

  // Side effects
  const onTreatmentChange: () => void = (): void => {
    if (isAcceptedUndefinedSelected) {
      const pendingVulnsToHandleAcceptation: IVulnDataAttr[] = getVulnsPendingOfAcceptation(
        vulns
      );
      setAcceptationVulns(pendingVulnsToHandleAcceptation);
    } else if (isConfirmZeroRiskSelected || isRejectZeroRiskSelected) {
      const requestedZeroRiskVulns: IVulnDataAttr[] = getRequestedZeroRiskVulns(
        vulns
      );
      setAcceptationVulns([...requestedZeroRiskVulns]);
    } else {
      setAcceptationVulns([]);
    }
  };
  React.useEffect(onTreatmentChange, [
    isAcceptedUndefinedSelected,
    isConfirmZeroRiskSelected,
    isRejectZeroRiskSelected,
    vulns,
  ]);

  const onAcceptationVulnsChange: () => void = (): void => {
    const newAcceptedVulns: IVulnDataAttr[] = acceptationVulns.reduce(
      (acc: IVulnDataAttr[], vuln: IVulnDataAttr): IVulnDataAttr[] =>
        vuln.acceptation === "APPROVED" ? [...acc, vuln] : acc,
      []
    );
    const newRejectedVulns: IVulnDataAttr[] = acceptationVulns.reduce(
      (acc: IVulnDataAttr[], vuln: IVulnDataAttr): IVulnDataAttr[] =>
        vuln.acceptation === "REJECTED" ? [...acc, vuln] : acc,
      []
    );
    setAcceptedVulns(newAcceptedVulns);
    setRejectedVulns(newRejectedVulns);
    setHasAcceptedVulns(newAcceptedVulns.length !== 0);
    setHasRejectedVulns(newRejectedVulns.length !== 0);
  };
  React.useEffect(onAcceptationVulnsChange, [acceptationVulns]);

  // GraphQL operations
  const [handleAcceptation, { loading: handlingAcceptation }] = useMutation(
    HANDLE_VULNS_ACCEPTATION,
    {
      onCompleted: (data: IHandleVulnsAcceptationResultAttr): void => {
        if (data.handleVulnsAcceptation.success) {
          msgSuccess(
            translate.t("search_findings.tab_vuln.alerts.acceptation_success"),
            translate.t("groupAlerts.updatedTitle")
          );
          refetchData();
          handleCloseModal();
        }
      },
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - It cant handle acceptation without being requested":
              msgError(
                translate.t(
                  "search_findings.tab_vuln.alerts.acceptation_not_requested"
                )
              );
              break;
            case "Exception - Vulnerability not found":
              msgError(translate.t("groupAlerts.noFound"));
              break;
            case "Exception - Invalid characters":
              msgError(translate.t("validations.invalid_char"));
              break;
            default:
              msgError(translate.t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred handling acceptation", error);
          }
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
    }
  );
  const [confirmZeroRisk, { loading: confirmingZeroRisk }] = useMutation(
    CONFIRM_ZERO_RISK_VULN,
    {
      onCompleted: (data: IConfirmZeroRiskVulnResultAttr): void => {
        if (data.confirmZeroRiskVuln.success) {
          msgSuccess(
            translate.t("groupAlerts.confirmedZeroRiskSuccess"),
            translate.t("groupAlerts.updatedTitle")
          );
          refetchData();
          handleCloseModal();
        }
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - Zero risk vulnerability is not requested":
              msgError(translate.t("groupAlerts.zeroRiskIsNotRequested"));
              break;
            default:
              msgError(translate.t("groupAlerts.errorTextsad"));
              Logger.warning(
                "An error occurred confirming zero risk vuln",
                error
              );
          }
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
        {
          query: GET_FINDING_HEADER,
          variables: {
            canGetExploit,
            canGetHistoricState,
            findingId,
          },
        },
      ],
    }
  );
  const [rejectZeroRisk, { loading: rejectingZeroRisk }] = useMutation(
    REJECT_ZERO_RISK_VULN,
    {
      onCompleted: (data: IRejectZeroRiskVulnResultAttr): void => {
        if (data.rejectZeroRiskVuln.success) {
          msgSuccess(
            translate.t("groupAlerts.rejectedZeroRiskSuccess"),
            translate.t("groupAlerts.updatedTitle")
          );
          refetchData();
          handleCloseModal();
        }
      },
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - Zero risk vulnerability is not requested":
              msgError(translate.t("groupAlerts.zeroRiskIsNotRequested"));
              break;
            default:
              msgError(translate.t("groupAlerts.errorTextsad"));
              Logger.warning(
                "An error occurred rejecting zero risk vuln",
                error
              );
          }
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
        {
          query: GET_FINDING_HEADER,
          variables: {
            canGetExploit,
            canGetHistoricState,
            findingId,
          },
        },
      ],
    }
  );

  function handleUpdateTreatmentAcceptation(): void {
    dispatch(submit("updateTreatmentAcceptation"));
  }

  function handleSubmit(values: { justification: string }): void {
    const acceptedVulnIds: string[] = acceptedVulns.map(
      (vuln: IVulnDataAttr): string => vuln.id
    );
    const rejectedVulnIds: string[] = rejectedVulns.map(
      (vuln: IVulnDataAttr): string => vuln.id
    );
    if (isAcceptedUndefinedSelected) {
      void handleAcceptation({
        variables: {
          acceptedVulns: acceptedVulnIds,
          findingId,
          justification: values.justification,
          rejectedVulns: rejectedVulnIds,
        },
      });
    }
    if (isConfirmZeroRiskSelected) {
      void confirmZeroRisk({
        variables: {
          findingId,
          justification: values.justification,
          vulnerabilities: acceptedVulnIds,
        },
      });
    }
    if (isRejectZeroRiskSelected) {
      void rejectZeroRisk({
        variables: {
          findingId,
          justification: values.justification,
          vulnerabilities: rejectedVulnIds,
        },
      });
    }
  }

  const initialTreatment: string = canHandleVulnsAcceptation
    ? "ACCEPTED_UNDEFINED"
    : canConfirmZeroRiskVuln
    ? "CONFIRM_ZERO_RISK"
    : "";

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t(
          "search_findings.tab_description.handleAcceptationModal.title"
        )}
        open={true}
      >
        <GenericForm
          initialValues={{
            treatment: _.isEmpty(formValues.treatment)
              ? initialTreatment
              : formValues.treatment,
          }}
          name={"updateTreatmentAcceptation"}
          onSubmit={handleSubmit}
        >
          <Row>
            <Col50>
              <TreatmentField />
            </Col50>
          </Row>
          <Row>
            <Col100>
              <AcceptedUndefinedTable
                acceptationVulns={acceptationVulns}
                isAcceptedUndefinedSelected={isAcceptedUndefinedSelected}
                setAcceptationVulns={setAcceptationVulns}
              />
            </Col100>
          </Row>
          <Row>
            <Col100>
              <ZeroRiskConfirmationTable
                acceptationVulns={acceptationVulns}
                isConfirmZeroRiskSelected={isConfirmZeroRiskSelected}
                setAcceptationVulns={setAcceptationVulns}
              />
            </Col100>
          </Row>
          <Row>
            <Col100>
              <ZeroRiskRejectionTable
                acceptationVulns={acceptationVulns}
                isRejectZeroRiskSelected={isRejectZeroRiskSelected}
                setAcceptationVulns={setAcceptationVulns}
              />
            </Col100>
          </Row>
          <Row>
            <Col100>
              <JustificationField
                isConfirmZeroRiskSelected={isConfirmZeroRiskSelected}
                isRejectZeroRiskSelected={isRejectZeroRiskSelected}
              />
            </Col100>
          </Row>
          <hr />
          <Row>
            <Col100>
              <ButtonToolbar>
                <Button onClick={handleCloseModal}>
                  {translate.t("group.findings.report.modalClose")}
                </Button>
                <Button
                  disabled={
                    !(hasAcceptedVulns || hasRejectedVulns) ||
                    handlingAcceptation ||
                    confirmingZeroRisk ||
                    rejectingZeroRisk
                  }
                  onClick={handleUpdateTreatmentAcceptation}
                >
                  {translate.t("confirmmodal.proceed")}
                </Button>
              </ButtonToolbar>
            </Col100>
          </Row>
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};

export { HandleAcceptationModal };
