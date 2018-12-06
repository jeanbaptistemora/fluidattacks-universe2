import { shallow, configure } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { expect } from "chai";
import { component as EvidenceView } from "./index";
import "mocha";
import React from "react";
import { Row } from "react-bootstrap";

configure({ adapter: new Adapter() });

describe('Evidence view', () => {

  it('should return a function', () => {
    expect(typeof (EvidenceView)).to.equal('function');
  });

  it('should render img', () => {
    const wrapper = shallow(
      <EvidenceView
        currentIndex={0}
        images={[
          {
            description: "Test evidence",
            url: "https://fluidattacks.com/test.png",
          }
        ]}
        isImageOpen={false}
      />
    );

    expect(wrapper.find('img').length).to.equal(1);
  });

  it('should render description', () => {
    const wrapper = shallow(
      <EvidenceView
        currentIndex={0}
        images={[
          {
            description: "Test evidence",
            url: "https://fluidattacks.com/test.png",
          }
        ]}
        isImageOpen={false}
      />
    );

    expect(wrapper.contains(
      <div className="panel-footer" style={{ backgroundColor: "#fff" }}>
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

  it('should render lightbox', () => {
    const wrapper = shallow(
      <EvidenceView
        currentIndex={0}
        images={[
          {
            description: "Test evidence",
            url: "https://fluidattacks.com/test.png",
          }
        ]}
        isImageOpen={true}
      />
    );

    expect(wrapper.find('ReactImageLightbox').length).to.equal(1);
  });
});
