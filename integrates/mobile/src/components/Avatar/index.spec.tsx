import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { mount } from "enzyme";
import type { ReactWrapper } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { I18nextProvider } from "react-i18next";
import { Alert, Modal, TouchableOpacity } from "react-native";
import {
  Avatar as PaperAvatar,
  Provider as PaperProvider,
} from "react-native-paper";
import { MemoryRouter } from "react-router-native";
import wait from "waait";

import { REMOVE_ACCOUNT_MUTATION } from "./queries";

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

  it("should render initials and successfully remove account", async (): Promise<void> => {
    expect.hasAssertions();

    jest.mock("react-native/Libraries/Alert/Alert");

    const removeAccountMock: Readonly<MockedResponse> = {
      request: {
        query: REMOVE_ACCOUNT_MUTATION,
      },
      result: {
        data: {
          removeStakeholder: {
            success: true,
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <MemoryRouter
            initialEntries={[
              { pathname: "/Dashboard", state: { user: { fullName: "Test" } } },
            ]}
          >
            <MockedProvider addTypename={false} mocks={[removeAccountMock]}>
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
    expect(wrapper.find(Modal).prop("visible")).toStrictEqual(false);

    const avatarTouchable: ReactWrapper<
      React.ComponentProps<typeof TouchableOpacity>
    > = wrapper.find(TouchableOpacity).first();
    (avatarTouchable.invoke("onPress") as () => void)();

    expect(wrapper.find(Modal).prop("visible")).toStrictEqual(true);

    const deleteBtn: ReactWrapper<
      React.ComponentProps<typeof TouchableOpacity>
    > = wrapper.find(TouchableOpacity).last();
    (deleteBtn.invoke("onPress") as () => void)();

    expect(Alert.alert).toHaveBeenCalledTimes(1);

    await act(async (): Promise<void> => {
      // eslint-disable-next-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
      await (Alert.alert as jest.Mock).mock.calls[0][2][1].onPress();
      await wait(0);
      wrapper.update();
    });

    expect(wrapper).toHaveLength(1);
    expect(mockHistoryReplace).toHaveBeenCalledWith("/Login");

    jest.clearAllMocks();
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
