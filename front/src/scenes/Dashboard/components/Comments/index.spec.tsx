import { shallow, ShallowWrapper } from "enzyme";
import React from "react";
import { Comments } from "./index";

const functionMock: (() => void) = (): void => undefined;

describe("Comments Box", () => {

  it("should return a function", () => {
    expect(typeof (Comments))
      .toEqual("function");
  });

  it("should render", () => {
    const wrapper: ShallowWrapper = shallow(
      <Comments
        id="comments-test"
        onLoad={functionMock}
        onPostComment={functionMock}
      />,
    );

    expect(wrapper.contains(<div id="comments-test" />))
      .toBeTruthy();
  });
});
