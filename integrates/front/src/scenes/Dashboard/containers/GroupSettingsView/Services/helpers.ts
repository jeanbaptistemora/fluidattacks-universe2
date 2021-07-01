import type {
  ApolloError,
  ApolloQueryResult,
  OperationVariables,
} from "@apollo/client";
import type { Dispatch } from "redux";
import { change } from "redux-form";

import type { IGroupData } from "./types";

import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const getHandleMachineBtnChange = (
  dispatch: Dispatch
): ((withMachine: boolean) => void) => {
  return (withMachine: boolean): void => {
    dispatch(change("editGroup", "machine", withMachine));

    if (withMachine) {
      dispatch(change("editGroup", "asm", true));
    } else {
      dispatch(change("editGroup", "squad", false));
    }
  };
};

const handleSquadBtnChangeHelper = (
  dispatch: Dispatch,
  withSquad: boolean,
  type: string,
  isContinuousType: (type: string) => boolean
): void => {
  if (withSquad) {
    dispatch(change("editGroup", "asm", true));
    dispatch(change("editGroup", "machine", isContinuousType(type)));
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
  getHandleMachineBtnChange,
  handleSquadBtnChangeHelper,
  editGroupDataHelper,
  handleEditGroupDataError,
};
