import { mount, ReactWrapper } from "enzyme";
import React from "react";
import { I18nextProvider } from "react-i18next";
import { Provider as PaperProvider } from "react-native-paper";
import { NativeRouter } from "react-router-native";

import { i18next } from "../../utils/translations/translate";

import { LoginView } from "./index";

describe("LoginView", (): void => {

  it("should return a function", (): void => {
    expect(typeof (LoginView))
      .toEqual("function");
  });

  it("should render", (): void => {

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/"]}>
            <LoginView />
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>,
    );

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.find("Image")
      .length)
      .toBeGreaterThan(0);
    expect(wrapper.find("Button"))
      .toHaveLength(1);
  });
});
