import { shallow, ShallowWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { useColorScheme } from "react-native";

import { App } from "./app";

describe("App root", (): void => {
  afterEach((): void => {
    jest.clearAllMocks();
  });

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
    jest.mock("react-native/Libraries/Utilities/useColorScheme");

    (useColorScheme as jest.Mock)
      .mockReturnValueOnce("light")
      .mockReturnValueOnce("dark");

    const wrapper: ShallowWrapper = shallow(<App />);
    expect(wrapper)
      .toHaveLength(1);

    expect(wrapper
      .find("StatusBar")
      .prop("barStyle"))
      .toEqual("dark-content");

    act((): void => { wrapper.setProps({}); });
    expect(wrapper
      .find("StatusBar")
      .prop("barStyle"))
      .toEqual("light-content");
  });
});
