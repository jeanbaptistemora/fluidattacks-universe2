import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router-dom";
import waitForExpect from "wait-for-expect";

import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { navbarComponent as NavbarComponent } from "scenes/Dashboard/components/Navbar";
import { GET_USER_ORGANIZATIONS } from "scenes/Dashboard/components/Navbar/queries";
import store from "store";
import { authContext } from "utils/auth";
import { authzPermissionsContext } from "utils/authz/config";
import { SplitButton } from "./components/splitbutton";

describe("Navbar", () => {
  it("should return a function", () => {
    expect(typeof (NavbarComponent))
      .toEqual("function");
  });

  it("should render", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "front_can_use_groups_searchbar" },
    ]);
    const organizationsQuery: Readonly<MockedResponse> = {
      request: {
        query: GET_USER_ORGANIZATIONS,
      },
      result: {
        data: {
          me: {
            __typename: "Me",
            organizations: [
              {
                __typename: "Organization",
                name: "okada",
              },
            ],
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <Provider store={store}>
          <MockedProvider mocks={[organizationsQuery]} addTypename={true} >
            <authContext.Provider value={{ userEmail: "test@fluidattacks.com", userName: "" }}>
              <NavbarComponent />
            </authContext.Provider>
         </MockedProvider>
        </Provider>
      </MemoryRouter>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      },
    );

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(wrapper.find(SplitButton)
          .props().title)
          .toBe("okada");
        expect(wrapper.find(GenericForm)
          .props().name)
          .toBe("searchBar");
      });
    });
  });
});
