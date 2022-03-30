import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { ActionButtons } from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { msgInfo } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgInfo").mockImplementation();

  return mockedNotifications;
});

describe("ActionButtons", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ActionButtons).toStrictEqual("function");
  });

  it("should render a component without permissions", (): void => {
    expect.hasAssertions();

    render(
      <authzPermissionsContext.Provider value={new PureAbility([])}>
        <ActionButtons
          areVulnerabilitiesPendingToAcceptance={true}
          areVulnsSelected={false}
          isEditing={false}
          isFindingReleased={true}
          isOpen={false}
          isReattackRequestedInAllVuln={false}
          isRequestingReattack={false}
          isVerified={false}
          isVerifying={false}
          onEdit={jest.fn()}
          onRequestReattack={jest.fn()}
          onVerify={jest.fn()}
          openHandleAcceptance={jest.fn()}
          openModal={jest.fn()}
          state={"open"}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_vulnerabilities_treatment_mutate" },
    ]);
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <ActionButtons
          areVulnerabilitiesPendingToAcceptance={true}
          areVulnsSelected={false}
          isEditing={false}
          isFindingReleased={true}
          isOpen={false}
          isReattackRequestedInAllVuln={false}
          isRequestingReattack={false}
          isVerified={false}
          isVerifying={false}
          onEdit={jest.fn()}
          onRequestReattack={jest.fn()}
          onVerify={jest.fn()}
          openHandleAcceptance={jest.fn()}
          openModal={jest.fn()}
          state={"open"}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("button")).toBeInTheDocument();
    expect(
      screen.getByText("searchFindings.tabVuln.buttons.edit")
    ).toBeInTheDocument();
  });

  it("should render request verification", async (): Promise<void> => {
    expect.hasAssertions();

    const onRequestReattack: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_request_vulnerabilities_verification_mutate" },
      { action: "api_mutations_update_vulnerabilities_treatment_mutate" },
    ]);
    const mockedServices: PureAbility<string> = new PureAbility([
      { action: "is_continuous" },
    ]);
    const { rerender } = render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <authzGroupContext.Provider value={mockedServices}>
          <ActionButtons
            areVulnerabilitiesPendingToAcceptance={true}
            areVulnsSelected={false}
            isEditing={false}
            isFindingReleased={true}
            isOpen={false}
            isReattackRequestedInAllVuln={false}
            isRequestingReattack={false}
            isVerified={false}
            isVerifying={false}
            onEdit={jest.fn()}
            onRequestReattack={onRequestReattack}
            onVerify={jest.fn()}
            openHandleAcceptance={jest.fn()}
            openModal={jest.fn()}
            state={"open"}
          />
        </authzGroupContext.Provider>
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryAllByRole("button")).toHaveLength(2);
    expect(
      screen.queryByText("searchFindings.tabVuln.buttons.edit")
    ).toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.tabDescription.requestVerify.text")
    ).toBeInTheDocument();

    userEvent.click(
      screen.getByText("searchFindings.tabDescription.requestVerify.text")
    );
    rerender(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <authzGroupContext.Provider value={mockedServices}>
          <ActionButtons
            areVulnerabilitiesPendingToAcceptance={true}
            areVulnsSelected={false}
            isEditing={false}
            isFindingReleased={true}
            isOpen={false}
            isReattackRequestedInAllVuln={false}
            isRequestingReattack={true}
            isVerified={false}
            isVerifying={false}
            onEdit={jest.fn()}
            onRequestReattack={onRequestReattack}
            onVerify={jest.fn()}
            openHandleAcceptance={jest.fn()}
            openModal={jest.fn()}
            state={"open"}
          />
        </authzGroupContext.Provider>
      </authzPermissionsContext.Provider>
    );
    await waitFor((): void => {
      expect(onRequestReattack).toHaveBeenCalledTimes(1);
    });

    expect(msgInfo).toHaveBeenCalledWith(
      "searchFindings.tabVuln.info.text",
      "searchFindings.tabVuln.info.title",
      true
    );
    expect(
      screen.queryByText("searchFindings.tabDescription.cancelVerify")
    ).toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.tabVuln.buttons.edit")
    ).not.toBeInTheDocument();

    userEvent.click(
      screen.getByText("searchFindings.tabDescription.cancelVerify")
    );

    rerender(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <authzGroupContext.Provider value={mockedServices}>
          <ActionButtons
            areVulnerabilitiesPendingToAcceptance={true}
            areVulnsSelected={false}
            isEditing={false}
            isFindingReleased={true}
            isOpen={false}
            isReattackRequestedInAllVuln={false}
            isRequestingReattack={false}
            isVerified={false}
            isVerifying={false}
            onEdit={jest.fn()}
            onRequestReattack={onRequestReattack}
            onVerify={jest.fn()}
            openHandleAcceptance={jest.fn()}
            openModal={jest.fn()}
            state={"open"}
          />
        </authzGroupContext.Provider>
      </authzPermissionsContext.Provider>
    );

    expect(
      screen.queryByText("searchFindings.tabDescription.cancelVerify")
    ).not.toBeInTheDocument();
    expect(msgInfo).toHaveBeenCalledWith(
      "searchFindings.tabVuln.info.text",
      "searchFindings.tabVuln.info.title",
      false
    );
  });
});
