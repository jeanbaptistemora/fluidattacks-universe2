import { configure } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { ConfigurableValidator } from "revalidate";
import {
  alphaNumeric, isLowerDate, isValidDate, isValidFileName, isValidFileSize,
  minLength, numberBetween, numeric, required, validEmail, validEvidenceImage,
  validExploitFile, validRecordsFile, validTag,
} from "./validations";

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

  it("should raise validation", () => {
    const nonRequired: ConfigurableValidator = required;
    expect(nonRequired(undefined))
      .toBeDefined();
  });

  it("shouldn't raise validation", () => {
    const requiredFn: ConfigurableValidator = required;
    expect(requiredFn("valid"))
      .toBeUndefined();
  });

  it("should raise validation", () => {
    const nonNumeric: ConfigurableValidator = numeric;
    expect(nonNumeric("invalid"))
      .toBeDefined();
  });

  it("shouldn't raise validation", () => {
    const numericFn: ConfigurableValidator = numeric;
    expect(numericFn("123"))
      .toBeUndefined();
  });

  it("shouldn't be alpha numeric", () => {
    const nonAlphaNumeric: ConfigurableValidator = alphaNumeric;
    expect(nonAlphaNumeric("asdf|sd34"))
      .toBeDefined();
  });

  it("should be alpha numeric", () => {
    const alphaNumericFn: ConfigurableValidator = alphaNumeric;
    expect(alphaNumericFn("asdfsd34"))
      .toBeUndefined();
  });

  it("should be a valid size .gif file", () => {
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: ".gif",
      size: 20000,
      slice: jest.fn(),
      type: ".gif",
    };
    const validFile: boolean = isValidFileSize(10)([file]) === undefined;
    expect(validFile)
    .toEqual(true);
  });

  it("shouldn't be a valid size .gif file", () => {
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: ".gif",
      size: 20000000,
      slice: jest.fn(),
      type: ".gif",
    };
    const validFile: boolean = isValidFileSize(10)([file]) === undefined;
    expect(validFile)
    .toEqual(false);
  });

  it("should be a valid size .png file", () => {
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: ".png",
      size: 100000,
      slice: jest.fn(),
      type: ".png",
    };
    const validFile: boolean = isValidFileSize(2)([file]) === undefined;
    expect(validFile)
    .toEqual(true);
  });

  it("shouldn't be a valid size .png file", () => {
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: ".png",
      size: 20000000,
      slice: jest.fn(),
      type: ".png",
    };
    const validFile: boolean = isValidFileSize(2)([file]) === undefined;
    expect(validFile)
    .toEqual(false);
  });

  it("should be a valid size .py file", () => {
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: ".py",
      size: 100000,
      slice: jest.fn(),
      type: ".py",
    };
    const validFile: boolean = isValidFileSize(1)([file]) === undefined;
    expect(validFile)
    .toEqual(true);
  });

  it("shouldn't be a valid size .py file", () => {
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: ".py",
      size: 20000000,
      slice: jest.fn(),
      type: ".py",
    };
    const validFile: boolean = isValidFileSize(1)([file]) === undefined;
    expect(validFile)
    .toEqual(false);
  });

  it("should be a valid .gif evidence", () => {
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: "foo.gif",
      size: 20000,
      slice: jest.fn(),
      type: "image/gif",
    };
    const evidenceValidType: boolean = validEvidenceImage([file]) === undefined;
    expect(evidenceValidType)
      .toEqual(true);
  });

  it("shouldn't be a valid .gif evidence", () => {
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: "foo.py",
      size: 20000,
      slice: jest.fn(),
      type: "text/plain",
    };
    const evidenceValidType: boolean = validEvidenceImage([file]) === undefined;
    expect(evidenceValidType)
      .toEqual(false);
  });

  it("should be a valid .png evidence", () => {
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: "foo.png",
      size: 20000,
      slice: jest.fn(),
      type: "image/png",
    };
    const evidenceValidType: boolean = validEvidenceImage([file]) === undefined;
    expect(evidenceValidType)
      .toEqual(true);
  });

  it("shouldn't be a valid .png evidence", () => {
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: "foo.py",
      size: 20000,
      slice: jest.fn(),
      type: "text/plain",
    };
    const evidenceValidType: boolean = validEvidenceImage([file]) === undefined;
    expect(evidenceValidType)
      .toEqual(false);
  });

  it("should be a valid .py evidence", () => {
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: "foo.py",
      size: 20000,
      slice: jest.fn(),
      type: "text/plain",
    };
    const evidenceValidType: boolean = validExploitFile([file]) === undefined;
    expect(evidenceValidType)
      .toEqual(true);
  });

  it("shouldn't be a valid .py evidence", () => {
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: "foo.gif",
      size: 20000,
      slice: jest.fn(),
      type: "image/gif",
    };
    const evidenceValidType: boolean = validExploitFile([file]) === undefined;
    expect(evidenceValidType)
      .toEqual(false);
  });

  it("should be a valid .csv evidence", () => {
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: "foo.csv",
      size: 20000,
      slice: jest.fn(),
      type: "text/csv",
    };
    const evidenceValidType: boolean = validRecordsFile([file]) === undefined;
    expect(evidenceValidType)
      .toEqual(true);
  });

  it("shouldn't be a valid .csv evidence", () => {
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: "foo.exp",
      size: 20000,
      slice: jest.fn(),
      type: "text/plain",
    };
    const evidenceValidType: boolean = validRecordsFile([file]) === undefined;
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
    const MIB: number = 1048576;
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: "filename.pdf",
      size: MIB * 2,
      slice: jest.fn(),
      type: "application/pdf",
    };
    const fileName: string | undefined = isValidFileName([file]);
    expect(fileName)
      .toEqual(undefined);
  });

  it("shouldn't be a valid fileName", () => {
    const MIB: number = 1048576;
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: "badFile{name.pdf.exe",
      size: MIB * 2,
      slice: jest.fn(),
      type: "application/octet-stream",
    };
    const fileName: string | undefined = isValidFileName([file]);
    expect(typeof fileName)
      .toEqual("string");
  });

  it("should be a valid file size", () => {
    const MIB: number = 1048576;
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: "badFile.exe",
      size: MIB * 1,
      slice: jest.fn(),
      type: "application/octet-stream",
    };
    const fileSize: string | undefined = isValidFileSize(2)([file]);
    expect(fileSize)
      .toEqual(undefined);
  });

  it("shouldn't be a valid file size", () => {
    const MIB: number = 1048576;
    const file: File = {
      ...new File([], ""),
      lastModified: 8 - 5 - 2019,
      name: "badFile.exe",
      size: MIB * 5,
      slice: jest.fn(),
      type: "application/octet-stream",
    };
    const fileSize: string | undefined = isValidFileSize(2)([file]);
    expect(typeof fileSize)
      .toEqual("string");
  });

  it("should be a valid date", () => {
    let today: Date; today = new Date(); today = new Date(today.setMonth(today.getMonth() + 1));
    const date: string | undefined = isLowerDate(today.toDateString());
    expect(date)
      .toBeUndefined();
  });

  it("should't be a valid date", () => {
    let today: Date; today = new Date(); today = new Date(today.setMonth(today.getMonth() - 1));
    const date: string | undefined = isLowerDate(today.toDateString());
    expect(date)
      .toBeDefined();
  });

  it("should be a maximum valid date", () => {
    let today: Date; today = new Date(); today = new Date(today.setMonth(today.getMonth() + 5));
    const date: string | undefined = isValidDate(today.toDateString());
    expect(date)
      .toBeUndefined();
  });

  it("shouldn't be a maximum valid date", () => {
    let today: Date; today = new Date(); today = new Date(today.setMonth(today.getMonth() + 7));
    const date: string | undefined = isValidDate(today.toDateString());
    expect(date)
      .toBeDefined();
  });
});
