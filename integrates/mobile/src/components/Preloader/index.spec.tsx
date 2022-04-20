import { shallow } from "enzyme";
import type { ShallowWrapper } from "enzyme";
import React from "react";

import { Preloader } from ".";

describe("Preloader", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof Preloader).toBe("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(<Preloader visible={true} />);

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find("Image")).toHaveLength(1);

    wrapper.setProps({ visible: false });

    expect(wrapper.find("Image")).toHaveLength(0);
  });
});
