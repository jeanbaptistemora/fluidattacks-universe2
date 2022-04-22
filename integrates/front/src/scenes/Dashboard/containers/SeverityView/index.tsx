import { gql, useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { mapSeveritytoStringValues, tooltipPropHelper } from "./helpers";
import { validateValues } from "./SeverityContent/utils";

import { Button } from "components/Button/index";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/FindingContent/queries";
import {
  GET_SEVERITY,
  UPDATE_SEVERITY_MUTATION,
} from "scenes/Dashboard/containers/SeverityView/queries";
import { SeverityContent } from "scenes/Dashboard/containers/SeverityView/SeverityContent/index";
import type {
  ISeverityAttr,
  ISeverityField,
  IUpdateSeverityAttr,
} from "scenes/Dashboard/containers/SeverityView/types";
import { castFieldsCVSS3 } from "scenes/Dashboard/containers/SeverityView/utils";
import { ButtonToolbarRow, Col100, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { calcCVSSv3 } from "utils/cvss";
import { EditableField, FormikDropdown } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { required } from "utils/validations";

const SeverityView: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { findingId } = useParams<{ findingId: string }>();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  const [isEditing, setIsEditing] = useState(false);

  const formValues = (values: Dictionary<string>): Dictionary<string> => {
    return (({
      cvssVersion,
      modifiedSeverityScope,
      severityScope,
    }): Dictionary<string> => ({
      cvssVersion,
      modifiedSeverityScope,
      severityScope,
    }))(values);
  };

  const handleErrors: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred loading finding severity", error);
    });
  };

  const { client, data, refetch } = useQuery<ISeverityAttr>(GET_SEVERITY, {
    onError: handleErrors,
    variables: { identifier: findingId },
  });

  const handleEditClick: () => void = useCallback((): void => {
    setIsEditing(!isEditing);
    if (!_.isUndefined(data)) {
      const severityScore: string = Number(
        calcCVSSv3(data.finding.severity)
      ).toFixed(2);
      client.writeFragment({
        data: { severityScore },
        fragment: gql`
          fragment score on Finding {
            severityScore
          }
        `,
        id: `Finding:${findingId}`,
      });
    }
  }, [client, data, findingId, isEditing]);

  const handleMtUpdateSeverityRes: (mtResult: IUpdateSeverityAttr) => void = (
    mtResult: IUpdateSeverityAttr
  ): void => {
    if (!_.isUndefined(mtResult)) {
      if (mtResult.updateSeverity.success) {
        void refetch();
        msgSuccess(t("groupAlerts.updated"), t("groupAlerts.updatedTitle"));
        mixpanel.track("UpdateSeverity");
      }
    }
  };

  const handleMtError: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(t("groupAlerts.errorTextsad"));
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
          canGetHistoricState: permissions.can(
            "api_resolvers_finding_historic_state_resolve"
          ),
          findingId,
        },
      },
    ],
  });

  const handleUpdateSeverity: (values: Record<string, unknown>) => void =
    useCallback(
      (values: Record<string, unknown>): void => {
        const stringValues = mapSeveritytoStringValues(values);
        setIsEditing(false);
        void updateSeverity({
          variables: { findingId, ...stringValues },
        });
      },
      [findingId, updateSeverity]
    );

  const handleFormChange: (
    values: ISeverityAttr["finding"]["severity"]
  ) => void = useCallback(
    (values: ISeverityAttr["finding"]["severity"]): void => {
      const severityScore: string = Number(calcCVSSv3(values)).toFixed(2);
      client.writeFragment({
        data: { severityScore },
        fragment: gql`
          fragment score on Finding {
            severityScore
          }
        `,
        id: `Finding:${findingId}`,
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
            <Can do={"api_mutations_update_severity_mutate"}>
              <ButtonToolbarRow>
                <TooltipWrapper
                  id={"severityEditTooltip"}
                  message={t("searchFindings.tabSeverity.editable.tooltip")}
                >
                  <Button onClick={handleEditClick} variant={"secondary"}>
                    <FluidIcon icon={"edit"} />
                    &nbsp;
                    {t("searchFindings.tabSeverity.editable.label")}
                  </Button>
                </TooltipWrapper>
              </ButtonToolbarRow>
            </Can>
            <br />
            {isEditing ||
            !validateValues(data.finding.severity) ||
            data.finding.severityScore <= 0 ||
            data.finding.cvssVersion !== "3.1" ? (
              <Formik
                enableReinitialize={true}
                initialValues={{
                  ...data.finding.severity,
                  cvssVersion: data.finding.cvssVersion,
                }}
                name={"editSeverity"}
                onChange={handleFormChange}
                onSubmit={handleUpdateSeverity}
              >
                {({ dirty, values }): React.ReactNode => (
                  <Form id={"editSeverity"}>
                    {isEditing ? (
                      <React.Fragment>
                        <ButtonToolbarRow>
                          <Button
                            disabled={!dirty || mutationRes.loading}
                            type={"submit"}
                            variant={"primary"}
                          >
                            <FluidIcon icon={"loading"} />
                            {t("searchFindings.tabSeverity.update")}
                          </Button>
                        </ButtonToolbarRow>
                        <Row>
                          <EditableField
                            alignField={"horizontal"}
                            component={FormikDropdown}
                            currentValue={"3.1"}
                            label={t("searchFindings.tabSeverity.cvssVersion")}
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
                      formValues(values)
                    ).map(
                      (field: ISeverityField, index: number): JSX.Element => {
                        const currentOption: string =
                          field.options[field.currentValue];

                        return (
                          <Row key={field.name}>
                            <EditableField
                              alignField={"horizontal"}
                              component={FormikDropdown}
                              currentValue={`${Number(
                                field.currentValue
                              ).toFixed(2)} | ${t(currentOption)}`}
                              id={`Row${index}`}
                              label={field.title}
                              name={field.name}
                              renderAsEditable={isEditing}
                              tooltip={tooltipPropHelper(currentOption)}
                              validate={required}
                            >
                              <option value={""} />
                              {_.map(
                                field.options,
                                (text: string, value: string): JSX.Element => (
                                  <option key={text} value={value}>
                                    {t(text)}
                                  </option>
                                )
                              )}
                            </EditableField>
                          </Row>
                        );
                      }
                    )}
                  </Form>
                )}
              </Formik>
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
