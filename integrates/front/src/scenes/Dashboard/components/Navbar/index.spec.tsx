import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { Link, MemoryRouter } from "react-router-dom";
import waitForExpect from "wait-for-expect";

import { SplitButton } from "./Breadcrumb/SplitButton";

import { Navbar } from "scenes/Dashboard/components/Navbar";
import {
  GET_FINDING_TITLE,
  GET_USER_ORGANIZATIONS,
} from "scenes/Dashboard/components/Navbar/Breadcrumb/queries";
import { authContext } from "utils/auth";
import { authzPermissionsContext } from "utils/authz/config";

describe("Navbar", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Navbar).toStrictEqual("function");
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
        <MockedProvider addTypename={true} mocks={[organizationsQuery]}>
          <authContext.Provider
            value={{ userEmail: "test@fluidattacks.com", userName: "" }}
          >
            <Navbar userRole={"customer"} />
          </authContext.Provider>
        </MockedProvider>
      </MemoryRouter>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper.find(SplitButton).props().title).toBe("okada");
        expect(wrapper.find("Formik").props().name).toBe("searchBar");
      });
    });
  });

  it("should display draft title", async (): Promise<void> => {
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
    const findingTitleQuery: Readonly<MockedResponse> = {
      request: {
        query: GET_FINDING_TITLE,
        variables: {
          findingId: "F3F42d73-c1bf-47c5-954e-FFFFFFFFFFFF",
        },
      },
      result: {
        data: {
          finding: {
            title: "001. Test draft title",
          },
        },
      },
    };
    const wrapper: ReactWrapper = mount(
      <MemoryRouter
        initialEntries={[
          "/orgs/okada/groups/unittesting/drafts/F3F42d73-c1bf-47c5-954e-FFFFFFFFFFFF/locations",
        ]}
      >
        <MockedProvider
          addTypename={true}
          mocks={[findingTitleQuery, organizationsQuery]}
        >
          <authContext.Provider
            value={{ userEmail: "test@fluidattacks.com", userName: "" }}
          >
            <Navbar userRole={"customer"} />
          </authContext.Provider>
        </MockedProvider>
      </MemoryRouter>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(
          wrapper
            .find(Link)
            .filter({
              to: "/orgs/okada/groups/unittesting/drafts/F3F42d73-c1bf-47c5-954e-FFFFFFFFFFFF",
            })
            .text()
        ).toStrictEqual("001. Test draft title");
      });
    });
  });

  it("should display finding title", async (): Promise<void> => {
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
    const findingTitleQuery: Readonly<MockedResponse> = {
      request: {
        query: GET_FINDING_TITLE,
        variables: {
          findingId: "436992569",
        },
      },
      result: {
        data: {
          finding: {
            title: "001. Test finding title",
          },
        },
      },
    };
    const wrapper: ReactWrapper = mount(
      <MemoryRouter
        initialEntries={[
          "/orgs/okada/groups/unittesting/vulns/436992569/description",
        ]}
      >
        <MockedProvider
          addTypename={true}
          mocks={[findingTitleQuery, organizationsQuery]}
        >
          <authContext.Provider
            value={{ userEmail: "test@fluidattacks.com", userName: "" }}
          >
            <Navbar userRole={"customer"} />
          </authContext.Provider>
        </MockedProvider>
      </MemoryRouter>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );

    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(
          wrapper
            .find(Link)
            .filter({
              to: "/orgs/okada/groups/unittesting/vulns/436992569",
            })
            .text()
        ).toStrictEqual("001. Test finding title");
      });
    });
  });
});
