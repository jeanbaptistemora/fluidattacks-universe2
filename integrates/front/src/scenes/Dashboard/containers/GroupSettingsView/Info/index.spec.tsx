import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { GroupInformation } from "scenes/Dashboard/containers/GroupSettingsView/Info";
import { GET_GROUP_DATA } from "scenes/Dashboard/containers/GroupSettingsView/queries";

describe("Info", (): void => {
  const mocksInfo: readonly MockedResponse[] = [
    {
      request: {
        query: GET_GROUP_DATA,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            hasMachine: true,
            hasSquad: true,
            language: "EN",
            name: "TEST",
            service: "WHITE",
            subscription: "TEST",
          },
        },
      },
    },
  ];

  it("should return a function group info", (): void => {
    expect.hasAssertions();
    expect(typeof GroupInformation).toStrictEqual("function");
  });

  it("should show group info", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={mocksInfo}>
        <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/scope"]}>
          <Route
            component={GroupInformation}
            path={"/orgs/:organizationName/groups/:groupName/scope"}
          />
        </MemoryRouter>
      </MockedProvider>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const firstRowInfo: ReactWrapper = wrapper.find("RowPureContent").at(0);

    expect(firstRowInfo.text()).toStrictEqual("LanguageEnglish");
  });
});
