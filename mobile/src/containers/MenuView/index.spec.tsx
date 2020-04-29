// tslint:disable-next-line: no-submodule-imports
import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { NativeRouter } from "react-router-native";
import wait from "waait";

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
      <NativeRouter initialEntries={["/Menu"]}>
        <MockedProvider mocks={[projectMock]} addTypename={false}>
          <MenuView />
        </MockedProvider>
      </NativeRouter>,
    );
    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);
  });
});
