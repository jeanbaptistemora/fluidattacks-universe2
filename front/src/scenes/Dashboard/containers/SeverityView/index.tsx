/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { MutationFunction, MutationResult, QueryResult } from "@apollo/react-common";
import { Mutation, Query } from "@apollo/react-components";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { ApolloError } from "apollo-client";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { useSelector } from "react-redux";
import { RouteComponentProps } from "react-router";
import { Field, formValueSelector, InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import { Can } from "../../../../utils/authz/Can";
import { authzContext } from "../../../../utils/authz/config";
import { calcCVSSv3 } from "../../../../utils/cvss";
import { castFieldsCVSS3 } from "../../../../utils/formatHelpers";
import { dropdownField } from "../../../../utils/forms/fields";
import { msgError, msgSuccess } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";
import { EditableField } from "../../components/EditableField";
import { GenericForm } from "../../components/GenericForm/index";
import { GET_FINDING_HEADER } from "../FindingContent/queries";
import { default as style } from "./index.css";
import { GET_SEVERITY, UPDATE_SEVERITY_MUTATION } from "./queries";
import { ISeverityAttr, ISeverityField, IUpdateSeverityAttr } from "./types";

type SeverityViewProps = RouteComponentProps<{ findingId: string }>;

const severityView: React.FC<SeverityViewProps> = (props: SeverityViewProps): JSX.Element => {
  const { findingId } = props.match.params;
  const { userName, userOrganization } = window as typeof window & Dictionary<string>;
  const permissions: PureAbility<string> = useAbility(authzContext);

  const onMount: (() => void) = (): void => {
    mixpanel.track("FindingSeverity", { Organization: userOrganization, User: userName });
  };
  React.useEffect(onMount, []);

  const [isEditing, setEditing] = React.useState(false);

  const selector: (state: {}, ...field: string[]) => Dictionary<string> = formValueSelector("editSeverity");
  const formValues: Dictionary<string> = useSelector((state: {}) => selector(
    state, "cvssVersion", "severityScope", "modifiedSeverityScope"));

  const handleErrors: ((error: ApolloError) => void) = (error: ApolloError): void => {
    msgError(translate.t("proj_alerts.error_textsad"));
    rollbar.error("An error occurred loading finding severity", error);
  };

  return (
    <React.StrictMode>
      <Row>
        <Col md={12} sm={12} xs={12}>
          <Query query={GET_SEVERITY} variables={{ identifier: findingId }} onError={handleErrors}>
            {({ client, data, refetch }: QueryResult<ISeverityAttr>): JSX.Element => {
              if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

              const handleEditClick: (() => void) = (): void => {
                setEditing(!isEditing);
                const severityScore: string = calcCVSSv3(data.finding.severity)
                  .toFixed(1);
                client.writeData({ data: { finding: { id: findingId, severityScore, __typename: "Finding" } } });
              };

              const handleMtUpdateSeverityRes: ((mtResult: IUpdateSeverityAttr) => void) =
                (mtResult: IUpdateSeverityAttr): void => {
                  if (!_.isUndefined(mtResult)) {
                    if (mtResult.updateSeverity.success) {
                      refetch()
                        .catch();
                      msgSuccess(translate.t("proj_alerts.updated"), translate.t("proj_alerts.updated_title"));
                      mixpanel.track("UpdateSeverity", { Organization: userOrganization, User: userName });
                    }
                  }
                };

              return (
                <React.Fragment>
                  <Can do="backend_api_resolvers_finding__do_update_severity">
                    <Row>
                      <Col md={2} mdOffset={10}>
                        <Button block={true} onClick={handleEditClick}>
                          <FluidIcon icon="edit" />&nbsp;{translate.t("search_findings.tab_severity.editable")}
                        </Button>
                      </Col>
                    </Row>
                  </Can>
                  <br />
                  <Mutation
                    mutation={UPDATE_SEVERITY_MUTATION}
                    onCompleted={handleMtUpdateSeverityRes}
                    refetchQueries={[
                      {
                        query: GET_FINDING_HEADER,
                        variables: {
                          canGetHistoricState: permissions.can("backend_api_dataloaders_finding__get_historic_state"),
                          findingId,
                        },
                      },
                    ]}
                  >
                    {(updateSeverity: MutationFunction, mutationRes: MutationResult): JSX.Element => {
                      const handleUpdateSeverity: ((values: {}) => void) = (values: {}): void => {
                        setEditing(false);
                        updateSeverity({ variables: { data: { ...values, id: findingId }, findingId } })
                          .catch();
                      };

                      const handleFormChange: ((values: ISeverityAttr["finding"]["severity"]) => void) = (
                        values: ISeverityAttr["finding"]["severity"],
                      ): void => {
                        const severityScore: string = calcCVSSv3(values)
                          .toFixed(1);
                        client.writeData({
                          data: {
                            finding: { id: findingId, severityScore, __typename: "Finding" },
                          },
                        });
                      };

                      return (
                        <GenericForm
                          name="editSeverity"
                          initialValues={{ ...data.finding.severity, cvssVersion: data.finding.cvssVersion }}
                          onSubmit={handleUpdateSeverity}
                          onChange={handleFormChange}
                        >
                          {({ pristine }: InjectedFormProps): React.ReactNode => (
                            <React.Fragment>
                              {isEditing ? (
                                <React.Fragment>
                                  <Row>
                                    <Col md={2} mdOffset={10}>
                                      <Button type="submit" block={true} disabled={pristine || mutationRes.loading}>
                                        <FluidIcon icon="loading" />
                                        {translate.t("search_findings.tab_severity.update")}
                                      </Button>
                                    </Col>
                                  </Row>
                                  <Row className={style.row}>
                                    <FormGroup>
                                      <Col md={3} className={style.title}>
                                        <ControlLabel>
                                          <b>{translate.t("search_findings.tab_severity.cvss_version")}</b>
                                        </ControlLabel>
                                      </Col>
                                      <Col md={9}>
                                        <Field
                                          component={dropdownField}
                                          name="cvssVersion"
                                          validate={required}
                                        >
                                          <option value="" />
                                          <option value="3.1">3.1</option>
                                        </Field>
                                      </Col>
                                    </FormGroup>
                                  </Row>
                                </React.Fragment>
                              ) : undefined}
                              {castFieldsCVSS3(data.finding.severity, isEditing, formValues)
                                .map((field: ISeverityField, index: number) => (
                                  <Row className={style.row} key={index}>
                                    <EditableField
                                      alignField="horizontal"
                                      component={dropdownField}
                                      currentValue={
                                        `${field.currentValue} | ${translate.t(field.options[field.currentValue])}`}
                                      label={field.title}
                                      name={field.name}
                                      renderAsEditable={isEditing}
                                      validate={required}
                                    >
                                      <option value="" />
                                      {_.map(field.options, (text: string, value: string) => (
                                        <option key={text} value={value}>{translate.t(text)}</option>
                                      ))}
                                    </EditableField>
                                  </Row>
                                ))}
                            </React.Fragment>
                          )}
                        </GenericForm>
                      );
                    }}
                  </Mutation>
                </React.Fragment>
              );
            }}
          </Query>
        </Col>
      </Row>
    </React.StrictMode>
  );
};

export { severityView as SeverityView };
