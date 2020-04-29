import { shallow, ShallowWrapper } from "enzyme";
import React from "react";
import { NativeRouter } from "react-router-native";

import { LoginView } from "./index";

describe("LoginView", (): void => {
  it("should render", (): void => {

    const wrapper: ShallowWrapper = shallow(
      <NativeRouter initialEntries={["/"]}>
        <LoginView />
      </NativeRouter>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
