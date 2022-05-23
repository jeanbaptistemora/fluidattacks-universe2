import type { FetchResult } from "@apollo/client";
import type { GraphQLError } from "graphql";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import { useCallback } from "react";
import { array, object, string } from "yup";

import { Logger } from "utils/logger";
import { translate } from "utils/translations/translate";

type modalMessages = React.Dispatch<
  React.SetStateAction<{
    message: string;
    type: string;
  }>
>;

interface IRootAttr {
  branch: string;
  credentialName: string;
  credentialType: string;
  env: string;
  exclusions: string[];
  url: string;
}

const handleCreationError = (
  graphQLErrors: readonly GraphQLError[],
  setMessages: modalMessages
): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - Error empty value is not valid":
        setMessages({
          message: translate.t("group.scope.git.errors.invalid"),
          type: "error",
        });
        break;
      case "Exception - Active root with the same Nickname already exists":
        setMessages({
          message: translate.t("group.scope.common.errors.duplicateNickname"),
          type: "error",
        });
        break;
      case "Exception - Active root with the same URL/branch already exists":
        setMessages({
          message: translate.t("group.scope.common.errors.duplicateUrl"),
          type: "error",
        });
        break;
      case "Exception - Root name should not be included in the exception pattern":
        setMessages({
          message: translate.t("group.scope.git.errors.rootInGitignore"),
          type: "error",
        });
        break;
      case "Exception - Invalid characters":
        setMessages({
          message: translate.t("validations.invalidChar"),
          type: "error",
        });
        break;
      default:
        setMessages({
          message: translate.t("groupAlerts.errorTextsad"),
          type: "error",
        });
        Logger.error("Couldn't add git roots", error);
    }
  });
};

function useRootSubmit(
  addGitRoot: (
    variables: Record<string, unknown>
  ) => Promise<FetchResult<unknown>>,
  group: string
): ({
  branch,
  credentialName,
  credentialType,
  env,
  exclusions,
  url,
}: IRootAttr) => Promise<void> {
  return useCallback(
    async ({
      branch,
      credentialName,
      credentialType,
      env,
      exclusions,
      url,
    }: IRootAttr): Promise<void> => {
      mixpanel.track("AddGitRoot");
      await addGitRoot({
        variables: {
          branch: branch.trim(),
          credentials: {
            id: "",
            key: "",
            name: credentialName,
            password: "asdfasdf",
            token: "",
            type: credentialType,
            user: "asdssad",
          },
          environment: env,
          gitignore: exclusions,
          groupName: group,
          includesHealthCheck: false,
          nickname: "",
          url: url.trim(),
          useVpn: false,
        },
      });
    },
    [addGitRoot, group]
  );
}

const rootSchema = object().shape({
  branch: string().required(),
  credentialName: string().required(),
  credentialType: string().required(),
  environment: string().required(),
  exclusions: array().of(string()),
  url: string().required(),
});

export { handleCreationError, rootSchema, useRootSubmit };
