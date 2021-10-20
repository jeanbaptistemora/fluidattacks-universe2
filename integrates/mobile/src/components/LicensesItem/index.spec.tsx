import { mount } from "enzyme";
import type { ReactWrapper } from "enzyme";
import React from "react";
import { Linking, TouchableOpacity } from "react-native";

import { LicensesItem } from ".";
import { Link } from "../Link";

describe("LicensesItem", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof LicensesItem).toStrictEqual("function");
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
      <LicensesItem
        licenseUrl={""}
        licenses={""}
        name={""}
        repository={""}
        version={""}
      />
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find(Link)).toHaveLength(1);

    const linkTouchable: ReactWrapper<
      React.ComponentProps<typeof TouchableOpacity>
    > = wrapper.find(TouchableOpacity).first();

    (linkTouchable.invoke("onPress") as () => void)();

    expect(Linking.openURL).toHaveBeenCalledTimes(1);
  });
});
