import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { FindingHeader } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("FindingHeader", () => {

  it("should return a function", () => {
    expect(typeof (FindingHeader))
      .toEqual("function");
  });

  it("should render finding header", () => {
    const wrapper: ShallowWrapper = shallow(
      <FindingHeader openVulns={9} reportDate="" severity={2} status="open" />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
