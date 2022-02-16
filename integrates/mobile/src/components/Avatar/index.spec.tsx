import { MockedProvider } from "@apollo/client/testing";
import { mount } from "enzyme";
import type { ReactWrapper } from "enzyme";
import React from "react";
import { I18nextProvider } from "react-i18next";
import {
  Avatar as PaperAvatar,
  Provider as PaperProvider,
} from "react-native-paper";
import { MemoryRouter } from "react-router-native";

import { Avatar } from ".";
import { i18next } from "../../utils/translations/translate";

const mockHistoryReplace: jest.Mock = jest.fn();

jest.mock("react-router-native", (): Record<string, unknown> => {
  const mockedRouter: Record<string, () => Record<string, unknown>> =
    jest.requireActual("react-router-native");

  return {
    ...mockedRouter,
    useHistory: (): Record<string, unknown> => ({
      ...mockedRouter.useHistory(),
      replace: mockHistoryReplace,
    }),
  };
});

jest.mock("../../utils/socialAuth");

describe("Avatar", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof Avatar).toStrictEqual("function");
  });

  it("should render initials", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <MemoryRouter
            initialEntries={[
              { pathname: "/Dashboard", state: { user: { fullName: "Test" } } },
            ]}
          >
            <MockedProvider addTypename={false} mocks={[]}>
              <Avatar
                photoUrl={undefined}
                size={40}
                userName={
                  "Simón José Antonio de la Santísima Trinidad Bolívar y Palacios Ponte-Andrade y Blanco"
                }
              />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find(PaperAvatar.Text).text()).toStrictEqual("SJ");
  });

  it("should render profile picture", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <MemoryRouter
            initialEntries={[
              { pathname: "/Dashboard", state: { user: { fullName: "Test" } } },
            ]}
          >
            <MockedProvider addTypename={false} mocks={[]}>
              <Avatar
                photoUrl={"https://some.com/image.png"}
                size={40}
                userName={"Test"}
              />
            </MockedProvider>
          </MemoryRouter>
        </I18nextProvider>
      </PaperProvider>
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find(PaperAvatar.Image)).toHaveLength(1);
  });
});
