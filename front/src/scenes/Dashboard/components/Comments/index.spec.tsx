import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { Comments } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

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
