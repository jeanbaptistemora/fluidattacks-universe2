import { mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import React from "react";
import { I18nextProvider } from "react-i18next";
import { Drawer } from "react-native-paper";

import { i18next } from "../../../utils/translations/translate";

import { Sidebar } from "./index";

const mockHistoryReplace: jest.Mock = jest.fn();

jest.mock("react-router-native", (): Dictionary => ({
  useHistory: (): Dictionary => ({
    replace: mockHistoryReplace,
  }),
}));

describe("MenuView", (): void => {
  it("should return a function", (): void => {
    expect(typeof (Sidebar))
      .toEqual("function");
  });

  it("should render", (): void => {
    const wrapper: ShallowWrapper = shallow(
      <I18nextProvider i18n={i18next}>
        <Sidebar />
      </I18nextProvider>,
    );

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper
      .dive()
      .dive()
      .find("Image"))
      .toHaveLength(1);
  });

  it("should perform logout", async (): Promise<void> => {
    const wrapper: ReactWrapper = mount(
      <I18nextProvider i18n={i18next}>
        <Sidebar />
      </I18nextProvider>,
    );

    expect(wrapper)
      .toHaveLength(1);

    const logoutBtn: ReactWrapper<React.ComponentProps<typeof Drawer.Item>> = wrapper
      .find({ label: "Logout" })
      .at(0);

    expect(logoutBtn)
      .toHaveLength(1);

    await (logoutBtn.invoke("onPress") as () => Promise<void>)();
    expect(mockHistoryReplace)
      .toHaveBeenCalled();
  });
});
