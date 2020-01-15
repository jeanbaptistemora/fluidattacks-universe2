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
import { connect, ConnectedComponent, MapDispatchToProps } from "react-redux";
import { RouteComponentProps } from "react-router";
import { Field, InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { DataTableNext } from "../../../../components/DataTableNext/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { fileInputField } from "../../../../utils/forms/fields";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { required, validRecordsFile } from "../../../../utils/validations";
import { GenericForm } from "../../components/GenericForm";
import { UPDATE_EVIDENCE_MUTATION } from "../EvidenceView/queries";
import { removeRecords, ThunkDispatcher } from "./actions";
import { GET_FINDING_RECORDS } from "./queries";

type IRecordsViewBaseProps = Pick<RouteComponentProps<{ findingId: string }>, "match">;

interface IRecordsViewDispatchProps {
  onRemove(): void;
}

type IRecordsViewProps = IRecordsViewBaseProps & IRecordsViewDispatchProps;

const renderRemoveField: ((arg1: IRecordsViewProps) => JSX.Element) = (props: IRecordsViewProps): JSX.Element => {
  const handleRemoveClick: (() => void) = (): void => {
    mixpanel.track("RemoveRecords", {
      Organization: (window as Window & { userOrganization: string }).userOrganization,
      User: (window as Window & { userName: string }).userName,
    });
    props.onRemove();
  };

  return (
    <Row>
      <Col md={4} mdOffset={6} xs={12} sm={12} />
      <Col sm={2}>
        <Button
          bsStyle="primary"
          block={true}
          onClick={handleRemoveClick}
        >
          <FluidIcon icon="delete" />
          &nbsp;{translate.t("search_findings.tab_evidence.remove")}
        </Button>
      </Col>
    </Row>
  );
};

export const recordsView: React.FC<IRecordsViewProps> = (props: IRecordsViewProps): JSX.Element => {
  const { findingId } = props.match.params;

  const onMount: (() => void) = (): void => {
    mixpanel.track("FindingRecords", {
      Organization: (window as Window & { userOrganization: string }).userOrganization,
      User: (window as Window & { userName: string }).userName,
    });
  };
  React.useEffect(onMount, []);

  const [isEditing, setEditing] = React.useState(false);
  const handleEditClick: (() => void) = (): void => { setEditing(!isEditing); };

  return (
    <React.StrictMode>
      <Query query={GET_FINDING_RECORDS} variables={{ findingId }}>
        {({ data, loading, refetch }: QueryResult): JSX.Element => {
          if (_.isUndefined(data) || loading) { return <React.Fragment />; }

          const handleUpdateResult: (() => void) = (): void => {
            hidePreloader();
            refetch()
              .catch();
          };
          const handleUpdateError: ((updateError: ApolloError) => void) = (updateError: ApolloError): void => {
            hidePreloader();
            updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
              switch (message) {
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

          const { userRole } = (window as typeof window & { userRole: string });
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
                      showPreloader();
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
              {isEditing && JSON.parse(data.finding.records).length > 0 ? renderRemoveField(props) : undefined}
              <Row>
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
              </Row>
            </React.Fragment>
          );
        }}
      </Query>
    </React.StrictMode>
  );
};

const mapDispatchToProps: MapDispatchToProps<IRecordsViewDispatchProps, IRecordsViewBaseProps> =
  (dispatch: ThunkDispatcher, ownProps: IRecordsViewBaseProps): IRecordsViewDispatchProps => {
    const { findingId } = ownProps.match.params;

    return ({
      onRemove: (): void => { dispatch(removeRecords(findingId)); },
    });
  };

const connectedRecordsView: ConnectedComponent<React.ComponentType<IRecordsViewProps>, IRecordsViewBaseProps> =
  connect(undefined, mapDispatchToProps)(recordsView);

export { connectedRecordsView as RecordsView };
