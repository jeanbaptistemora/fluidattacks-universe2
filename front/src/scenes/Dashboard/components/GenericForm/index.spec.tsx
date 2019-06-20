import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { Provider } from "react-redux";
import { Action, createStore, Store } from "redux";
import { GenericForm } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("GenericForm", () => {

  const store: Store<{}, Action<{}>> = createStore(() => ({}));
  const wrapper: ShallowWrapper = shallow(
    <Provider store={store}>
      <GenericForm
        name="test"
        onSubmit={functionMock}
      >
        <div />
      </GenericForm>
    </Provider>,
  );

  it("should return a function", () => {
    expect(typeof (GenericForm))
      .toEqual("function");
  });

  it("should render", () => {
    expect(wrapper)
      .toHaveLength(1);
  });
});
