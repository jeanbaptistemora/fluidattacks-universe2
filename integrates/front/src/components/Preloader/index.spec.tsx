import { Preloader } from "components/Preloader";
import React from "react";
import { ShallowWrapper, shallow } from "enzyme";

describe("Preloader", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Preloader).toStrictEqual("function");
  });

  it("should render a preloader", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(<Preloader />);

    expect(wrapper).toHaveLength(1);
  });
});
