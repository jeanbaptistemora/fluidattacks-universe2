import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import { createStore } from "redux";
import type { Action, Store } from "redux";

import { GenericForm } from "scenes/Dashboard/components/GenericForm";

const functionMock: () => void = (): void => undefined;

describe("GenericForm", (): void => {
  const store: Store<
    unknown,
    Action<unknown>
  > = createStore((): unknown => ({}));
  const wrapper: ShallowWrapper = shallow(
    <Provider store={store}>
      <GenericForm name={"test"} onSubmit={functionMock}>
        <div />
      </GenericForm>
    </Provider>
  );

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GenericForm).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();
    expect(wrapper).toHaveLength(1);
  });
});
