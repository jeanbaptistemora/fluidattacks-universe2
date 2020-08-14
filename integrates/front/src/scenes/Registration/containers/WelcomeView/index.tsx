/* eslint-disable react/forbid-component-props
  ------
  We need to override default styles from react-bootstrap
*/
import { Button } from "../../../../components/Button";
import { CompulsoryNotice } from "../../components/CompulsoryNotice";
import React from "react";
import _ from "lodash";
import { default as globalStyle } from "../../../../styles/global.css";
import { default as logo } from "../../../../resources/integrates.svg";
import { default as style } from "./index.css";
import translate from "../../../../utils/translations/translate";
import { ACCEPT_LEGAL_MUTATION, GET_USER_AUTHORIZATION } from "./queries";
import { Col, Row } from "react-bootstrap";
import { Mutation, Query } from "@apollo/react-components";
import { MutationFunction, QueryResult } from "@apollo/react-common";
import { Redirect, useHistory } from "react-router-dom";

export const WelcomeView: React.FC = (): JSX.Element => {
  const history: ReturnType<typeof useHistory> = useHistory();
  const [isLegalModalOpen, setLegalModalOpen] = React.useState(true);

  const savedUrl: string = _.get(localStorage, "start_url", "/home");
  const initialUrl: string = savedUrl === "/logout" ? "/home" : savedUrl;

  function loadDashboard(): void {
    localStorage.removeItem("showAlreadyLoggedin");
    localStorage.removeItem("concurrentSession");
    localStorage.removeItem("start_url");
    history.replace(initialUrl);
  }

  const { userEmail, userName } = window as typeof window & Dictionary<string>;

  return (
    <React.StrictMode>
      <div className={`${style.container} ${globalStyle.lightFg}`}>
        <div className={style.content}>
          <div className={style.imgDiv}>
            <img alt={"logo"} className={style.img} src={logo} />
            <br />
            <h1>
              {translate.t("registration.greeting")} {userName}
              {"!"}
            </h1>
          </div>
          {localStorage.getItem("showAlreadyLoggedin") === "1" ? (
            <div>
              <Row className={style.row}>
                <h3>{translate.t("registration.logged_in_title")}</h3>
              </Row>
              <Row>
                <Col md={12}>
                  <p>{translate.t("registration.logged_in_message")}</p>
                </Col>
              </Row>
              <Row>
                <Col md={12}>
                  <Button
                    block={true}
                    bsStyle={"primary"}
                    onClick={loadDashboard}
                  >
                    {translate.t("registration.continue_as_btn")} {userEmail}
                  </Button>
                </Col>
              </Row>
            </div>
          ) : localStorage.getItem("concurrentSession") === "1" ? (
            <div>
              <Row className={style.row}>
                <h3>
                  {translate.t("registration.concurrent_session_message")}
                </h3>
              </Row>
              <Row>
                <Col md={12}>
                  <Button
                    block={true}
                    bsStyle={"primary"}
                    onClick={loadDashboard}
                  >
                    {translate.t("registration.continue_btn")}
                  </Button>
                </Col>
              </Row>
            </div>
          ) : (
            <Query fetchPolicy={"network-only"} query={GET_USER_AUTHORIZATION}>
              {({
                data,
                loading,
              }: QueryResult<{ me: { remember: boolean } }>): JSX.Element => {
                if (_.isUndefined(data) || loading) {
                  return <div />;
                }

                return data.me.remember ? (
                  <Redirect
                    to={initialUrl === "/registration" ? "/home" : initialUrl}
                  />
                ) : (
                  <Mutation
                    mutation={ACCEPT_LEGAL_MUTATION}
                    onCompleted={loadDashboard}
                  >
                    {(acceptLegal: MutationFunction): JSX.Element => {
                      function handleAccept(remember: boolean): void {
                        setLegalModalOpen(false);
                        void acceptLegal({ variables: { remember } }).catch();
                      }

                      return (
                        <CompulsoryNotice
                          content={translate.t("legalNotice.description")}
                          onAccept={handleAccept}
                          open={isLegalModalOpen}
                        />
                      );
                    }}
                  </Mutation>
                );
              }}
            </Query>
          )}
        </div>
      </div>
    </React.StrictMode>
  );
};
