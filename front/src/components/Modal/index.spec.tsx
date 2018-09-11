import React from "react";
import { expect } from "chai";
import { shallow } from "enzyme";
import { default as Modal } from "./index";
import "mocha";
import Enzyme from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { Button } from "react-bootstrap";

Enzyme.configure({ adapter: new Adapter() });

describe('Generic modal', () => {
  it('should return a function', () => {
    expect(typeof(Modal)).to.equal('function');
  });

  it('should be rendered', () => {
    const wrapper = shallow(
      <Modal
        open={true}
        onClose={(): void => { console.log("onClose triggered!") }}
        headerTitle="Unit test title"
        content={
          <p>Unit modal content</p>
        }
        footer={
          <Button>
            test btn
          </Button>
        }
      />
    );
    expect(
      wrapper.contains(
        <div>
          <div>
            <h3>
              Unit test title
            </h3>
          </div>
          <div>
            <p>
              Unit modal content
            </p>
          </div>
          <div>
            <Button>
              test btn
            </Button>
          </div>
        </div>
      )
    ).to.equal(true);
  });
});
