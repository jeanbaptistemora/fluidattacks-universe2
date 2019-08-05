import { configure } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { ConfigurableValidator } from "revalidate";
import { evidenceHasValidSize, evidenceHasValidType, isValidFileName,
         isValidFileSize, minLength, numberBetween, validEmail, validTag } from "./validations";

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

  it("should required 4 minimum characters", () => {
    const length: ConfigurableValidator = minLength(4);
    expect(length("4"))
      .toEqual("This field requires at least 4 characters");
  });

  it("should be a valid size .gif file", () => {
    const file: File = {
      lastModified: 8 - 5 - 2019,
      name: ".gif",
      size: 20000,
      slice: jest.fn(),
      type: ".gif",
    };
    const validFile: boolean = evidenceHasValidSize(file);
    expect(validFile)
    .toEqual(true);
  });

  it("shouldn't be a valid size .gif file", () => {
    const file: File = {
      lastModified: 8 - 5 - 2019,
      name: ".gif",
      size: 20000000,
      slice: jest.fn(),
      type: ".gif",
    };
    const validFile: boolean = evidenceHasValidSize(file);
    expect(validFile)
    .toEqual(false);
  });

  it("should be a valid size .png file", () => {
    const file: File = {
      lastModified: 8 - 5 - 2019,
      name: ".png",
      size: 100000,
      slice: jest.fn(),
      type: ".png",
    };
    const validFile: boolean = evidenceHasValidSize(file);
    expect(validFile)
    .toEqual(true);
  });

  it("shouldn't be a valid size .png file", () => {
    const file: File = {
      lastModified: 8 - 5 - 2019,
      name: ".png",
      size: 20000000,
      slice: jest.fn(),
      type: ".png",
    };
    const validFile: boolean = evidenceHasValidSize(file);
    expect(validFile)
    .toEqual(false);
  });

  it("should be a valid size .py file", () => {
    const file: File = {
      lastModified: 8 - 5 - 2019,
      name: ".py",
      size: 100000,
      slice: jest.fn(),
      type: ".py",
    };
    const validFile: boolean = evidenceHasValidSize(file);
    expect(validFile)
    .toEqual(true);
  });

  it("shouldn't be a valid size .py file", () => {
    const file: File = {
      lastModified: 8 - 5 - 2019,
      name: ".py",
      size: 20000000,
      slice: jest.fn(),
      type: ".py",
    };
    const validFile: boolean = evidenceHasValidSize(file);
    expect(validFile)
    .toEqual(false);
  });

  it("shouldn't be a valid type file", () => {
    const file: File = {
      lastModified: 8 - 5 - 2019,
      name: ".test",
      size: 2000,
      slice: jest.fn(),
      type: ".test",
    };
    const validFile: boolean = evidenceHasValidSize(file);
    expect(validFile)
    .toEqual(false);
  });

  it("should be a valid .gif evidence", () => {
    const file: File = new File(["foo"], "foo.gif", {
      type: "image/gif",
    });
    const evidenceValidType: boolean = evidenceHasValidType(file, 0);
    expect(evidenceValidType)
      .toEqual(true);
  });

  it("shouldn't be a valid .gif evidence", () => {
    const file: File = new File(["foo"], "foo.py", {
      type: "image/py",
    });
    const evidenceValidType: boolean = evidenceHasValidType(file, 0);
    expect(evidenceValidType)
      .toEqual(false);
  });

  it("should be a valid .png evidence", () => {
    const file: File = new File(["foo"], "foo.png", {
      type: "image/png",
    });
    const evidenceValidType: boolean = evidenceHasValidType(file, 4);
    expect(evidenceValidType)
      .toEqual(true);
  });

  it("shouldn't be a valid .png evidence", () => {
    const file: File = new File(["foo"], "foo.py", {
      type: "image/py",
    });
    const evidenceValidType: boolean = evidenceHasValidType(file, 4);
    expect(evidenceValidType)
      .toEqual(false);
  });

  it("should be a valid .py evidence", () => {
    const file: File = new File(["foo"], "foo.py", {
      type: "file/py",
    });
    const evidenceValidType: boolean = evidenceHasValidType(file, 7);
    expect(evidenceValidType)
      .toEqual(true);
  });

  it("shouldn't be a valid .py evidence", () => {
    const file: File = new File(["foo"], "foo.gif", {
      type: "file/gif",
    });
    const evidenceValidType: boolean = evidenceHasValidType(file, 7);
    expect(evidenceValidType)
      .toEqual(false);
  });

  it("should be a valid .csv evidence", () => {
    const file: File = new File(["foo"], "foo.csv", {
      type: "file/csv",
    });
    const evidenceValidType: boolean = evidenceHasValidType(file, 8);
    expect(evidenceValidType)
      .toEqual(true);
  });

  it("shouldn't be a valid .csv evidence", () => {
    const file: File = new File(["foo"], "foo.exp", {
      type: "file/exp",
    });
    const evidenceValidType: boolean = evidenceHasValidType(file, 8);
    expect(evidenceValidType)
      .toEqual(false);
  });

  it("shouldn't be a valid evidence type", () => {
    const file: File = new File(["foo"], "foo.doc", {
      type: "file/doc",
    });
    const evidenceValidType: boolean = evidenceHasValidType(file, 10);
    expect(evidenceValidType)
      .toEqual(false);
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
