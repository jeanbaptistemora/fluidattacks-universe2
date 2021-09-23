import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { RecordsView } from "scenes/Dashboard/containers/RecordsView";
import { GET_FINDING_RECORDS } from "scenes/Dashboard/containers/RecordsView/queries";
import { authzPermissionsContext } from "utils/authz/config";

describe("FindingRecordsView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FINDING_RECORDS,
        variables: { findingId: "422286126" },
      },
      result: {
        data: {
          finding: {
            id: "422286126",
            records: JSON.stringify([
              {
                Character: "Cobra Commander",
                Genre: "action",
                Release: "2013",
                Title: "G.I. Joe: Retaliation",
              },
              {
                Character: "Tony Stark",
                Genre: "action",
                Release: "2008",
                Title: "Iron Man",
              },
            ]),
          },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof RecordsView).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/422286126/records"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={RecordsView}
            path={"/:groupName/vulns/:findingId/records"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const table: ReactWrapper = wrapper.find("BootstrapTable");

    expect(table).toHaveLength(1);
    expect(table.find("HeaderCell")).toHaveLength(4);
  });

  it("should render as editable", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_evidence_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/422286126/records"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={RecordsView}
              path={"/:groupName/vulns/:findingId/records"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const editButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Edit"))
      .at(0);

    expect(editButton).toHaveLength(1);

    editButton.simulate("click");

    expect(wrapper.contains("Update")).toBe(true);
  });

  it("should render as readonly", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/422286126/records"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={RecordsView}
            path={"/:groupName/vulns/:findingId/records"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.contains("Edit")).toBe(false);
  });

  it("should render delete button", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_evidence_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/422286126/records"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={RecordsView}
              path={"/:groupName/vulns/:findingId/records"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    const editButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Edit"))
      .at(0);

    expect(editButton).toHaveLength(1);

    editButton.simulate("click");

    expect(wrapper.contains("Delete")).toBe(true);
  });

  it("should render empty UI", async (): Promise<void> => {
    expect.hasAssertions();

    const emptyMocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_FINDING_RECORDS,
          variables: { findingId: "422286126" },
        },
        result: {
          data: {
            finding: {
              id: "422286126",
              records: "[]",
            },
          },
        },
      },
    ];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/vulns/422286126/records"]}>
        <MockedProvider addTypename={false} mocks={emptyMocks}>
          <Route
            component={RecordsView}
            path={"/:groupName/vulns/:findingId/records"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.text()).toContain("There are no records");
  });
});
