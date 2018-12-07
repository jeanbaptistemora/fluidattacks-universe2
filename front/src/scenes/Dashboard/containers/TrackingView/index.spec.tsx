import { shallow, configure } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { expect } from "chai";
import {
  trackingViewComponent as TrackingView,
  closing
} from "./index";
import "mocha";
import React from "react";
import TextareaAutosize from "react-textarea-autosize";
import { Col, Row } from "react-bootstrap";

configure({ adapter: new Adapter() });

describe('Tracking view', () => {

  it('should return a function', () => {
    expect(typeof(TrackingView)).to.equal('function');
  });

  it('should render vulnerabilities', () => {
    const testClosings: closing[] = [{
      closed: "2",
      cycle: "1",
      date: "2018-10-10",
      effectiveness: "20",
      open: "1",
    }]
    const wrapper = shallow(
      <TrackingView
        openFindingsContent="unit/test/index.js line:32"
        closedFindingsContent="unit/main/index.js line:16"
        closings={testClosings}
        findingId="422286126"
        hasNewVulnerabilities={false}
      />
    );
    expect(
      wrapper.contains(
        <Row>
        <React.Fragment>
          <Col
            md={12}
            componentClass="div"
          >
            <p>search_findings.tab_tracking.open</p>
            <TextareaAutosize
              disabled={true}
              value="unit/test/index.js line:32"
            />
          </Col>
          <Col
            md={12}
            componentClass="div"
          >
            <p>search_findings.tab_tracking.closed</p>
            <TextareaAutosize
              disabled={true}
              value="unit/main/index.js line:16"
            />
          </Col>
          </React.Fragment>
        </Row>
      )
    ).to.equal(true);
  });
  it('should render closings timeline', () => {
    const testClosings: closing[] = [{
      closed: "0",
      cycle: "0",
      date: "2018-10-10",
      effectiveness: "0",
      open: "4",
    }]
    const wrapper = shallow(
      <TrackingView
        closings={testClosings}
        findingId="422286126"
        hasNewVulnerabilities={true}
      />
    );
    expect(
      wrapper.find('ul').contains([
        <li>
          <div>
            <span>
              2018-10-10
            </span>
          </div>
          <div>
            <p>
              search_findings.tab_tracking.founded,search_findings.tab_tracking.open: 4,search_findings.tab_tracking.closed: 0
            </p>
          </div>
        </li>
      ])
    ).to.equal(true);

 });
});
