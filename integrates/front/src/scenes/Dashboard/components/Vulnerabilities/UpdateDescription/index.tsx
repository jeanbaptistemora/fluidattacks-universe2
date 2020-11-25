/* tslint:disable:jsx-no-multiline-js
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code in graphql queries
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { ApolloError } from "apollo-client";
import { ExecutionResult, GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Glyphicon } from "react-bootstrap";
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
  Col50,
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
const updateTreatmentModal: React.FC<IUpdateTreatmentModal> = (
  props: IUpdateTreatmentModal,
): JSX.Element => {
  const { userEmail } = window as typeof window & Dictionary<string>;
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const { handleCloseModal } = props;
  const [isRunning, setRunning] = React.useState(false);

  const vulnsTags: string[][] = props.vulnerabilities.map((vuln: IVulnDataType) => sortTags(vuln.tag));

  const dispatch: Dispatch = useDispatch();
  const [updateVuln, {loading: updatingVuln}] = useMutation<IUpdateVulnDescriptionResult>(UPDATE_DESCRIPTION_MUTATION, {
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

  const handleUpdateTreatmentVuln: ((dataTreatment: IUpdateTreatmentVulnAttr) => Promise<void>) = async (
    dataTreatment: IUpdateTreatmentVulnAttr): Promise<void> => {
      if (props.vulnerabilities.length === 0) {
        msgError(translate.t("search_findings.tab_resources.no_selection"));
      } else {
        try {
          setRunning(true);
          const results: Array<ExecutionResult<IUpdateVulnDescriptionResult>> = await Promise.all(
            _.chunk(props.vulnerabilities, props.vulnerabilitiesChunk)
              .map((vulnsChuncked: IVulnDataType[]) => (
                updateVuln({variables: {
                  externalBts: dataTreatment.externalBts,
                  findingId: props.findingId,
                  severity: _.isEmpty(dataTreatment.severity) ? -1 : Number(dataTreatment.severity),
                  tag: dataTreatment.tag,
                  treatmentManager: dataTreatment.treatmentManager,
                  vulnerabilities: vulnsChuncked.map((vuln: IVulnDataType) => vuln.id),
                }})
              )));

          const areAllMutationValid: boolean[] = results.map((
            result: ExecutionResult<IUpdateVulnDescriptionResult>,
          ) => {
            if (!_.isUndefined(result.data) && !_.isNull(result.data)) {

              return result.data.updateTreatmentVuln.success;
            }

            return false;
          });

          if (areAllMutationValid.every(Boolean)) {
            mixpanel.track(
              "UpdatedTreatmentVulnerabilities", {
              User: (window as typeof window & { userName: string }).userName,
            });
            msgSuccess(
              translate.t("search_findings.tab_description.update_vulnerabilities"),
              translate.t("group_alerts.title_success"),
            );
            handleCloseModal();
          }
        } catch (updateError) {
          if (_.includes(String(updateError), "Invalid treatment manager")) {
            msgError(translate.t("group_alerts.invalid_treatment_mgr"));
          } else {
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("An error occurred updating vuln treatment", updateError);
          }
        } finally {
          setRunning(false);
        }
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
            treatmentManager: props.vulnerabilities[0].treatmentManager,
          }}
        >
          <Row>
            <Col50>
              <FormGroup>
                <ControlLabel>
                  <b>{translate.t("search_findings.tab_description.treatment.title")}</b>
                </ControlLabel>
                <p>{translate.t(formatDropdownField(lastTreatment.treatment))}</p>
              </FormGroup>
            </Col50>
            <Col50>
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
            </Col50>
          </Row>
          <Row>
            <Col100>
              <FormGroup>
                <ControlLabel>
                  <b>{translate.t("search_findings.tab_description.treatment_just")}</b>
                </ControlLabel>
                <p>{lastTreatment.justification}</p>
              </FormGroup>
            </Col100>
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
            <Col100>
              <FormGroup>
                <ControlLabel>
                  <b>{translate.t("search_findings.tab_description.tag")}</b>
                </ControlLabel>
                <Field component={TagInput} name="tag" onDeletion={handleDeletion} type="text" />
              </FormGroup>
            </Col100>
            <Col50>
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
            </Col50>
          </Row>
          <Row>
            <Col50>
              <Button onClick={handleDeleteTag}>
                <Glyphicon glyph="minus" />&nbsp;
                {translate.t("search_findings.tab_description.deleteTags")}
              </Button>
            </Col50>
          </Row>
        </GenericForm>
        <ButtonToolbar className="pull-right">
          <Button onClick={handleCloseModal}>
            {translate.t("group.findings.report.modal_close")}
          </Button>
          <Can do="backend_api_resolvers_vulnerability__do_update_treatment_vuln">
            <Button
              disabled={updatingVuln || deletingTag || isRunning || isEditPristine}
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
