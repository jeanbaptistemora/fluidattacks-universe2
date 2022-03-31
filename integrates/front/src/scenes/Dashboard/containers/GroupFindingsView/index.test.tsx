import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GroupFindingsView } from "scenes/Dashboard/containers/GroupFindingsView";
import {
  GET_FINDINGS,
  GET_GROUP_VULNS,
  GET_HAS_MOBILE_APP,
  REQUEST_GROUP_REPORT,
} from "scenes/Dashboard/containers/GroupFindingsView/queries";
import { ReportsModal } from "scenes/Dashboard/containers/GroupFindingsView/reportsModal";
import { msgError } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();

  return mockedNotifications;
});

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
                minTimeToRemediate: 60,
                openAge: 60,
                openVulnerabilities: 6,
                releaseDate: null,
                remediated: false,
                severityScore: 2.9,
                state: "open",
                title: "038. Business information leak",
                treatment: ["IN PROGRESS"],
                treatmentSummary: {
                  accepted: 0,
                  acceptedUndefined: 0,
                  inProgress: 0,
                  new: 1,
                },
                verified: false,
                vulnerabilities: [
                  {
                    where: "This is a test where",
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

  const mockMobile: MockedResponse = {
    request: {
      query: GET_HAS_MOBILE_APP,
    },
    result: {
      data: {
        me: {
          hasMobileApp: true,
          role: "",
          userEmail: "",
        },
      },
    },
  };

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
                minTimeToRemediate: 60,
                openAge: 60,
                openVulnerabilities: 6,
                releaseDate: null,
                remediated: false,
                severityScore: 2.9,
                state: "open",
                title: "038. Business information leak",
                treatment: ["IN PROGRESS"],
                treatmentSummary: {
                  accepted: 0,
                  acceptedUndefined: 0,
                  inProgress: 0,
                  new: 1,
                },
                verified: false,
              },
            ],
            name: "TEST",
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_VULNS,
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
                id: "438679960",
                vulnerabilities: [
                  {
                    __typename: "Vulnerability",
                    id: "",
                    where: "This is a test where",
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

  const mockReportError: MockedResponse = {
    request: {
      query: REQUEST_GROUP_REPORT,
      variables: {
        groupName: "testgroup",
        reportType: "PDF",
      },
    },
    result: {
      errors: [
        new GraphQLError(
          "Exception - The user already has a requested report for the same group"
        ),
      ],
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupFindingsView).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/TEST/vulns"]}>
        <MockedProvider addTypename={true} mocks={apolloDataMock}>
          <Route
            component={GroupFindingsView}
            path={"/groups/:groupName/vulns"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("table")).toHaveLength(1);
    });
  });

  it("should render report modal and mock request error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleClose: jest.Mock = jest.fn();
    render(
      <MemoryRouter initialEntries={["orgs/testorg/groups/testgroup/vulns"]}>
        <MockedProvider
          addTypename={true}
          mocks={[mockMobile, mockReportError]}
        >
          <Route path={"orgs/:organizationName/groups/:groupName/vulns"}>
            <ReportsModal
              hasMobileApp={true}
              isOpen={true}
              onClose={handleClose}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    // Find buttons
    const buttons: HTMLElement[] = screen.getAllByRole("button", {
      hidden: true,
    });

    expect(buttons[0].querySelector(".svg-inline--fa")).toHaveAttribute(
      "data-icon",
      "file-pdf"
    );
    expect(buttons[1].querySelector(".svg-inline--fa")).toHaveAttribute(
      "data-icon",
      "file-excel"
    );
    expect(buttons[2].querySelector(".svg-inline--fa")).toHaveAttribute(
      "data-icon",
      "sliders"
    );
    // eslint-disable-next-line @typescript-eslint/no-magic-numbers
    expect(buttons[3].querySelector(".svg-inline--fa")).toHaveAttribute(
      "data-icon",
      "file-zipper"
    );

    await waitFor((): void => {
      expect(
        screen.getByText("group.findings.report.modalTitle")
      ).toBeInTheDocument();
    });
    userEvent.click(screen.getByText("group.findings.report.pdf"));
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        "groupAlerts.reportAlreadyRequested"
      );
    });
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/TEST/vulns"]}>
        <MockedProvider addTypename={true} mocks={mockError}>
          <Route
            component={GroupFindingsView}
            path={"/groups/:groupName/vulns"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(1);
    });
  });

  it("should display all finding columns", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    render(
      <MemoryRouter initialEntries={["/groups/TEST/vulns"]}>
        <MockedProvider addTypename={true} mocks={mocksFindings}>
          <Route
            component={GroupFindingsView}
            path={"/groups/:groupName/vulns"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.getByText("038. Business information leak")
      ).toBeInTheDocument();
    });

    expect(screen.queryByText("Where")).not.toBeInTheDocument();
    expect(screen.queryByText("Reattack")).not.toBeInTheDocument();

    userEvent.click(screen.getByText("group.findings.tableSet.btn.text"));

    userEvent.click(
      screen.getByRole("checkbox", { checked: false, name: "where" })
    );
    userEvent.click(
      screen.getByRole("checkbox", { checked: false, name: "remediated" })
    );
    userEvent.type(
      screen.getByText("group.findings.tableSet.modalTitle"),
      "{esc}"
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("group.findings.tableSet.modalTitle")
      ).not.toBeInTheDocument();
    });

    expect(screen.getByText("Type")).toBeInTheDocument();
    expect(screen.getByText("Last report")).toBeInTheDocument();
    expect(screen.getByText("Status")).toBeInTheDocument();
    expect(screen.getByText("Severity")).toBeInTheDocument();
    expect(screen.getByText("Vulnerabilities")).toBeInTheDocument();
    expect(screen.getByText("Locations")).toBeInTheDocument();
    expect(screen.getByText("Reattack")).toBeInTheDocument();

    expect(
      screen.getByText("038. Business information leak")
    ).toBeInTheDocument();
    expect(
      screen.getByText("group.findings.description.value")
    ).toBeInTheDocument();
    expect(screen.getByText("Open")).toBeInTheDocument();
    expect(screen.getByText("2.9")).toBeInTheDocument();
    expect(screen.getByText("6")).toBeInTheDocument();
    expect(screen.getByText("This is a test where")).toBeInTheDocument();
    expect(screen.getByText("Pending")).toBeInTheDocument();
  });
});
