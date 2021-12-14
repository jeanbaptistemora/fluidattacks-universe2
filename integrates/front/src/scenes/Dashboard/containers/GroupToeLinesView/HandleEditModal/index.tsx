import { useMutation } from "@apollo/client";
import { Formik } from "formik";
import _ from "lodash";
import moment from "moment";
import React from "react";
import { useTranslation } from "react-i18next";

import { HandleEditModalForm } from "./form";
import { UPDATE_TOE_LINES_ATTACKED_LINES } from "./queries";
import type {
  IFormValues,
  IHandleEditModalProps,
  IUpdateToeLinesAttackedLinesResultAttr,
} from "./types";

import type { IToeLinesData } from "../types";
import { Modal } from "components/Modal";

const HandleEditModal: React.FC<IHandleEditModalProps> = (
  props: IHandleEditModalProps
): JSX.Element => {
  const { groupName, selectedToeLinesDatas, handleCloseModal } = props;

  const { t } = useTranslation();

  const isOneSelected = selectedToeLinesDatas.length === 1;

  // GraphQL operations
  const [handleUpdateToeLinesAttackedLines] =
    useMutation<IUpdateToeLinesAttackedLinesResultAttr>(
      UPDATE_TOE_LINES_ATTACKED_LINES
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
            attackedAt: values.attackedAt,
            attackedLines: values.attackedLines,
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
          <HandleEditModalForm
            handleCloseModal={handleCloseModal}
            selectedToeLinesDatas={selectedToeLinesDatas}
          />
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { HandleEditModal };
