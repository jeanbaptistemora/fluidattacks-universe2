import { shallow, configure } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { expect } from "chai";
import { evidenceImage as EvidenceImage } from "./index";
import "mocha";
import React from "react";
import { Row } from "react-bootstrap";

configure({ adapter: new Adapter() });

describe('Evidence image', () => {

  it('should return a function', () => {
    expect(typeof (EvidenceImage)).to.equal('function');
  });

  it('should render img', () => {
    const wrapper = shallow(
      <EvidenceImage
        name={"evidence1"}
        description={"Test evidence"}
        isDescriptionEditable={false}
        isEditing={false}
        url={"https://fluidattacks.com/test.png"}
        onClick={(): void => undefined}
        onUpdate={(): void => undefined}
      />
    );

    expect(wrapper.find('img').length).to.equal(1);
  });

  it('should render description', () => {
    const wrapper = shallow(
      <EvidenceImage
        name={"evidence1"}
        description={"Test evidence"}
        isDescriptionEditable={false}
        isEditing={false}
        url={"https://fluidattacks.com/test.png"}
        onClick={(): void => undefined}
        onUpdate={(): void => undefined}
      />
    );

    expect(wrapper.contains(
      <div>
        <Row componentClass="div">
          <label>
            <b>search_findings.tab_evidence.detail</b>
          </label>
        </Row>
        <Row componentClass="div">
          <p>Test evidence</p>
        </Row>
      </div>
    )).to.equal(true);
  });
});
