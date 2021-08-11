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

const handleMachineBtnChangeHelper = (
  setFieldValue: (
    field: string,
    value: any,
    shouldValidate?: boolean | undefined
  ) => void,
  withMachine: boolean
): void => {
  if (withMachine) {
    setFieldValue("asm", true);
  } else {
    setFieldValue("squad", false);
  }
};

const handleSquadBtnChangeHelper = (
  setFieldValue: (
    field: string,
    value: any,
    shouldValidate?: boolean | undefined
  ) => void,
  withSquad: boolean,
  type: string,
  isContinuousType: (type: string) => boolean
): void => {
  if (withSquad) {
    setFieldValue("asm", true);
    setFieldValue("machine", isContinuousType(type));
  }
};

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

export {
  handleMachineBtnChangeHelper,
  handleSquadBtnChangeHelper,
  editGroupDataHelper,
  handleEditGroupDataError,
};
