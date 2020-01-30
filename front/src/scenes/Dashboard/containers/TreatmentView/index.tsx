/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { Mutation, MutationFn, MutationResult, Query, QueryResult } from "react-apollo";
import { GenericForm } from "redux-form";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { GET_FINDING_TREATMENT, UPDATE_TREATMENT_MUTATION } from "./queries";

interface ITreatmentViewProps {
  findingId: string;
  isEditing: boolean;
}

const treatmentView: React.FC<ITreatmentViewProps> = (props: ITreatmentViewProps): JSX.Element => (
  <React.StrictMode>
    <Query query={GET_FINDING_TREATMENT} variables={{ findingId: props.findingId }}>
      {({ data, loading }: QueryResult): JSX.Element => {
        if (_.isUndefined(data) || loading) { return <React.Fragment />; }

        const handleUpdateError: ((updateError: ApolloError) => void) = (updateError: ApolloError): void => {
          updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
            switch (message) {
              case "Invalid treatment manager":
                msgError(translate.t("proj_alerts.invalid_treatment_mgr"));
                break;
              case "Exception - The inserted date is invalid":
                msgError(translate.t("proj_alerts.invalid_date"));
                break;
              default:
                msgError(translate.t("proj_alerts.error_textsad"));
                rollbar.error("An error occurred updating treatment", updateError);
            }
          });
        };

        return (
          <React.Fragment>
            <Mutation mutation={UPDATE_TREATMENT_MUTATION} onError={handleUpdateError}>
              {(updateTreatment: MutationFn, updateRes: MutationResult): React.ReactNode => {
                const handleSubmit: ((values: Dictionary<string>) => void) = (values: Dictionary<string>): void => {
                  updateTreatment({ variables: {} })
                    .catch();
                };

                return (
                  <GenericForm name="editTreatment" onSubmit={handleSubmit} />
                );
              }}
            </Mutation>
          </React.Fragment>
        );
      }}
    </Query>
  </React.StrictMode>
);

export { treatmentView as TreatmentView };
