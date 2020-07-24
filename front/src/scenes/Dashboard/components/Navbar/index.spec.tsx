import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
import { BreadcrumbItem } from "react-bootstrap";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { RouteComponentProps } from "react-router";
import { Link, MemoryRouter } from "react-router-dom";
import store from "../../../../store";
import translate from "../../../../utils/translations/translate";
import { navbarComponent as NavbarComponent } from "./index";
import { GET_USER_ORGANIZATIONS } from "./queries";

describe("Navbar", () => {

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
        pathname: "/home",
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
        path: "/home",
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
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.contains(
      <BreadcrumbItem active={false}>
        <Link to="/home">
          <b>
            {translate.t("navbar.breadcrumbRoot")}
          </b>
        </Link>
      </BreadcrumbItem>,
    ))
      .toBeTruthy();
  });
});
