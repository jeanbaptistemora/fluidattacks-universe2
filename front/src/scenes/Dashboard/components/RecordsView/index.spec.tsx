import { shallow, configure } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { expect } from "chai";
import "mocha";
import React from "react";
import { component as RecordsView } from "./index";

configure({ adapter: new Adapter() });

describe('Records view', () => {

  it('should return a function', () => {
    expect(typeof(RecordsView)).to.equal('function');
  });

  it('should render', () => {
    const wrapper = shallow(
      <RecordsView
        canEdit={true}
        findingId="422286126"
        dataset={[]}
        isEditing={true}
        translations={{
          "search_findings.tab_evidence.update": "Update",
          "search_findings.tab_evidence.editable": "Edit",
        }}
        onUploadFile={() => undefined}
      />
    );

    expect(wrapper).to.have.length(1);
  });
});
