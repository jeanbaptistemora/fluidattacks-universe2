import { useMutation, useQuery } from "@apollo/react-hooks";
import { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { useSelector } from "react-redux";
import { useParams } from "react-router";
import { formValueSelector, InjectedFormProps } from "redux-form";

import { Button } from "components/Button/index";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { EditableField } from "scenes/Dashboard/components/EditableField";
import { GenericForm } from "scenes/Dashboard/components/GenericForm/index";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import {
  GET_SEVERITY,
  UPDATE_SEVERITY_MUTATION,
} from "scenes/Dashboard/containers/SeverityView/queries";
import {
  ISeverityAttr,
  ISeverityField,
  IUpdateSeverityAttr,
} from "scenes/Dashboard/containers/SeverityView/types";
import { castFieldsCVSS3 } from "scenes/Dashboard/containers/SeverityView/utils";
import { ButtonToolbarRow, Col100, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { calcCVSSv3 } from "utils/cvss";
import { Dropdown } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { required } from "utils/validations";

const severityView: React.FC = (): JSX.Element => {
  const { findingId } = useParams<{ findingId: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const groupPermissions: PureAbility<string> = useAbility(authzGroupContext);

  const [isEditing, setEditing] = React.useState(false);

  const selector: (state: {}, ...field: string[]) => Dictionary<string> = formValueSelector("editSeverity");
  const formValues: Dictionary<string> = useSelector((state: {}) => selector(
    state, "cvssVersion", "severityScope", "modifiedSeverityScope"));

  const handleErrors: ((error: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred loading finding severity", error);
    });
  };

  const {client, data, refetch } = useQuery<ISeverityAttr>(GET_SEVERITY, {
    onError: handleErrors,
    variables: { identifier: findingId },
  });

  const handleEditClick: (() => void) = (): void => {
    setEditing(!isEditing);
    if (!_.isUndefined(data)) {
      const severityScore: string = Number(calcCVSSv3(data.finding.severity))
        .toFixed(2);
      client.writeData({ data: { finding: { id: findingId, severityScore, __typename: "Finding" } } });
    }
  };

  const handleMtUpdateSeverityRes: ((mtResult: IUpdateSeverityAttr) => void) =
    (mtResult: IUpdateSeverityAttr): void => {
      if (!_.isUndefined(mtResult)) {
        if (mtResult.updateSeverity.success) {
          void refetch();
          msgSuccess(translate.t("groupAlerts.updated"), translate.t("groupAlerts.updatedTitle"));
          mixpanel.track("UpdateSeverity");
        }
      }
  };

  const handleMtError: ((error: ApolloError) => void) = (
    { graphQLErrors }: ApolloError,
  ): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred updating severity", error);
    });
  };

  const [updateSeverity, mutationRes] = useMutation(UPDATE_SEVERITY_MUTATION, {
    onCompleted: handleMtUpdateSeverityRes,
    onError: handleMtError,
    refetchQueries: [
      {
        query: GET_FINDING_HEADER,
        variables: {
          canGetExploit: groupPermissions.can("has_forces"),
          canGetHistoricState: permissions.can("backend_api_resolvers_finding_historic_state_resolve"),
          findingId,
        },
      },
    ],
  });

  const handleUpdateSeverity: ((values: {}) => void) = (values: {}): void => {
    setEditing(false);
    void updateSeverity({ variables: { data: { ...values, id: findingId }, findingId } });
  };

  const handleFormChange: ((values: ISeverityAttr["finding"]["severity"]) => void) = (
    values: ISeverityAttr["finding"]["severity"],
  ): void => {
    const severityScore: string = Number(calcCVSSv3(values))
      .toFixed(2);
    client.writeData({
      data: {
        finding: { id: findingId, severityScore, __typename: "Finding" },
      },
    });
  };

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <Row>
        <Col100>
          <React.Fragment>
            <Can do="backend_api_mutations_update_severity_mutate">
              <ButtonToolbarRow>
                <TooltipWrapper
                  id={translate.t("search_findings.tab_severity.editableTooltip.id")}
                  message={translate.t("search_findings.tab_severity.editableTooltip")}
                >
                  <Button onClick={handleEditClick}>
                    <FluidIcon icon="edit" />&nbsp;{translate.t("search_findings.tab_severity.editable")}
                  </Button>
                </TooltipWrapper>
              </ButtonToolbarRow>
            </Can>
            <br />
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
                      <ButtonToolbarRow>
                        <Button type="submit" disabled={pristine || mutationRes.loading}>
                          <FluidIcon icon="loading" />
                          {translate.t("search_findings.tab_severity.update")}
                        </Button>
                      </ButtonToolbarRow>
                      <Row>
                        <EditableField
                            style={"background-color: 000;" as React.CSSProperties}
                            alignField="horizontal"
                            component={Dropdown}
                            currentValue={"3.1"}
                            label={translate.t("search_findings.tab_severity.cvssVersion")}
                            name={"cvssVersion"}
                            renderAsEditable={isEditing}
                            validate={required}
                          >
                            <option value="" />
                            <option value="3.1">3.1</option>
                          </EditableField>
                      </Row>
                    </React.Fragment>
                  ) : undefined}
                  {castFieldsCVSS3(data.finding.severity, isEditing, formValues)
                    .map((field: ISeverityField, index: number) => {
                      const currentOption: string = field.options[field.currentValue];

                      return (
                        <Row key={index}>
                          <EditableField
                            style={"background-color: 000;" as React.CSSProperties}
                            alignField="horizontal"
                            component={Dropdown}
                            currentValue={
                              `${Number(field.currentValue)
                                .toFixed(2)} | ${translate.t(currentOption)}`}
                            id={`Row${index}`}
                            label={field.title}
                            name={field.name}
                            renderAsEditable={isEditing}
                            tooltip={_.isEmpty(currentOption)
                              ? undefined : translate.t(currentOption.replace(/text/, "tooltip"))}
                            validate={required}
                          >
                            <option value="" />
                            {_.map(field.options, (text: string, value: string) => (
                              <option key={text} value={value}>{translate.t(text)}</option>
                            ))}
                          </EditableField>
                        </Row>
                      );
                    })}
                </React.Fragment>
              )}
            </GenericForm>
          </React.Fragment>
        </Col100>
      </Row>
    </React.StrictMode>
  );
};

export { severityView as SeverityView };
