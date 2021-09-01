import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import { CustomToggleList } from "components/DataTableNext/customToggleList";
import type { ITableProps } from "components/DataTableNext/types";
import { GroupFindingsView } from "scenes/Dashboard/containers/GroupFindingsView";
import { GET_FINDINGS } from "scenes/Dashboard/containers/GroupFindingsView/queries";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";

describe("GroupFindingsView", (): void => {
  const apolloDataMock: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            findings: [
              {
                __typename: "Finding",
                age: 252,
                description: "This is a test description",
                id: "438679960",
                isExploitable: true,
                lastVulnerability: 33,
                openVulnerabilities: 6,
                remediated: false,
                severityScore: 2.9,
                state: "open",
                title: "038. Business information leak",
                treatment: ["IN PROGRESS"],
                type: "SECURITY",
                verified: false,
                vulnerabilities: [
                  {
                    __typename: "Vulnerability",
                    historicTreatment: [],
                    id: "547be2a2-03d4-47d8-9f66-9ca9512f8eb1",
                    where: "This is a test where",
                    zeroRisk: "",
                  },
                ],
              },
            ],
            name: "TEST",
          },
        },
      },
    },
  ];

  const mockError: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  const mocksFindings: MockedResponse[] = [
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            findings: [
              {
                __typename: "Finding",
                age: 252,
                description: "Test description",
                id: "438679960",
                isExploitable: true,
                lastVulnerability: 33,
                openAge: 99,
                openVulnerabilities: 6,
                remediated: false,
                severityScore: 2.9,
                state: "open",
                title: "038. Business information leak",
                treatment: ["IN PROGRESS"],
                type: "SECURITY",
                verified: false,
                vulnerabilities: [
                  {
                    __typename: "Vulnerability",
                    historicTreatment: [],
                    id: "a4185d47-65c3-44fc-b461-a15ee7a7e47f",
                    where: "This is a test where",
                    zeroRisk: "",
                  },
                ],
                where: "This is a test where",
              },
            ],
            name: "TEST",
          },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupFindingsView).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/vulns"]}>
        <Provider store={store}>
          <MockedProvider addTypename={true} mocks={apolloDataMock}>
            <Route
              component={GroupFindingsView}
              path={"/groups/:groupName/vulns"}
            />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);
  });

  it("should render a svg", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_resolvers_query_report__get_url_group_report" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/vulns"]}>
        <Provider store={store}>
          <MockedProvider addTypename={true} mocks={mocksFindings}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route
                component={GroupFindingsView}
                path={"/groups/:groupName/vulns"}
              />
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    const reportsModal: ReactWrapper = wrapper.find("Button#reports");

    // Open Modal
    reportsModal.simulate("click");

    // Find buttons
    const reportPdf: ReactWrapper = wrapper
      .find("Button#report-pdf")
      .find("svg")
      .prop("data-icon");

    const reportXls: ReactWrapper = wrapper
      .find("Button#report-excel")
      .find("svg")
      .prop("data-icon");

    const reportZip: ReactWrapper = wrapper
      .find("Button#report-zip")
      .find("svg")
      .prop("data-icon");

    expect(reportPdf).toStrictEqual("file-pdf");
    expect(reportXls).toStrictEqual("file-excel");
    expect(reportZip).toStrictEqual("file-archive");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/vulns"]}>
        <Provider store={store}>
          <MockedProvider addTypename={true} mocks={mockError}>
            <Route
              component={GroupFindingsView}
              path={"/groups/:groupName/vulns"}
            />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );
    await wait(0);

    expect(wrapper).toHaveLength(1);
  });

  it("should display all finding columns", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/TEST/vulns"]}>
        <Provider store={store}>
          <MockedProvider addTypename={true} mocks={mocksFindings}>
            <Route
              component={GroupFindingsView}
              path={"/groups/:groupName/vulns"}
            />
          </MockedProvider>
        </Provider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    const customToggleListButton: ReactWrapper = wrapper
      .find(CustomToggleList)
      .find(Button);

    customToggleListButton.simulate("click");

    const columnFilterInputs: ReactWrapper = wrapper
      .find(CustomToggleList)
      .find("input");

    const ageCheckbox: ReactWrapper = columnFilterInputs.find({ name: "age" });
    const remediatedCheckbox: ReactWrapper = columnFilterInputs.find({
      name: "remediated",
    });
    const whereCheckbox: ReactWrapper = columnFilterInputs.find({
      name: "where",
    });

    ageCheckbox.simulate("change");
    remediatedCheckbox.simulate("change");
    whereCheckbox.simulate("change");

    const findingTable: ReactWrapper<ITableProps> = wrapper
      .find(DataTableNext)
      .filter({ id: "tblFindings" });

    const tableHeader: ReactWrapper = findingTable.find("Header");

    expect(tableHeader.text()).toContain("Age");
    expect(tableHeader.text()).toContain("Type");
    expect(tableHeader.text()).toContain("Severity");
    expect(tableHeader.text()).toContain("Status");
    expect(tableHeader.text()).toContain("Reattack");
    expect(tableHeader.text()).toContain("Where");

    const firstRow: ReactWrapper = findingTable.find("Body").find("tr");

    expect(firstRow.text()).toContain("252");
    expect(firstRow.text()).toContain("038. Business information leak");
    expect(firstRow.text()).toContain("2.9");
    expect(firstRow.text()).toContain("Open");
    expect(firstRow.text()).toContain("Pending");
    expect(firstRow.text()).toContain("This is a test where");
  });
});
