import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React, { useCallback, useState } from "react";

import { ServicesForm } from "./form";
import { handleEditGroupDataError } from "./helpers";

import { GET_GROUP_DATA as GET_GROUP_SERVICES } from "scenes/Dashboard/containers/GroupRoute/queries";
import {
  GET_GROUP_DATA,
  UPDATE_GROUP_DATA,
} from "scenes/Dashboard/containers/GroupSettingsView/queries";
import type {
  IFormData,
  IGroupData,
  IServicesProps,
} from "scenes/Dashboard/containers/GroupSettingsView/Services/types";
import { Col80, Row } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const Services: React.FC<IServicesProps> = (
  props: IServicesProps
): JSX.Element => {
  const { groupName } = props;

  // State management
  const [isModalOpen, setIsModalOpen] = useState(false);

  // GraphQL Logic
  const {
    data,
    loading: loadingGroupData,
    refetch: refetchGroupData,
  } = useQuery<IGroupData>(GET_GROUP_DATA, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred getting group data", error);
      });
    },
    variables: { groupName },
  });

  const [editGroupData, { loading: submittingGroupData }] = useMutation(
    UPDATE_GROUP_DATA,
    {
      onCompleted: (): void => {
        track("EditGroupData");
        msgSuccess(
          translate.t("searchFindings.servicesTable.success"),
          translate.t("searchFindings.servicesTable.successTitle")
        );
        void refetchGroupData({ groupName });
      },
      onError: (error: ApolloError): void => {
        handleEditGroupDataError(error);
      },
      refetchQueries: [
        {
          query: GET_GROUP_SERVICES,
          variables: {
            groupName,
          },
        },
      ],
    }
  );

  const handleFormSubmit = useCallback(
    (values: IFormData): void => {
      void editGroupData({
        variables: {
          comments: values.comments,
          description: values.description,
          groupName,
          hasASM: values.asm,
          hasMachine: values.machine,
          hasSquad: values.squad,
          language: values.language,
          reason: values.reason,
          service: values.service,
          subscription: values.type,
        },
      });
      setIsModalOpen(false);
    },
    [editGroupData, groupName]
  );

  // Using form validation instead of field validation to avoid an infinite-loop error
  const formValidations: (values: { confirmation: string }) => {
    confirmation?: string;
  } = useCallback(
    (values: { confirmation: string }): { confirmation?: string } => {
      if (values.confirmation === groupName) {
        return {};
      }

      const errorsFound: { confirmation?: string } = {
        // Exception: FP(Implicit treatment in assignment)
        // eslint-disable-next-line
        confirmation: translate.t( // NOSONAR
          "searchFindings.servicesTable.errors.expectedGroupName",
          { groupName }
        ),
      };

      return errorsFound;
    },
    [groupName]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <React.StrictMode>
      <div>
        <Row>
          {/* eslint-disable-next-line react/forbid-component-props */}
          <Col80 className={"pa0"}>
            <h2>{translate.t("searchFindings.servicesTable.services")}</h2>
          </Col80>
        </Row>
        <Formik
          enableReinitialize={true}
          initialValues={{
            asm: true,
            comments: "",
            confirmation: "",
            description: data.group.description,
            language: data.group.language,
            machine: data.group.hasMachine,
            reason: "NONE",
            service: data.group.service,
            squad: data.group.hasSquad,
            type: data.group.subscription.toUpperCase(),
          }}
          name={"editGroup"}
          onSubmit={handleFormSubmit}
          validate={formValidations}
        >
          <ServicesForm
            data={data}
            groupName={groupName}
            isModalOpen={isModalOpen}
            loadingGroupData={loadingGroupData}
            setIsModalOpen={setIsModalOpen}
            submittingGroupData={submittingGroupData}
          />
        </Formik>
      </div>
    </React.StrictMode>
  );
};

export { Services };
