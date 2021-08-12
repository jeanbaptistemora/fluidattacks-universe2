/* eslint-disable  @typescript-eslint/no-explicit-any */
import type {
  ApolloError,
  ApolloQueryResult,
  OperationVariables,
} from "@apollo/client";

import type { IGroupData } from "./types";

import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const editGroupDataHelper = (
  asm: boolean,
  groupName: string,
  push: (path: string, state?: unknown) => void,
  refetchGroupData: (
    variables?: Partial<OperationVariables> | undefined
  ) => Promise<ApolloQueryResult<IGroupData>>
): void => {
  if (asm) {
    void refetchGroupData({ groupName });
  } else {
    push("/home");
  }
};

const handleEditGroupDataError = (error: ApolloError): void => {
  msgError(translate.t("groupAlerts.errorTextsad"));
  Logger.warning("An error occurred editing group services", error);
};

export { editGroupDataHelper, handleEditGroupDataError };
