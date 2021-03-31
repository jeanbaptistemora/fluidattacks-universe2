import type { ApolloError } from "apollo-client";
import { Button } from "components/Button/index";
import { Can } from "utils/authz/Can";
import { Dropdown } from "utils/forms/fields";
import { EditableField } from "scenes/Dashboard/components/EditableField";
import { FluidIcon } from "components/FluidIcon";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import { GenericForm } from "scenes/Dashboard/components/GenericForm/index";
import type { GraphQLError } from "graphql";
import type { InjectedFormProps } from "redux-form";
import { Logger } from "utils/logger";
import type { PureAbility } from "@casl/ability";
import { SeverityContent } from "scenes/Dashboard/containers/SeverityView/SeverityContent/index";
import { TooltipWrapper } from "components/TooltipWrapper";
import _ from "lodash";
import { calcCVSSv3 } from "utils/cvss";
import { castFieldsCVSS3 } from "scenes/Dashboard/containers/SeverityView/utils";
import { formValueSelector } from "redux-form";
import { required } from "utils/validations";
import { track } from "mixpanel-browser";
import { translate } from "utils/translations/translate";
import { useAbility } from "@casl/react";
import { useParams } from "react-router";
import { useSelector } from "react-redux";
import { ButtonToolbarRow, Col100, Row } from "styles/styledComponents";
import {
  GET_SEVERITY,
  UPDATE_SEVERITY_MUTATION,
} from "scenes/Dashboard/containers/SeverityView/queries";
import type {
  ISeverityAttr,
  ISeverityField,
  IUpdateSeverityAttr,
} from "scenes/Dashboard/containers/SeverityView/types";
import React, { useCallback, useState } from "react";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";
import { useMutation, useQuery } from "@apollo/react-hooks";

