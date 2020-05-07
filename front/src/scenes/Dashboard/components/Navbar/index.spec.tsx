import { mount, ReactWrapper } from "enzyme";
import React from "react";
import { BreadcrumbItem } from "react-bootstrap";
import { Provider } from "react-redux";
import { RouteComponentProps } from "react-router";
import { Link, MemoryRouter } from "react-router-dom";
import store from "../../../../store";
import translate from "../../../../utils/translations/translate";
import { navbarComponent as NavbarComponent } from "./index";

describe("Navbar", () => {

  it("should return a function", () => {
    expect(typeof (NavbarComponent))
      .toEqual("function");
  });

  it("should render", () => {
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
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/home"]}>
        <Provider store={store}><NavbarComponent {...mockProps}/></Provider>
      </MemoryRouter>,
    );
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
