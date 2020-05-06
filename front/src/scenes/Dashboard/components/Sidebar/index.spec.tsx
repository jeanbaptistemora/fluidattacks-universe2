import { shallow, ShallowWrapper } from "enzyme";
import * as React from "react";
import { MemoryRouter } from "react-router-dom";
import { Sidebar } from "./index";

const functionMock: (() => JSX.Element) = (): JSX.Element => <div />;

describe("Sidebar", () => {

  it("should return a function", () => {
    expect(typeof (Sidebar))
      .toEqual("function");
  });

  it("should render a sidebar", () => {
    const wrapper: ShallowWrapper = shallow(
      <MemoryRouter initialEntries={["/home"]}>
      <Sidebar onLogoutClick={functionMock} onOpenAccessTokenModal={functionMock} onOpenAddUserModal={functionMock}/>
      </MemoryRouter>,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
