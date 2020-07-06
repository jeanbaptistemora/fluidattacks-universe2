import React from "react";
import { Col, Row } from "react-bootstrap";
import { Route, Switch, useRouteMatch } from "react-router-dom";
import { default as globalStyle } from "../../../../styles/global.css";
import translate from "../../../../utils/translations/translate";
import { ContentTab } from "../../components/ContentTab";
import { OrganizationPolicies } from "../OrganizationPoliciesView/index";
import { OrganizationUsers } from "../OrganizationUsersView/index";

const organizationContent: React.FC = (): JSX.Element => {
  const { path, url } = useRouteMatch();

  return(
    <React.StrictMode>
      <React.Fragment>
        <Row>
          <Col md={12} sm={12}>
            <div className={globalStyle.stickyContainer}>
              <ul className={globalStyle.tabsContainer}>
                <ContentTab
                  icon="icon pe-7s-box1"
                  id="policiesTab"
                  link={`${url}/policies`}
                  title={translate.t("organization.tabs.policies.text")}
                  tooltip={translate.t("organization.tabs.policies.tooltip")}
                />
                <ContentTab
                  icon="icon pe-7s-users"
                  id="usersTab"
                  link={`${url}/users`}
                  title={translate.t("organization.tabs.users.text")}
                  tooltip={translate.t("organization.tabs.users.tooltip")}
                />
              </ul>
            </div>
            <div className={globalStyle.tabContent}>
              <Switch>
                <Route path={`${path}/policies`} component={OrganizationPolicies} exact={true} />
                <Route path={`${path}/users`} component={OrganizationUsers} exact={true} />
              </Switch>
            </div>
          </Col>
        </Row>
      </React.Fragment>
    </React.StrictMode>
  );
};

export { organizationContent as OrganizationContent };
