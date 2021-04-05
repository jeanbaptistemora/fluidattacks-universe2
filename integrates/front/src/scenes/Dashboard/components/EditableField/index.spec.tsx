import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";

import { EditableField } from "scenes/Dashboard/components/EditableField";

describe("Confirm dialog", (): void => {
  it("should return an function", (): void => {
    expect.hasAssertions();

    expect(typeof EditableField).toStrictEqual("function");
  });

  it("should render a horizontal wide editable field", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <EditableField
        alignField={"horizontalWide"}
        component={"input"}
        currentValue={"test"}
        label={"Test Field"}
        name={"testName"}
        renderAsEditable={true}
        type={"text"}
      />
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render a horizontal wide field", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <EditableField
        alignField={"horizontalWide"}
        component={"input"}
        currentValue={"test"}
        label={"Test Field"}
        name={"testName"}
        renderAsEditable={false}
        type={"text"}
      />
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render a horizontal editable field", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <EditableField
        alignField={"horizontal"}
        component={"input"}
        currentValue={"test"}
        label={"Test Field"}
        name={"testName"}
        renderAsEditable={true}
        type={"text"}
      />
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render a horizontal field", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <EditableField
        alignField={"horizontal"}
        component={"input"}
        currentValue={"test"}
        label={"Test Field"}
        name={"testName"}
        renderAsEditable={false}
        type={"text"}
      />
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render a vertical editable field", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <EditableField
        component={"input"}
        currentValue={"test"}
        label={"Test Field"}
        name={"testName"}
        renderAsEditable={true}
        type={"text"}
      />
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render a vertical field", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <EditableField
        component={"input"}
        currentValue={"test"}
        label={"Test Field"}
        name={"testName"}
        renderAsEditable={false}
        type={"text"}
      />
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render a url field", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <EditableField
        alignField={"horizontal"}
        component={"input"}
        currentValue={"https://test.html"}
        label={"Test Field"}
        name={"testName"}
        renderAsEditable={false}
        type={"text"}
      />
    );

    expect(wrapper).toHaveLength(1);
  });

  it("should render a invisible field", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <EditableField
        alignField={"horizontal"}
        component={"input"}
        currentValue={"https://test.html"}
        label={"Test Field"}
        name={"testName"}
        renderAsEditable={true}
        type={"text"}
        visibleWhileEditing={false}
      />
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.text()).toHaveLength(0);
  });
});
