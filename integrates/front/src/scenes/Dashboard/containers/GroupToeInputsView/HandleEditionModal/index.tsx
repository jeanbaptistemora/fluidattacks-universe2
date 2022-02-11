import type { ApolloError, FetchResult } from "@apollo/client";
import { useMutation } from "@apollo/client";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import moment from "moment";
import React from "react";
import { useTranslation } from "react-i18next";

import { HandleEditionModalForm } from "./form";
import { UPDATE_TOE_INPUT } from "./queries";
import type {
  IFormValues,
  IHandleEditionModalProps,
  IUpdateToeInputResultAttr,
} from "./types";

import type { IToeInputData } from "../types";
import { Modal } from "components/Modal";
import { getErrors } from "utils/helpers";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const HandleEditionModal: React.FC<IHandleEditionModalProps> = (
  props: IHandleEditionModalProps
): JSX.Element => {
  const {
    groupName,
    selectedToeInputDatas,
    handleCloseModal,
    refetchData,
    setSelectedToeInputDatas,
  } = props;

  const { t } = useTranslation();

  // GraphQL operations
  const [handleUpdateToeInput] = useMutation<IUpdateToeInputResultAttr>(
    UPDATE_TOE_INPUT,
    {
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - The toe input is not present":
              msgError(t("group.toe.inputs.editModal.alerts.nonPresent"));
              break;
            case "Exception - The attack time must be between the previous attack and the current time":
              msgError(
                t("group.toe.inputs.editModal.alerts.invalidAttackedAt")
              );
              break;
            case "Exception - The toe input has been updated by another operation":
              msgError(t("group.toe.inputs.editModal.alerts.alreadyUpdate"));
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred updating the toe input", error);
          }
        });
      },
    }
  );

  const handleOnCompleted = (
    result: FetchResult<IUpdateToeInputResultAttr>
  ): void => {
    if (!_.isNil(result.data) && result.data.updateToeInput.success) {
      msgSuccess(
        t("group.toe.inputs.editModal.alerts.success"),
        t("groupAlerts.updatedTitle")
      );
      setSelectedToeInputDatas([]);
      refetchData();
      handleCloseModal();
    }
  };

  async function handleSubmit(values: IFormValues): Promise<void> {
    const results = await Promise.all(
      selectedToeInputDatas.map(
        async (
          toeInputData: IToeInputData
        ): Promise<FetchResult<IUpdateToeInputResultAttr>> =>
          handleUpdateToeInput({
            variables: {
              attackedAt: _.isEmpty(values.attackedAt)
                ? undefined
                : values.attackedAt.format(),
              bePresent: values.bePresent,
              component: toeInputData.component,
              entryPoint: toeInputData.entryPoint,
              groupName,
            },
          })
      )
    );
    const errors = getErrors<IUpdateToeInputResultAttr>(results);

    if (!_.isEmpty(results) && _.isEmpty(errors)) {
      handleOnCompleted(results[0]);
    } else {
      refetchData();
    }
  }

  return (
    <React.StrictMode>
      <Modal
        headerTitle={t("group.toe.inputs.editModal.title")}
        open={true}
        size={"largeModal"}
      >
        <Formik
          initialValues={{
            attackedAt: moment(),
            bePresent: true,
          }}
          name={"updateToeInput"}
          onSubmit={handleSubmit}
        >
          <HandleEditionModalForm
            handleCloseModal={handleCloseModal}
            selectedToeInputDatas={selectedToeInputDatas}
          />
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { HandleEditionModal };
