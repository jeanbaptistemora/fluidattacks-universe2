/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { Mutation, MutationFn, MutationResult, Query, QueryResult } from "react-apollo";
import { Col, Row } from "react-bootstrap";
import { useSelector } from "react-redux";
import { formValueSelector, InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { FluidIcon } from "../../../../components/FluidIcon";
import { hidePreloader, showPreloader } from "../../../../utils/apollo";
import { castFieldsCVSS3, castPrivileges } from "../../../../utils/formatHelpers";
import { dropdownField } from "../../../../utils/forms/fields";
import { msgSuccess } from "../../../../utils/notifications";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";
import { EditableField } from "../../components/EditableField";
import { GenericForm } from "../../components/GenericForm/index";
import { GET_FINDING_HEADER } from "../FindingContent/queries";
import * as actions from "./actions";
import { default as style } from "./index.css";
import { GET_SEVERITY, UPDATE_SEVERITY_MUTATION } from "./queries";
import { ISeverityAttr, ISeverityField, ISeverityViewProps, IUpdateSeverityAttr } from "./types";

const renderCVSSFields: ((props: ISeverityViewProps, data: ISeverityAttr) => JSX.Element[]) =
  (props: ISeverityViewProps, data: ISeverityAttr): JSX.Element[] =>
  []
        .map((field: ISeverityField, index: number) => {
        const value: string = field.currentValue;
        const text: string = field.options[value];

        return (
          <Row className={style.row} key={index}>
            <EditableField
              alignField="horizontal"
              component={dropdownField}
              currentValue={`${value} | ${translate.t(text)}`}
              label={field.title}
              name={field.name}
              renderAsEditable={props.isEditing}
              validate={[required]}
            >
              <option value="" selected={true} />
              {Object.keys(field.options)
                .map((key: string) => (
                <option value={`${key}`}>
                  {translate.t(field.options[key])}
                </option>
              ))}
            </EditableField>
          </Row>
        );
      });

const renderEnvironmentFields: ((props: ISeverityViewProps, data: ISeverityAttr) => JSX.Element[]) =
  (props: ISeverityViewProps,  data: ISeverityAttr): JSX.Element[] =>
  []
        .map((field: ISeverityField, index: number) => {
        const value: string = field.currentValue;
        const text: string = field.options[value];

        return (
          <Row className={style.row} key={index}>
            <EditableField
              alignField="horizontal"
              component={dropdownField}
              currentValue={`${value} | ${translate.t(text)}`}
              label={field.title}
              name={field.name}
              renderAsEditable={props.isEditing}
              validate={[required]}
              visible={props.isEditing}
            >
              <option value="" selected={true} />
              {Object.keys(field.options)
                .map((key: string) => (
                <option value={`${key}`}>
                  {translate.t(field.options[key])}
                </option>
              ))}
            </EditableField>
          </Row>
        );
      });

export const renderSeverityFields: ((props: ISeverityViewProps, data: ISeverityAttr) => JSX.Element) =
(props: ISeverityViewProps, data: ISeverityAttr): JSX.Element => {
  const cvssVersion: string = (props.isEditing)
    ? props.formValues.editSeverity.values.cvssVersion
    : data.finding.cvssVersion;

  const severityScope: string = (props.isEditing)
    ? props.formValues.editSeverity.values.severityScope
    : data.finding.severity.severityScope;

  const modifiedSeverityScope: string = (props.isEditing)
    ? props.formValues.editSeverity.values.modifiedSeverityScope
    : data.finding.severity.modifiedSeverityScope;

  const privilegesOptions: {[value: string]: string} = castPrivileges(severityScope);
  const modPrivilegesOptions: {[value: string]: string} = castPrivileges(modifiedSeverityScope);

  const privileges: string = data.finding.severity.privilegesRequired;
  const modPrivileges: string = data.finding.severity.modifiedPrivilegesRequired;

  return (
    <React.Fragment>
      <Row className={style.row}>
        <EditableField
          alignField="horizontal"
          component={dropdownField}
          currentValue={data.finding.cvssVersion}
          label={translate.t("search_findings.tab_severity.cvss_version")}
          name="cvssVersion"
          renderAsEditable={props.isEditing}
          validate={[required]}
          visible={props.isEditing}
        >
          <option value="" selected={true} />
          <option value="3.1">3.1</option>
        </EditableField>
      </Row>
      {renderCVSSFields(props, data)}
      <Row className={style.row}>
        <EditableField
          alignField="horizontal"
          component={dropdownField}
          currentValue={`${privileges} | ${translate.t(privilegesOptions[privileges])}`}
          label={translate.t("search_findings.tab_severity.privileges_required")}
          name="privilegesRequired"
          renderAsEditable={props.isEditing}
          validate={[required]}
        >
          <option value="" selected={true} />
          {Object.keys(privilegesOptions)
            .map((key: string) => (
            <option value={`${key}`}>
              {translate.t(privilegesOptions[key])}
            </option>
          ))}
        </EditableField>
      </Row>
      { cvssVersion === "3.1" && props.isEditing
        ?
        <React.Fragment>
          {renderEnvironmentFields(props, data)}
          <Row className={style.row}>
            <EditableField
              alignField="horizontal"
              component={dropdownField}
              currentValue={`${modPrivileges} | ${translate.t(modPrivilegesOptions[modPrivileges])}`}
              label={translate.t("search_findings.tab_severity.modified_privileges_required")}
              name="modifiedPrivilegesRequired"
              renderAsEditable={props.isEditing}
              validate={[required]}
              visible={props.isEditing}
            >
              <option value="" selected={true} />
              {Object.keys(modPrivilegesOptions)
                .map((key: string) => (
                <option value={`${key}`}>
                  {translate.t(modPrivilegesOptions[key])}
                </option>
              ))}
            </EditableField>
          </Row>
        </React.Fragment>
        : undefined
      }
    </React.Fragment>
  );
};

const severityView: React.FC<ISeverityViewProps> = (props: ISeverityViewProps): JSX.Element => {
  const onMount: (() => void) = (): void => {
    mixpanel.track("FindingSeverity", {
      Organization: (window as Window & { userOrganization: string }).userOrganization,
      User: (window as Window & { userName: string }).userName,
    });
  };
  React.useEffect(onMount, []);

  const [isEditing, setEditing] = React.useState(false);

  const selector: (state: {}, ...field: string[]) => Dictionary<string> = formValueSelector("editSeverity");
  const formValues: Dictionary<string> = useSelector((state: {}) => selector(
    state, "cvssVersion", "severityScope", "modifiedSeverityScope"));

  return (
    <React.StrictMode>
      <Row>
        <Col md={12} sm={12} xs={12}>
          <Query query={GET_SEVERITY} variables={{ identifier: props.findingId }}>
            {({ client, data, loading, refetch }: QueryResult<ISeverityAttr>): React.ReactNode => {
              if (_.isUndefined(data) || loading) { return <React.Fragment />; }

              const handleEditClick: (() => void) = (): void => {
                setEditing(!isEditing);
                const severityScore: string = actions.calcCVSSv3(data.finding.severity)
                  .toFixed(1);
                client.writeData({ data: { finding: { id: props.findingId, severityScore, __typename: "Finding" } } });
              };

              const handleMtUpdateSeverityRes: ((mtResult: IUpdateSeverityAttr) => void) =
                (mtResult: IUpdateSeverityAttr): void => {
                  if (!_.isUndefined(mtResult)) {
                    if (mtResult.updateSeverity.success) {
                      refetch()
                        .catch();
                      hidePreloader();
                      msgSuccess(translate.t("proj_alerts.updated"), translate.t("proj_alerts.updated_title"));
                      mixpanel.track("UpdateSeverity", {
                        Organization: (window as Window & { userOrganization: string }).userOrganization,
                        User: (window as Window & { userName: string }).userName,
                      });
                    }
                  }
                };

              const { userRole } = (window as typeof window & { userRole: string });
              const canEdit: boolean = _.includes(["admin", "analyst"], userRole);

              return (
                <React.Fragment>
                  <Row>
                    <Col md={2} mdOffset={10}>
                      {canEdit ? (
                        <Button block={true} onClick={handleEditClick}>
                          <FluidIcon icon="edit" />&nbsp;{translate.t("search_findings.tab_severity.editable")}
                        </Button>
                      ) : undefined}
                    </Col>
                  </Row>
                  <br />
                  <Mutation
                    mutation={UPDATE_SEVERITY_MUTATION}
                    onCompleted={handleMtUpdateSeverityRes}
                    refetchQueries={[{
                      query: GET_FINDING_HEADER,
                      variables: { findingId: props.findingId, submissionField: canEdit },
                    }]}
                  >
                    {(updateSeverity: MutationFn, mutationRes: MutationResult): React.ReactNode => {
                      if (mutationRes.loading) {
                        showPreloader();
                      }

                      const handleUpdateSeverity: ((values: {}) => void) = (values: {}): void => {
                        setEditing(false);
                        showPreloader();
                        updateSeverity({
                          variables: { data: { ...values, id: props.findingId }, findingId: props.findingId },
                        })
                          .catch();
                      };

                      const handleFormChange: ((values: ISeverityAttr["finding"]["severity"]) => void) = (
                        values: ISeverityAttr["finding"]["severity"],
                      ): void => {
                        const severityScore: string = actions.calcCVSSv3(values)
                          .toFixed(1);
                        client.writeData({
                          data: {
                            finding: { id: props.findingId, severityScore, __typename: "Finding" },
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
                                <Row>
                                  <Col md={2} mdOffset={10}>
                                    <Button type="submit" block={true} disabled={pristine || mutationRes.loading}>
                                      <FluidIcon icon="loading" /> {translate.t("search_findings.tab_severity.update")}
                                    </Button>
                                  </Col>
                                </Row>
                              ) : undefined}
                              <Row className={style.row}>
                                <EditableField
                                  alignField="horizontal"
                                  component={dropdownField}
                                  currentValue={data.finding.cvssVersion}
                                  label={translate.t("search_findings.tab_severity.cvss_version")}
                                  name="cvssVersion"
                                  renderAsEditable={isEditing}
                                  validate={[required]}
                                  visible={isEditing}
                                >
                                  <option value="" selected={true} />
                                  <option value="3.1">3.1</option>
                                </EditableField>
                              </Row>
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
                                      validate={[required]}
                                    >
                                      <option value="" selected={true} />
                                      {_.map(field.options, (text: string, value: string) => (
                                        <option value={value}>{translate.t(text)}</option>
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
