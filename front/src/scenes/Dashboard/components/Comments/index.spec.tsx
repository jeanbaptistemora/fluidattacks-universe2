import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { describe, it } from "mocha";
import React from "react";
import { component as Comments } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Comments Box", () => {

  it("should return a function", () => {
    expect(typeof (Comments)).to
      .equal("function");
  });

  it("should render", () => {
    const wrapper: ShallowWrapper = shallow(
      <Comments
        id="comments-test"
        onLoad={functionMock}
        onPostComment={functionMock}
      />,
    );

    expect(wrapper.contains(<div id="comments-test" />)).to
      .equal(true);
  });
});
