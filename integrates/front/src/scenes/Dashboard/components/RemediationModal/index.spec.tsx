import { Provider } from "react-redux";
import React from "react";
import { RemediationModal } from "scenes/Dashboard/components/RemediationModal";
import type { ShallowWrapper } from "enzyme";
import { createStore } from "redux";
import { shallow } from "enzyme";
import type { Action, Store } from "redux";

const functionMock: () => void = (): void => undefined;

describe("Remediation modal", (): void => {
  const store: Store<
    Record<string, unknown>,
    Action<Record<string, unknown>>
  > = createStore((): Record<string, unknown> => ({}));
  const wrapper: ShallowWrapper = shallow(
    <Provider store={store}>
      <RemediationModal
        isLoading={false}
        isOpen={true}
        message={"test"}
        onClose={functionMock}
        onSubmit={functionMock}
        title={"title"}
      />
    </Provider>
  );

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof RemediationModal).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();
    expect(wrapper).toHaveLength(1);
  });
});
