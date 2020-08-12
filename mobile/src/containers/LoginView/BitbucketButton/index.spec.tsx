import { mount, ReactWrapper } from "enzyme";
import React from "react";
import { I18nextProvider } from "react-i18next";
import { TouchableOpacity, TouchableOpacityProps } from "react-native";

import { i18next } from "../../../utils/translations/translate";

import { BitbucketButton, IBitbucketButtonProps } from "./index";

describe("BitbucketButton", (): void => {

  it("should return a function", (): void => {
    expect(typeof (BitbucketButton))
      .toEqual("function");
  });

  it("should render", (): void => {
    const wrapper: ReactWrapper = mount(
      <I18nextProvider i18n={i18next}>
        <BitbucketButton onPress={jest.fn()} disabled={true} />
      </I18nextProvider>,
    );

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper
      .text())
      .toContain("Bitbucket");
  });

  it("should execute callbacks", (): void => {
    const performAuth: jest.Mock = jest.fn();
    const wrapper: ReactWrapper<IBitbucketButtonProps> = mount(
      <I18nextProvider i18n={i18next}>
        <BitbucketButton onPress={performAuth} disabled={false} />
      </I18nextProvider>,
    );

    expect(wrapper)
      .toHaveLength(1);
    const button: ReactWrapper<TouchableOpacityProps> = wrapper.find(TouchableOpacity);
    (button.invoke("onPress") as () => void)();

    expect(performAuth)
      .toHaveBeenCalled();
  });
});
