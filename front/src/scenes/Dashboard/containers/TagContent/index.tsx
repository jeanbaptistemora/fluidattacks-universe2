import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { NavLink, Redirect, Route, RouteComponentProps, Switch } from "react-router-dom";
import { default as globalStyle } from "../../../../styles/global.css";
import translate from "../../../../utils/translations/translate";
import { TagsInfo } from "./TagInfo/index";

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
                  <li id="tagIndicatorsTab" className={globalStyle.tab}>
                    <NavLink activeClassName={globalStyle.active} to={`${props.match.url}/indicators`}>
                      <i className="icon pe-7s-graph3" />
                      &nbsp;{translate.t("project.tabs.indicators")}
                    </NavLink>
                  </li>
                </ul>
              </div>
              <div className={globalStyle.tabContent}>
                <Switch>
                  <Route path={`${props.match.path}/indicators`} component={TagsInfo} exact={true} />
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
