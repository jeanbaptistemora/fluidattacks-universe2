import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import React from "react";
import { FileInput } from "./index";

describe("File input", () => {
  it("should return a function", () => {
    expect(typeof (FileInput))
      .toEqual("function");
  });

  it("should be rendered", () => {
    const wrapper: ShallowWrapper = shallow(
      <FileInput
        icon="search"
        id="test"
        type=".exp"
        visible={true}
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render selected file name", () => {
    const wrapper: ReactWrapper = mount(
      <FileInput
        icon="search"
        id="test"
        type=".exp"
        visible={true}
      />,
    );
    const input: ReactWrapper = wrapper.find("input");
    const fileName: ReactWrapper = wrapper.find("label")
                                          .find("span")
                                          .at(0);
    expect("")
      .toEqual(fileName.text());

    input.simulate("change", { target: { files: [ { name: "Test file name"} ] } });
    expect("Test file name")
      .toEqual(fileName.text());
  });
});
