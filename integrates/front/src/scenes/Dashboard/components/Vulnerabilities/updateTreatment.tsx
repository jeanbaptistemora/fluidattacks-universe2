/* tslint:disable:jsx-no-multiline-js
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code in graphql queries
 */
import { MutationFunction, MutationResult } from "@apollo/react-common";
import { Mutation } from "@apollo/react-components";
import { useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, ControlLabel, FormGroup, Glyphicon, Row } from "react-bootstrap";
import { Field, submit } from "redux-form";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import {
  DELETE_TAGS_MUTATION,
  GET_PROJECT_USERS,
  GET_VULNERABILITIES,
  UPDATE_TREATMENT_MUTATION,
} from "scenes/Dashboard/components/Vulnerabilities/queries";
import {
  IDeleteTagAttr, IDeleteTagResult, IUpdateTreatmentVulnAttr, IUpdateVulnTreatment, IVulnDataType,
} from "scenes/Dashboard/components/Vulnerabilities/types";
import { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";
import { formatDropdownField } from "utils/formatHelpers";
import { Dropdown, TagInput, Text } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { isValidVulnSeverity, numeric, required } from "utils/validations";

export interface IUpdateTreatmentModal {
  btsUrl?: string;
  findingId: string;
  lastTreatment?: IHistoricTreatment;
  projectName?: string;
  vulnerabilities: IVulnDataType[];
  handleCloseModal(): void;
}

const updateTreatmentModal: ((props: IUpdateTreatmentModal) => JSX.Element) = (
  props: IUpdateTreatmentModal,
): JSX.Element => {
  const { userEmail } = window as typeof window & Dictionary<string>;
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  const sortTags: ((tags: string) => string[]) = (tags: string): string[] => {
    const tagSplit: string[] = tags.trim()
      .split(",");

    return tagSplit.map((tag: string) => tag.trim());
  };

  const vulnsTags: string[][] = props.vulnerabilities.map((vuln: IVulnDataType) => sortTags(vuln.treatments.tag));

  const handleUpdateTreatError: ((updateError: ApolloError) => void) = (updateError: ApolloError): void => {
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
  };
  const handleClose: (() => void) = (): void => { props.handleCloseModal(); };
  const handleUpdateResult: ((mtResult: IUpdateVulnTreatment) => void) = (mtResult: IUpdateVulnTreatment): void => {
    if (!_.isUndefined(mtResult)) {
      if (mtResult.updateTreatmentVuln.success) {
        mixpanel.track(
          "UpdatedTreatmentVulnerabilities", {
            User: (window as typeof window & { userName: string }).userName,
          });
        msgSuccess(
          translate.t("search_findings.tab_description.update_vulnerabilities"),
          translate.t("group_alerts.title_success"));
        props.handleCloseModal();
      }
    }
  };

  const { data } = useQuery(GET_PROJECT_USERS, {
    skip: permissions.cannot("backend_api_resolvers_project__get_users"),
    variables: {
      projectName: props.projectName,
    },
  });

  const userEmails: string[] = (_.isUndefined(data) || _.isEmpty(data))
    ? [userEmail]
    : data.project.users.map((user: Dictionary<string>): string => user.email);

  const lastTreatment: IHistoricTreatment = props.lastTreatment === undefined
    ? {date: "", treatment: "", user: ""}
    : props.lastTreatment;

  return(
    <Mutation
      mutation={UPDATE_TREATMENT_MUTATION}
      onCompleted={handleUpdateResult}
      onError={handleUpdateTreatError}
      refetchQueries={[
        {
          query: GET_VULNERABILITIES,
          variables: {
            analystField: permissions.can("backend_api_resolvers_finding__get_analyst"),
            identifier: props.findingId,
          },
        },
      ]}
    >
      {(updateTreatmentVuln: MutationFunction<IUpdateVulnTreatment, IUpdateTreatmentVulnAttr>,
        updateResult: MutationResult): JSX.Element => {

          const handleUpdateTreatmentVuln: ((dataTreatment: IUpdateTreatmentVulnAttr) => void) =
            (dataTreatment: IUpdateTreatmentVulnAttr): void => {
              if (props.vulnerabilities.length === 0) {
                msgError(translate.t("search_findings.tab_resources.no_selection"));
              } else {
                void updateTreatmentVuln({variables: {
                  findingId: props.findingId,
                  severity: !_.isEmpty(dataTreatment.severity) ? Number(dataTreatment.severity) : -1,
                  tag: dataTreatment.tag,
                  treatmentManager: dataTreatment.treatmentManager,
                  vulnerabilities: props.vulnerabilities.map((vuln: IVulnDataType) => vuln.id),
                }});
              }
          };
          const handleEditTreatment: (() => void) = (): void => {
            store.dispatch(submit("editTreatmentVulnerability"));
          };

          const handleDeleteError: ((updateError: ApolloError) => void) = (
            { graphQLErrors }: ApolloError,
          ): void => {
            graphQLErrors.forEach((error: GraphQLError): void => {
              msgError(translate.t("group_alerts.error_textsad"));
              Logger.warning("An error occurred deleting vulnerabilities", error);
            });
          };
          const handleDeleteResult: ((mtResult: IDeleteTagResult) => void) =
          (mtResult: IDeleteTagResult): void => {
            if (!_.isUndefined(mtResult)) {
              if (mtResult.deleteTags.success) {
                msgSuccess(
                  translate.t("search_findings.tab_description.update_vulnerabilities"),
                  translate.t("group_alerts.title_success"));
              }
            }
          };

          return (
            <Mutation
              mutation={DELETE_TAGS_MUTATION}
              onCompleted={handleDeleteResult}
              onError={handleDeleteError}
              refetchQueries={[
                {
                  query: GET_VULNERABILITIES,
                  variables: {
                    analystField: permissions.can("backend_api_resolvers_finding__get_analyst"),
                    identifier: props.findingId,
                  },
                },
              ]}
            >
              {(deleteTagVuln: MutationFunction<IDeleteTagResult, IDeleteTagAttr>,
                tagsResult: MutationResult): JSX.Element => {
                const handleDeleteTag: (() => void) = (): void => {
                  if (props.vulnerabilities.length === 0) {
                    msgError(translate.t("search_findings.tab_resources.no_selection"));
                  } else {
                    void deleteTagVuln({variables: {
                      findingId: props.findingId,
                      vulnerabilities: props.vulnerabilities.map((vuln: IVulnDataType) => vuln.id),
                    }});
                  }
                };
                const handleDeletion: ((tag: string) => void) = (tag: string): void => {
                  void deleteTagVuln({variables: {
                    findingId: props.findingId,
                    tag,
                    vulnerabilities: props.vulnerabilities.map((vuln: IVulnDataType) => vuln.id),
                  }});
                };

                return (
                  <Modal
                    open={true}
                    footer={
                      <ButtonToolbar className="pull-right">
                        <Button onClick={handleClose}>
                          {translate.t("group.findings.report.modal_close")}
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
                      tag: _.join((_.intersection(...vulnsTags)), ","),
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
