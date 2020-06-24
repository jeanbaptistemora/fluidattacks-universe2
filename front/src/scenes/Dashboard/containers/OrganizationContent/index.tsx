import React from "react";
import { Col, Row } from "react-bootstrap";
import { Route, Switch, useRouteMatch } from "react-router-dom";
import { default as globalStyle } from "../../../../styles/global.css";
import translate from "../../../../utils/translations/translate";
import { ContentTab } from "../../components/ContentTab";
import { OrganizationSettings } from "../OrganizationSettings/index";

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
                  id="settingsTab"
                  link={`${url}/settings`}
                  title={translate.t("organization.tabs.settings.text")}
                  tooltip={translate.t("organization.tabs.settings.tooltip")}
                />
              </ul>
            </div>

            <div className={globalStyle.tabContent}>
              <Switch>
                <Route path={`${path}/settings`} component={OrganizationSettings} exact={true} />
              </Switch>
            </div>
          </Col>
        </Row>
      </React.Fragment>
    </React.StrictMode>
  );
};

export { organizationContent as OrganizationContent };
