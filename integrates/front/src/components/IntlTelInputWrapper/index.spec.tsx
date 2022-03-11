import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";

import { IntlTelInputWrapper } from ".";

describe("IntlTelInputWrapper", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof IntlTelInputWrapper).toStrictEqual("function");
  });

  it("should render international tel input wrapper", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(<IntlTelInputWrapper />);

    expect(wrapper).toHaveLength(1);
  });
});
