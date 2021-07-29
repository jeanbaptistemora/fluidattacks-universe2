import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";
import { Provider } from "react-redux";

import { DeleteGroupModal } from "scenes/Dashboard/components/DeleteGroupModal";
import store from "store";

const functionMock: () => void = (): void => undefined;

describe("Delete Group Modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof DeleteGroupModal).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <DeleteGroupModal
          groupName={"TEST"}
          isOpen={true}
          onClose={functionMock}
          onSubmit={functionMock}
        />
      </Provider>
    );

    expect(wrapper).toHaveLength(1);
  });
});
