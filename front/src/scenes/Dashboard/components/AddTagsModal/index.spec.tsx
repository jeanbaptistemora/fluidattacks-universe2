import { shallow, ShallowWrapper } from "enzyme";
import * as React from "react";
import { Provider } from "react-redux";
import { Action, createStore, Store } from "redux";
import { AddTagsModal } from "./index";

const functionMock: (() => void) = (): void => undefined;

describe("Add Tags modal", () => {

  const store: Store<{}, Action<{}>> = createStore(() => ({}));
  const wrapper: ShallowWrapper = shallow(
    <Provider store={store}>
      <AddTagsModal
        isOpen={true}
        onClose={functionMock}
        onSubmit={functionMock}
      />
    </Provider>,
  );

  it("should return a function", () => {
    expect(typeof (AddTagsModal))
      .toEqual("function");
  });

  it("should render", () => {
    expect(wrapper)
      .toHaveLength(1);
  });
});
