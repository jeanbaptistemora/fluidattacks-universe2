/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ConfigurableValidator } from "revalidate";

import { calcPrivilegesRequired } from "utils/cvss";
import { getEnvironment } from "utils/environment";
import {
  alphaNumeric,
  isLowerDate,
  isValidFileName,
  isValidFileSize,
  maxLength,
  minLength,
  numberBetween,
  numeric,
  required,
  validCsvInput,
  validEmail,
  validEvidenceImage,
  validExploitFile,
  validRecordsFile,
  validTag,
  validTextField,
  validUrlField,
} from "utils/validations";

describe("Validations", (): void => {
  it("should be in the range of numbers", (): void => {
    expect.hasAssertions();

    const max: number = 5;
    const severityBetween: (value: number) => string | undefined =
      numberBetween(0, max);

    const severity: number = 3;

    expect(severityBetween(severity)).toBeUndefined();
  });

  it("shouldn't be in the range of numbers", (): void => {
    expect.hasAssertions();

    const max: number = 5;
    const severityBetween: (value: number) => string | undefined =
      numberBetween(0, max);

    const severity: number = 6;

    expect(severityBetween(severity)).toBe(
      "This value must be between 0 and 5"
    );
  });

  it("should required at least 10 characters", (): void => {
    expect.hasAssertions();

    const max: number = 10;
    const length: ConfigurableValidator = maxLength(max);

    expect(length("testmaxlength")).toBe(`Type ${max} characters or less`);
  });

  it("should required 4 minimum characters", (): void => {
    expect.hasAssertions();

    const min: number = 4;
    const length: ConfigurableValidator = minLength(min);

    expect(length(min.toString())).toBe(`Type ${min} characters or more`);
  });

  it("should raise validation", (): void => {
    expect.hasAssertions();

    const nonRequired: ConfigurableValidator = required;
    const nonNumeric: ConfigurableValidator = numeric;

    expect(nonRequired(undefined)).toBeDefined();
    expect(nonNumeric("invalid")).toBeDefined();
  });

  it("shouldn't raise validation", (): void => {
    expect.hasAssertions();

    const requiredFn: ConfigurableValidator = required;
    const numericFn: ConfigurableValidator = numeric;

    expect(requiredFn("valid")).toBeUndefined();
    expect(numericFn("123")).toBeUndefined();
  });

  it("shouldn't be alpha numeric", (): void => {
    expect.hasAssertions();

    const nonAlphaNumeric: ConfigurableValidator = alphaNumeric;

    expect(nonAlphaNumeric("asdf|sd34")).toBeDefined();
  });

  it("should be alpha numeric", (): void => {
    expect.hasAssertions();

    const alphaNumericFn: ConfigurableValidator = alphaNumeric;

    expect(alphaNumericFn("asdfsd34")).toBeUndefined();
  });

  it("should be a valid size .gif file", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const maxSize: number = 10;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: ".gif",
      size: 20000,
      slice: jest.fn(),
      type: ".gif",
    };

    const validFile: boolean = isValidFileSize(maxSize)([file]) === undefined;

    expect(validFile).toBe(true);
  });

  it("shouldn't be a valid size .gif file", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const maxSize: number = 10;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: ".gif",
      size: 20000000,
      slice: jest.fn(),
      type: ".gif",
    };
    const validFile: boolean = isValidFileSize(maxSize)([file]) === undefined;

    expect(validFile).toBe(false);
  });

  it("should be a valid size .png file", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: ".png",
      size: 100000,
      slice: jest.fn(),
      type: ".png",
    };
    const validFile: boolean = isValidFileSize(2)([file]) === undefined;

    expect(validFile).toBe(true);
  });

  it("shouldn't be a valid size .png file", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: ".png",
      size: 20000000,
      slice: jest.fn(),
      type: ".png",
    };
    const validFile: boolean = isValidFileSize(2)([file]) === undefined;

    expect(validFile).toBe(false);
  });

  it("should be a valid size .py file", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: ".py",
      size: 100000,
      slice: jest.fn(),
      type: ".py",
    };
    const validFile: boolean = isValidFileSize(1)([file]) === undefined;

    expect(validFile).toBe(true);
  });

  it("shouldn't be a valid size .py file", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: ".py",
      size: 20000000,
      slice: jest.fn(),
      type: ".py",
    };
    const validFile: boolean = isValidFileSize(1)([file]) === undefined;

    expect(validFile).toBe(false);
  });

  it("should be a valid .gif evidence", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: "foo.gif",
      size: 20000,
      slice: jest.fn(),
      type: "image/gif",
    };
    const evidenceValidType: boolean = validEvidenceImage([file]) === undefined;

    expect(evidenceValidType).toBe(true);
  });

  it("shouldn't be a valid .gif evidence", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: "foo.py",
      size: 20000,
      slice: jest.fn(),
      type: "text/plain",
    };
    const evidenceValidType: boolean = validEvidenceImage([file]) === undefined;

    expect(evidenceValidType).toBe(false);
  });

  it("should be a valid .png evidence", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: "foo.png",
      size: 20000,
      slice: jest.fn(),
      type: "image/png",
    };
    const evidenceValidType: boolean = validEvidenceImage([file]) === undefined;

    expect(evidenceValidType).toBe(true);
  });

  // Exception: WF(This function must contain explicit assert)
  // eslint-disable-next-line
  it("shouldn't be a valid .png evidence", (): void => { // NOSONAR
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: "foo.py",
      size: 20000,
      slice: jest.fn(),
      type: "text/plain",
    };
    const evidenceValidType: boolean = validEvidenceImage([file]) === undefined;

    expect(evidenceValidType).toBe(false);
  });

  it("should be a valid .py evidence", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: "foo.py",
      size: 20000,
      slice: jest.fn(),
      type: "text/plain",
    };
    const evidenceValidType: boolean = validExploitFile([file]) === undefined;

    expect(evidenceValidType).toBe(true);
  });

  it("shouldn't be a valid .py evidence", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: "foo.gif",
      size: 20000,
      slice: jest.fn(),
      type: "image/gif",
    };
    const evidenceValidType: boolean = validExploitFile([file]) === undefined;

    expect(evidenceValidType).toBe(false);
  });

  it("should be a valid .csv evidence", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: "foo.csv",
      size: 20000,
      slice: jest.fn(),
      type: "text/csv",
    };
    const evidenceValidType: boolean = validRecordsFile([file]) === undefined;

    expect(evidenceValidType).toBe(true);
  });

  it("shouldn't be a valid .csv evidence", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: "foo.exp",
      size: 20000,
      slice: jest.fn(),
      type: "text/plain",
    };
    const evidenceValidType: boolean = validRecordsFile([file]) === undefined;

    expect(evidenceValidType).toBe(false);
  });

  it("should be a valid email", (): void => {
    expect.hasAssertions();

    const email: string | undefined = validEmail("user@test.com");

    expect(email).toBeUndefined();
  });

  it("shouldn't be a valid email", (): void => {
    expect.hasAssertions();

    const email: string | undefined = validEmail("usertest.com");

    expect(email).toBe("The email format is not valid");
  });

  it("should be a valid text field", (): void => {
    expect.hasAssertions();

    const textField: string | undefined = validTextField("t3 stfíel#-d");

    expect(textField).toBeUndefined();
  });

  it("shouldn't be a valid text field", (): void => {
    expect.hasAssertions();

    const feedbackEqual: string | undefined = validTextField("=testfield");
    const feedbackLessThan: string | undefined = validTextField("<testfield");

    expect(feedbackEqual).toBe(
      "Field cannot begin with the following character: '='"
    );
    expect(feedbackLessThan).toBe(
      "Field cannot contain the following characters: '<'"
    );
  });

  it("should be a valid url", (): void => {
    expect.hasAssertions();

    const url: string | undefined = validUrlField("test/url/field#1");

    expect(url).toBeUndefined();
  });

  it("shouldn't be a valid url", (): void => {
    expect.hasAssertions();

    const feedbackMissChar: string | undefined =
      validUrlField("test/url/fi eld#1");
    const feedbackInvalidChar: string | undefined =
      validUrlField("test/url/fiéld");

    expect(feedbackMissChar).toBe(
      "URL value cannot contain the following characters: ' '"
    );
    expect(feedbackInvalidChar).toBe(
      "URL value cannot contain the following characters: 'é'"
    );
  });

  it("Should be invalid begin of url", (): void => {
    expect.hasAssertions();

    const BadBeginUrl = validUrlField("=test/url/field");

    expect(BadBeginUrl).toBe(
      "Field cannot begin with the following character: '='"
    );
  });

  it("should be a valid tag", (): void => {
    expect.hasAssertions();

    const tag: string | undefined = validTag("test");

    expect(tag).toBeUndefined();
  });

  it("shouldn't be a valid tag", (): void => {
    expect.hasAssertions();

    const tag: string | undefined = validTag("test.1");

    expect(tag).toBe(
      "This field can only contain alphanumeric characters and dashes"
    );
  });

  it("should be a valid fileName", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;
    const MIB: number = 1048576;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: "filename.pdf",
      size: MIB * 2,
      slice: jest.fn(),
      type: "application/pdf",
    };
    const fileName: string | undefined = isValidFileName([file]);

    expect(fileName).toBeUndefined();
  });

  it("shouldn't be a valid fileName", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;
    const MIB: number = 1048576;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: "badFile{name.pdf.exe",
      size: MIB * 2,
      slice: jest.fn(),
      type: "application/octet-stream",
    };
    const fileName: string | undefined = isValidFileName([file]);

    expect(typeof fileName).toBe("string");
  });

  it("should be a valid file size", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;
    const MIB: number = 1048576;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: "badFile.exe",
      size: MIB,
      slice: jest.fn(),
      type: "application/octet-stream",
    };
    const fileSize: string | undefined = isValidFileSize(2)([file]);

    expect(fileSize).toBeUndefined();
  });

  it("shouldn't be a valid file size", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;
    const MIB: number = 5242880;

    const file: File = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: "badFile.exe",
      size: MIB,
      slice: jest.fn(),
      type: "application/octet-stream",
    };
    const fileSize: string | undefined = isValidFileSize(2)([file]);

    expect(typeof fileSize).toBe("string");
  });

  it("should be a valid date", (): void => {
    expect.hasAssertions();

    const today: Date = new Date();
    const oneMonthLater: Date = new Date(today.setMonth(today.getMonth() + 1));
    const date: string | undefined = isLowerDate(oneMonthLater.toDateString());

    expect(date).toBeUndefined();
  });

  it("should't be a valid date", (): void => {
    expect.hasAssertions();

    const today: Date = new Date();
    const oneMonthEarlier: Date = new Date(
      today.setMonth(today.getMonth() - 1)
    );
    const date: string | undefined = isLowerDate(
      oneMonthEarlier.toDateString()
    );

    expect(date).toBeDefined();
  });

  it("Should be a invalid input", (): void => {
    expect.hasAssertions();

    const BadBegin: string | undefined = validCsvInput("=testText");
    const BadPattern: string | undefined = validCsvInput("ThisIsA,=Test");

    expect(BadBegin).toBe(
      "Field cannot begin with the following character: '='"
    );
    expect(BadPattern).toBe(
      "Field cannot contain the following character pattern: ',='"
    );
  });
});

describe("environments", (): void => {
  it("should return development", (): void => {
    expect.hasAssertions();

    const environment: string = getEnvironment();

    expect(environment).toBe("development");
  });
});

describe("cvss", (): void => {
  it("Should required LOW_SCOPE_C privileges", (): void => {
    expect.hasAssertions();

    const privReq: number = calcPrivilegesRequired("0.62", "1");

    expect(privReq).toBe(0.68);
  });

  it("Should required HIGH_SCOPE_C privileges", (): void => {
    expect.hasAssertions();

    const privReq: number = calcPrivilegesRequired("0.27", "1");

    expect(privReq).toBe(0.5);
  });

  it("Should required LOW_SCOPE_U privileges", (): void => {
    expect.hasAssertions();

    const privReq: number = calcPrivilegesRequired("0.68", "0");

    expect(privReq).toBe(0.62);
  });

  it("Should required HIGH_SCOPE_U privileges", (): void => {
    expect.hasAssertions();

    const privReq: number = calcPrivilegesRequired("0.5", "0");

    expect(privReq).toBe(0.27);
  });

  it("Should required privReq privileges", (): void => {
    expect.hasAssertions();

    const privReq: number = calcPrivilegesRequired("1", "0");

    expect(privReq).toBe(1);
  });
});
