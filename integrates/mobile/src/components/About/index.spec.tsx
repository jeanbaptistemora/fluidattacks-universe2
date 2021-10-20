import { MaterialIcons } from "@expo/vector-icons";
import { mount } from "enzyme";
import type { ReactWrapper } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { Alert, Modal } from "react-native";
import wait from "waait";

import { About } from ".";

describe("About", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof About).toStrictEqual("function");
  });

  it("should display dialog", (): void => {
    expect.hasAssertions();

    jest.mock("react-native/Libraries/Alert/Alert");

    const wrapper: ReactWrapper = mount(<About />);

    expect(wrapper).toHaveLength(1);

    const aboutBtn: ReactWrapper<React.ComponentProps<typeof MaterialIcons>> =
      wrapper.find(MaterialIcons);

    (aboutBtn.invoke("onPress") as () => void)();

    expect(Alert.alert).toHaveBeenCalledTimes(1);

    jest.clearAllMocks();
  });

  it("should display dialog and licenses", async (): Promise<void> => {
    expect.hasAssertions();

    jest.mock("react-native/Libraries/Alert/Alert");

    const wrapper: ReactWrapper = mount(<About />);

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find(Modal).prop("visible")).toStrictEqual(false);

    const aboutBtn: ReactWrapper<React.ComponentProps<typeof MaterialIcons>> =
      wrapper.find(MaterialIcons);
    (aboutBtn.invoke("onPress") as () => void)();

    expect(Alert.alert).toHaveBeenCalledTimes(1);

    // eslint-disable-next-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
    (Alert.alert as jest.Mock).mock.calls[0][2][0].onPress();
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.find(Modal).prop("visible")).toStrictEqual(true);

    const onClose: ReactWrapper<React.ComponentProps<typeof Modal>> =
      wrapper.find(Modal);
    (onClose.invoke("onRequestClose") as () => void)();

    expect(wrapper.find(Modal).prop("visible")).toStrictEqual(false);

    jest.clearAllMocks();
  });
});
