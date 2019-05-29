import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { describe, it } from "mocha";
import * as React from "react";
import { Provider } from "react-redux";
import { Action, createStore, Store } from "redux";
import { reduxForm as ReduxForm } from "redux-form";
import { addResourcesModal as AddResourcesModal } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Add resources modal", () => {

  const store: Store<{}, Action<{}>> = createStore(() => ({}));
  const wrapper: ShallowWrapper = shallow(
    <Provider store={store}>
      <AddResourcesModal
        isOpen={true}
        type="file"
        onClose={functionMock}
        onSubmit={functionMock}
      />
    </Provider>,
  );

  it("should return a function", () => {
    expect(typeof (AddResourcesModal)).to
      .equal("function");
  });

  it("should render", () => {
    expect(wrapper).to
      .contain(ReduxForm);
  });
});
