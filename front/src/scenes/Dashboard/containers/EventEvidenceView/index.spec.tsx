import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { configure, mount, ReactWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import _ from "lodash";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { RouteComponentProps } from "react-router";
import wait from "waait";
import { EventEvidenceView } from "./index";
import { DOWNLOAD_FILE_MUTATION, GET_EVENT_EVIDENCES } from "./queries";

configure({ adapter: new ReactSixteenAdapter() });
describe("EventEvidenceView", () => {

  const mockProps: RouteComponentProps<{ eventId: string }> = {
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
      params: { eventId: "413372600" },
      path: "/",
      url: "",
    },
  };

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
            evidenceFile: "",
            id: "413372600",
          },
        },
      },
    }];
    const wrapper: ReactWrapper = mount(
      <MockedProvider mocks={mocks} addTypename={false}>
        <EventEvidenceView {...mockProps} />
      </MockedProvider>,
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
            evidenceFile: "",
            id: "413372600",
          },
        },
      },
    }];
    const wrapper: ReactWrapper = mount(
      <MockedProvider mocks={mocks} addTypename={false}>
        <EventEvidenceView {...mockProps} />
      </MockedProvider>,
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
            evidenceFile: "some_file.pdf",
            id: "413372600",
          },
        },
      },
    }];
    const wrapper: ReactWrapper = mount(
      <MockedProvider mocks={mocks} addTypename={false}>
        <EventEvidenceView {...mockProps} />
      </MockedProvider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.containsMatchingElement(<img />))
      .toBe(true);
    expect(wrapper.containsMatchingElement(<p>File</p>))
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
            evidenceFile: "",
            id: "413372600",
          },
        },
      },
    }];
    const wrapper: ReactWrapper = mount(
      <MockedProvider mocks={mocks} addTypename={false}>
        <EventEvidenceView {...mockProps} />
      </MockedProvider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    wrapper.find("img")
      .simulate("click");
    await act(async () => { wrapper.update(); });
    expect(wrapper.find("ReactImageLightbox"))
      .toHaveLength(1);
  });

  it("should not render edit when closed", async () => {
    const mocks: ReadonlyArray<MockedResponse> = [{
      request: {
        query: GET_EVENT_EVIDENCES,
        variables: { eventId: "413372600" },
      },
      result: {
        data: {
          event: {
            eventStatus: "CLOSED",
            evidence: "",
            evidenceFile: "",
            id: "413372600",
          },
        },
      },
    }];
    (window as typeof window & { userRole: string }).userRole = "analyst";
    const wrapper: ReactWrapper = mount(
      <MockedProvider mocks={mocks} addTypename={false}>
        <EventEvidenceView {...mockProps} />
      </MockedProvider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper
      .find("Button")
      .filterWhere((button: ReactWrapper): boolean => _.includes(button.text(), "Edit")))
      .toHaveLength(0);
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
              evidenceFile: "some_file.pdf",
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
      <MockedProvider mocks={mocks} addTypename={false}>
        <EventEvidenceView {...mockProps} />
      </MockedProvider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    wrapper.find("span")
      .find({ className: "img glyphicon glyphicon-file" })
      .simulate("click");
    await act(async () => { await wait(0); });
    expect(onOpenLink)
      .toHaveBeenCalledWith("https://cloudfront/some_file.pdf");
  });
});
