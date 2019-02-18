import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { describe, it } from "mocha";
import React from "react";
import { projectCommentsView as CommentsView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Project comments view", () => {

  it("should return a function", () => {
    expect(typeof (CommentsView)).to
      .equal("function");
  });

  it("should render", () => {
    const wrapper: ShallowWrapper = shallow(
      <CommentsView
        projectName="unittesting"
      />,
    );

    expect(wrapper.find('[id="project-comments"]')).to.have
      .lengthOf(1);
  });
});
