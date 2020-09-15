import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { Redirect, Route, RouteComponentProps, Switch } from "react-router-dom";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { TagsGroup } from "scenes/Dashboard/containers/TagContent/TagGroup";
import { TagsInfo } from "scenes/Dashboard/containers/TagContent/TagInfo";
import { default as globalStyle } from "styles/global.css";
import { translate } from "utils/translations/translate";

type IProjectContentProps = RouteComponentProps<{ tagName: string }>;

const tagContent: React.FC<IProjectContentProps> = (props: IProjectContentProps): JSX.Element => (
  <React.StrictMode>
    <React.Fragment>
      <React.Fragment>
        <Row>
          <Col md={12} sm={12}>
            <React.Fragment>
              <div className={globalStyle.stickyContainer}>
                <ul className={globalStyle.tabsContainer}>
                  <ContentTab
                    icon="icon pe-7s-graph3"
                    id="tagIndicatorsTab"
                    link={`${props.match.url}/indicators`}
                    title={translate.t("organization.tabs.portfolios.tabs.indicators.text")}
                    tooltip={translate.t("organization.tabs.portfolios.tabs.indicators.tooltip")}
                  />
                  <ContentTab
                    icon="icon pe-7s-albums"
                    id="tagGroupsTab"
                    link={`${props.match.url}/groups`}
                    title={translate.t("organization.tabs.portfolios.tabs.group.text")}
                    tooltip={translate.t("organization.tabs.portfolios.tabs.group.tooltip")}
                  />
                </ul>
              </div>
              <div className={globalStyle.tabContent}>
                <Switch>
                  <Route path={`${props.match.path}/indicators`} component={TagsInfo} exact={true} />
                  <Route path={`${props.match.path}/groups`} component={TagsGroup} exact={true} />
                  <Redirect to={`${props.match.path}/indicators`} />
                </Switch>
              </div>
            </React.Fragment>
          </Col>
        </Row>
      </React.Fragment>
    </React.Fragment>
  </React.StrictMode>
);

export { tagContent as TagContent };
