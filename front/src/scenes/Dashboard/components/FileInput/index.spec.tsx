import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { describe, it } from "mocha";
import React from "react";
import { ControlLabel, Glyphicon } from "react-bootstrap";
import { FileInput } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("File input", () => {
  it("should return a function", () => {
    expect(typeof (FileInput)).to
      .equal("function");
  });

  it("should be rendered", () => {
    const wrapper: ShallowWrapper = shallow(
      <FileInput
        icon="search"
        id="test"
        type=".py"
        visible={true}
      />,
    );
    expect(
      wrapper.contains(
        <ControlLabel srOnly={false} bsClass="control-label">
          <span>
            testFile
          </span>
          <strong>
            <Glyphicon glyph="search" bsClass="glyphicon" />
            &nbsp;Choose a file…
          </strong>
        </ControlLabel>,
      ),
    ).to
      .equal(true);
  });
});
