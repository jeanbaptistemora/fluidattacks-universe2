import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import CommentsView from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Finding comments view", () => {

  it("should return a function", () => {
    expect(typeof (CommentsView)).to
      .equal("function");
  });

  it("should render", () => {
    const wrapper: ShallowWrapper = shallow(
      <CommentsView
        findingId="435326633"
        type="comment"
      />,
    );

    expect(wrapper.find('[id="finding-comments"]')).to.have
      .lengthOf(1);
  });
});
