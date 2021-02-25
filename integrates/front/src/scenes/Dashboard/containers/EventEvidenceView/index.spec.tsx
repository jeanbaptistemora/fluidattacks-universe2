import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import _ from "lodash";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter, Route } from "react-router";
import wait from "waait";

import { EventEvidenceView } from "scenes/Dashboard/containers/EventEvidenceView";
import {
  DOWNLOAD_FILE_MUTATION,
  GET_EVENT_EVIDENCES,
} from "scenes/Dashboard/containers/EventEvidenceView/queries";
import store from "store";
import { EvidenceDescription } from "styles/styledComponents";
import { authzPermissionsContext } from "utils/authz/config";

describe("EventEvidenceView", () => {
  it("should return a fuction", () => {
    expect(typeof (EventEvidenceView))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [{
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
    }];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <Route path={"/:projectName/events/:eventId/evidence"} component={EventEvidenceView}/>
        </MockedProvider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); });
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render empty UI", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [{
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
    }];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <Provider store={store}>
            <Route path={"/:projectName/events/:eventId/evidence"} component={EventEvidenceView}/>
          </Provider>
        </MockedProvider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("There are no evidences");
  });

  it("should render image and file", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [{
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
    }];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <Provider store={store}>
            <Route path={"/:projectName/events/:eventId/evidence"} component={EventEvidenceView}/>
          </Provider>
        </MockedProvider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.containsMatchingElement(<img />))
      .toBe(true);
    expect(wrapper.containsMatchingElement(<EvidenceDescription>File</EvidenceDescription>))
      .toBe(true);
  });

  it("should render image lightbox", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [{
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
    }];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <Provider store={store}>
            <Route path={"/:projectName/events/:eventId/evidence"} component={EventEvidenceView}/>
          </Provider>
        </MockedProvider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    wrapper.find("img")
      .simulate("click");
    await act(async () => { wrapper.update(); });
    expect(wrapper.find("ReactImageLightbox"))
      .toHaveLength(1);
  });

  it("should disable edit when closed", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [{
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
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_update_event_evidence_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <Provider store={store}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route path={"/:projectName/events/:eventId/evidence"} component={EventEvidenceView} />
            </authzPermissionsContext.Provider>
          </Provider>
        </MockedProvider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper
      .find("Button")
      .filterWhere((button: ReactWrapper): boolean => _.includes(button.text(), "Edit"))
      .prop("disabled"))
      .toEqual(true);
  });

  it("should open file link", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [
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
              url: "https://cloudfront/some_file.pdf",
            },
          },
        },
      },
    ];

    const onOpenLink: jest.Mock = jest.fn()
      .mockReturnValue({ opener: undefined });
    (window as { open: ((url: string) => { opener: undefined }) }).open = onOpenLink;
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/TEST/events/413372600/evidence"]}>
        <MockedProvider mocks={mocks} addTypename={false}>
          <Provider store={store}>
            <Route path={"/:projectName/events/:eventId/evidence"} component={EventEvidenceView}/>
          </Provider>
        </MockedProvider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    wrapper.find("svg")
      .find(".fa-file")
      .simulate("click");
    await act(async () => { await wait(0); });
    expect(onOpenLink)
      .toHaveBeenCalledWith("https://cloudfront/some_file.pdf", undefined, "noopener,noreferrer,");
  });
});
