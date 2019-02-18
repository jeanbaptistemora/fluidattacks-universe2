import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { describe, it } from "mocha";
import React from "react";
import { default as SimpleTable } from "../SimpleTable/index";
import { vulnsViewComponent as VulnerabilitiesView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Vulnerabilities view", () => {

  const wrapper: ShallowWrapper = shallow(
    <VulnerabilitiesView
      editMode={false}
      dataInputs={[{ currentState: "open", specific: "phone", vulnType: "inputs", where: "https://example.com" }]}
      dataLines={[]}
      dataPorts={[]}
      findingId="422286126"
      state="open"
      releaseDate=""
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
