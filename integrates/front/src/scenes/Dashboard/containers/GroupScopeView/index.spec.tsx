import { GET_ROOTS } from "./query";
import { GroupScopeView } from ".";
import { MockedProvider } from "@apollo/react-testing";
import type { MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { act } from "react-dom/test-utils";
import { authzGroupContext } from "utils/authz/config";
import { cache } from "utils/apollo";
import { mount } from "enzyme";
import wait from "waait";
import { MemoryRouter, Route } from "react-router";

describe("GroupScopeView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupScopeView).toStrictEqual("function");
  });

  it("should render git roots", async (): Promise<void> => {
    expect.hasAssertions();

    const queryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
        variables: { groupName: "unittesting" },
      },
      result: {
        data: {
          group: {
            __typename: "Project",
            roots: [
              {
                __typename: "GitRoot",
                branch: "master",
                directoryFiltering: {
                  __typename: "DirectoryFilteringConfig",
                  paths: ["^.*/bower_components/.*$", "^.*/node_modules/.*$"],
                  policy: "EXCLUDE",
                },
                environment: {
                  __typename: "IntegrationEnvironment",
                  kind: "production",
                  url: "https://integrates.fluidattacks.com",
                },
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                url: "https://gitlab.com/fluidattacks/product/",
              },
            ],
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <authzGroupContext.Provider
        value={new PureAbility([{ action: "has_drills_white" }])}
      >
        <MemoryRouter initialEntries={["/orgs/okada/groups/unittesting/scope"]}>
          <MockedProvider cache={cache} mocks={[queryMock]}>
            <Route
              component={GroupScopeView}
              path={"/orgs/:organizationName/groups/:projectName/scope"}
            />
          </MockedProvider>
        </MemoryRouter>
      </authzGroupContext.Provider>
    );

    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    const firstRowInfo: ReactWrapper = wrapper.find("RowPureContent").at(0);

    expect(firstRowInfo.text()).toStrictEqual(
      "https://gitlab.com/fluidattacks/product/master"
    );
  });
});
