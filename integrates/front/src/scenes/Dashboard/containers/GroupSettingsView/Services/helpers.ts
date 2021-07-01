import type {
  ApolloError,
  ApolloQueryResult,
  OperationVariables,
} from "@apollo/client";
import type { GraphQLError } from "graphql";
import type { Dispatch } from "redux";
import { change } from "redux-form";

import type { IGroupData } from "./types";

import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const getHandleASMBtnChange = (
  dispatch: Dispatch
): ((withASM: boolean) => void) => {
  return (withASM: boolean): void => {
    dispatch(change("editGroup", "asm", withASM));

    if (!withASM) {
      dispatch(change("editGroup", "machine", false));
      dispatch(change("editGroup", "squad", false));
      dispatch(change("editGroup", "forces", false));
    }
  };
};

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

const handleForcesBtnChangeHelper = (
  dispatch: Dispatch,
  withForces: boolean
): void => {
  if (withForces) {
    dispatch(change("editGroup", "asm", true));
    dispatch(change("editGroup", "machine", true));
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
  error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    switch (message) {
      case "Exception - Forces is only available when Squad is too":
        msgError(
          translate.t("searchFindings.servicesTable.errors.forcesOnlyIfSquad")
        );
        break;
      case "Exception - Forces is only available in groups of type Continuous":
        msgError(
          translate.t(
            "searchFindings.servicesTable.errors.forcesOnlyIfContinuous"
          )
        );
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred editing group services", error);
    }
  });
};

export {
  getHandleASMBtnChange,
  getHandleMachineBtnChange,
  handleSquadBtnChangeHelper,
  handleForcesBtnChangeHelper,
  editGroupDataHelper,
  handleEditGroupDataError,
};
