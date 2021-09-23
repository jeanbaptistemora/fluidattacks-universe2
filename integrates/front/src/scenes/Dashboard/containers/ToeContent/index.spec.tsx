import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { ToeContent } from ".";
import { GroupToeLinesView } from "../GroupToeLinesView";
import type { IContentTabProps } from "scenes/Dashboard/components/ContentTab";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { authzPermissionsContext } from "utils/authz/config";

describe("ToeContent", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ToeContent).toStrictEqual("function");
  });

  it("should display toe tabs", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_git_root_toe_lines_resolve" },
      { action: "api_resolvers_group_toe_inputs_resolve" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/unittesting/surface"]}>
        <MockedProvider addTypename={false} mocks={[]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route component={ToeContent} path={"/:groupName/surface"} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const toeLinesTab: ReactWrapper<IContentTabProps> = wrapper
      .find(ContentTab)
      .filter({ id: "toeLinesTab" });
    const toeInputsTab: ReactWrapper<IContentTabProps> = wrapper
      .find(ContentTab)
      .filter({ id: "toeInputsTab" });

    expect(toeLinesTab).toHaveLength(1);
    expect(toeInputsTab).toHaveLength(1);

    const groupToeLinesView: ReactWrapper = wrapper.find(GroupToeLinesView);

    expect(groupToeLinesView).toHaveLength(1);
  });
});
