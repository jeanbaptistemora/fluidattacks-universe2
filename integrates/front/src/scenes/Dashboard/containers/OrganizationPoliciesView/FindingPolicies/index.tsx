import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FormikHelpers } from "formik";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams } from "react-router-dom";

import { Button } from "components/Button";
import { TooltipWrapper } from "components/TooltipWrapper";
import { OrganizationFindingPolicy } from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/content";
import {
  ADD_ORGANIZATION_FINDING_POLICY,
  GET_ORGANIZATION_FINDINGS_TITLES,
} from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/queries";
import type {
  IFindingPolicies,
  IFindingPoliciesData,
  IFindingPoliciesForm,
  IOrganizationFindingTitles,
} from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/types";
import { GET_ORGANIZATION_POLICIES } from "scenes/Dashboard/containers/OrganizationPoliciesView/queries";
import { Row } from "styles/styledComponents";
import { FormikAutocompleteText } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import {
  composeValidators,
  required,
  validDraftTitle,
} from "utils/validations";

const FindingPolicies: React.FC<IFindingPolicies> = ({
  findingPolicies,
  organizationId,
}: IFindingPolicies): JSX.Element => {
  const { organizationName } = useParams<{ organizationName: string }>();
  const { t } = useTranslation();
  const [suggestions, setSuggestions] = useState<string[]>([]);

  const { data } = useQuery<IOrganizationFindingTitles>(
    GET_ORGANIZATION_FINDINGS_TITLES,
    {
      fetchPolicy: "cache-first",
      onError: (error: ApolloError): void => {
        error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          Logger.error("Error loading findings titles", message);
        });
      },
      variables: {
        organizationId,
      },
    }
  );

  const [addOrgFindingPolicy, { loading: submitting }] = useMutation(
    ADD_ORGANIZATION_FINDING_POLICY,
    {
      onCompleted: (result: {
        addOrgFindingPolicy: { success: boolean };
      }): void => {
        if (result.addOrgFindingPolicy.success) {
          msgSuccess(
            t("organization.tabs.policies.findings.addPolicies.success"),
            t("sidebar.newOrganization.modal.successTitle")
          );
        }
      },
      onError: (error: ApolloError): void => {
        error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          switch (message) {
            case "Exception - The finding name is invalid":
              msgError(t("validations.draftTitle"));
              break;
            case "Exception - The finding name policy already exists":
              msgError(
                t("organization.tabs.policies.findings.errors.duplicateFinding")
              );
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.error("Error adding finding policy", message);
          }
        });
      },
      refetchQueries: [
        {
          query: GET_ORGANIZATION_POLICIES,
          variables: {
            organizationId,
          },
        },
      ],
    }
  );

  async function handleSubmit(
    values: IFindingPoliciesForm,
    formikHelpers: FormikHelpers<IFindingPoliciesForm>
  ): Promise<void> {
    track("addNewOrgFindingPolicies");
    await addOrgFindingPolicy({
      variables: { name: values.name, organizationName },
    });
    formikHelpers.resetForm();
  }

  useEffect((): void => {
    const findingNames: string[] = _.flatten(
      data?.organization.projects.map(
        (
          group: IOrganizationFindingTitles["organization"]["projects"][0]
        ): string[] =>
          group.findings.map(
            (
              finding: IOrganizationFindingTitles["organization"]["projects"][0]["findings"][0]
            ): string => _.first(finding.title.split(" -")) as string
          )
      )
    );
    setSuggestions(Array.from(new Set(findingNames)));
  }, [data, organizationId]);

  return (
    <React.StrictMode>
      <Formik
        enableReinitialize={true}
        initialValues={{ name: "" }}
        name={"addNewOrgFindingPolicies"}
        onSubmit={handleSubmit}
      >
        <Form>
          <Row>
            <div className={"w-50-l w-50-m w-100-ns"}>
              {_.isUndefined(data) ? undefined : (
                <div className={"flex items-center"}>
                  <div className={"w-90-ns"}>
                    <TooltipWrapper
                      id={"nameInputToolTip"}
                      message={t(
                        "organization.tabs.policies.findings.tooltip.nameInput"
                      )}
                    >
                      <Field
                        component={FormikAutocompleteText}
                        name={"name"}
                        suggestions={suggestions}
                        validate={composeValidators([
                          required,
                          validDraftTitle,
                        ])}
                      />
                    </TooltipWrapper>
                  </div>
                  <div className={"w-10-ns"}>
                    <TooltipWrapper
                      id={"addButtonToolTip"}
                      message={t(
                        "organization.tabs.policies.findings.tooltip.addButton"
                      )}
                    >
                      <Button
                        // Use className to override default styles
                        // eslint-disable-next-line react/forbid-component-props
                        className={"lh-copy"}
                        disabled={submitting}
                        type={"submit"}
                      >
                        <FontAwesomeIcon icon={faPlus} />
                      </Button>
                    </TooltipWrapper>
                  </div>
                </div>
              )}
            </div>
          </Row>
        </Form>
      </Formik>
      <br />
      <div className={"w-100 mb3"}>
        {findingPolicies.map(
          (policy: IFindingPoliciesData): JSX.Element => (
            <OrganizationFindingPolicy
              id={policy.id}
              key={policy.id}
              lastStatusUpdate={policy.lastStatusUpdate}
              name={policy.name}
              organizationId={organizationId}
              status={policy.status}
            />
          )
        )}
      </div>
    </React.StrictMode>
  );
};

export { FindingPolicies };
