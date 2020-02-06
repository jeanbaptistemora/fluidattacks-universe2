/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Mutation, MutationFn, MutationResult, Query, QueryResult } from "react-apollo";
import { Col, FormGroup, Glyphicon, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import { Field, InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import { default as globalStyle } from "../../../../styles/global.css";
import { fileInputField } from "../../../../utils/forms/fields";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { required, validRecordsFile } from "../../../../utils/validations";
import { GenericForm } from "../../components/GenericForm";
import { REMOVE_EVIDENCE_MUTATION, UPDATE_EVIDENCE_MUTATION } from "../EvidenceView/queries";
import { GET_FINDING_RECORDS } from "./queries";

type IRecordsViewProps = RouteComponentProps<{ findingId: string }>;

const recordsView: React.FC<IRecordsViewProps> = (props: IRecordsViewProps): JSX.Element => {
  const { findingId } = props.match.params;
  const { userName, userOrganization, userRole } = window as typeof window & Dictionary<string>;

  const onMount: (() => void) = (): void => {
    mixpanel.track("FindingRecords", { Organization: userOrganization, User: userName });
  };
  React.useEffect(onMount, []);

  const [isEditing, setEditing] = React.useState(false);
  const handleEditClick: (() => void) = (): void => { setEditing(!isEditing); };

  return (
    <React.StrictMode>
      <Query query={GET_FINDING_RECORDS} variables={{ findingId }}>
        {({ data, refetch }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

          const handleUpdateResult: (() => void) = (): void => {
            refetch()
              .catch();
          };
          const handleUpdateError: ((updateError: ApolloError) => void) = (updateError: ApolloError): void => {
            updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
              switch (message) {
                case "Exception - Wrong File Structure":
                  msgError(translate.t("proj_alerts.invalid_structure"));
                  break;
                case "Exception - Invalid File Size":
                  msgError(translate.t("proj_alerts.file_size"));
                  break;
                case "Exception - Invalid File Type":
                  msgError(translate.t("proj_alerts.file_type_wrong"));
                  break;
                default:
                  msgError(translate.t("proj_alerts.error_textsad"));
                  rollbar.error("An error occurred updating records", updateError);
              }
            });
          };

          const canEdit: boolean = _.includes(["admin", "analyst"], userRole);

          return (
            <React.Fragment>
              <Row>
                <Col md={2} mdOffset={10} xs={12} sm={12}>
                  {canEdit ? (
                    <Button block={true} onClick={handleEditClick}>
                      <FluidIcon icon="edit" />&nbsp;{translate.t("search_findings.tab_evidence.editable")}
                    </Button>
                  ) : undefined}
                </Col>
              </Row>
              <br />
              {isEditing ? (
                <Mutation
                  mutation={UPDATE_EVIDENCE_MUTATION}
                  onCompleted={handleUpdateResult}
                  onError={handleUpdateError}
                >
                  {(updateRecords: MutationFn, updateRes: MutationResult): React.ReactNode => {
                    const handleSubmit: ((values: { filename: FileList }) => void) = (
                      values: { filename: FileList },
                    ): void => {
                      setEditing(false);
                      updateRecords({ variables: { evidenceId: "8", file: values.filename[0], findingId } })
                        .catch();
                    };

                    return (
                      <GenericForm name="records" onSubmit={handleSubmit}>
                        {({ pristine }: InjectedFormProps): React.ReactNode => (
                          <React.Fragment>
                            <Row>
                              <Col md={3} mdOffset={7}>
                                <FormGroup>
                                  <Field
                                    accept=".csv"
                                    component={fileInputField}
                                    id="recordsFile"
                                    name="filename"
                                    validate={[required, validRecordsFile]}
                                  />
                                </FormGroup>
                              </Col>
                              <Col md={2}>
                                <Button type="submit" block={true} disabled={pristine || updateRes.loading}>
                                  <Glyphicon glyph="cloud-upload" />
                                  &nbsp;{translate.t("search_findings.tab_evidence.update")}
                                </Button>
                              </Col>
                            </Row>
                          </React.Fragment>
                        )}
                      </GenericForm>
                    );
                  }}
                </Mutation>
              ) : undefined}
              {isEditing && !_.isEmpty(JSON.parse(data.finding.records)) ? (
                <Mutation mutation={REMOVE_EVIDENCE_MUTATION} onCompleted={handleUpdateResult}>
                  {(removeRecords: MutationFn, removeRes: MutationResult): React.ReactNode => {
                    const handleRemoveClick: (() => void) = (): void => {
                      mixpanel.track("RemoveRecords", { Organization: userOrganization, User: userName });
                      setEditing(false);
                      removeRecords({ variables: { evidenceId: "8", findingId } })
                        .catch();
                    };

                    return (
                      <Row>
                        <Col md={2} mdOffset={10}>
                          <Button onClick={handleRemoveClick} block={true} disabled={removeRes.loading}>
                            <FluidIcon icon="delete" />
                            &nbsp;{translate.t("search_findings.tab_evidence.remove")}
                          </Button>
                        </Col>
                      </Row>
                    );
                  }}
                </Mutation>
              ) : undefined}
              <Row>
                {_.isEmpty(JSON.parse(data.finding.records)) ? (
                  <div className={globalStyle.noData}>
                    <Glyphicon glyph="list" />
                    <p>{translate.t("project.findings.records.no_data")}</p>
                  </div>
                ) : (
                    <DataTableNext
                      bordered={true}
                      dataset={JSON.parse(data.finding.records)}
                      exportCsv={false}
                      headers={[]}
                      id="tblRecords"
                      pageSize={15}
                      remote={false}
                      search={false}
                    />
                  )}
              </Row>
            </React.Fragment>
          );
        }}
      </Query>
    </React.StrictMode>
  );
};

export { recordsView as RecordsView };
