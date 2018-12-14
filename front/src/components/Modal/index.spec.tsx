import React from "react";
import { expect } from "chai";
import { shallow } from "enzyme";
import { default as Modal } from "./index";
import "mocha";
import Enzyme from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { Button, ModalHeader, ModalTitle, ModalBody, ModalFooter } from "react-bootstrap";

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
      wrapper.contains([
        <ModalHeader closeLabel="Close" closeButton={false} bsClass="modal-header">
          <ModalTitle componentClass="h4">
            Unit test title
          </ModalTitle>
        </ModalHeader>,
        <ModalBody componentClass="div">
          <p>
            Unit modal content
          </p>
        </ModalBody>,
        <ModalFooter componentClass="div">
          <Button active={false} block={false} disabled={false} bsStyle="default" bsClass="btn">
            test btn
          </Button>
        </ModalFooter>
      ])
    ).to.equal(true);
  });
});
