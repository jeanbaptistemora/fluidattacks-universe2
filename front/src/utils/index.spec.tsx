import { configure } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { isValidFileName, isValidFileSize, numberBetween, validEmail, validTag } from "./validations";

configure({ adapter: new ReactSixteenAdapter() });

describe("Validations", () => {

  it("should be in the range of numbers", () => {
    const severityBetween: ((value: number) => string | undefined) = numberBetween(0, 5);
    expect(severityBetween(3))
      .toEqual(undefined);
  });

  it("shouldn't be in the range of numbers", () => {
    const severityBetween: ((value: number) => string | undefined) = numberBetween(0, 5);
    expect(severityBetween(6))
      .toEqual("This value must be between 0 and 5");
  });

  it("should be a valid email", () => {
    const email: string | undefined = validEmail("user@test.com");
    expect(email)
      .toEqual(undefined);
  });

  it("shouldn't be a valid email", () => {
    const email: string | undefined = validEmail("usertest.com");
    expect(email)
      .toEqual("The email format is not valid");
  });

  it("should be a valid tag", () => {
    const tag: string | undefined = validTag("test");
    expect(tag)
      .toEqual(undefined);
  });

  it("shouldn't be a valid tag", () => {
    const tag: string | undefined = validTag("test.1");
    expect(tag)
      .toEqual("This field can only contain alphanumeric characters and dashes");
  });

  it("should be a valid fileName", () => {
    const fileName: boolean = isValidFileName("filename");
    expect(fileName)
      .toEqual(true);
  });

  it("shouldn't be a valid fileName", () => {
    const fileName: boolean = isValidFileName("badFile{name");
    expect(fileName)
      .toEqual(false);
  });

  it("should be a valid file size", () => {
    const file: File = new File(["foo"], "foo.gif", {
      type: "image/gif",
    });
    const fileSize: boolean = isValidFileSize(file, 2);
    expect(fileSize)
      .toEqual(true);
  });

  it("shouldn't be a valid file size", () => {
    const file: File = new File(["foo"], "foo.gif", {
      type: "image/gif",
    });
    const fileSize: boolean = isValidFileSize(file, 0);
    expect(fileSize)
      .toEqual(false);
  });
});
