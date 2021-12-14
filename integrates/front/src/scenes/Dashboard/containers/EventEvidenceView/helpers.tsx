import type { ApolloError, FetchResult } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";

import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleUpdateEvidenceError = (updateError: ApolloError): void => {
  updateError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    switch (message) {
      case "Exception - The event has already been closed":
        msgError(translate.t("group.events.alreadyClosed"));
        break;
      case "Exception - Invalid File Size":
        msgError(translate.t("validations.fileSize", { count: 10 }));
        break;
      case "Exception - Invalid File Type: EVENT_IMAGE":
        msgError(translate.t("group.events.form.wrongImageType"));
        break;
      case "Exception - Invalid File Type: EVENT_FILE":
        msgError(translate.t("group.events.form.wrongFileType"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred updating event evidence",
          updateError
        );
    }
  });
};

const getUpdateChanges = (
  eventId: string,
  updateEvidence: (
    variables: Record<string, unknown>
  ) => Promise<FetchResult<unknown>>
): ((evidence: { file?: FileList }, key: string) => Promise<void>) => {
  return async (evidence: { file?: FileList }, key: string): Promise<void> => {
    const { file } = evidence;

    if (!_.isUndefined(file)) {
      await updateEvidence({
        variables: {
          eventId,
          evidenceType: key.toUpperCase(),
          file: file[0],
        },
      });
    }
  };
};

const getDownloadHandler = (
  isEditing: boolean,
  downloadEvidence: (
    variables: Record<string, unknown>
  ) => Promise<FetchResult<unknown>>,
  eventId: string,
  data: { event: { evidenceFile: File } }
): (() => void) => {
  return (): void => {
    if (!isEditing) {
      void downloadEvidence({
        variables: { eventId, fileName: data.event.evidenceFile },
      });
    }
  };
};

const showContent = (
  showEmpty: boolean,
  data: { event: { evidence: string } }
): JSX.Element | string => {
  return showEmpty ? <div /> : `${location.href}/${data.event.evidence}`;
};

const checkNotEmptyOrEditing = (
  value: unknown,
  isEditing: boolean
): boolean => {
  return !_.isEmpty(value) || isEditing;
};

export {
  handleUpdateEvidenceError,
  getUpdateChanges,
  showContent,
  getDownloadHandler,
  checkNotEmptyOrEditing,
};
