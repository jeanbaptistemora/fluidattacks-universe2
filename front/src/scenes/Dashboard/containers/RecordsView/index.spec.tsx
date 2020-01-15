import { configure, mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import React from "react";
import { RouteComponentProps } from "react-router";
import { recordsView as RecordsView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe.skip("Records view", () => {

  const routePropsMock: RouteComponentProps<{ findingId: string }> = {
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
    match: { isExact: true, params: { findingId: "422286126" }, path: "/", url: "" },
  };

  const dataset: object[] = [
    { Character: "Cobra Commander", Genre: "action", Release: "2013", Title: "G.I. Joe: Retaliation" },
    { Character: "Tony Stark", Genre: "action", Release: "2008", Title: "Iron Man" },
  ];

  it("should return a function", (): void => {
    expect(typeof (RecordsView))
      .toEqual("function");
  });

  it("should render a component", (): void => {
    const wrapper: ReactWrapper = mount(
      <RecordsView
        onRemove={jest.fn()}
        {...routePropsMock}
      />,
    );
    const table: ReactWrapper = wrapper.find("BootstrapTable");
    expect(table)
      .toHaveLength(1);
    expect(table.find("HeaderCell"))
      .toHaveLength(Object.keys(dataset[0]).length - 1);
  });

  it("should render as editable", (): void => {
    const handleEditClick: jest.Mock = jest.fn();

    const wrapper: ShallowWrapper = shallow(
      <RecordsView
        onRemove={jest.fn()}
        {...routePropsMock}
      />,
    );
    const editButton: ShallowWrapper = wrapper.find("button")
      .findWhere((element: ShallowWrapper) => element.contains("Edit"))
      .at(0);
    expect(editButton)
      .toHaveLength(1);
    editButton.simulate("click");
    expect(handleEditClick.mock.calls.length)
      .toEqual(1);
  });

  it("should render as readonly", (): void => {
    const wrapper: ShallowWrapper = shallow(
      <RecordsView
        onRemove={jest.fn()}
        {...routePropsMock}
      />,
    );
    expect(wrapper.find("button")
      .findWhere((element: ShallowWrapper) => element.contains("Edit"))
      .at(0))
      .toHaveLength(0);
  });

  it("should render upload field", (): void => {
    const wrapper: ShallowWrapper = shallow(
      <RecordsView
        onRemove={jest.fn()}
        {...routePropsMock}
      />,
    );
    expect(wrapper.find("button")
      .findWhere((element: ShallowWrapper) => element.contains("Update"))
      .at(0))
      .toHaveLength(1);
  });

  it("should render remove field", (): void => {
    const wrapper: ShallowWrapper = shallow(
      <RecordsView
        onRemove={jest.fn()}
        {...routePropsMock}
      />,
    );
    expect(wrapper.find("button")
      .findWhere((element: ShallowWrapper) => element.contains("Delete"))
      .at(0))
      .toHaveLength(1);
  });

  it("should change edit mode", (): void => {

    const wrapper: ShallowWrapper = shallow(
      <RecordsView
        onRemove={jest.fn()}
        {...routePropsMock}
      />,
    );
    expect(wrapper.find("button")
      .findWhere((element: ShallowWrapper) => element.contains("Update"))
      .at(0))
      .toHaveLength(0);
    wrapper.setProps({ isEditing: true });
    expect(wrapper.find("button")
      .findWhere((element: ShallowWrapper) => element.contains("Update"))
      .at(0))
      .toHaveLength(1);
  });
});
