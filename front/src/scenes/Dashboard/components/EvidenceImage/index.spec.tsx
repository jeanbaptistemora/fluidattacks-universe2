import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { Row } from "react-bootstrap";
import { evidenceImage as EvidenceImage } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Evidence image", () => {

  it("should return a function", () => {
    expect(typeof (EvidenceImage))
      .toEqual("function");
  });

  it("should render img", () => {
    const wrapper: ShallowWrapper = shallow(
      <EvidenceImage
        name={"evidence1"}
        description={"Test evidence"}
        isDescriptionEditable={false}
        isEditing={false}
        content="https://fluidattacks.com/test.png"
        onClick={functionMock}
        onUpdate={functionMock}
      />,
    );

    expect(wrapper.find("img").length)
      .toEqual(1);
  });

  it("should render description", () => {
    const wrapper: ShallowWrapper = shallow(
      <EvidenceImage
        name={"evidence1"}
        description={"Test evidence"}
        isDescriptionEditable={false}
        isEditing={false}
        content={"https://fluidattacks.com/test.png"}
        onClick={functionMock}
        onUpdate={functionMock}
      />,
    );

    expect(wrapper.contains(
      <div className="description">
        <Row componentClass="div">
          <label>
            <b>
              Detail
            </b>
          </label>
        </Row>
        <Row componentClass="div">
          <p>
            Test evidence
          </p>
        </Row>
      </div>,
    ))
      .toBeTruthy();
  });
});
