import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { CommentsView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Finding comments view", () => {

  it("should return a function", () => {
    expect(typeof (CommentsView))
      .toEqual("function");
  });

  it("should render a comment view", () => {
    const wrapper: ShallowWrapper = shallow(
      <CommentsView
        findingId="435326633"
        type="comment"
      />,
    );
    expect(wrapper.html())
      .toEqual('<div id="finding-comments"></div>');
  });

  it("should render an observation view", () => {
    const wrapper: ShallowWrapper = shallow(
      <CommentsView
        findingId="435326633"
        type="observation"
      />,
    );
    expect(wrapper.html())
      .toEqual('<div id="finding-observations"></div>');
  });
});
