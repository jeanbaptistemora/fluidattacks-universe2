import { mount, ReactWrapper } from "enzyme";
import React from "react";
import { Alert } from "react-native";
import { Text } from "react-native-paper";

import { About } from "./index";

describe("About", (): void => {

  it("should return a function", (): void => {
    expect(typeof (About))
      .toEqual("function");
  });

  it("should display dialog", (): void => {
    jest.mock("react-native/Libraries/Alert/Alert");

    const wrapper: ReactWrapper = mount(<About />);

    expect(wrapper)
      .toHaveLength(1);

    const aboutBtn: ReactWrapper<React.ComponentProps<typeof Text>> = wrapper
      .find(Text);

    (aboutBtn.invoke("onPress") as () => void)();
    expect(Alert.alert)
      .toHaveBeenCalled();
  });
});
