import { mount, shallow } from "enzyme";
import type { ShallowWrapper } from "enzyme";
import { isRootedExperimentalAsync } from "expo-device";
import React from "react";
import { act } from "react-dom/test-utils";
import { Alert, useColorScheme } from "react-native";
import wait from "waait";

import { App } from "./app";

jest.mock(
  "expo-device",
  (): Record<string, jest.Mock> => ({
    ...jest.requireActual("expo-device"),
    isRootedExperimentalAsync: jest.fn(),
  })
);

describe("App root", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof App).toBe("function");
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

    expect(wrapper.find("StatusBar").prop("barStyle")).toBe("dark-content");

    act((): void => {
      wrapper.setProps({});
    });

    expect(wrapper.find("StatusBar").prop("barStyle")).toBe("light-content");

    jest.clearAllMocks();
  });

  it("should display root error", async (): Promise<void> => {
    expect.hasAssertions();

    (isRootedExperimentalAsync as jest.Mock).mockResolvedValue(true);

    jest.mock("react-native/Libraries/Alert/Alert");

    const wrapper = mount(<App />);

    expect(wrapper).toHaveLength(1);

    await wait(0);

    expect(Alert.alert).toHaveBeenCalledWith(
      "Insecure device",
      expect.anything(),
      expect.anything(),
      expect.anything()
    );

    jest.clearAllMocks();
  });
});
