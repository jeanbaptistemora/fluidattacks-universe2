import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import {
  closing,
  trackingViewComponent as TrackingView,
} from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Tracking view", () => {

  it("should return a function", () => {
    expect(typeof (TrackingView)).to
      .equal("function");
  });

  it("should render closings timeline", () => {
    const testClosings: closing[] = [{
      closed: 0,
      cycle: 0,
      date: "2018-10-10",
      effectiveness: 0,
      open: 4,
    }];
    const wrapper: ShallowWrapper = shallow(
      <TrackingView
        closings={testClosings}
        findingId="422286126"
        userRole="admin"
      />,
    );

    const expectedText: string = "search_findings.tab_tracking.founded,search_findings.tab_tracking.open: 4,"
      + "search_findings.tab_tracking.closed: 0";

    expect(wrapper.find("ul")
      .contains([(
        <li className="undefined undefined">
          <div>
            <span>
              2018-10-10
          </span>
          </div>
          <div>
            <p>
              {expectedText}
            </p>
          </div>
        </li>
      )]),
    ).to
      .equal(true);
  });
});
