import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";

import { Badge } from "components/Badge";

describe("Badge", (): void => {
  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof Badge).toStrictEqual("function");
  });

  it("should render a badge", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(<Badge>{"Test"}</Badge>);

    expect(wrapper).toHaveLength(1);
  });
});
