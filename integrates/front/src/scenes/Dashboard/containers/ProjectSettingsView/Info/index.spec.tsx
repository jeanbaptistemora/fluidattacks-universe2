
import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router";
import { GroupInformation } from "scenes/Dashboard/containers/ProjectSettingsView/Info";
import { GET_GROUP_DATA } from "scenes/Dashboard/containers/ProjectSettingsView/queries";
import store from "store";

describe("Environments", () => {
  const mocksInfo: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_GROUP_DATA,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          project: {
            hasDrills: true,
            hasForces: true,
            language: "EN",
            subscription: "TEST",
          },
        },
      },
    },
  ];

  it("should return a function group info", () => {
    expect(typeof (GroupInformation))
      .toEqual("function");
  });

  it("should show group info", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksInfo} addTypename={false}>
          <MemoryRouter
            initialEntries={["/orgs/okada/groups/TEST/scope"]}
          >
            <Route
              component={GroupInformation}
              path={"/orgs/:organizationName/groups/:projectName/scope"}
            />
          </MemoryRouter>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const firstRowInfo: ReactWrapper = wrapper
      .find("RowPureContent")
      .at(0);
    expect(firstRowInfo.text())
      .toEqual("LanguageEnglish");
  });
});
