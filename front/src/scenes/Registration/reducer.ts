import * as actions from "./actions";
import * as actionType from "./actionTypes";

interface IRegistrationState {
  legalNotice: {
    open: boolean;
    rememberDecision: boolean;
  };
}

const initialState: IRegistrationState = {
  legalNotice: {
    open: true,
    rememberDecision: false,
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
    default:
      return state;
  }
};

export = registration;
