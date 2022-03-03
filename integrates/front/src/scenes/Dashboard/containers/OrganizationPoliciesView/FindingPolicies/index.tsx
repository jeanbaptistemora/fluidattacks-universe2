import { useMutation } from "@apollo/client";
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
import type { ConfigurableValidator } from "revalidate";

import { getFindingNames } from "../../GroupDraftsView/findingNames";
import type { ISuggestion } from "../../GroupDraftsView/types";
import { Button } from "components/Button";
import { TooltipWrapper } from "components/TooltipWrapper";
import { OrganizationFindingPolicy } from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/content";
import { ADD_ORGANIZATION_FINDING_POLICY } from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/queries";
import type {
  IFindingPolicies,
  IFindingPoliciesData,
  IFindingPoliciesForm,
} from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/types";
import { GET_ORGANIZATION_POLICIES } from "scenes/Dashboard/containers/OrganizationPoliciesView/queries";
import { FormikAutocompleteText, FormikTagInput } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import {
  composeValidators,
  required,
  validDraftTitle,
  validFindingTypology,
} from "utils/validations";

const FindingPolicies: React.FC<IFindingPolicies> = ({
  findingPolicies,
  organizationId,
}: IFindingPolicies): JSX.Element => {
  const { organizationName } = useParams<{ organizationName: string }>();
  const { t } = useTranslation();
  const [suggestions, setSuggestions] = useState<string[]>([]);

  const [addOrganizationFindingPolicy, { loading: submitting }] = useMutation(
    ADD_ORGANIZATION_FINDING_POLICY,
    {
      onCompleted: (result: {
        addOrganizationFindingPolicy: { success: boolean };
      }): void => {
        if (result.addOrganizationFindingPolicy.success) {
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
    track("addNewOrgFindingPolicies", {
      Organization: organizationName,
    });
    await addOrganizationFindingPolicy({
      variables: {
        name: values.name,
        organizationName,
        tags: _.isEmpty(values.tags) ? undefined : values.tags.split(","),
      },
    });
    formikHelpers.resetForm();
  }

  useEffect((): void => {
    async function fetchData(): Promise<void> {
      const findingNames: ISuggestion[] = await getFindingNames("EN").catch(
        (error: Error): ISuggestion[] => {
          Logger.error("An error occurred getting title suggestions", error);

          return [];
        }
      );

      setSuggestions(
        _.sortBy(
          findingNames.map(
            (findingName: ISuggestion): string =>
              `${findingName.key}. ${findingName.title}`
          )
        )
      );
    }
    void fetchData();
  }, []);

  const validateFindingTypology: ConfigurableValidator =
    validFindingTypology(suggestions);

  return (
    <React.StrictMode>
      <Formik
        enableReinitialize={true}
        initialValues={{ name: "", tags: "" }}
        name={"addNewOrgFindingPolicies"}
        onSubmit={handleSubmit}
      >
        <Form>
          <div className={"flex flex-wrap justify-between"}>
            <div className={"w-50-l w-50-m w-100-ns"}>
              <TooltipWrapper
                id={"nameInputToolTip"}
                message={t(
                  "organization.tabs.policies.findings.tooltip.nameInput"
                )}
                placement={"top"}
              >
                <label className={"mb1"}>
                  <b>{t("organization.tabs.policies.findings.form.finding")}</b>
                </label>
                <Field
                  component={FormikAutocompleteText}
                  name={"name"}
                  suggestions={suggestions}
                  validate={composeValidators([
                    required,
                    validDraftTitle,
                    validateFindingTypology,
                  ])}
                />
              </TooltipWrapper>
            </div>
            <div className={"pl2-l pl2-m pl0-ns w-50-l w-50-m w-100-ns"}>
              <div className={"flex items-start"}>
                <div className={"w-90-ns"}>
                  <TooltipWrapper
                    id={"tagsInputToolTip"}
                    message={t(
                      "organization.tabs.policies.findings.tooltip.tagsInput"
                    )}
                    placement={"top"}
                  >
                    <label className={"mb1"}>
                      <b>
                        {t("organization.tabs.policies.findings.form.tags")}
                      </b>
                    </label>
                    <Field
                      component={FormikTagInput}
                      name={"tags"}
                      placeholder={""}
                      type={"text"}
                    />
                  </TooltipWrapper>
                </div>
                <div className={"w-10-ns"}>
                  <TooltipWrapper
                    displayClass={"flex justify-end"}
                    id={"addButtonToolTip"}
                    message={t(
                      "organization.tabs.policies.findings.tooltip.addButton"
                    )}
                  >
                    <Button
                      disabled={submitting}
                      type={"submit"}
                      variant={"secondary"}
                    >
                      <FontAwesomeIcon icon={faPlus} />
                    </Button>
                  </TooltipWrapper>
                </div>
              </div>
            </div>
          </div>
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
              tags={policy.tags}
            />
          )
        )}
      </div>
    </React.StrictMode>
  );
};

export { FindingPolicies };
