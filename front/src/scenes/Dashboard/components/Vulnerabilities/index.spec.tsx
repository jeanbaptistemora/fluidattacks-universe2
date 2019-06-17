import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { default as SimpleTable } from "../SimpleTable/index";
import { VulnerabilitiesView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Vulnerabilities view", () => {

  const wrapper: ShallowWrapper = shallow(
    <VulnerabilitiesView
      editMode={false}
      findingId="422286126"
      state="open"
      userRole="admin"
    />,
  );

  it("should return a function", () => {
    expect(typeof (VulnerabilitiesView)).to
      .equal("function");
  });

  it("should render input title", () => {
    expect(wrapper.contains(<label>search_findings.tab_description.inputs</label>)).to
      .equal(true);
  });

  it("should render input table", () => {
    const tables: ShallowWrapper = wrapper.find(SimpleTable);
    const inputTable: string = tables.at(0)
      .html();
    expect(inputTable).to
      .contain('<div id="inputsVulns">');
  });
});
