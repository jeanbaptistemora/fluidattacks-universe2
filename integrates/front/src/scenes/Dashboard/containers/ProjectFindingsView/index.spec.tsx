import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { Button } from "components/Button";
import { CustomToggleList } from "components/DataTableNext/customToggleList";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import * as React from "react";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router-dom";
import wait from "waait";

import { DataTableNext } from "components/DataTableNext";
import { ITableProps } from "components/DataTableNext/types";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { ProjectFindingsView } from "scenes/Dashboard/containers/ProjectFindingsView";
import { GET_FINDINGS } from "scenes/Dashboard/containers/ProjectFindingsView/queries";
import { IProjectFindingsProps } from "scenes/Dashboard/containers/ProjectFindingsView/types";
import store from "store";

describe("ProjectFindingsView", () => {

  const propsMock: IProjectFindingsProps = {
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
      params: { projectName: "TEST" },
      path: "/",
      url: "",
    },
  };

  const apolloDataMock: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          project: {
            __typename: "Project",
            findings: [{
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
              title: "FIN.S.0038. Fuga de informaci\u00f3n de negocio",
              treatment: ["IN PROGRESS"],
              type: "SECURITY",
              verified: false,
              vulnerabilities: [{ __typename: "Vulnerability", where: "This is a test where" }],
            }],
          },
        },
      },
  }];

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", () => {
    expect(typeof (ProjectFindingsView))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/test/vulns"]}>
        <Provider store={store}>
          <MockedProvider mocks={apolloDataMock} addTypename={true}>
            <ProjectFindingsView {...propsMock} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render an error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/test/vulns"]}>
        <Provider store={store}>
          <MockedProvider mocks={mockError} addTypename={true}>
            <ProjectFindingsView {...propsMock} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should display all finding columns", async (): Promise<void> => {
    const mocksFindings: MockedResponse[] = [
      {
        request: {
          query: GET_FINDINGS,
          variables: {
            projectName: "TEST",
          },
        },
        result: {
          data: {
            project: {
              __typename: "Project",
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
                  title: "FIN.S.0038. Fuga de informaci\u00f3n de negocio",
                  treatment: ["IN PROGRESS"],
                  type: "SECURITY",
                  verified: false,
                  vulnerabilities: [
                    {
                      __typename: "Vulnerability",
                      historicTreatment: [],
                      where: "This is a test where",
                    },
                  ],
                },
              ],
            },
          },
        },
      },
    ];

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/groups/test/vulns"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocksFindings} addTypename={true}>
            <ProjectFindingsView {...propsMock} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      },
    );

    const customToggleListButton: ReactWrapper = wrapper
      .find(CustomToggleList)
      .find(Button);

    customToggleListButton.simulate("click");

    const columnFilterInputs: ReactWrapper = wrapper
      .find(CustomToggleList)
      .find("input");

    const ageCheckbox: ReactWrapper = columnFilterInputs.find({ name: "age" });
    const openAgeCheckbox: ReactWrapper = columnFilterInputs.find({
      name: "openAge",
    });
    const remediatedCheckbox: ReactWrapper = columnFilterInputs.find({
      name: "remediated",
    });
    const whereCheckbox: ReactWrapper = columnFilterInputs.find({
      name: "where",
    });

    ageCheckbox.simulate("change");
    openAgeCheckbox.simulate("change");
    remediatedCheckbox.simulate("change");
    whereCheckbox.simulate("change");

    const findingTable: ReactWrapper<ITableProps> = wrapper
      .find(DataTableNext)
      .filter({ id: "tblFindings" });

    const tableHeader: ReactWrapper = findingTable.find("Header");

    expect(tableHeader.text())
      .toContain("Age (days)");
    expect(tableHeader.text())
      .toContain("Open Age (days)");
    expect(tableHeader.text())
      .toContain("Last report (days)");
    expect(tableHeader.text())
      .toContain("Type");
    expect(tableHeader.text())
      .toContain("Description");
    expect(tableHeader.text())
      .toContain("Severity");
    expect(tableHeader.text())
      .toContain("Open");
    expect(tableHeader.text())
      .toContain("Status");
    expect(tableHeader.text())
      .toContain("Treatment");
    expect(tableHeader.text())
      .toContain("Verification");
    expect(tableHeader.text())
      .toContain("Exploitable");
    expect(tableHeader.text())
      .toContain("Where");

    const firstRow: ReactWrapper = findingTable.find("SimpleRow");

    expect(firstRow.text())
      .toContain("252");
    expect(firstRow.text())
      .toContain("99");
    expect(firstRow.text())
      .toContain("33");
    expect(firstRow.text())
      .toContain("FIN.S.0038. Fuga de informaci\u00f3n de negocio");
    expect(firstRow.text())
      .toContain("Test description");
    expect(firstRow.text())
      .toContain("2.9");
    expect(firstRow.text())
      .toContain("6");
    expect(firstRow.text())
      .toContain("Open");
    expect(firstRow.text())
      .toContain("New: 1In progress: 0Temporarily accepted: 0Eternally accepted: 0");
    expect(firstRow.text())
      .toContain("Pending");
    expect(firstRow.text())
      .toContain("Yes");
    expect(firstRow.text())
      .toContain("This is a test where");
  });
});
