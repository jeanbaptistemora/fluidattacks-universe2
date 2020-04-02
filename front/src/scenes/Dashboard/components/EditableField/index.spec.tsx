import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { EditableField } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Confirm dialog", () => {

  it("should return an function", () => {
    expect(typeof (EditableField))
      .toEqual("function");
  });

  it("should render a horizontal wide editable field", () => {
    const wrapper: ShallowWrapper = shallow(
      <EditableField
        alignField="horizontalWide"
        component="input"
        currentValue="test"
        label="Test Field"
        name="testName"
        renderAsEditable={true}
        type="text"
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a horizontal wide field", () => {
    const wrapper: ShallowWrapper = shallow(
      <EditableField
        alignField="horizontalWide"
        component="input"
        currentValue="test"
        label="Test Field"
        name="testName"
        renderAsEditable={false}
        type="text"
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a horizontal editable field", () => {
    const wrapper: ShallowWrapper = shallow(
      <EditableField
        alignField="horizontal"
        component="input"
        currentValue="test"
        label="Test Field"
        name="testName"
        renderAsEditable={true}
        type="text"
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a horizontal field", () => {
    const wrapper: ShallowWrapper = shallow(
      <EditableField
        alignField="horizontal"
        component="input"
        currentValue="test"
        label="Test Field"
        name="testName"
        renderAsEditable={false}
        type="text"
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a vertical editable field", () => {
    const wrapper: ShallowWrapper = shallow(
      <EditableField
        component="input"
        currentValue="test"
        label="Test Field"
        name="testName"
        renderAsEditable={true}
        type="text"
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a vertical field", () => {
    const wrapper: ShallowWrapper = shallow(
      <EditableField
        component="input"
        currentValue="test"
        label="Test Field"
        name="testName"
        renderAsEditable={false}
        type="text"
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a url field", () => {
    const wrapper: ShallowWrapper = shallow(
      <EditableField
        alignField="horizontal"
        component="input"
        currentValue="https://test.html"
        label="Test Field"
        name="testName"
        renderAsEditable={false}
        type="text"
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a invisible field", () => {
    const wrapper: ShallowWrapper = shallow(
      <EditableField
        alignField="horizontal"
        component="input"
        currentValue="https://test.html"
        label="Test Field"
        name="testName"
        renderAsEditable={true}
        type="text"
        visibleWhileEditing={false}
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.text())
      .toHaveLength(0);
  });
});
