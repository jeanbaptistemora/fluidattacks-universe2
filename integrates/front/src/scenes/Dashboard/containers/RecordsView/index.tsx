/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { MutationFunction, MutationResult, QueryResult } from "@apollo/react-common";
import { Mutation, Query } from "@apollo/react-components";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Glyphicon } from "react-bootstrap";
import { useParams } from "react-router";
import { Field, InjectedFormProps } from "redux-form";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { FluidIcon } from "components/FluidIcon";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { REMOVE_EVIDENCE_MUTATION, UPDATE_EVIDENCE_MUTATION } from "scenes/Dashboard/containers/EvidenceView/queries";
import { GET_FINDING_RECORDS } from "scenes/Dashboard/containers/RecordsView/queries";
import { default as globalStyle } from "styles/global.css";
import { ButtonToolbarRow, Col100, Row, RowCenter } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { FileInput } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { required, validRecordsFile } from "utils/validations";

const recordsView: React.FC = (): JSX.Element => {
  const { findingId } = useParams<{ findingId: string }>();

  const onMount: (() => void) = (): void => {
    mixpanel.track("FindingRecords");
  };
  React.useEffect(onMount, []);

  const [isEditing, setEditing] = React.useState(false);
  const handleEditClick: (() => void) = (): void => { setEditing(!isEditing); };

  const handleErrors: ((error: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("group_alerts.error_textsad"));
      Logger.warning("An error occurred loading finding records", error);
    });
  };

  const handleRemoveErrors: ((removeError: ApolloError) => void) = (removeError: ApolloError): void => {
    msgError(translate.t("group_alerts.error_textsad"));
    Logger.warning("An error occurred removing records", removeError);
  };

  return (
    <React.StrictMode>
      <Query query={GET_FINDING_RECORDS} variables={{ findingId }} onError={handleErrors}>
        {({ data, refetch }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

          const handleUpdateResult: (() => void) = (): void => {
            void refetch();
          };
          const handleUpdateError: ((updateError: ApolloError) => void) = (updateError: ApolloError): void => {
            updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
              switch (message) {
                case "Exception - Wrong File Structure":
                  msgError(translate.t("group_alerts.invalid_structure"));
                  break;
                case "Exception - Invalid File Size":
                  msgError(translate.t("validations.file_size", { count: 1 }));
                  break;
                case "Exception - Invalid File Type":
                  msgError(translate.t("group_alerts.file_type_csv"));
                  break;
                default:
                  msgError(translate.t("group_alerts.error_textsad"));
                  Logger.warning("An error occurred updating records", updateError);
              }
            });
          };

          return (
            <React.Fragment>
              <Can do="backend_api_mutations_update_evidence_mutate">
                <Row>
                  <Col100 className={"pa0"}>
                    <Button className={"fr"} onClick={handleEditClick}>
                      <FluidIcon icon="edit" />&nbsp;{translate.t("search_findings.tab_evidence.editable")}
                    </Button>
                  </Col100>
                </Row>
              </Can>
              <br />
              {isEditing ? (
                <Mutation
                  mutation={UPDATE_EVIDENCE_MUTATION}
                  onCompleted={handleUpdateResult}
                  onError={handleUpdateError}
                >
                  {(updateRecords: MutationFunction, updateRes: MutationResult): JSX.Element => {
                    const handleSubmit: ((values: { filename: FileList }) => void) = (
                      values: { filename: FileList },
                    ): void => {
                      setEditing(false);
                      void updateRecords({ variables: { evidenceId: "RECORDS", file: values.filename[0], findingId } });
                    };

                    return (
                      <GenericForm name="records" onSubmit={handleSubmit}>
                        {({ pristine }: InjectedFormProps): React.ReactNode => (
                          <React.Fragment>
                            <ButtonToolbarRow className={"mb3"}>
                              <Field
                                accept=".csv"
                                component={FileInput}
                                className={"fr"}
                                id="recordsFile"
                                name="filename"
                                validate={[required, validRecordsFile]}
                              />
                              <Button className={"h-25"} type="submit" disabled={pristine || updateRes.loading}>
                                <Glyphicon glyph="cloud-upload" />
                                &nbsp;{translate.t("search_findings.tab_evidence.update")}
                              </Button>
                            </ButtonToolbarRow>
                          </React.Fragment>
                        )}
                      </GenericForm>
                    );
                  }}
                </Mutation>
              ) : undefined}
              {isEditing && !_.isEmpty(JSON.parse(data.finding.records)) ? (
                <Mutation
                  mutation={REMOVE_EVIDENCE_MUTATION}
                  onCompleted={handleUpdateResult}
                  onError={handleRemoveErrors}
                >
                  {(removeRecords: MutationFunction, removeRes: MutationResult): JSX.Element => {
                    const handleRemoveClick: (() => void) = (): void => {
                      mixpanel.track("RemoveRecords");
                      setEditing(false);
                      void removeRecords({ variables: { evidenceId: "RECORDS", findingId } });
                    };

                    return (
                      <Row>
                        <Col100 className={"pa0"}>
                          <Button className={"fr"} onClick={handleRemoveClick} disabled={removeRes.loading}>
                            <FluidIcon icon="delete" />
                            &nbsp;{translate.t("search_findings.tab_evidence.remove")}
                          </Button>
                        </Col100>
                      </Row>
                    );
                  }}
                </Mutation>
              ) : undefined}
              <RowCenter>
                {_.isEmpty(JSON.parse(data.finding.records)) ? (
                  <div className={globalStyle["no-data"]}>
                    <Glyphicon glyph="list" />
                    <p>{translate.t("group.findings.records.no_data")}</p>
                  </div>
                ) : (
                    <DataTableNext
                      bordered={true}
                      dataset={JSON.parse(data.finding.records)}
                      exportCsv={false}
                      headers={[]}
                      id="tblRecords"
                      pageSize={15}
                      search={false}
                    />
                  )}
              </RowCenter>
            </React.Fragment>
          );
        }}
      </Query>
    </React.StrictMode>
  );
};

export { recordsView as RecordsView };
