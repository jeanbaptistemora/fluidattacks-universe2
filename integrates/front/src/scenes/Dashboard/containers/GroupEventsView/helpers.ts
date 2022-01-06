import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";

import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleFileListUpload = (file: FileList | undefined): File | undefined => {
  return _.isEmpty(file) ? undefined : (file as FileList)[0];
};

const handleCreationError: (creationError: ApolloError) => void = (
  creationError: ApolloError
): void => {
  creationError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    switch (message) {
      case "Exception - Invalid File Size":
        msgError(translate.t("validations.fileSize", { count: 10 }));
        break;
      case "Exception - Invalid characters in filename":
        msgError(translate.t("validations.invalidFileName"));
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
          creationError
        );
    }
  });
};

export { handleCreationError, handleFileListUpload };
