import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { confirmDialog as ConfirmDialog } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Confirm dialog", () => {

  it("should return a function", () => {
    expect(typeof (ConfirmDialog))
      .toEqual("function");
  });

  it("should render a component", () => {
    const handleProceed: jest.Mock = jest.fn();
    const handleClose: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <ConfirmDialog isOpen={true} name="confirmTest" onClose={handleClose} onProceed={handleProceed} title="Test" />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should call onProceed", () => {
    const handleProceed: jest.Mock = jest.fn();
    const handleClose: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <ConfirmDialog isOpen={true} name="confirmTest" onClose={handleClose} onProceed={handleProceed} title="Test" />,
    );
    const proceedButton: ShallowWrapper = wrapper
      .find("modal")
      .dive()
      .find("button")
      .filterWhere((element: ShallowWrapper) => element.contains("Proceed"));
    proceedButton.simulate("click");
    expect(handleProceed.mock.calls.length)
      .toEqual(1);
  });

  it("should close", () => {
    const handleProceed: jest.Mock = jest.fn();
    const handleClose: jest.Mock = jest.fn();
    const wrapper: ShallowWrapper = shallow(
      <ConfirmDialog isOpen={true} name="confirmTest" onClose={handleClose} onProceed={handleProceed} title="Test" />,
    );
    const cancelButton: ShallowWrapper = wrapper
      .find("modal")
      .dive()
      .find("button")
      .filterWhere((element: ShallowWrapper) => element.contains("Cancel"));
    if (cancelButton.length > 0) {
      cancelButton.simulate("click");
      expect(handleClose.mock.calls.length)
        .toEqual(1);
    }
  });
});
