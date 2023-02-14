import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { HandleAdditionModalForm } from "./form";
import { ADD_TOE_INPUT, GET_ROOTS } from "./queries";
import type {
  IAddToeInputResultAttr,
  IFormValues,
  IGitRootAttr,
  IHandleAdditionModalProps,
  IURLRootAttr,
  Root,
} from "./types";
import {
  isActiveGitRoot,
  isActiveURLRoot,
  isGitRoot,
  isURLRoot,
} from "./utils";

import { Modal } from "components/Modal";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const HandleAdditionModal: React.FC<IHandleAdditionModalProps> = ({
  groupName,
  handleCloseModal,
  refetchData,
}: IHandleAdditionModalProps): JSX.Element => {
  const [host, setHost] = useState<string | undefined>();

  const { t } = useTranslation();

  const { data: rootsData } = useQuery<{ group: { roots: Root[] } }>(
    GET_ROOTS,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          Logger.error("Couldn't load roots", error);
        });
      },
      variables: { groupName },
    }
  );
  const roots: (IGitRootAttr | IURLRootAttr)[] =
    rootsData === undefined
      ? []
      : [
          ...rootsData.group.roots.filter(isGitRoot).filter(isActiveGitRoot),
          ...rootsData.group.roots.filter(isURLRoot).filter(isActiveURLRoot),
        ];

  // GraphQL operations
  const [handleAddToeInput] = useMutation<IAddToeInputResultAttr>(
    ADD_TOE_INPUT,
    {
      onCompleted: (data: IAddToeInputResultAttr): void => {
        if (data.addToeInput.success) {
          msgSuccess(
            t("group.toe.inputs.addModal.alerts.success"),
            t("groupAlerts.titleSuccess")
          );
          refetchData();
          handleCloseModal();
        }
      },
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - Toe input already exists":
              msgError(t("group.toe.inputs.addModal.alerts.alreadyExists"));
              break;
            case "Exception - The root does not have the component":
              msgError(t("group.toe.inputs.addModal.alerts.invalidComponent"));
              break;
            case "Exception - The URL is not valid":
              msgError(t("group.toe.inputs.addModal.alerts.invalidUrl"));
              break;
            case "Exception - Invalid characters":
              msgError(t("group.toe.inputs.addModal.alerts.invalidCharacter"));
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred adding toe input", error);
          }
        });
      },
    }
  );

  const handleSubmit = useCallback(
    (values: IFormValues): void => {
      if (!_.isUndefined(host)) {
        void handleAddToeInput({
          variables: {
            component: `${host}${values.path}`,
            entryPoint: values.entryPoint,
            groupName,
            rootId: values.rootId,
          },
        });
      }
    },
    [groupName, handleAddToeInput, host]
  );

  return (
    <React.StrictMode>
      {rootsData === undefined ? undefined : (
        <Modal open={true} title={t("group.toe.inputs.addModal.title")}>
          <Formik
            initialValues={{
              entryPoint: "",
              environmentUrl:
                !_.isEmpty(roots) &&
                isGitRoot(roots[0]) &&
                !_.isEmpty(roots[0].gitEnvironmentUrls)
                  ? roots[0].gitEnvironmentUrls[0].url
                  : "",
              path: "",
              rootId: _.isEmpty(roots) ? undefined : roots[0].id,
            }}
            name={"addToeInput"}
            onSubmit={handleSubmit}
          >
            <HandleAdditionModalForm
              handleCloseModal={handleCloseModal}
              host={host}
              roots={roots}
              setHost={setHost}
            />
          </Formik>
        </Modal>
      )}
    </React.StrictMode>
  );
};

export { HandleAdditionModal };
