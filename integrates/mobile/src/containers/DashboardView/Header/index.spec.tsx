import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { I18nextProvider } from "react-i18next";
import type { Text } from "react-native-paper";

import { Header } from ".";
import { i18next } from "../../../utils/translations/translate";

describe("Header", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof Header).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <I18nextProvider i18n={i18next}>
        <Header
          onLogout={jest.fn()}
          user={{
            email: "jdoe@mail.com",
            firstName: "John",
            fullName: "John Doe",
            photoUrl: "https://test.com/image.png",
          }}
        />
      </I18nextProvider>
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find("Image").length).toBeGreaterThan(1);
    expect(wrapper.text()).toContain("John Doe");
    expect(wrapper.text()).toContain("jdoe@mail.com");
  });

  it("should execute logout callback", (): void => {
    expect.hasAssertions();

    const logoutMock: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <I18nextProvider i18n={i18next}>
        <Header
          onLogout={logoutMock}
          user={{
            email: "jdoe@mail.com",
            firstName: "John",
            fullName: "John Doe",
            photoUrl: "https://test.com/image.png",
          }}
        />
      </I18nextProvider>
    );

    expect(wrapper).toHaveLength(1);

    const logoutBtn: ReactWrapper<
      React.ComponentProps<typeof Text>
    > = wrapper.find({ children: "Logout" }).at(0);

    expect(logoutBtn).toHaveLength(1);

    (logoutBtn.invoke("onPress") as () => void)();

    // eslint-disable-next-line jest/prefer-called-with
    expect(logoutMock).toHaveBeenCalled();
  });
});
