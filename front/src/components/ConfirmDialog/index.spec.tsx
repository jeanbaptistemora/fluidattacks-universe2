import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { describe, it } from "mocha";
import * as React from "react";
import { confirmDialog as ConfirmDialog } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Confirm dialog", () => {

  it("should return a function", () => {
    expect(typeof (ConfirmDialog)).to
      .equal("function");
  });

  it("should render", () => {
    const wrapper: ShallowWrapper = shallow(
      <ConfirmDialog
        open={true}
        title="Test"
        onProceed={functionMock}
      />,
    );
    expect(wrapper).to.have
      .length(1);
  });
});
