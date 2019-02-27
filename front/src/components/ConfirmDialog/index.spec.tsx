import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { describe, it } from "mocha";
import * as React from "react";
import { Provider } from "react-redux";
import store from "../../store/index";
import ConfirmDialog from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Confirm dialog", () => {

  it("should return a function", () => {
    expect(typeof (ConfirmDialog)).to
      .equal("function");
  });

  it("should render", () => {
    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
      <ConfirmDialog
        name="confirmTest"
        title="Test"
        onProceed={functionMock}
      />
      </Provider>,
    );
    expect(wrapper).to.have
      .length(1);
  });
});
