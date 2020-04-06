/* tslint:disable:jsx-no-multiline-js
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code in graphql queries
 */
import { MutationFunction, MutationResult } from "@apollo/react-common";
import { Mutation } from "@apollo/react-components";
import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, ControlLabel, FormGroup, Glyphicon, Row } from "react-bootstrap";
import { Field, submit } from "redux-form";
import { Button } from "../../../../components/Button";
import { Modal } from "../../../../components/Modal";
import store from "../../../../store";
import { formatDropdownField } from "../../../../utils/formatHelpers";
import { dropdownField, tagInputField, textField } from "../../../../utils/forms/fields";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { isValidVulnSeverity, numeric, required } from "../../../../utils/validations";
import { IHistoricTreatment } from "../../containers/DescriptionView/types";
import { GenericForm } from "../GenericForm";
import { DELETE_TAGS_MUTATION, GET_PROJECT_USERS, GET_VULNERABILITIES, UPDATE_TREATMENT_MUTATION } from "./queries";
import {
  IDeleteTagAttr, IDeleteTagResult, IUpdateTreatmentVulnAttr, IUpdateVulnTreatment, IVulnDataType,
} from "./types";

export interface IUpdateTreatmentModal {
  btsUrl?: string;
  findingId: string;
  lastTreatment?: IHistoricTreatment;
  projectName?: string;
  userRole: string;
  vulnerabilities: IVulnDataType[];
  handleCloseModal(): void;
}

