import { App } from "./app";
import React from "react";
import type { ShallowWrapper } from "enzyme";
import { act } from "react-dom/test-utils";
import { shallow } from "enzyme";
import { useColorScheme } from "react-native";

describe("App root", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof App).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(<App />);

    expect(wrapper).toHaveLength(1);

    jest.clearAllMocks();
  });

  it("should change color scheme", (): void => {
    expect.hasAssertions();

    jest.mock("react-native/Libraries/Utilities/useColorScheme");

    (useColorScheme as jest.Mock)
      .mockReturnValueOnce("light")
      .mockReturnValueOnce("dark");

    const wrapper: ShallowWrapper = shallow(<App />);

    expect(wrapper).toHaveLength(1);

    expect(wrapper.find("StatusBar").prop("barStyle")).toStrictEqual(
      "dark-content"
    );

    act((): void => {
      wrapper.setProps({});
    });

    expect(wrapper.find("StatusBar").prop("barStyle")).toStrictEqual(
      "light-content"
    );

    jest.clearAllMocks();
  });
});
