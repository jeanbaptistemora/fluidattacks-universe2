// tslint:disable-next-line: no-submodule-imports
import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { RouteComponentProps } from "react-router-native";
import wait from "waait";

import { MenuView } from "./index";
import { PROJECTS_QUERY } from "./queries";

describe("MenuView", (): void => {
  it("should render", async (): Promise<void> => {

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
        pathname: "/Menu",
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
        path: "/Menu",
        url: "",
      },
    };

    const projectMock: Readonly<MockedResponse> = {
      request: {
        query: PROJECTS_QUERY,
      },
      result: {
        data: {
          me: {
            projects: [
              { name: "unittesting", description: "Integrates unit test project" },
            ],
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <MockedProvider mocks={[projectMock]} addTypename={false}>
        <MenuView {...mockProps} />
      </MockedProvider>,
    );
    await act(async (): Promise<void> => { await wait(0); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);
  });
});