const updateTreatmentModal: ((props: IUpdateTreatmentModal) => JSX.Element) =
(props: IUpdateTreatmentModal): JSX.Element => {
  const canDisplayAnalyst: boolean = _.includes(["analyst", "admin"], props.userRole);

  const sortTags: ((tags: string) => string) = (tags: string): string => {
    const tagSplit: string[] = tags.trim()
      .split(",");

    return tagSplit.sort()
      .join(", ");
  };

  const sameTags: boolean = props.vulnerabilities.every(
    (vuln: IVulnDataType) => sortTags(vuln.treatments.tag) === sortTags(props.vulnerabilities[0].treatments.tag));

  const handleUpdateTreatError: ((updateError: ApolloError) => void) = (updateError: ApolloError): void => {
    updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
      switch (message) {
        case "Invalid treatment manager":
          msgError(translate.t("proj_alerts.invalid_treatment_mgr"));
          break;
        default:
          msgError(translate.t("proj_alerts.error_textsad"));
          rollbar.error("An error occurred updating vuln treatment", updateError);
      }
    });
  };
  const handleClose: (() => void) = (): void => { props.handleCloseModal(); };
  const handleUpdateResult: ((mtResult: IUpdateVulnTreatment) => void) = (mtResult: IUpdateVulnTreatment): void => {
    if (!_.isUndefined(mtResult)) {
      if (mtResult.updateTreatmentVuln.success) {
        mixpanel.track(
          "UpdatedTreatmentVulnerabilities", {
            Organization: (window as typeof window & { userOrganization: string }).userOrganization,
            User: (window as typeof window & { userName: string }).userName,
          });
        msgSuccess(
          translate.t("search_findings.tab_description.update_vulnerabilities"),
          translate.t("proj_alerts.title_success"));
        props.handleCloseModal();
      }
    }
  };

  const canEditManager: boolean = _.includes(["admin", "customeradmin"], props.userRole);

  const { data } = useQuery(GET_PROJECT_USERS, {
    skip: !canEditManager,
    variables: {
      projectName: props.projectName,
    },
  });

  const userEmails: string[] = canEditManager && !(_.isUndefined(data) || _.isEmpty(data))
    ? data.project.users.map((user: Dictionary<string>): string => user.email)
    : [(window as typeof window & Dictionary<string>).userEmail];

  const lastTreatment: IHistoricTreatment = props.lastTreatment === undefined
    ? {date: "", treatment: "", user: ""}
    : props.lastTreatment;

  return(
    <Mutation
      mutation={UPDATE_TREATMENT_MUTATION}
      onCompleted={handleUpdateResult}
      onError={handleUpdateTreatError}
      refetchQueries={[{ query: GET_VULNERABILITIES,
                         variables: { analystField: canDisplayAnalyst, identifier: props.findingId } }]}
    >
      {(updateTreatmentVuln: MutationFunction<IUpdateVulnTreatment, IUpdateTreatmentVulnAttr>,
        updateResult: MutationResult): JSX.Element => {

          const handleUpdateTreatmentVuln: ((dataTreatment: IUpdateTreatmentVulnAttr) => void) =
            (dataTreatment: IUpdateTreatmentVulnAttr): void => {
              if (props.vulnerabilities.length === 0) {
                msgError(translate.t("search_findings.tab_resources.no_selection"));
              } else {
                updateTreatmentVuln({variables: {
                  findingId: props.findingId,
                  severity: !_.isEmpty(dataTreatment.severity) ? Number(dataTreatment.severity) : -1,
                  tag: dataTreatment.tag,
                  treatmentManager: dataTreatment.treatmentManager,
                  vulnerabilities: props.vulnerabilities.map((vuln: IVulnDataType) => vuln.id),
                }})
                .catch();
              }
          };
          const handleEditTreatment: (() => void) = (): void => {
            store.dispatch(submit("editTreatmentVulnerability"));
          };

          const handleDeleteError: ((updateError: ApolloError) => void) = (updateError: ApolloError): void => {
            msgError(translate.t("proj_alerts.error_textsad"));
          };
          const handleDeleteResult: ((mtResult: IDeleteTagResult) => void) =
          (mtResult: IDeleteTagResult): void => {
            if (!_.isUndefined(mtResult)) {
              if (mtResult.deleteTags.success) {
                msgSuccess(
                  translate.t("search_findings.tab_description.update_vulnerabilities"),
                  translate.t("proj_alerts.title_success"));
                props.handleCloseModal();
              }
            }
          };

          return (
            <Mutation
              mutation={DELETE_TAGS_MUTATION}
              onCompleted={handleDeleteResult}
              onError={handleDeleteError}
              refetchQueries={[{ query: GET_VULNERABILITIES,
                                 variables: { analystField: canDisplayAnalyst, identifier: props.findingId } }]}
            >
              {(deleteTagVuln: MutationFunction<IDeleteTagResult, IDeleteTagAttr>,
                tagsResult: MutationResult): JSX.Element => {
                const handleDeleteTag: (() => void) = (): void => {
                  if (props.vulnerabilities.length === 0) {
                    msgError(translate.t("search_findings.tab_resources.no_selection"));
                  } else {
                    deleteTagVuln({variables: {
                      findingId: props.findingId,
                      vulnerabilities: props.vulnerabilities.map((vuln: IVulnDataType) => vuln.id),
                    }})
                    .catch();
                  }
                };

                return (
                  <Modal
                    open={true}
                    footer={
                      <ButtonToolbar className="pull-right">
                        <Button onClick={handleClose}>
                          {translate.t("project.findings.report.modal_close")}
                        </Button>
                        <Button
                          disabled={updateResult.loading || tagsResult.loading}
                          onClick={handleEditTreatment}
                        >
                          {translate.t("confirmmodal.proceed")}
                        </Button>
                      </ButtonToolbar>
                    }
                    headerTitle={translate.t("search_findings.tab_description.editVuln")}
                  >
                  <GenericForm
                    name="editTreatmentVulnerability"
                    onSubmit={handleUpdateTreatmentVuln}
                    initialValues={{
                      tag: sameTags ? props.vulnerabilities[0].treatments.tag : undefined,
                      treatmentManager: props.vulnerabilities[0].treatments.treatmentManager,
                    }}
                  >
                      <Row>
                        <Col md={12}>
                          <FormGroup>
                            <ControlLabel>
                              <b>{translate.t("search_findings.tab_description.bts")}</b>
                            </ControlLabel>
                            <p>{props.btsUrl}</p>
                          </FormGroup>
                        </Col>
                      </Row>
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
                              component={dropdownField}
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
                        <Col md={12}>
                          <FormGroup>
                            <ControlLabel>
                              <b>{translate.t("search_findings.tab_description.tag")}</b>
                            </ControlLabel>
                            <Field component={tagInputField} name="tag" type="text" />
                          </FormGroup>
                        </Col>
                        <Col md={6}>
                          <FormGroup>
                            <ControlLabel>
                              <b>{translate.t("search_findings.tab_description.business_criticality")}</b>
                            </ControlLabel>
                            <Field
                              component={textField}
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
                  </Modal>
                );
              }}
            </Mutation>
          );
      }}
    </Mutation>
  );
};

export { updateTreatmentModal as UpdateTreatmentModal };
