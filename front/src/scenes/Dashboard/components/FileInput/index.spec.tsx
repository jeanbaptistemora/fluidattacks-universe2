import React from "react";
import { expect } from "chai";
import { shallow } from "enzyme";
import { fileInputComponent as FileInput } from "./index";
import "mocha";
import Enzyme from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { FormGroup, FormControl, ControlLabel, Glyphicon } from "react-bootstrap";

Enzyme.configure({ adapter: new Adapter() });

describe('File input', () => {
  it('should return a function', () => {
    expect(typeof(FileInput)).to.equal('function');
  });

  it('should be rendered', () => {
    const wrapper = shallow(
      <FileInput
        icon="search"
        id="test"
        type=".py"
        visible={true}
        fileName=""
      />
    );
    expect(
      wrapper.find(
        <FormGroup controlId="test" className="" bsClass="form-group">
          <FormControl className="undefined undefined" type="file" accept=".py" name="test[]" componentClass="input" bsClass="form-control" />
          <ControlLabel srOnly={false} bsClass="control-label">
            <span />
            <strong>
              <Glyphicon glyph="search" bsClass="glyphicon" />
               Choose a file…
            </strong>
          </ControlLabel>
        </FormGroup>
      )
    ).to.exist;
  });
});
