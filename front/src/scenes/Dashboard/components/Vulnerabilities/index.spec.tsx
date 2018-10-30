import { configure, shallow } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { expect } from "chai";
import { vulnsViewComponent as VulnerabilitiesView } from "./index";
import "mocha";
import * as React from "react";
import {default as SimpleTable} from '../SimpleTable/index';

configure({ adapter: new Adapter() });

describe('Vulnerabilities view', () => {

  const wrapper = shallow(
    <VulnerabilitiesView
      editMode={false}
      dataInputs={[{currentState: "open",
        specific: "phone",
        vulnType: "inputs",
        where: "https://example.com"}]}
      dataLines={[]}
      dataPorts={[]}
      findingId="422286126"
      translations={{
        "search_findings.tab_description.inputs": "Inputs",
        "search_findings.tab_description.field": "Field",
      }}
    />
  );

  it('should return a function', () => {
    expect(typeof(VulnerabilitiesView)).to.equal('function');
  });

  it('should render input title', () => {
    expect(wrapper.contains(<label>Inputs</label>)).to.equal(true);
  });

  it('should render input table', () => {
    let tables = wrapper.find(SimpleTable);
    let inputTable = tables.at(0).html();
    expect(inputTable).to.contain('<div id="inputsVulns">');
  });
});
