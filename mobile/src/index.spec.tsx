import { shallow, ShallowWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Appearance, AppearanceProvider } from "react-native-appearance";

import { App } from "./app";

describe("App root", (): void => {
  it("should return a function", (): void => {
    expect(typeof (App))
      .toEqual("function");
  });

  it("should render", (): void => {
    const wrapper: ShallowWrapper = shallow(<App />);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should change color scheme", (): void => {
    const wrapper: ShallowWrapper = shallow(
      <AppearanceProvider>
        <App />
      </AppearanceProvider>,
    );
    expect(wrapper)
      .toHaveLength(1);

    Appearance.set({ colorScheme: "light" });
    act((): void => { wrapper.update(); });
    expect(wrapper
      .find("App")
      .dive()
      .find("StatusBar")
      .prop("barStyle"))
      .toEqual("dark-content");

    Appearance.set({ colorScheme: "dark" });
    act((): void => { wrapper.update(); });
    expect(wrapper
      .find("App")
      .dive()
      .find("StatusBar")
      .prop("barStyle"))
      .toEqual("light-content");
  });
});
