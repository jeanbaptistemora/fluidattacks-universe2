import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router-dom";
import waitForExpect from "wait-for-expect";

import { SplitButton } from "./components/splitbutton";

import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { NavbarComponent } from "scenes/Dashboard/components/Navbar";
import { GET_USER_ORGANIZATIONS } from "scenes/Dashboard/components/Navbar/queries";
import store from "store";
import { authContext } from "utils/auth";
import { authzPermissionsContext } from "utils/authz/config";

describe("Navbar", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof NavbarComponent).toStrictEqual("function");
  });

  it("should render", async (): Promise<void> => {
    expect.hasAssertions();

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
            userEmail: "test@fluidattacks.com",
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <Provider store={store}>
          <MockedProvider addTypename={true} mocks={[organizationsQuery]}>
            <authContext.Provider
              value={{ userEmail: "test@fluidattacks.com", userName: "" }}
            >
              <NavbarComponent />
            </authContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );

    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          expect(wrapper.find(SplitButton).props().title).toBe("okada");
          expect(wrapper.find(GenericForm).props().name).toBe("searchBar");
        });
      }
    );
  });
});
