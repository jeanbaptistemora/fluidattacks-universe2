import * as actions from "./actions";
import * as actionType from "./actionTypes";
import { IWelcomeViewProps } from "./containers/WelcomeView";

interface IRegistrationState {
  legalNotice: {
    open: boolean;
    rememberDecision: boolean;
  };
  welcomeView: Pick<IWelcomeViewProps, "isAuthorized" | "isRememberEnabled">;
}

const initialState: IRegistrationState = {
  legalNotice: {
    open: true,
    rememberDecision: false,
  },
  welcomeView: {
    isAuthorized: undefined,
    isRememberEnabled: false,
  },
};

type RegistrationReducer = ((
  arg1: IRegistrationState | undefined,
  arg2: actions.IActionStructure,
) => IRegistrationState);

const registration: RegistrationReducer =
  (state: IRegistrationState = initialState,
   action: actions.IActionStructure): IRegistrationState => {
  switch (action.type) {
    case actionType.CHECK_REMEMBER:
      return {
        ...state,
        legalNotice: {
          ...state.legalNotice,
          rememberDecision: !state.legalNotice.rememberDecision,
        },
      };
    case actionType.LOAD_AUTHORIZATION:
      return {
        ...state,
        welcomeView: {
          ...state.welcomeView,
          isAuthorized: action.payload.isAuthorized,
          isRememberEnabled: action.payload.isRememberEnabled,
        },
      };
    default:
      return state;
  }
};

export = registration;
