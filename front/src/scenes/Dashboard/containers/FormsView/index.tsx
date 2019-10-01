import React from "react";
import { Col, Row } from "react-bootstrap";
import { Redirect, Route, Switch } from "react-router";
import { NavLink } from "react-router-dom";
import { default as Frame } from "../../../../components/Frame";
import translate from "../../../../utils/translations/translate";
import style from "../ProjectContent/index.css";

const formsView: React.FC = (): JSX.Element => {
  const progressForm: (() => JSX.Element) = (): JSX.Element => (
    <Frame src="https://fluidsignal.formstack.com/forms/avance" height={3000} id="ifrmProgress" />
  );

  const findingForm: (() => JSX.Element) = (): JSX.Element => (
    <Row>
      <Col xs={12} md={12} sm={12} style={{ textAlign: "center" }}>
        <h3>There is a new way to report findings!</h3>
        <br />
        <p>
          Read more details in&nbsp;
          <a
            href="https://community.fluidattacks.com/t/finding-report-from-integrates/454"
            rel="noopener"
            target="_blank"
          >
            Fluid Attacks's community
          </a>
        </p>
      </Col>
    </Row>
  );

  const closingForm: (() => JSX.Element) = (): JSX.Element => (
    <Frame src="https://fluidsignal.formstack.com/forms/cierres" height={3000} id="ifrmClosure" />
  );

  const eventForm: (() => JSX.Element) = (): JSX.Element => (
    <Frame src="https://fluidsignal.formstack.com/forms/eventualidad" height={3000} id="ifrmEvents" />
  );

  return (
    <React.StrictMode>
      <div>
        <ul className={style.tabsContainer}>
          <li id="progressItem" className={style.tab}>
            <NavLink activeClassName={style.active} to="/forms/progress">
              <i className="icon pe-7s-refresh-2" />
              &nbsp;{translate.t("forms.progress")}
            </NavLink>
          </li>
          <li id="findingsItem" className={style.tab}>
            <NavLink activeClassName={style.active} to="/forms/findings">
              <i className="icon pe-7s-id" />
              &nbsp;{translate.t("forms.findings")}
            </NavLink>
          </li>
          <li id="closingItem" className={style.tab}>
            <NavLink activeClassName={style.active} to="/forms/closing">
              <i className="icon pe-7s-less" />
              &nbsp;{translate.t("forms.closing")}
            </NavLink>
          </li>
          <li id="eventItem" className={style.tab}>
            <NavLink activeClassName={style.active} to="/forms/events">
              <i className="icon pe-7s-way" />
              &nbsp;{translate.t("forms.events")}
            </NavLink>
          </li>
        </ul>
      </div>
      <div className={style.tabContent}>
        <Switch>
          <Route path="/forms/progress" exact={true} component={progressForm} />
          <Route path="/forms/findings" exact={true} component={findingForm} />
          <Route path="/forms/closing" exact={true} component={closingForm} />
          <Route path="/forms/events" exact={true} component={eventForm} />
          <Redirect to="/forms/progress" />
        </Switch>
      </div>
    </React.StrictMode>
  );
};

export { formsView as FormsView };
