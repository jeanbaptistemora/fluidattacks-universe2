import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { Row } from "react-bootstrap";
import { evidenceImage as EvidenceImage } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Evidence image", () => {

  it("should return a function", () => {
    expect(typeof (EvidenceImage)).to
      .equal("function");
  });

  it("should render img", () => {
    const wrapper: ShallowWrapper = shallow(
      <EvidenceImage
        name={"evidence1"}
        description={"Test evidence"}
        isDescriptionEditable={false}
        isEditing={false}
        url={"https://fluidattacks.com/test.png"}
        onClick={functionMock}
        onUpdate={functionMock}
      />,
    );

    expect(wrapper.find("img").length).to
      .equal(1);
  });

  it("should render description", () => {
    const wrapper: ShallowWrapper = shallow(
      <EvidenceImage
        name={"evidence1"}
        description={"Test evidence"}
        isDescriptionEditable={false}
        isEditing={false}
        url={"https://fluidattacks.com/test.png"}
        onClick={functionMock}
        onUpdate={functionMock}
      />,
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
      </div>,
    )).to
      .equal(true);
  });
});
