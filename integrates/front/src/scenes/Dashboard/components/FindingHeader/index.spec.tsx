import { shallow, ShallowWrapper } from "enzyme";
import * as React from "react";
import { FindingHeader } from "scenes/Dashboard/components/FindingHeader";

describe("FindingHeader", () => {

  it("should return a function", () => {
    expect(typeof (FindingHeader))
      .toEqual("function");
  });

  it("should render finding header", () => {
    const wrapper: ShallowWrapper = shallow(
      <FindingHeader openVulns={9} discoveryDate="" severity={2} status="open" />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
