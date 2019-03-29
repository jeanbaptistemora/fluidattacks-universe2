import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { describe, it } from "mocha";
import React from "react";
import ProjectCommentsView from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Project comments view", () => {

  it("should return a function", () => {
    expect(typeof (ProjectCommentsView)).to
      .equal("function");
  });

  it("should render", () => {
    const wrapper: ShallowWrapper = shallow(
      <ProjectCommentsView match={{ params: { projectName: "unittesting" }, isExact: false, path: "", url: "" }} />,
    );

    expect(wrapper.find('[id="project-comments"]')).to.have
      .lengthOf(1);
  });
});
