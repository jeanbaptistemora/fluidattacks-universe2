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

const getHandleIntegratesBtnChange = (
  dispatch: Dispatch
): ((withIntegrates: boolean) => void) => {
  return (withIntegrates: boolean): void => {
    dispatch(change("editGroup", "integrates", withIntegrates));

    if (!withIntegrates) {
      dispatch(change("editGroup", "skims", false));
      dispatch(change("editGroup", "drills", false));
      dispatch(change("editGroup", "forces", false));
    }
  };
};

const getHandleSkimsBtnChange = (
  dispatch: Dispatch
): ((withSkims: boolean) => void) => {
  return (withSkims: boolean): void => {
    dispatch(change("editGroup", "skims", withSkims));

    if (withSkims) {
      dispatch(change("editGroup", "integrates", true));
    } else {
      dispatch(change("editGroup", "drills", false));
      dispatch(change("editGroup", "forces", false));
    }
  };
};

const handleDrillsBtnChangeHelper = (
  dispatch: Dispatch,
  withDrills: boolean,
  type: string,
  isContinuousType: (type: string) => boolean
): void => {
  if (withDrills) {
    dispatch(change("editGroup", "integrates", true));
    dispatch(change("editGroup", "skims", isContinuousType(type)));
  } else {
    dispatch(change("editGroup", "forces", false));
  }
};

const handleForcesBtnChangeHelper = (
  dispatch: Dispatch,
  withForces: boolean
): void => {
  if (withForces) {
    dispatch(change("editGroup", "integrates", true));
    dispatch(change("editGroup", "skims", true));
    dispatch(change("editGroup", "drills", true));
  }
};

const editGroupDataHelper = (
  integrates: boolean,
  groupName: string,
  push: (path: string, state?: unknown) => void,
  refetchGroupData: (
    variables?: Partial<OperationVariables> | undefined
  ) => Promise<ApolloQueryResult<IGroupData>>
): void => {
  if (integrates) {
    void refetchGroupData({ groupName });
  } else {
    push("/home");
  }
};

const handleEditGroupDataError = (error: ApolloError): void => {
  error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    switch (message) {
      case "Exception - Forces is only available when Drills is too":
        msgError(
          translate.t("searchFindings.servicesTable.errors.forcesOnlyIfDrills")
        );
        break;
      case "Exception - Forces is only available in projects of type Continuous":
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
  getHandleIntegratesBtnChange,
  getHandleSkimsBtnChange,
  handleDrillsBtnChangeHelper,
  handleForcesBtnChangeHelper,
  editGroupDataHelper,
  handleEditGroupDataError,
};