const SeverityView: React.FC = (): JSX.Element => {
  const { findingId } = useParams<{ findingId: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const groupPermissions: PureAbility<string> = useAbility(authzGroupContext);

  const [isEditing, setEditing] = useState(false);

  const selector: (
    state: Record<string, unknown>,
    // eslint-disable-next-line fp/no-rest-parameters
    ...field: string[]
  ) => Dictionary<string> = formValueSelector("editSeverity");
  const formValues: Dictionary<string> = useSelector(
    (state: Record<string, unknown>): Dictionary<string> =>
      selector(state, "cvssVersion", "severityScope", "modifiedSeverityScope")
  );

  const handleErrors: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred loading finding severity", error);
    });
  };

  const { client, data, refetch } = useQuery<ISeverityAttr>(GET_SEVERITY, {
    onError: handleErrors,
    variables: { identifier: findingId },
  });

  const handleEditClick: () => void = useCallback((): void => {
    setEditing(!isEditing);
    if (!_.isUndefined(data)) {
      const severityScore: string = Number(
        calcCVSSv3(data.finding.severity)
      ).toFixed(2);
      client.writeData({
        data: {
          finding: { __typename: "Finding", id: findingId, severityScore },
        },
      });
    }
  }, [client, data, findingId, isEditing]);

  const handleMtUpdateSeverityRes: (mtResult: IUpdateSeverityAttr) => void = (
    mtResult: IUpdateSeverityAttr
  ): void => {
    if (!_.isUndefined(mtResult)) {
      if (mtResult.updateSeverity.success) {
        void refetch();
        msgSuccess(
          translate.t("groupAlerts.updated"),
          translate.t("groupAlerts.updatedTitle")
        );
        track("UpdateSeverity");
      }
    }
  };

  const handleMtError: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
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
          canGetHistoricState: permissions.can(
            "backend_api_resolvers_finding_historic_state_resolve"
          ),
          findingId,
        },
      },
    ],
  });

  const handleUpdateSeverity: (
    values: Record<string, unknown>
  ) => void = useCallback(
    (values: Record<string, unknown>): void => {
      setEditing(false);
      void updateSeverity({
        variables: { data: { ...values, id: findingId }, findingId },
      });
    },
    [findingId, updateSeverity]
  );

  const handleFormChange: (
    values: ISeverityAttr["finding"]["severity"]
  ) => void = useCallback(
    (values: ISeverityAttr["finding"]["severity"]): void => {
      const severityScore: string = Number(calcCVSSv3(values)).toFixed(2);
      client.writeData({
        data: {
          finding: { __typename: "Finding", id: findingId, severityScore },
        },
      });
    },
    [client, findingId]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <Row>
        <Col100>
          <React.Fragment>
            <Can do={"backend_api_mutations_update_severity_mutate"}>
              <ButtonToolbarRow>
                <TooltipWrapper
                  id={translate.t(
                    "searchFindings.tabSeverity.editableTooltip.id"
                  )}
                  message={translate.t(
                    "searchFindings.tabSeverity.editableTooltip"
                  )}
                >
                  <Button onClick={handleEditClick}>
                    <FluidIcon icon={"edit"} />
                    &nbsp;{translate.t("searchFindings.tabSeverity.editable")}
                  </Button>
                </TooltipWrapper>
              </ButtonToolbarRow>
            </Can>
            <br />
            {isEditing ||
            data.finding.severityScore <= 0 ||
            data.finding.cvssVersion !== "3.1" ? (
              <GenericForm
                initialValues={{
                  ...data.finding.severity,
                  cvssVersion: data.finding.cvssVersion,
                }}
                name={"editSeverity"}
                onChange={handleFormChange}
                onSubmit={handleUpdateSeverity}
              >
                {({ pristine }: InjectedFormProps): React.ReactNode => (
                  <React.Fragment>
                    {isEditing ? (
                      <React.Fragment>
                        <ButtonToolbarRow>
                          <Button
                            disabled={pristine || mutationRes.loading}
                            type={"submit"}
                          >
                            <FluidIcon icon={"loading"} />
                            {translate.t("searchFindings.tabSeverity.update")}
                          </Button>
                        </ButtonToolbarRow>
                        <Row>
                          <EditableField
                            alignField={"horizontal"}
                            component={Dropdown}
                            currentValue={"3.1"}
                            label={translate.t(
                              "searchFindings.tabSeverity.cvssVersion"
                            )}
                            name={"cvssVersion"}
                            renderAsEditable={isEditing}
                            validate={required}
                          >
                            <option value={""} />
                            <option value={"3.1"}>{"3.1"}</option>
                          </EditableField>
                        </Row>
                      </React.Fragment>
                    ) : undefined}
                    {castFieldsCVSS3(
                      data.finding.severity,
                      isEditing,
                      formValues
                    ).map(
                      (field: ISeverityField, index: number): JSX.Element => {
                        const currentOption: string =
                          field.options[field.currentValue];

                        return (
                          <Row key={index.toString()}>
                            <EditableField
                              alignField={"horizontal"}
                              component={Dropdown}
                              currentValue={`${Number(
                                field.currentValue
                              ).toFixed(2)} | ${translate.t(currentOption)}`}
                              id={`Row${index}`}
                              label={field.title}
                              name={field.name}
                              renderAsEditable={isEditing}
                              tooltip={
                                _.isEmpty(currentOption)
                                  ? undefined
                                  : translate.t(
                                      currentOption.replace(/text/u, "tooltip")
                                    )
                              }
                              validate={required}
                            >
                              <option value={""} />
                              {_.map(
                                field.options,
                                (text: string, value: string): JSX.Element => (
                                  <option key={text} value={value}>
                                    {translate.t(text)}
                                  </option>
                                )
                              )}
                            </EditableField>
                          </Row>
                        );
                      }
                    )}
                  </React.Fragment>
                )}
              </GenericForm>
            ) : (
              /* eslint-disable-next-line react/jsx-props-no-spreading -- Preferred for readability */
              <SeverityContent {...data.finding.severity} />
            )}
          </React.Fragment>
        </Col100>
      </Row>
    </React.StrictMode>
  );
};

export { SeverityView };
