import { Badge } from "components/Badge";
import React from "react";
import { ShallowWrapper, shallow } from "enzyme";

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

  it("should render a responsive medium size badge", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Badge responsive={true} size={"md"}>
        {"Test"}
      </Badge>
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.prop("bsClass")).toStrictEqual("badge badge position md");
  });
});
