/* eslint-disable react/forbid-component-props
  ------
  We need to override default styles from react-bootstrap
*/
import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { CompulsoryNotice } from "scenes/Registration/components/CompulsoryNotice";
import type { GraphQLError } from "graphql";
import { Logger } from "utils/logger";
import React from "react";
import _ from "lodash";
import globalStyle from "styles/global.css";
import logo from "resources/integrates.svg";
import style from "scenes/Registration/containers/WelcomeView/index.css";
import { translate } from "utils/translations/translate";
import { useHistory } from "react-router-dom";
import {
  ACCEPT_LEGAL_MUTATION,
  GET_USER_AUTHORIZATION,
} from "scenes/Registration/containers/WelcomeView/queries";
import { Col100, Row } from "styles/styledComponents";
import { useMutation, useQuery } from "@apollo/react-hooks";

export const WelcomeView: React.FC = (): JSX.Element => {
  // Load on last visited url
  const savedUrl: string = _.get(localStorage, "start_url", "/home");
  const initialUrl: string =
    savedUrl === "/logout" || savedUrl === "/registration" ? "/home" : savedUrl;
  const history: ReturnType<typeof useHistory> = useHistory();
  function loadDashboard(): void {
    localStorage.removeItem("showAlreadyLoggedin");
    localStorage.removeItem("concurrentSession");
    localStorage.removeItem("start_url");
    history.replace(initialUrl);
  }

  // Display legal notice
  interface IUser {
    me: { remember: boolean; userName: string };
  }
  const { data, loading } = useQuery<IUser>(GET_USER_AUTHORIZATION, {
    fetchPolicy: "network-only",
    onCompleted: (userData): void => {
      if (userData.me.remember) {
        loadDashboard();
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error(
          "An error occurred while fetching user authorization",
          error
        );
      });
    },
  });
  const [acceptLegal] = useMutation(ACCEPT_LEGAL_MUTATION, {
    onCompleted: loadDashboard,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error(
          "An error occurred while accepting user legal notice",
          error
        );
      });
    },
  });
  const [isLegalModalOpen, setLegalModalOpen] = React.useState(true);
  function handleAccept(remember: boolean): void {
    setLegalModalOpen(false);
    void acceptLegal({ variables: { remember } });
  }

  return (
    <div className={style.container}>
      <div className={style.content}>
        <div className={`${style.imgDiv} ${globalStyle["light-fg"]}`}>
          <img alt={"logo"} className={style.img} src={logo} />
          <br />
          <h1>
            {translate.t("registration.greeting")}{" "}
            {data?.me.userName.split(" ")[0]}
            {"!"}
          </h1>
        </div>
        {localStorage.getItem("concurrentSession") === "1" ? (
          <div>
            <Row>
              <h2>{translate.t("registration.concurrent_session_message")}</h2>
            </Row>
            <Row>
              <Col100>
                <Button onClick={loadDashboard}>
                  {translate.t("registration.continue_btn")}
                </Button>
              </Col100>
            </Row>
          </div>
        ) : (
          !(_.isUndefined(data) || loading || data.me.remember) && (
            <CompulsoryNotice
              content={translate.t("legalNotice.description")}
              onAccept={handleAccept}
              open={isLegalModalOpen}
            />
          )
        )}
      </div>
    </div>
  );
};
