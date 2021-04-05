import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import { createStore } from "redux";
import type { Action, Store } from "redux";

import { FileOptionsModal } from "scenes/Dashboard/components/FileOptionsModal";

const functionMock: () => void = (): void => undefined;

describe("Add resources modal", (): void => {
  const store: Store<
    unknown,
    Action<unknown>
  > = createStore((): unknown => ({}));
  const wrapper: ShallowWrapper = shallow(
    <Provider store={store}>
      <FileOptionsModal
        canRemove={true}
        fileName={""}
        isOpen={true}
        onClose={functionMock}
        onDelete={functionMock}
        onDownload={functionMock}
      />
    </Provider>
  );

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FileOptionsModal).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();
    expect(wrapper).toHaveLength(1);
  });
});
