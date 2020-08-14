import { mount, ReactWrapper } from "enzyme";
import React from "react";
import { I18nextProvider } from "react-i18next";
import { Text } from "react-native-paper";

import { i18next } from "../../../utils/translations/translate";

import { Header } from "./index";

describe("Header", (): void => {

  it("should return a function", (): void => {
    expect(typeof (Header))
      .toEqual("function");
  });

  it("should render", (): void => {
    const wrapper: ReactWrapper = mount(
      <I18nextProvider i18n={i18next}>
        <Header
          user={{
            email: "jdoe@mail.com",
            firstName: "John",
            fullName: "John Doe",
            id: "0",
            photoUrl: "https://test.com/image.png",
          }}
          onLogout={jest.fn()}
        />
      </I18nextProvider>,
    );

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.find("Image").length)
      .toBeGreaterThan(1);
    expect(wrapper.text())
      .toContain("John Doe");
    expect(wrapper.text())
      .toContain("jdoe@mail.com");
  });

  it("should execute logout callback", (): void => {
    const logoutMock: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <I18nextProvider i18n={i18next}>
        <Header
          user={{
            email: "jdoe@mail.com",
            firstName: "John",
            fullName: "John Doe",
            id: "0",
            photoUrl: "https://test.com/image.png",
          }}
          onLogout={logoutMock}
        />
      </I18nextProvider>,
    );

    expect(wrapper)
      .toHaveLength(1);

    const logoutBtn: ReactWrapper<React.ComponentProps<typeof Text>> = wrapper
      .find({ children: "Logout" })
      .at(0);

    expect(logoutBtn)
      .toHaveLength(1);

    (logoutBtn.invoke("onPress") as () => void)();
    expect(logoutMock)
      .toHaveBeenCalled();
  });
});
