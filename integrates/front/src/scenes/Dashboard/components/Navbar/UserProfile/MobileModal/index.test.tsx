import { MobileModal } from ".";

jest.mock("../../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("Mobile modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof MobileModal).toStrictEqual("function");
  });
});
