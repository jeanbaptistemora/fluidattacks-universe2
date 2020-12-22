import { AcceptedUndefinedTable } from "./AcceptedUndefinedTable";
import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import type { Dispatch } from "redux";
import { GET_VULNERABILITIES } from "scenes/Dashboard/components/Vulnerabilities/queries";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { GraphQLError } from "graphql";
import { HANDLE_VULNS_ACCEPTATION } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/queries";
import { JustificationField } from "./JustificationField";
import { Logger } from "utils/logger";
import { Modal } from "components/Modal";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { TreatmentField } from "./TreatmentField";
import { authzPermissionsContext } from "utils/authz/config";
import { getVulnsPendingOfAcceptation } from "../utils";
import { translate } from "utils/translations/translate";
import { useAbility } from "@casl/react";
import { useMutation } from "@apollo/react-hooks";
import { ButtonToolbar, Col100, Col50, Row } from "styles/styledComponents";
import type {
  IHandleVulnsAcceptationModalProps,
  IHandleVulnsAcceptationResultAttr,
  IVulnDataAttr,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/types";
import { formValueSelector, submit } from "redux-form";
import { msgError, msgSuccess } from "utils/notifications";
import { useDispatch, useSelector } from "react-redux";

const HandleAcceptationModal: React.FC<IHandleVulnsAcceptationModalProps> = (
  props: IHandleVulnsAcceptationModalProps
): JSX.Element => {
  const { findingId, vulns, handleCloseModal, refetchData } = props;

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canDisplayAnalyst: boolean = permissions.can(
    "backend_api_resolvers_new_finding_analyst_resolve"
  );
  const canHandleVulnsAcceptation: boolean = permissions.can(
    "backend_api_mutations_handle_vulns_acceptation_mutate"
  );

  const dispatch: Dispatch = useDispatch();

  const [acceptationVulns, setAcceptationVulns] = React.useState<
    IVulnDataAttr[]
  >([]);

  const formValues: Dictionary<string> = useSelector(
    (state: Record<string, unknown>): Dictionary<string> =>
      // It is necessary since formValueSelector returns an any type
      // eslint-disable-next-line @typescript-eslint/no-unsafe-return
      formValueSelector("updateTreatmentAcceptation")(state, "treatment", "")
  );

  const isAcceptedUndefinedSelected: boolean =
    formValues.treatment === "ACCEPTED_UNDEFINED";
  const hasAcceptationVulns: boolean = acceptationVulns.length !== 0;

  // Side effects
  const onTreatmentChange: () => void = (): void => {
    if (isAcceptedUndefinedSelected) {
      const pendingVulnsToHandleAcceptation: IVulnDataAttr[] = getVulnsPendingOfAcceptation(
        vulns
      );
      setAcceptationVulns(pendingVulnsToHandleAcceptation);
    } else {
      setAcceptationVulns([]);
    }
  };
  React.useEffect(onTreatmentChange, [isAcceptedUndefinedSelected, vulns]);

  // GraphQL operations
  const [handleAcceptation, { loading: handlingAcceptation }] = useMutation(
    HANDLE_VULNS_ACCEPTATION,
    {
      onCompleted: (data: IHandleVulnsAcceptationResultAttr): void => {
        if (data.handleVulnsAcceptation.success) {
          msgSuccess(
            translate.t("search_findings.tab_vuln.alerts.acceptation_success"),
            translate.t("group_alerts.updated_title")
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
              msgError(translate.t("group_alerts.no_found"));
              break;
            case "Exception - Invalid characters":
              msgError(translate.t("validations.invalid_char"));
              break;
            default:
              msgError(translate.t("group_alerts.error_textsad"));
              Logger.warning("An error occurred handling acceptation", error);
          }
        });
      },
      refetchQueries: [
        {
          query: GET_VULNERABILITIES,
          variables: {
            analystField: canDisplayAnalyst,
            identifier: findingId,
          },
        },
      ],
    }
  );

  function handleUpdateTreatmentAcceptation(): void {
    dispatch(submit("updateTreatmentAcceptation"));
  }

  function handleSubmit(values: { justification: string }): void {
    const acceptedVulns: string[] = acceptationVulns.reduce(
      (acc: string[], vuln: IVulnDataAttr): string[] =>
        vuln.acceptation === "APPROVED" ? [...acc, vuln.id] : acc,
      []
    );
    const rejectedVulns: string[] = acceptationVulns.reduce(
      (acc: string[], vuln: IVulnDataAttr): string[] =>
        vuln.acceptation === "REJECTED" ? [...acc, vuln.id] : acc,
      []
    );
    void handleAcceptation({
      variables: {
        acceptedVulns,
        findingId: props.findingId,
        justification: values.justification,
        rejectedVulns,
      },
    });
  }

  const initialTreatment: string = canHandleVulnsAcceptation
    ? "ACCEPTED_UNDEFINED"
    : "";

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t(
          "search_findings.tab_description.handle_acceptation_modal.title"
        )}
        open={true}
      >
        <GenericForm
          initialValues={{
            treatment: initialTreatment,
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
              <JustificationField />
            </Col100>
          </Row>
          <ButtonToolbar>
            <Button onClick={handleCloseModal}>
              {translate.t("group.findings.report.modal_close")}
            </Button>
            <Button
              disabled={!hasAcceptationVulns || handlingAcceptation}
              onClick={handleUpdateTreatmentAcceptation}
            >
              {translate.t("confirmmodal.proceed")}
            </Button>
          </ButtonToolbar>
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};

export { HandleAcceptationModal };
