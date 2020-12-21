import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import type { Dispatch } from "redux";
import { GET_VULNERABILITIES } from "scenes/Dashboard/components/Vulnerabilities/queries";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { GraphQLError } from "graphql";
import { HANDLE_VULNS_ACCEPTATION } from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/queries";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { JustificationField } from "./JustificationField";
import { Logger } from "utils/logger";
import { Modal } from "components/Modal";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { authzPermissionsContext } from "utils/authz/config";
import { changeVulnTreatmentFormatter } from "components/DataTableNext/formatters";
import { submit } from "redux-form";
import { translate } from "utils/translations/translate";
import { useAbility } from "@casl/react";
import { useDispatch } from "react-redux";
import { useMutation } from "@apollo/react-hooks";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import type {
  IHandleVulnsAcceptationModalProps,
  IHandleVulnsAcceptationResultAttr,
  IVulnDataAttr,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/types";
import { msgError, msgSuccess } from "utils/notifications";

const HandleAcceptationModal: React.FC<IHandleVulnsAcceptationModalProps> = (
  props: IHandleVulnsAcceptationModalProps
): JSX.Element => {
  const { findingId, vulns, handleCloseModal, refetchData } = props;

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canDisplayAnalyst: boolean = permissions.can(
    "backend_api_resolvers_new_finding_analyst_resolve"
  );
  const [vulnerabilitiesList, setVulnerabilities] = React.useState(vulns);
  const dispatch: Dispatch = useDispatch();

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
    const acceptedVulns: string[] = vulnerabilitiesList.reduce(
      (acc: string[], vuln: IVulnDataAttr): string[] =>
        vuln.acceptation === "APPROVED" ? [...acc, vuln.id] : acc,
      []
    );
    const rejectedVulns: string[] = vulnerabilitiesList.reduce(
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

  const handleUpdateAcceptation: (vulnInfo: Dictionary<string>) => void = (
    vulnInfo: Dictionary<string>
  ): void => {
    const newVulnList: IVulnDataAttr[] = vulnerabilitiesList.map(
      (vuln: IVulnDataAttr): IVulnDataAttr =>
        vuln.id !== vulnInfo.id
          ? vuln
          : {
              ...vuln,
              acceptation:
                vuln.acceptation === "APPROVED" ? "REJECTED" : "APPROVED",
            }
    );
    setVulnerabilities([...newVulnList]);
  };
  const vulnsHeader: IHeaderConfig[] = [
    {
      align: "left",
      dataField: "where",
      header: "Where",
      width: "50%",
      wrapped: true,
    },
    {
      align: "left",
      dataField: "specific",
      header: "Specific",
      width: "25%",
      wrapped: true,
    },
    {
      align: "left",
      changeFunction: handleUpdateAcceptation,
      dataField: "acceptation",
      formatter: changeVulnTreatmentFormatter,
      header: "Acceptation",
      width: "25%",
      wrapped: true,
    },
  ];

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t("search_findings.tab_description.editVuln")}
        open={true}
      >
        <GenericForm
          name={"updateTreatmentAcceptation"}
          onSubmit={handleSubmit}
        >
          <Row>
            <Col100>
              <DataTableNext
                bordered={false}
                dataset={vulnerabilitiesList}
                exportCsv={false}
                headers={vulnsHeader}
                id={"vulnsToHandleAcceptation"}
                pageSize={10}
                search={false}
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
              disabled={handlingAcceptation}
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
