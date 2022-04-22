import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { EventEvidenceView } from "scenes/Dashboard/containers/EventEvidenceView";
import {
  DOWNLOAD_FILE_MUTATION,
  GET_EVENT_EVIDENCES,
} from "scenes/Dashboard/containers/EventEvidenceView/queries";
import { authzPermissionsContext } from "utils/authz/config";

describe("EventEvidenceView", (): void => {
  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof EventEvidenceView).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENT_EVIDENCES,
          variables: { eventId: "413372600" },
        },
        result: {
          data: {
            event: {
              eventStatus: "CREATED",
              evidence: "some_image.png",
              evidenceDate: "2020-10-17 00:00:00",
              evidenceFile: "",
              evidenceFileDate: "",
              id: "413372600",
            },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_event_evidence_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={EventEvidenceView}
              path={"/:groupName/events/:eventId/evidence"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("group.events.evidence.edit")
      ).toBeInTheDocument();
    });

    expect(screen.queryByText("group.events.evidence.edit")).not.toBeDisabled();
  });

  it("should render empty UI", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENT_EVIDENCES,
          variables: { eventId: "413372600" },
        },
        result: {
          data: {
            event: {
              eventStatus: "CREATED",
              evidence: "",
              evidenceDate: "",
              evidenceFile: "",
              evidenceFileDate: "",
              id: "413372600",
            },
          },
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventEvidenceView}
            path={"/:groupName/events/:eventId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("group.events.evidence.noData")
      ).toBeInTheDocument();
    });

    expect(screen.queryByText("File")).not.toBeInTheDocument();
  });

  it("should render image and file", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENT_EVIDENCES,
          variables: { eventId: "413372600" },
        },
        result: {
          data: {
            event: {
              eventStatus: "CREATED",
              evidence: "some_image.png",
              evidenceDate: "2020-10-17 00:00:00",
              evidenceFile: "some_file.pdf",
              evidenceFileDate: "2020-10-17 00:00:00",
              id: "413372600",
            },
          },
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventEvidenceView}
            path={"/:groupName/events/:eventId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("img")).toBeInTheDocument();
    });

    expect(screen.queryByText("File")).toBeInTheDocument();
  });

  it("should render image lightbox", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENT_EVIDENCES,
          variables: { eventId: "413372600" },
        },
        result: {
          data: {
            event: {
              eventStatus: "CREATED",
              evidence: "some_image.png",
              evidenceDate: "2021-02-17 00:00:00",
              evidenceFile: "",
              evidenceFileDate: "",
              id: "413372600",
            },
          },
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventEvidenceView}
            path={"/:groupName/events/:eventId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("img")).toHaveLength(1);
    });

    expect(screen.queryAllByRole("button", { hidden: true })).toHaveLength(0);

    userEvent.click(screen.getAllByRole("img")[0]);
    userEvent.hover(
      screen.getByRole("dialog", { hidden: true, name: "Lightbox" })
    );

    const ReactImageLightboxButtons: number = 5;
    await waitFor((): void => {
      expect(screen.queryAllByRole("button", { hidden: true })).toHaveLength(
        ReactImageLightboxButtons
      );
    });

    jest.clearAllMocks();
  });

  it("should disable edit when closed", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENT_EVIDENCES,
          variables: { eventId: "413372600" },
        },
        result: {
          data: {
            event: {
              eventStatus: "SOLVED",
              evidence: "",
              evidenceDate: "",
              evidenceFile: "",
              evidenceFileDate: "",
              id: "413372600",
            },
          },
        },
      },
    ];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_event_evidence_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={EventEvidenceView}
              path={"/:groupName/events/:eventId/evidence"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("group.events.evidence.edit")).toBeDisabled();
    });
  });

  it("should open file link", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENT_EVIDENCES,
          variables: { eventId: "413372600" },
        },
        result: {
          data: {
            event: {
              eventStatus: "CLOSED",
              evidence: "",
              evidenceDate: "",
              evidenceFile: "some_file.pdf",
              evidenceFileDate: "2020-10-17 00:00:00",
              id: "413372600",
            },
          },
        },
      },
      {
        request: {
          query: DOWNLOAD_FILE_MUTATION,
          variables: { eventId: "413372600", fileName: "some_file.pdf" },
        },
        result: {
          data: {
            downloadEventFile: {
              success: true,
              url: "https://localhost:9000/some_file.pdf",
            },
          },
        },
      },
    ];

    const onOpenLink: jest.Mock = jest
      .fn()
      .mockReturnValue({ opener: undefined });
    // eslint-disable-next-line fp/no-mutation -- Mutation needed for the test
    (
      window as typeof window & {
        open: (url: string) => { opener: undefined };
      }
    ).open = onOpenLink;
    const { container } = render(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventEvidenceView}
            path={"/:groupName/events/:eventId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(container.querySelectorAll(".fa-file")).toHaveLength(1);
    });
    userEvent.click(container.querySelectorAll(".fa-file")[0]);
    await waitFor((): void => {
      expect(onOpenLink).toHaveBeenCalledWith(
        "https://localhost:9000/some_file.pdf",
        undefined,
        "noopener,noreferrer,"
      );
    });
    jest.clearAllMocks();
  });
});
