import { MaterialIcons } from "@expo/vector-icons";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { Alert } from "react-native";

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

    const aboutBtn: ReactWrapper<
      React.ComponentProps<typeof MaterialIcons>
    > = wrapper.find(MaterialIcons);

    (aboutBtn.invoke("onPress") as () => void)();

    // eslint-disable-next-line jest/prefer-called-with
    expect(Alert.alert).toHaveBeenCalled();
  });
});
