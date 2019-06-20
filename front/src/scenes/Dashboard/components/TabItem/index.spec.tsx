import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { TabItem } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("TabItem", () => {

  it("should return a function", () => {
    expect(typeof (TabItem))
      .toEqual("function");
  });

  it("should render a TabItem", () => {
    const wrapper: ShallowWrapper = shallow(
      <TabItem icon={<i className="icon pe-7s-note2" />} label="Test" to="/forms" />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
