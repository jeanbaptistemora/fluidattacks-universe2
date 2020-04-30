import { shallow, ShallowWrapper } from "enzyme";
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
});
