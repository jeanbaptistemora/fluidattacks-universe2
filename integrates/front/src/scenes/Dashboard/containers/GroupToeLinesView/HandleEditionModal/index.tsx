import type { ApolloError } from "@apollo/client";
import { useMutation } from "@apollo/client";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import moment from "moment";
import React from "react";
import { useTranslation } from "react-i18next";

import { HandleEditionModalForm } from "./form";
import { UPDATE_TOE_LINES_ATTACKED_LINES } from "./queries";
import type {
  IFormValues,
  IHandleEditionModalProps,
  IUpdateToeLinesAttackedLinesResultAttr,
} from "./types";

import type { IToeLinesData } from "../types";
import { Modal } from "components/Modal";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const HandleEditionModal: React.FC<IHandleEditionModalProps> = (
  props: IHandleEditionModalProps
): JSX.Element => {
  const { groupName, selectedToeLinesDatas, handleCloseModal, refetchData } =
    props;

  const { t } = useTranslation();

  const isOneSelected = selectedToeLinesDatas.length === 1;

  // GraphQL operations
  const [handleUpdateToeLinesAttackedLines] =
    useMutation<IUpdateToeLinesAttackedLinesResultAttr>(
      UPDATE_TOE_LINES_ATTACKED_LINES,
      {
        onCompleted: (data: IUpdateToeLinesAttackedLinesResultAttr): void => {
          if (data.updateToeLinesAttackedLines.success) {
            msgSuccess(
              t("group.toe.lines.editModal.alerts.success"),
              t("groupAlerts.updatedTitle")
            );
            refetchData();
            handleCloseModal();
          }
        },
        onError: (errors: ApolloError): void => {
          errors.graphQLErrors.forEach((error: GraphQLError): void => {
            switch (error.message) {
              case "Exception - The toe lines is not present":
                msgError(t("group.toe.lines.editModal.alerts.nonPresent"));
                break;
              case "Exception - The attack time must be between the previous attack and the current time":
                msgError(
                  t("group.toe.lines.editModal.alerts.invalidAttackedAt")
                );
                break;
              case "Exception - The attacked lines must be between 1 and the loc (lines of code)":
                msgError(
                  t("group.toe.lines.editModal.alerts.invalidAttackedLines")
                );
                break;
              case "Exception - The toe lines has been updated by another operation":
                msgError(t("group.toe.lines.editModal.alerts.alreadyUpdate"));
                break;
              default:
                msgError(t("groupAlerts.errorTextsad"));
                Logger.warning(
                  "An error occurred updating the toe lines attacked lines",
                  error
                );
            }
          });
        },
      }
    );

  function handleSubmit(values: IFormValues): void {
    const selectedToeLinesDatasByGroup = _.groupBy(
      selectedToeLinesDatas,
      (selectedToeLinesData: IToeLinesData): string =>
        selectedToeLinesData.rootId
    );
    Object.entries(selectedToeLinesDatasByGroup).map(
      async ([rootId, rootSelectedToeLinesDatas]: [
        string,
        IToeLinesData[]
      ]): Promise<unknown> =>
        handleUpdateToeLinesAttackedLines({
          variables: {
            attackedAt: values.attackedAt.format(),
            attackedLines: _.isNumber(values.attackedLines)
              ? values.attackedLines
              : undefined,
            comments: values.comments,
            filenames: rootSelectedToeLinesDatas.map(
              (selectedToeLinesData: IToeLinesData): string =>
                selectedToeLinesData.filename
            ),
            groupName,
            rootId,
          },
        })
    );
  }

  return (
    <React.StrictMode>
      <Modal
        headerTitle={t("group.toe.lines.editModal.title")}
        open={true}
        size={"largeModal"}
      >
        <Formik
          initialValues={{
            attackedAt: moment(),
            attackedLines: isOneSelected
              ? selectedToeLinesDatas[0].loc
              : undefined,
            comments: "",
          }}
          name={"updateToeLinesAttackedLines"}
          onSubmit={handleSubmit}
        >
          <HandleEditionModalForm
            handleCloseModal={handleCloseModal}
            selectedToeLinesDatas={selectedToeLinesDatas}
          />
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { HandleEditionModal };
