/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */

import _ from "lodash";
import React, { ComponentType } from "react";
import { Query, QueryResult } from "react-apollo";
import { Col, Row } from "react-bootstrap";
import { Redirect } from "react-router-dom";
import { AnyAction, Reducer } from "redux";
import { ThunkDispatch } from "redux-thunk";
import { StateType } from "typesafe-actions";
import { Button } from "../../../../components/Button";
import { default as logo } from "../../../../resources/logo.png";
import store from "../../../../store/index";
import { default as globalStyle } from "../../../../styles/global.css";
import reduxWrapper from "../../../../utils/reduxWrapper";
import translate from "../../../../utils/translations/translate";
import * as actions from "../../actions";
import { CompulsoryNotice } from "../../components/CompulsoryNotice";
import { default as style } from "./index.css";
import { GET_USER_AUTHORIZATION } from "./queries";

export interface IWelcomeViewProps {
  legalNotice: {
    open: boolean;
    rememberDecision: boolean;
  };
}

const acceptLegal: ((rememberValue: boolean) => void) = (rememberValue: boolean): void => {
  const thunkDispatch: ThunkDispatch<{}, {}, AnyAction> = (
    store.dispatch as ThunkDispatch<{}, {}, AnyAction>
  );

  thunkDispatch(actions.acceptLegal(rememberValue));
};

const renderLegalNotice: ((props: IWelcomeViewProps) => JSX.Element) = (props: IWelcomeViewProps): JSX.Element => (
  <div>
    <React.Fragment>
      <CompulsoryNotice
        content={translate.t("legalNotice.description")}
        onAccept={acceptLegal}
        open={props.legalNotice.open}
      />
    </React.Fragment>
  </div>
);

const renderUnauthorized: (() => JSX.Element) = (): JSX.Element => {
  const handleLogoutClick: (() => void) = (): void => { location.assign("/integrates/logout"); };

  return (
    <React.Fragment>
      <Row>
        <Col md={12}>
          <p>{translate.t("registration.unauthorized")}</p>
        </Col>
      </Row>
      <Row>
        <Col md={12}>
          <Button bsStyle="primary" block={true} onClick={handleLogoutClick}>{translate.t("logout")}</Button>
        </Col>
      </Row>
    </React.Fragment>
  );
};

const renderAlreadyLoggedIn: ((email: string) => JSX.Element) =
  (email: string): JSX.Element => (
    <React.Fragment>
      <div>
        <Row style={{ paddingBottom: "20px" }}><h3>{translate.t("registration.logged_in_title")}</h3></Row>
        <Row>
          <Col md={12}>
            <p>{translate.t("registration.logged_in_message")}</p>
          </Col>
        </Row>
        <Row>
          <Col md={12}>
            <Button bsStyle="primary" block={true} onClick={actions.loadDashboard}>
              {translate.t("registration.continue_btn")} {email}
            </Button>
          </Col>
        </Row>
      </div>
    </React.Fragment>
  );

export const component: React.FC<IWelcomeViewProps> = (props: IWelcomeViewProps): JSX.Element => {
  const onMount: (() => void) = (): void => {
    if (localStorage.getItem("showAlreadyLoggedin") === "1") {
      localStorage.removeItem("showAlreadyLoggedin");
    }
  };
  React.useEffect(onMount, []);

  const { userEmail, userName } = window as typeof window & Dictionary<string>;

  return (
    <React.StrictMode>
      <div className={`${style.container} ${globalStyle.lightFg}`}>
        <div className={style.content}>
          <div style={{ paddingBottom: "50px" }}>
            <img style={{ paddingBottom: "30px" }} src={logo} alt="logo" /><br />
            <h1>{translate.t("registration.greeting")} {userName}!</h1>
          </div>
          {localStorage.getItem("showAlreadyLoggedin") === "1"
            ? renderAlreadyLoggedIn(userEmail)
            :
            <Query query={GET_USER_AUTHORIZATION} fetchPolicy="network-only">
              {({ data, loading }: QueryResult): JSX.Element => {
                if (_.isUndefined(data) || loading) { return <React.Fragment />; }

                return (
                  <React.Fragment>
                    {data.me.authorized
                      ? data.me.remember
                        ? <Redirect to="/dashboard" />
                        : renderLegalNotice(props)
                      : renderUnauthorized()
                    }
                  </React.Fragment>
                );
              }}
            </Query>
          }
        </div>
      </div>
    </React.StrictMode>
  );
};

export const welcomeView: ComponentType<IWelcomeViewProps> = reduxWrapper(
  component,
  (state: StateType<Reducer>): Partial<IWelcomeViewProps> => ({
    legalNotice: state.registration.legalNotice,
  }),
);
