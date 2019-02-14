import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { describe, it } from "mocha";
import React from "react";
import { Button, ModalBody, ModalFooter, ModalHeader, ModalTitle } from "react-bootstrap";
import { default as Modal } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Generic modal", () => {
  it("should return a function", () => {
    expect(typeof (Modal)).to
      .equal("function");
  });

  it("should be rendered", () => {
    const wrapper: ShallowWrapper = shallow(
      <Modal
        open={true}
        onClose={functionMock}
        headerTitle="Unit test title"
        content={<p>Unit modal content</p>}
        footer={<Button>test btn</Button>}
      />,
    );
    expect(
      wrapper.contains([
        (
          <ModalHeader closeLabel="Close" closeButton={false} bsClass="modal-header">
            <ModalTitle componentClass="h4">
              Unit test title
          </ModalTitle>
          </ModalHeader>),
        (
          <ModalBody componentClass="div">
            <p>
              Unit modal content
          </p>
          </ModalBody>),
        (
          <ModalFooter componentClass="div">
            <Button active={false} block={false} disabled={false} bsStyle="default" bsClass="btn">
              test btn
          </Button>
          </ModalFooter>),
      ]),
    ).to
      .equal(true);
  });
});
