import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
import { SplitButton } from "react-bootstrap";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { RouteComponentProps } from "react-router";
import { MemoryRouter } from "react-router-dom";
import waitForExpect from "wait-for-expect";
import store from "../../../../store";
import { GenericForm } from "../GenericForm";
import { navbarComponent as NavbarComponent } from "./index";
import { GET_USER_ORGANIZATIONS } from "./queries";

describe("Navbar", () => {
  (window as typeof window & { userEmail: string }).userEmail = "test@fluidattacks.com";

  it("should return a function", () => {
    expect(typeof (NavbarComponent))
      .toEqual("function");
  });

  it("should render", async () => {
    const mockProps: RouteComponentProps = {
      history: {
        action: "PUSH",
        block: (): (() => void) => (): void => undefined,
        createHref: (): string => "",
        go: (): void => undefined,
        goBack: (): void => undefined,
        goForward: (): void => undefined,
        length: 1,
        listen: (): (() => void) => (): void => undefined,
        location: {
          hash: "",
          pathname: "/",
          search: "",
          state: {},
        },
        push: (): void => undefined,
        replace: (): void => undefined,
      },
      location: {
        hash: "",
        pathname: "/orgs/imamura",
        search: "",
        state: {
          userInfo: {
            givenName: "Test",
          },
        },
      },
      match: {
        isExact: true,
        params: {},
        path: "/orgs/imamura",
        url: "",
      },
    };

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
                name: "imamura",
              },
            ],
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/home"]}>
        <Provider store={store}>
          <MockedProvider mocks={[organizationsQuery]} addTypename={true} >
            <NavbarComponent {...mockProps}/>
         </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();

        expect(wrapper.find(SplitButton)
          .props().title)
          .toBe("imamura");
        expect(wrapper.find(GenericForm)
          .props().name)
          .toBe("searchBar");
      });
    });
  });
});
