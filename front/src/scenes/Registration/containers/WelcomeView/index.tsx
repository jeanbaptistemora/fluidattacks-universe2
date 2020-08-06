/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for accessing render props from
 * apollo components
 */

import { MutationFunction, QueryResult } from "@apollo/react-common";
import { Mutation, Query } from "@apollo/react-components";
import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { Redirect, RouteComponentProps } from "react-router-dom";
import { Button } from "../../../../components/Button";
import { default as logo } from "../../../../resources/integrates.svg";
import { default as globalStyle } from "../../../../styles/global.css";
import translate from "../../../../utils/translations/translate";
import { CompulsoryNotice } from "../../components/CompulsoryNotice";
import { default as style } from "./index.css";
import { ACCEPT_LEGAL_MUTATION, GET_USER_AUTHORIZATION } from "./queries";

type WelcomeViewProps = RouteComponentProps;

const welcomeView: React.FC<WelcomeViewProps> = (): JSX.Element => {

  const [isLegalModalOpen, setLegalModalOpen] = React.useState(true);

  const savedUrl: string = _.get(localStorage, "start_url", "/home");
  const initialUrl: string = savedUrl === "/logout" ? "/home" : savedUrl;

  const loadDashboard: (() => void) = (): void => {
    localStorage.removeItem("showAlreadyLoggedin");
    localStorage.removeItem("concurrentSession");
    localStorage.removeItem("start_url");
    location.assign(`/integrates${initialUrl}`);
  };

  const { userEmail, userName } = window as typeof window & Dictionary<string>;

  return (
    <React.StrictMode>
      <div className={`${style.container} ${globalStyle.lightFg}`}>
        <div className={style.content}>
          <div className={style.imgDiv}>
            <img className={style.img} src={logo} alt="logo" /><br />
            <h1>{translate.t("registration.greeting")} {userName}!</h1>
          </div>
          {localStorage.getItem("showAlreadyLoggedin") === "1"
            ?
            <div>
              <Row className={style.row}><h3>{translate.t("registration.logged_in_title")}</h3></Row>
              <Row>
                <Col md={12}>
                  <p>{translate.t("registration.logged_in_message")}</p>
                </Col>
              </Row>
              <Row>
                <Col md={12}>
                  <Button bsStyle="primary" block={true} onClick={loadDashboard}>
                    {translate.t("registration.continue_as_btn")} {userEmail}
                  </Button>
                </Col>
              </Row>
            </div>
            :
            localStorage.getItem("concurrentSession") === "1"
              ?
              <div>
                <Row className={style.row}>
                  <h3>{translate.t("registration.concurrent_session_message")}</h3>
                </Row>
                <Row>
                  <Col md={12}>
                    <Button bsStyle="primary" block={true} onClick={loadDashboard}>
                      {translate.t("registration.continue_btn")}
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
                    {data.me.remember
                        ? <Redirect to={initialUrl === "/registration" ? "/home" : initialUrl}/>
                        :
                        <Mutation mutation={ACCEPT_LEGAL_MUTATION} onCompleted={loadDashboard}>
                          {(acceptLegal: MutationFunction): JSX.Element => {

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
