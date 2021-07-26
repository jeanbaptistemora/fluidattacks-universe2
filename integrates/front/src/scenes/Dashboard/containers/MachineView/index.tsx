import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useParams } from "react-router-dom";

import { GET_FINDING_MACHINE_JOBS } from "./queries";

import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const MachineView: React.FC = (): JSX.Element => {
  const { findingId } = useParams<{ findingId: string }>();

  // GraphQL operations
  const { data } = useQuery(GET_FINDING_MACHINE_JOBS, {
    notifyOnNetworkStatusChange: true,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading machine jobs", error);
      });
    },
    variables: { findingId },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return <React.StrictMode>{JSON.stringify(data)}</React.StrictMode>;
};

export { MachineView };
