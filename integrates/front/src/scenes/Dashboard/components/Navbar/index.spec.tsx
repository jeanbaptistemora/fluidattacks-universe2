import { GET_USER_ORGANIZATIONS } from "scenes/Dashboard/components/Navbar/queries";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import { MemoryRouter } from "react-router-dom";
import { MockedProvider } from "@apollo/react-testing";
import type { MockedResponse } from "@apollo/react-testing";
import { NavbarComponent } from "scenes/Dashboard/components/Navbar";
import { Provider } from "react-redux";
import { PureAbility } from "@casl/ability";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { SplitButton } from "./components/splitbutton";
import { act } from "react-dom/test-utils";
import { authContext } from "utils/auth";
import { authzPermissionsContext } from "utils/authz/config";
import { mount } from "enzyme";
import store from "store";
import waitForExpect from "wait-for-expect";

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
