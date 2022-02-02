import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";

import { FindingHeader } from "scenes/Dashboard/components/FindingHeader";

describe("FindingHeader", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FindingHeader).toStrictEqual("function");
  });

  it("should render finding header", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <FindingHeader
        discoveryDate={""}
        estRemediationTime={"42.1"}
        openVulns={9}
        severity={2}
        status={"open"}
      />
    );

    expect(wrapper).toHaveLength(1);
  });
});
