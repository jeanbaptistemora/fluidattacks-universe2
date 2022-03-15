/* eslint-disable @typescript-eslint/no-magic-numbers */
import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { useTranslation } from "react-i18next";
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
import { translate } from "utils/translations/translate";

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
    expect(buttons[3].querySelector(".svg-inline--fa")).toHaveAttribute(
      "data-icon",
      "file-zipper"
    );

    userEvent.click(
      screen.getByText(translate.t("group.findings.report.btn.text"))
    );

    await waitFor((): void => {
      expect(
        screen.getByText(translate.t("group.findings.report.modalTitle"))
      ).toBeInTheDocument();
    });
    userEvent.click(screen.getByText("Executive"));
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        translate.t("groupAlerts.reportAlreadyRequested")
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

    const { t } = useTranslation();
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
    userEvent.click(
      screen.getByText(t("group.findings.tableSet.btn.text").toString())
    );

    userEvent.click(screen.getAllByRole("checkbox")[6]);
    userEvent.click(screen.getAllByRole("checkbox")[5]);

    const tableHeader: HTMLElement[] = screen.getAllByRole("columnheader");

    expect(tableHeader[1].textContent).toContain("Last report");
    expect(tableHeader[2].textContent).toContain("Type");
    expect(tableHeader[3].textContent).toContain("Status");
    expect(tableHeader[4].textContent).toContain("Severity");
    expect(tableHeader[5].textContent).toContain("Locations");
    expect(tableHeader[6].textContent).toContain("Where");
    expect(tableHeader[7].textContent).toContain("Reattack");

    const firstRow: HTMLElement[] = screen.getAllByRole("cell");

    expect(firstRow[1].textContent).toContain("33");
    expect(firstRow[2].textContent).toContain("038. Business information leak");
    expect(firstRow[3].textContent).toContain("Open");
    expect(firstRow[4].textContent).toContain("2.9");
    expect(firstRow[5].textContent).toContain("6");
    expect(firstRow[6].textContent).toContain("This is a test where");
    expect(firstRow[7].textContent).toContain("Pending");
  });
});
