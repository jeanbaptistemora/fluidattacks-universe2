import { MockedProvider } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import * as React from "react";
import { Provider } from "react-redux";
import { MemoryRouter, RouteComponentProps } from "react-router-dom";
import wait from "waait";
import store from "../../../../store/index";
import { ProjectContent } from "./index";

describe("ProjectContent", () => {

  const mockProps: RouteComponentProps<{ projectName: string }> = {
    history: {
      action: "PUSH",
      block: (): (() => void) => (): void => undefined,
      createHref: (): string => "",
      go: (): void => undefined,
      goBack: (): void => undefined,
      goForward: (): void => undefined,
      length: 1,
      listen: (): (() => void) => (): void => undefined,
      location: { hash: "", pathname: "/", search: "", state: {} },
      push: (): void => undefined,
      replace: (): void => undefined,
    },
    location: { hash: "", pathname: "/", search: "", state: {} },
    match: {
      isExact: true,
      params: {projectName: "TEST"},
      path: "/",
      url: "",
    },
  };

  it("should return a function", () => {
    expect(typeof (ProjectContent))
      .toEqual("function");
  });

  it("should render an error in component", async () => {
    (window as typeof window & { userEmail: string }).userEmail = "test@test.com";
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/indicators"]}>
        <Provider store={store}>
          <MockedProvider mocks={[]} addTypename={false}>
            <ProjectContent {...mockProps} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a component", async () => {
    (window as typeof window & { userEmail: string }).userEmail = "test@test.com";
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/indicators"]}>
        <Provider store={store}>
          <MockedProvider mocks={[]} addTypename={false}>
            <ProjectContent {...mockProps} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });
});
