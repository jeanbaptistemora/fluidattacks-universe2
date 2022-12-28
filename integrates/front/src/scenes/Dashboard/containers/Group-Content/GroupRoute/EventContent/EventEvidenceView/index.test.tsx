import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { EventEvidenceView } from "scenes/Dashboard/containers/Group-Content/GroupRoute/EventContent/EventEvidenceView";
import {
  DOWNLOAD_FILE_MUTATION,
  GET_EVENT_EVIDENCES,
  UPDATE_EVIDENCE_MUTATION,
} from "scenes/Dashboard/containers/Group-Content/GroupRoute/EventContent/EventEvidenceView/queries";
import { authzPermissionsContext } from "utils/authz/config";
import { msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../../../utils/notifications",
  (): Record<string, unknown> => {
    const mockedNotifications: Record<string, () => Record<string, unknown>> =
      jest.requireActual("../../../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

describe("eventEvidenceView", (): void => {
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
              evidences: {
                file1: null,
                image1: {
                  date: "2020-10-17 00:00:00",
                  fileName: "some_image.png",
                },
                image2: null,
                image3: null,
                image4: null,
                image5: null,
                image6: null,
              },
              id: "413372600",
            },
          },
        },
      },
    ];
    const mockedPermissions = new PureAbility<string>([
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

    jest.clearAllMocks();
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
              evidences: {
                file1: null,
                image1: null,
                image2: null,
                image3: null,
                image4: null,
                image5: null,
                image6: null,
              },
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

    jest.clearAllMocks();
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
              evidences: {
                file1: {
                  date: "2020-10-11 00:00:00",
                  fileName: "some_file.pdf",
                },
                image1: {
                  date: "2020-10-12 00:00:00",
                  fileName: "some_image.png",
                },
                image2: null,
                image3: null,
                image4: null,
                image5: null,
                image6: null,
              },
              id: "413372600",
            },
          },
        },
      },
    ];
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
      expect(screen.queryByRole("img")).toBeInTheDocument();
      expect(container.querySelectorAll(".fa-file")).toHaveLength(1);
    });
    jest.clearAllMocks();
  });

  it("should render image viewer", async (): Promise<void> => {
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
              evidences: {
                file1: null,
                image1: {
                  date: "2021-02-17 00:00:00",
                  fileName: "some_image.png",
                },
                image2: null,
                image3: null,
                image4: null,
                image5: null,
                image6: null,
              },
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

    expect(screen.queryAllByRole("span", { hidden: true })).toHaveLength(0);

    await userEvent.click(screen.getAllByRole("img")[0]);
    await userEvent.hover(
      screen.getByRole("dialog", {
        hidden: true,
        name: "ImageViewer",
      })
    );

    const ReactImageViewerButtons: number = 3;
    await waitFor((): void => {
      expect(screen.queryAllByRole("img", { hidden: true })).toHaveLength(
        ReactImageViewerButtons
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
              evidences: {
                file1: null,
                image1: null,
                image2: null,
                image3: null,
                image4: null,
                image5: null,
                image6: null,
              },
              id: "413372600",
            },
          },
        },
      },
    ];
    const mockedPermissions = new PureAbility<string>([
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
    jest.clearAllMocks();
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
              evidences: {
                file1: {
                  date: "020-10-17 00:00:00",
                  fileName: "some_file.pdf",
                },
                image1: {
                  date: "2020-10-12 00:00:00",
                  fileName: "some_image.png",
                },
                image2: null,
                image3: null,
                image4: null,
                image5: null,
                image6: null,
              },
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
    await userEvent.click(container.querySelectorAll(".fa-file")[0]);
    await waitFor((): void => {
      expect(onOpenLink).toHaveBeenCalledWith(
        "https://localhost:9000/some_file.pdf",
        undefined,
        "noopener,noreferrer,"
      );
    });
    jest.clearAllMocks();
  });

  it("should edit evidences", async (): Promise<void> => {
    expect.hasAssertions();

    const image1 = new File(
      ["okada-test-0123456789.png"],
      "okada-test-0123456789.png",
      { type: "image/png" }
    );
    const file = new File(
      ["okada-test-0987654321.txt"],
      "okada-test-0987654321.txt",
      {
        type: "text/plain",
      }
    );

    const mockedQueries: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENT_EVIDENCES,
          variables: { eventId: "413372600" },
        },
        result: {
          data: {
            event: {
              eventStatus: "CREATED",
              evidences: {
                file1: null,
                image1: null,
                image2: null,
                image3: null,
                image4: null,
                image5: null,
                image6: null,
              },
              id: "413372600",
            },
          },
        },
      },
    ];
    const mockedMutations: MockedResponse[] = [
      {
        request: {
          query: UPDATE_EVIDENCE_MUTATION,
          variables: {
            eventId: "413372600",
            evidenceType: "IMAGE_1",
            file: image1,
          },
        },
        result: {
          data: {
            updateEventEvidence: {
              success: true,
            },
          },
        },
      },
      {
        request: {
          query: UPDATE_EVIDENCE_MUTATION,
          variables: {
            eventId: "413372600",
            evidenceType: "FILE_1",
            file,
          },
        },
        result: {
          data: {
            updateEventEvidence: {
              success: true,
            },
          },
        },
      },
    ];

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_event_evidence_mutate" },
    ]);
    render(
      <MemoryRouter
        initialEntries={["orgs/okada/groups/test/events/413372600/evidence"]}
      >
        <MockedProvider
          addTypename={false}
          mocks={[...mockedQueries, ...mockedMutations]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={EventEvidenceView}
              path={
                "orgs/:organizationName/groups/:groupName/events/:eventId/evidence"
              }
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("group.events.evidence.edit")
      ).not.toBeDisabled();
    });
    await userEvent.click(screen.getByText("group.events.evidence.edit"));
    await waitFor((): void => {
      expect(
        screen.getByRole("button", {
          name: /searchfindings\.tabevidence\.update/iu,
        })
      ).toBeDisabled();
    });
    await userEvent.upload(screen.getByTestId("image1.file"), image1);
    await userEvent.upload(screen.getByTestId("file1.file"), file);
    await waitFor((): void => {
      expect(
        screen.getByRole("button", {
          name: /searchfindings\.tabevidence\.update/iu,
        })
      ).not.toBeDisabled();
    });
    await userEvent.click(
      screen.getByRole("button", {
        name: /searchfindings\.tabevidence\.update/iu,
      })
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.events.evidence.alerts.update.success",
        "groupAlerts.updatedTitle"
      );
    });
    jest.clearAllMocks();
  });
});
