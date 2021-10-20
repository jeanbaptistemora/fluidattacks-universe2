import { mount } from "enzyme";
import type { ReactWrapper } from "enzyme";
import React from "react";
import { Linking, TouchableOpacity } from "react-native";

import { Link } from ".";

describe("Link", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof Link).toStrictEqual("function");
  });

  it("should display", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      /* eslint-disable-next-line react/forbid-component-props */
      <Link style={{}}>{""}</Link>
    );

    const linkTouchable: ReactWrapper<
      React.ComponentProps<typeof TouchableOpacity>
    > = wrapper.find(TouchableOpacity);

    (linkTouchable.invoke("onPress") as () => void)();

    expect(wrapper).toHaveLength(1);
  });

  it("should display and mock open_url", (): void => {
    expect.hasAssertions();

    interface IOpenURLMock {
      openURL: jest.Mock<Promise<string>, []>;
    }
    jest.mock(
      "react-native/Libraries/Linking/Linking",
      (): IOpenURLMock => ({
        openURL: jest.fn(
          async (): Promise<string> => Promise.resolve("mockResolve")
        ),
      })
    );

    const wrapper: ReactWrapper = mount(
      /* eslint-disable-next-line react/forbid-component-props */
      <Link style={{}} url={""}>
        {""}
      </Link>
    );

    expect(wrapper).toHaveLength(1);

    const linkTouchable: ReactWrapper<
      React.ComponentProps<typeof TouchableOpacity>
    > = wrapper.find(TouchableOpacity);

    (linkTouchable.invoke("onPress") as () => void)();

    expect(Linking.openURL).toHaveBeenCalledTimes(1);
  });
});
