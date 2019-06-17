import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { Provider } from "react-redux";
import { Action, createStore, Store } from "redux";
import { reduxForm as ReduxForm } from "redux-form";
import { remediationModal as RemediationModal } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Remediation modal", () => {

  const store: Store<{}, Action<{}>> = createStore(() => ({}));
  const wrapper: ShallowWrapper = shallow(
    <Provider store={store}>
      <RemediationModal
        isOpen={true}
        onClose={functionMock}
        onSubmit={functionMock}
      />
    </Provider>,
  );

  it("should return a function", () => {
    expect(typeof (RemediationModal)).to
      .equal("function");
  });

  it("should render", () => {
    expect(wrapper).to
      .contain(ReduxForm);
  });
});
