import { I18nextProvider } from "react-i18next";
import type { IMicrosoftButtonProps } from ".";
import { MicrosoftButton } from ".";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { TouchableOpacity } from "react-native";
import type { TouchableOpacityProps } from "react-native";
import { i18next } from "../../../utils/translations/translate";
import { mount } from "enzyme";

describe("MicrosoftButton", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof MicrosoftButton).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <I18nextProvider i18n={i18next}>
        <MicrosoftButton disabled={true} onPress={jest.fn()} />
      </I18nextProvider>
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.text()).toContain("Microsoft");
  });

  it("should execute callbacks", (): void => {
    expect.hasAssertions();

    const performAuth: jest.Mock = jest.fn();
    const wrapper: ReactWrapper<IMicrosoftButtonProps> = mount(
      <I18nextProvider i18n={i18next}>
        <MicrosoftButton disabled={false} onPress={performAuth} />
      </I18nextProvider>
    );

    expect(wrapper).toHaveLength(1);

    const button: ReactWrapper<TouchableOpacityProps> = wrapper.find(
      TouchableOpacity
    );
    (button.invoke("onPress") as () => void)();

    expect(performAuth).toHaveBeenCalledTimes(1);
  });
});
