import { AxiosResponse } from "axios";
import rollbar from "../../utils/rollbar";
import Xhr from "../../utils/xhr";
import { RegistrationAction } from "./actions";

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

const loadDashboard: (() => void) = (): void => {
  let location: string;
  if (localStorage.getItem("url_inicio") === null) {
    location = "dashboard";
  } else {
    location = `dashboard#${localStorage.getItem("url_inicio")}`;
    localStorage.removeItem("url_inicio");
  }
  window.location.href = location;
};

type RegistrationReducer = ((arg1: IRegistrationState | undefined, arg2: RegistrationAction) => IRegistrationState);

const registration: RegistrationReducer =
  (state: IRegistrationState = initialState, action: RegistrationAction): IRegistrationState => {
  switch (action.type) {
    case "ACCEPT_LEGAL":
      let getLoginInfoQry: string;
      getLoginInfoQry = `{
        login{
          authorized
        }
      }`;
      new Xhr().request(getLoginInfoQry, "An error ocurred resolving user authorization")
      .then((authorizationResp: AxiosResponse) => {
        /* tslint:disable-next-line:no-any
         * Disabling here is necessary because TypeScript relies
         * on its JS base for functions like JSON.parse whose type is 'any'
         */
        const authorizedRespData: any = JSON.parse(JSON.stringify(authorizationResp.data)).data;
        if (authorizedRespData.login.authorized) {
          let acceptLegalQry: string;
          acceptLegalQry = `mutation {
            acceptLegal(remember:$rem){
              success
            }
          }`;
          acceptLegalQry = acceptLegalQry.replace("$rem", action.payload.toString());
          new Xhr().request(acceptLegalQry, "An error ocurred updating legal acceptance status")
          .then((acceptResponse: AxiosResponse) => {
            // tslint:disable-next-line:no-any
            const acceptRespData: any = JSON.parse(JSON.stringify(acceptResponse.data)).data;

            if (acceptRespData.acceptLegal.success) {
              loadDashboard();
            }
          })
          .catch((error: string) => {
            rollbar.error(error);
          });
        }
      })
      .catch((error: string) => {
        rollbar.error(error);
      });

      return {
        ...state,
        legalNotice: {
          open: false,
          rememberDecision: action.payload,
        },
      };
    case "SET_REMEMBER":

      return {
        ...state,
        legalNotice: {
          open: true,
          rememberDecision: action.payload,
        },
      };
    default:
      return state;
  }
};

export = registration;
