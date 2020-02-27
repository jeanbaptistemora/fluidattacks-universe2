import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { configure, mount, ReactWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { GraphQLError } from "graphql";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import * as React from "react";
import { Provider } from "react-redux";
import wait from "waait";
import store from "../../../../store/index";
import ProjectResourcesView from "./index";
import { GET_ENVIRONMENTS, GET_REPOSITORIES, GET_TAGS } from "./queries";
import { IResourcesViewProps } from "./types";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Resources view", () => {

  const mockProps: IResourcesViewProps = {
    defaultSort: {
      files: {},
      tags: {},
    },
    files: [{
      description: "test",
      fileName: "fileTest",
      uploadDate: "",
    }],
    filesModal: {
      open: false,
    },
    match: {
      isExact: true,
      params: {projectName: "TEST"},
      path: "/",
      url: "",
    },
    onCloseFilesModal: functionMock,
    onCloseOptionsModal: functionMock,
    onCloseTagsModal: functionMock,
    onDeleteFile: functionMock,
    onDownloadFile: functionMock,
    onLoad: functionMock,
    onOpenFilesModal: functionMock,
    onOpenOptionsModal: functionMock,
    onOpenTagsModal: functionMock,
    onSaveFiles: functionMock,
    onSort: functionMock,
    optionsModal: {
      open: false,
      rowInfo: { fileName: "fileTest"},
    },
    showUploadProgress: false,
    tagsModal: {
      open: false,
    },
    uploadProgress: 0,
  };

  const mocksTags: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_TAGS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          project: {
            __typename: "Project",
            deletionDate: "",
            name: "oneshottest",
            subscription: "oneshot",
            tags: ["test"],
          },
        },
      },
  }];

  const mocksRepositories: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_REPOSITORIES,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          me: {
            __typename: "Me",
            role: "customer",
          },
          project: {
            __typename: "Project",
            deletionDate: "",
          },
          resources: {
            __typename: "Resource",
            repositories: JSON.stringify([{
              branch: "test",
              historic_state: [{ state: "ACTIVE" }],
              protocol: "HTTPS",
              urlRepo: "https://gitlab.com/fluidattacks/integrates",
            }]),
          },
        },
      },
  }];

  const mocksEnvironments: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_ENVIRONMENTS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          project: {
            __typename: "Project",
            deletionDate: "",
          },
          resources: {
            __typename: "Resource",
            environments: JSON.stringify([{
              urlEnv: "https://gitlab.com/fluidattacks/integrates",
            }]),
          },
        },
      },
  }];

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_TAGS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a object", () => {
    expect(typeof (ProjectResourcesView))
      .toEqual("object");
  });

  it("should render tags component", async () => {
    (window as typeof window & Dictionary<string>).userRole = "customer";
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksTags} addTypename={true}>
          <ProjectResourcesView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render repositories component", async () => {
    (window as typeof window & Dictionary<string>).userRole = "customer";
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksRepositories} addTypename={true}>
          <ProjectResourcesView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    wrapper.update();
    const onerow: ReactWrapper = wrapper
                                 .find("BootstrapTable")
                                 .find("RowPureContent")
                                 .find("Cell");
    const statuschecked: boolean | undefined = wrapper
                                               .find("BootstrapTable")
                                               .find("RowPureContent")
                                               .find("Cell")
                                               .at(3)
                                               .find("e")
                                               .prop("checked");
    const protocol: string = wrapper
                            .find("BootstrapTable")
                            .find("RowPureContent")
                            .find("Cell")
                            .at(0)
                            .find("td")
                            .text();
    expect(wrapper)
      .toHaveLength(1);
    expect(onerow)
      .toHaveLength(4);
    expect(statuschecked)
      .toEqual(true || false);
    expect(protocol)
      .toMatch(/^(HTTPS|SSH)$/);
  });

  it("should render environments component", async () => {
    (window as typeof window & Dictionary<string>).userRole = "customer";
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksEnvironments} addTypename={true}>
          <ProjectResourcesView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    wrapper.update();
    const onerow: ReactWrapper = wrapper
                                 .find("BootstrapTable")
                                 .find("RowPureContent")
                                 .find("Cell");
    const statuschecked: boolean | undefined = wrapper
                                               .find("BootstrapTable")
                                               .find("RowPureContent")
                                               .find("Cell")
                                               .at(1)
                                               .find("e")
                                               .prop("checked");
    expect(wrapper)
      .toHaveLength(1);
    expect(onerow)
      .toHaveLength(2);
    expect(statuschecked)
      .toEqual(true || false);
  });

  it("should render a error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={true}>
          <ProjectResourcesView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render files component", async () => {
    (window as typeof window & Dictionary<string>).userRole = "customer";
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksTags} addTypename={true}>
          <ProjectResourcesView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper.find("#tblFiles"))
      .toBeTruthy();
  });
});
