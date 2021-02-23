import { MemoryRouter } from "react-router-dom";
import React from "react";
import type { ShallowWrapper } from "enzyme";
import { Sidebar } from "scenes/Dashboard/components/Sidebar";
import { shallow } from "enzyme";

const functionMock: () => JSX.Element = (): JSX.Element => <div />;

describe("Sidebar", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Sidebar).toStrictEqual("function");
  });

  it("should render a sidebar", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <MemoryRouter initialEntries={["/home"]}>
        <Sidebar
          onLogoutClick={functionMock}
          onOpenAccessTokenModal={functionMock}
          onOpenAddOrganizationModal={functionMock}
          onOpenAddUserModal={functionMock}
          userEmail={"test@test.com"}
          userRole={"Unit role"}
        />
      </MemoryRouter>
    );

    expect(wrapper).toHaveLength(1);
  });
});
