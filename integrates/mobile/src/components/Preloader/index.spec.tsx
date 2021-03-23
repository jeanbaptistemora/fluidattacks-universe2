import { Preloader } from ".";
import React from "react";
import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";

describe("Preloader", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof Preloader).toStrictEqual("function");
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
