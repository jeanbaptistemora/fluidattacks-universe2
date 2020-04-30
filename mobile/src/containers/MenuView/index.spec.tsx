// tslint:disable-next-line: no-submodule-imports
import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { I18nextProvider } from "react-i18next";
import { Provider as PaperProvider } from "react-native-paper";
import { NativeRouter } from "react-router-native";
import wait from "waait";

import { i18next } from "../../utils/translations/translate";

import { MenuView } from "./index";
import { PROJECTS_QUERY } from "./queries";

describe("MenuView", (): void => {
  it("should render", async (): Promise<void> => {

    const projectMock: Readonly<MockedResponse> = {
      request: {
        query: PROJECTS_QUERY,
      },
      result: {
        data: {
          me: {
            projects: [
              { name: "unittesting", description: "Integrates unit test project" },
            ],
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <PaperProvider>
        <I18nextProvider i18n={i18next}>
          <NativeRouter initialEntries={["/Menu"]}>
            <MockedProvider mocks={[projectMock]} addTypename={false}>
              <MenuView />
            </MockedProvider>
          </NativeRouter>
        </I18nextProvider>
      </PaperProvider>,
    );
    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);
  });
});
