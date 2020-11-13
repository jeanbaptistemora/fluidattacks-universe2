/* tslint:disable:jsx-no-multiline-js
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code in graphql queries
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, Glyphicon } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { Dispatch } from "redux";
import { Field, isPristine, submit } from "redux-form";
import { ConfigurableValidator } from "revalidate";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { EditableField } from "scenes/Dashboard/components/EditableField";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import {
  GET_PROJECT_USERS,
  GET_VULNERABILITIES,
} from "scenes/Dashboard/components/Vulnerabilities/queries";
import { IUpdateTreatmentVulnAttr, IVulnDataType } from "scenes/Dashboard/components/Vulnerabilities/types";
import {
  DELETE_TAGS_MUTATION,
  UPDATE_DESCRIPTION_MUTATION,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/queries";
import {
  IDeleteTagAttr,
  IDeleteTagResult,
  IUpdateTreatmentModal,
  IUpdateVulnDescriptionResult,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/types";
import { groupExternalBts, sortTags } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import {
  Col100,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { formatDropdownField } from "utils/formatHelpers";
import { Dropdown, TagInput, Text } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { isValidVulnSeverity, maxLength, numeric, required, validUrlField } from "utils/validations";

const maxBtsLength: ConfigurableValidator = maxLength(80);
const updateTreatmentModal: ((props: IUpdateTreatmentModal) => JSX.Element) = (
  props: IUpdateTreatmentModal,
): JSX.Element => {
  const { userEmail } = window as typeof window & Dictionary<string>;
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const { handleCloseModal } = props;

  const vulnsTags: string[][] = props.vulnerabilities.map((vuln: IVulnDataType) => sortTags(vuln.treatments.tag));

  const dispatch: Dispatch = useDispatch();
  const [updateVuln, {loading: updatingVuln}] = useMutation<IUpdateVulnDescriptionResult>(UPDATE_DESCRIPTION_MUTATION, {
    onCompleted: async (result: IUpdateVulnDescriptionResult): Promise<void> => {
      if (result.updateTreatmentVuln.success) {
        mixpanel.track(
          "UpdatedTreatmentVulnerabilities", {
            User: (window as typeof window & { userName: string }).userName,
          });
        msgSuccess(
          translate.t("search_findings.tab_description.update_vulnerabilities"),
          translate.t("group_alerts.title_success"));
        handleCloseModal();
      }
    },
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        switch (message) {
          case "Invalid treatment manager":
            msgError(translate.t("group_alerts.invalid_treatment_mgr"));
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("An error occurred updating vuln treatment", updateError);
        }
      });
    },
    refetchQueries: [
      { query: GET_VULNERABILITIES,
        variables: {
          analystField: permissions.can("backend_api_resolvers_new_finding_analyst_resolve"),
          identifier: props.findingId,
        },
      },
    ],
  });

  const { data } = useQuery(GET_PROJECT_USERS, {
    skip: permissions.cannot("backend_api_resolvers_project__get_users"),
    variables: {
      projectName: props.projectName,
    },
  });

  const [deleteTagVuln, {loading: deletingTag}] = useMutation<IDeleteTagResult, IDeleteTagAttr>
  (DELETE_TAGS_MUTATION, {
    onCompleted: async (result: IDeleteTagResult): Promise<void> => {
      if (!_.isUndefined(result)) {
        if (result.deleteTags.success) {
          msgSuccess(
            translate.t("search_findings.tab_description.update_vulnerabilities"),
            translate.t("group_alerts.title_success"));
        }
      }
    },
    onError: (updateError: ApolloError): void => {
      updateError.graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        Logger.warning("An error occurred deleting vulnerabilities", error);
      });
    },
    refetchQueries: [
      { query: GET_VULNERABILITIES,
        variables: {
          analystField: permissions.can("backend_api_resolvers_new_finding_analyst_resolve"),
          identifier: props.findingId,
        },
      },
    ],
  });

  const handleUpdateTreatmentVuln: ((dataTreatment: IUpdateTreatmentVulnAttr) => void) =
    (dataTreatment: IUpdateTreatmentVulnAttr): void => {
      if (props.vulnerabilities.length === 0) {
        msgError(translate.t("search_findings.tab_resources.no_selection"));
      } else {
        updateVuln({variables: {
          externalBts: dataTreatment.externalBts,
          findingId: props.findingId,
          severity: !_.isEmpty(dataTreatment.severity) ? Number(dataTreatment.severity) : -1,
          tag: dataTreatment.tag,
          treatmentManager: dataTreatment.treatmentManager,
          vulnerabilities: props.vulnerabilities.map((vuln: IVulnDataType) => vuln.id),
        }});
      }
  };

  const handleDeleteTag: (() => void) = (): void => {
    if (props.vulnerabilities.length === 0) {
      msgError(translate.t("search_findings.tab_resources.no_selection"));
    } else {
      deleteTagVuln({variables: {
        findingId: props.findingId,
        vulnerabilities: props.vulnerabilities.map((vuln: IVulnDataType) => vuln.id),
      }});
      handleCloseModal();
    }
  };

  const handleEditTreatment: (() => void) = (): void => {
    dispatch(submit("editTreatmentVulnerability"));
  };

  const handleDeletion: ((tag: string) => void) = (tag: string): void => {
    deleteTagVuln({variables: {
      findingId: props.findingId,
      tag,
      vulnerabilities: props.vulnerabilities.map((vuln: IVulnDataType) => vuln.id),
    }});
  };

  const userEmails: string[] = (_.isUndefined(data) || _.isEmpty(data))
    ? [userEmail]
    : data.project.stakeholders.map((stakeholder: Dictionary<string>): string => stakeholder.email);

  const lastTreatment: IHistoricTreatment = props.lastTreatment === undefined
    ? {date: "", treatment: "", user: ""}
    : props.lastTreatment;

  const isEditPristine: boolean = useSelector((state: {}) =>
    isPristine("editTreatmentVulnerability")(state));

  return(
    <React.StrictMode>
      <Modal
        open={true}
        headerTitle={translate.t("search_findings.tab_description.editVuln")}
      >
        <GenericForm
          name="editTreatmentVulnerability"
          onSubmit={handleUpdateTreatmentVuln}
          initialValues={{
            externalBts: groupExternalBts(props.vulnerabilities),
            tag: _.join((_.intersection(...vulnsTags)), ","),
            treatmentManager: props.vulnerabilities[0].treatments.treatmentManager,
          }}
        >
          <Row>
            <Col md={6}>
              <FormGroup>
                <ControlLabel>
                  <b>{translate.t("search_findings.tab_description.treatment.title")}</b>
                </ControlLabel>
                <p>{translate.t(formatDropdownField(lastTreatment.treatment))}</p>
              </FormGroup>
            </Col>
            <Col md={6}>
              <FormGroup>
                <ControlLabel>
                  <b>{translate.t("search_findings.tab_description.treatment_mgr")}</b>
                </ControlLabel>
                <Field
                  component={Dropdown}
                  name="treatmentManager"
                  type="text"
                  validate={lastTreatment.treatment === "IN PROGRESS" ? required : undefined}
                >
                  <option value="" />
                  {userEmails.map((email: string, index: number): JSX.Element => (
                    <option key={index} value={email}>{email}</option>
                  ))}
                </Field>
              </FormGroup>
            </Col>
          </Row>
          <Row>
            <Col md={12}>
              <FormGroup>
                <ControlLabel>
                  <b>{translate.t("search_findings.tab_description.treatment_just")}</b>
                </ControlLabel>
                <p>{lastTreatment.justification}</p>
              </FormGroup>
            </Col>
          </Row>
          <Row>
            <Col100>
              <Can do="backend_api_resolvers_vulnerability__do_update_treatment_vuln" passThrough={true}>
                {(canEdit: boolean): JSX.Element => (
                  <EditableField
                    component={Text}
                    currentValue={groupExternalBts(props.vulnerabilities)}
                    label={translate.t("search_findings.tab_description.bts")}
                    name="externalBts"
                    placeholder={translate.t("search_findings.tab_description.bts_placeholder")}
                    renderAsEditable={canEdit}
                    type="text"
                    validate={[maxBtsLength, validUrlField]}
                  />
                )}
              </Can>
            </Col100>
          </Row>
          <Row>
            <Col md={12}>
              <FormGroup>
                <ControlLabel>
                  <b>{translate.t("search_findings.tab_description.tag")}</b>
                </ControlLabel>
                <Field component={TagInput} name="tag" onDeletion={handleDeletion} type="text" />
              </FormGroup>
            </Col>
            <Col md={6}>
              <FormGroup>
                <ControlLabel>
                  <b>{translate.t("search_findings.tab_description.business_criticality")}</b>
                </ControlLabel>
                <Field
                  component={Text}
                  name="severity"
                  type="number"
                  validate={[isValidVulnSeverity, numeric]}
                />
              </FormGroup>
            </Col>
          </Row>
          <Row>
            <Col md={6}>
              <Button onClick={handleDeleteTag}>
                <Glyphicon glyph="minus" />&nbsp;
                {translate.t("search_findings.tab_description.deleteTags")}
              </Button>
            </Col>
          </Row>
        </GenericForm>
        <ButtonToolbar className="pull-right">
          <Button onClick={handleCloseModal}>
            {translate.t("group.findings.report.modal_close")}
          </Button>
          <Can do="backend_api_resolvers_vulnerability__do_update_treatment_vuln">
            <Button
              disabled={updatingVuln || deletingTag || isEditPristine}
              onClick={handleEditTreatment}
            >
              {translate.t("confirmmodal.proceed")}
            </Button>
          </Can>
        </ButtonToolbar>
      </Modal>
    </React.StrictMode>
  );
};

export { updateTreatmentModal as UpdateTreatmentModal };
