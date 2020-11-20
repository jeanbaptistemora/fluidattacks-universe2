import { GET_ROOTS } from "./query";
import { GroupScopeView } from ".";
import { I18nextProvider } from "react-i18next";
import { MockedProvider } from "@apollo/react-testing";
import type { MockedResponse } from "@apollo/react-testing";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { act } from "react-dom/test-utils";
import { cache } from "utils/apollo";
import { i18next } from "utils/translations/translate";
import { mount } from "enzyme";
import wait from "waait";
import { MemoryRouter, Route } from "react-router";

describe("GroupScopeView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupScopeView).toStrictEqual("function");
  });

  it("should render roots table", async (): Promise<void> => {
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
      <I18nextProvider i18n={i18next}>
        <MemoryRouter initialEntries={["/orgs/okada/groups/unittesting/scope"]}>
          <MockedProvider cache={cache} mocks={[queryMock]}>
            <Route
              component={GroupScopeView}
              path={"/orgs/:organizationName/groups/:projectName/scope"}
            />
          </MockedProvider>
        </MemoryRouter>
      </I18nextProvider>
    );

    await wait(0);
    act((): void => {
      wrapper.update();
    });

    const firstRowInfo: ReactWrapper = wrapper.find("RowPureContent").at(0);

    expect(firstRowInfo.text()).toStrictEqual(
      "https://gitlab.com/fluidattacks/product/master"
    );
  });
});
