import React from "react";
import { expect } from "chai";
import { shallow } from "enzyme";
import RButton from "./index";
import "mocha";
import Enzyme from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { Button, Glyphicon } from "react-bootstrap";

Enzyme.configure({ adapter: new Adapter() });

describe('Generic modal', () => {
  it('should return a function', () => {
    expect(typeof(RButton)).to.equal('function');
  });

  it('should be rendered', () => {
    const wrapper = shallow(
      <RButton
        bstyle="btn-success"
        btitle="This is a text"
        bicon="replay"
        onClickButton={() => {}}
      />
    );
    expect(
      wrapper.find(
        <Button className=""
                onClick={() => {}}
                block={true}
                active={false}
                disabled={false}
                bsStyle="default"
                bsClass="btn">
              <Glyphicon glyph="replay" bsClass="glyphicon" />
                    This is a text
        </Button>
      )
    ).to.exist;
  });
});
