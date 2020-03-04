import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { Provider } from "react-redux";
import { Action, createStore, Store } from "redux";
import { RemediationModal } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Remediation modal", () => {

  const store: Store<{}, Action<{}>> = createStore(() => ({}));
  const wrapper: ShallowWrapper = shallow(
    <Provider store={store}>
      <RemediationModal
        isLoading={false}
        isOpen={true}
        message="test"
        onClose={functionMock}
        onSubmit={functionMock}
        title="title"
      />
    </Provider>,
  );

  it("should return a function", () => {
    expect(typeof (RemediationModal))
    .toEqual("function");
  });

  it("should render", () => {
    expect(wrapper)
      .toHaveLength(1);
  });
});
