interface IAction {
  payload: boolean;
  type: string;
}
export type RegistrationAction = IAction;

export const acceptLegal: ((arg1: boolean) => RegistrationAction) =
  (remember: boolean): RegistrationAction => ({
    payload: remember,
    type: "ACCEPT_LEGAL",
  });

export const setRemember: ((arg1: boolean) => RegistrationAction) =
  (value: boolean): RegistrationAction => ({
    payload: value,
    type: "SET_REMEMBER",
  });
