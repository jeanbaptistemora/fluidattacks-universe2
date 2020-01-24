/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */

import _ from "lodash";
import React from "react";
import { Mutation, MutationFn, Query, QueryResult } from "react-apollo";
import { Col, Row } from "react-bootstrap";
import { Redirect, RouteComponentProps } from "react-router-dom";
import { Button } from "../../../../components/Button";
import { default as logo } from "../../../../resources/logo.png";
import { default as globalStyle } from "../../../../styles/global.css";
import translate from "../../../../utils/translations/translate";
import { CompulsoryNotice } from "../../components/CompulsoryNotice";
import { default as style } from "./index.css";
import { ACCEPT_LEGAL_MUTATION, GET_USER_AUTHORIZATION } from "./queries";

type WelcomeViewProps = RouteComponentProps;

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

const welcomeView: React.FC<WelcomeViewProps> = (): JSX.Element => {
  const onMount: (() => void) = (): void => {
    localStorage.removeItem("showAlreadyLoggedin");
    localStorage.removeItem("url_inicio");
  };
  React.useEffect(onMount, []);

  const [isLegalModalOpen, setLegalModalOpen] = React.useState(true);

  const initialUrl: string = _.get(localStorage, "url_inicio", "!/home");
  const loadDashboard: (() => void) = (): void => {
    location.assign(`/dashboard#${initialUrl}`);
  };

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
            ?
            <div>
              <Row style={{ paddingBottom: "20px" }}><h3>{translate.t("registration.logged_in_title")}</h3></Row>
              <Row>
                <Col md={12}>
                  <p>{translate.t("registration.logged_in_message")}</p>
                </Col>
              </Row>
              <Row>
                <Col md={12}>
                  <Button bsStyle="primary" block={true} onClick={loadDashboard}>
                    {translate.t("registration.continue_btn")} {userEmail}
                  </Button>
                </Col>
              </Row>
            </div>
            :
            <Query query={GET_USER_AUTHORIZATION} fetchPolicy="network-only">
              {({ data, loading }: QueryResult): JSX.Element => {
                if (_.isUndefined(data) || loading) { return <React.Fragment />; }

                return (
                  <React.Fragment>
                    {data.me.authorized
                      ? data.me.remember
                        ? <Redirect to={`/dashboard#${initialUrl}`} />
                        :
                        <Mutation mutation={ACCEPT_LEGAL_MUTATION} onCompleted={loadDashboard}>
                          {(acceptLegal: MutationFn): React.ReactNode => {

                            const handleAccept: ((remember: boolean) => void) = (remember: boolean): void => {
                              setLegalModalOpen(false);
                              acceptLegal({ variables: { remember } })
                                .catch();
                            };

                            return (
                              <CompulsoryNotice
                                content={translate.t("legalNotice.description")}
                                onAccept={handleAccept}
                                open={isLegalModalOpen}
                              />
                            );
                          }}
                        </Mutation>
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

export { welcomeView as WelcomeView };
