import { shallow, configure } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { expect } from "chai";
import {
  trackingView as TrackingView,
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

  it('should render findings', () => {
    const testClosings: closing[] = [{
      closed: "2",
      cycle: "1",
      efectividad: "20",
      estado: "Parcialmente cerrado",
      finding: "363808260",
      id: "400903395",
      opened: "1",
      position: 1,
      requested: "10",
      timeFormat: "2018/09/17",
      timestamp: "2018/09/17 09:06:44",
      verified: "10",
      visibles: "10",
      whichClosed: "unit/test/index.js line:32",
      whichOpened: "",
    }]
    const wrapper = shallow(
      <TrackingView
        openFindingsTitle="Open"
        openFindingsContent="unit/test/index.js line:32"
        closedFindingsTitle="Closed"
        closedFindingsContent="unit/main/index.js line:16"
        closings={testClosings}
        discoveryDate="2018/08/23"
        discoveryText="Discovery"
        cycleText="Cycle"
        efectivenessText="Efectiveness"
      />
    );
    expect(
      wrapper.contains(
        <Row>
          <Col
            md={12}
          >
            <p>Open</p>
            <TextareaAutosize
              disabled={true}
            >
              unit/test/index.js line:32
            </TextareaAutosize>
          </Col>
          <Col
            md={12}
          >
            <p>Closed</p>
            <TextareaAutosize
              disabled={true}
            >
              unit/main/index.js line:16
            </TextareaAutosize>
          </Col>
        </Row>
      )
    ).to.equal(true);
  });

  it('should render closings timeline', () => {
    const testClosings: closing[] = [{
      closed: "2",
      cycle: "1",
      efectividad: "20",
      estado: "Parcialmente cerrado",
      finding: "363808260",
      id: "400903395",
      opened: "1",
      position: 1,
      requested: "10",
      timeFormat: "2018/09/17",
      timestamp: "2018/09/17 09:06:44",
      verified: "10",
      visibles: "10",
      whichClosed: "unit/test/index.js line:32",
      whichOpened: "",
    }]
    const wrapper = shallow(
      <TrackingView
        openFindingsTitle="Open"
        openFindingsContent="unit/test/index.js line:32"
        closedFindingsTitle="Closed"
        closedFindingsContent="unit/main/index.js line:16"
        closings={testClosings}
        discoveryDate="2018/08/23"
        discoveryText="Discovery"
        cycleText="Cycle"
        efectivenessText="Efectiveness"
      />
    );
    expect(
      wrapper.find('ul').contains([
        <li>
          <div>
            <span>
              2018/08/23
            </span>
          </div>
          <div>
            <p>
              Discovery
            </p>
          </div>
        </li>,
        <li>
          <div>
            <span>
              2018/09/17
            </span>
          </div>
          <div>
            <p>
              Cycle: 1,Open: 1,Closed: 2,Efectiveness: 20%
            </p>
          </div>
        </li>
      ])
    ).to.equal(true);
  });
});
