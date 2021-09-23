import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import _ from "lodash";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";

import { EventEvidenceView } from "scenes/Dashboard/containers/EventEvidenceView";
import {
  DOWNLOAD_FILE_MUTATION,
  GET_EVENT_EVIDENCES,
} from "scenes/Dashboard/containers/EventEvidenceView/queries";
import { EvidenceDescription } from "styles/styledComponents";
import { authzPermissionsContext } from "utils/authz/config";

describe("EventEvidenceView", (): void => {
  it("should return a fuction", (): void => {
    expect.hasAssertions();
    expect(typeof EventEvidenceView).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENT_EVIDENCES,
          variables: { identifier: "413372600" },
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
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventEvidenceView}
            path={"/:groupName/events/:eventId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
    });

    expect(wrapper).toHaveLength(1);
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
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventEvidenceView}
            path={"/:groupName/events/:eventId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.text()).toContain("There are no evidences");
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
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventEvidenceView}
            path={"/:groupName/events/:eventId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.containsMatchingElement(<img alt={""} />)).toBe(true);
    expect(
      wrapper.containsMatchingElement(
        <EvidenceDescription>{"File"}</EvidenceDescription>
      )
    ).toBe(true);
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
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventEvidenceView}
            path={"/:groupName/events/:eventId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    wrapper.find("img").simulate("click");
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(wrapper.find("ReactImageLightbox")).toHaveLength(1);
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
    const wrapper: ReactWrapper = mount(
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
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });

    expect(
      wrapper
        .find("Button")
        .filterWhere((button: ReactWrapper): boolean =>
          _.includes(button.text(), "Edit")
        )
        .prop("disabled")
    ).toStrictEqual(true);
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
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route
            component={EventEvidenceView}
            path={"/:groupName/events/:eventId/evidence"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await act(async (): Promise<void> => {
      await wait(0);
      wrapper.update();
    });
    wrapper.find("svg").find(".fa-file").simulate("click");
    await act(async (): Promise<void> => {
      await wait(0);
    });

    expect(onOpenLink).toHaveBeenCalledWith(
      "https://localhost:9000/some_file.pdf",
      undefined,
      "noopener,noreferrer,"
    );
  });
});
