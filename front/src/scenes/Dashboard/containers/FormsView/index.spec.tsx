import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { FormsView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("FormsView", () => {

  it("should return a fuction", () => {
    expect(typeof (FormsView))
      .toEqual("function");
  });

  it("should render findings form", async () => {
    const wrapper: ShallowWrapper = shallow(
      <FormsView />,
    );
    expect(wrapper.find("#findingsItem"))
      .toBeTruthy();
  });

  it("should render a component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <FormsView />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
