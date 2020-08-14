import { shallow, ShallowWrapper } from "enzyme";
import React from "react";

import { Preloader } from "./index";

describe("Preloader", (): void => {

  it("should return a function", (): void => {
    expect(typeof (Preloader))
      .toEqual("function");
  });

  it("should render", (): void => {
    const wrapper: ShallowWrapper = shallow(<Preloader visible={true} />);

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.find("Image"))
      .toHaveLength(1);
    wrapper.setProps({ visible: false });
    expect(wrapper.find("Image"))
      .toHaveLength(0);
  });
});
