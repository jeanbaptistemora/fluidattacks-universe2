import dayjs from "dayjs";
import type { FieldValidator } from "formik";
import type { ConfigurableValidator } from "revalidate";

import { calcPrivilegesRequired } from "utils/cvss";
import {
  formatIsoDate,
  getDatePlusDeltaDays,
  getRemainingDays,
  isWithInAWeek,
} from "utils/date";
import { getEnvironment } from "utils/environment";
import { formatDate, formatDuration } from "utils/formatHelpers";
import {
  alphaNumeric,
  excludeFormat,
  hasSshFormat,
  isFloatOrInteger,
  isLowerDate,
  isPositive,
  isValidEnvironmentUrl,
  isValidEvidenceDescription,
  isValidFileName,
  isValidFileSize,
  isValidVulnSeverity,
  isValidVulnsFile,
  maxLength,
  minLength,
  numberBetween,
  numeric,
  required,
  sameValue,
  someRequired,
  validCsvInput,
  validDraftTitle,
  validEmail,
  validEvidenceImage,
  validExploitFile,
  validFindingTypology,
  validPath,
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

  it("should required at least 9 characters", (): void => {
    expect.hasAssertions();

    const max: number = 10;
    const length: ConfigurableValidator = maxLength(max);

    // HasLengthLessThan test that the value is less than a predefined length

    expect(length("testmaxlength")).toBe(`Type ${max - 1} characters or less`);
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

  it("should be a valid size .webm file", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const maxSize: number = 10;

    const file = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: ".webm",
      size: 20000,
      slice: jest.fn(),
      type: ".webm",
    };

    const validFile: boolean = isValidFileSize(maxSize)([file]) === undefined;

    expect(validFile).toBe(true);
  });

  it("shouldn't be a valid size .webm file", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const maxSize: number = 10;

    const file = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: ".webm",
      size: 20000000,
      slice: jest.fn(),
      type: ".webm",
    };
    const validFile: boolean = isValidFileSize(maxSize)([file]) === undefined;

    expect(validFile).toBe(false);
  });

  it("should be a valid size .png file", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const file = {
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

    const file = {
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

    const file = {
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

    const file = {
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

  it("should be a valid .webm evidence", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const file = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: "foo.webm",
      size: 20000,
      slice: jest.fn(),
      type: "video/webm",
    };
    const evidenceValidType: boolean = validEvidenceImage([file]) === undefined;

    expect(evidenceValidType).toBe(true);
  });

  it("shouldn't be a valid .webm evidence", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const file = {
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

    const file = {
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
  it("shouldn't be a valid .png evidence", (): void => {
    // NOSONAR
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const file = {
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

    const file = {
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

    const file = {
      ...new File([], ""),
      lastModified: day - month - year,
      name: "foo.png",
      size: 20000,
      slice: jest.fn(),
      type: "image/png",
    };
    const evidenceValidType: boolean = validExploitFile([file]) === undefined;

    expect(evidenceValidType).toBe(false);
  });

  it("should be a valid .csv evidence", (): void => {
    expect.hasAssertions();

    const day: number = 8;
    const month: number = 5;
    const year: number = 2019;

    const file = {
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

    const file = {
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

  it("Should be valid draft", (): void => {
    expect.hasAssertions();

    const ValidDraft = validDraftTitle("111. .test");

    expect(ValidDraft).toBeUndefined();
  });

  it("Should be negative", (): void => {
    expect.hasAssertions();

    const NegativeNum: string | undefined = isPositive(-2);

    expect(NegativeNum).toBe("The number must be greater than 0");
  });

  it("Should be float or integer", (): void => {
    expect.hasAssertions();

    const Num = isFloatOrInteger(1);

    expect(Num).toBeUndefined();
  });

  it("Should'nt be float or integer", (): void => {
    expect.hasAssertions();

    const Num = isFloatOrInteger("a");

    expect(Num).toBe("This field can only contain numbers");
  });

  it("Should be in list", (): void => {
    expect.hasAssertions();

    const Findingtypology = validFindingTypology(["Hello", "World"])("World");

    expect(Findingtypology).toBeUndefined();
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

    const file = {
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

    const file = {
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

    const file = {
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

    const file = {
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

  it("Should be an invalid vuln", (): void => {
    expect.hasAssertions();

    const TestVuln: string = "11111111111";
    const CheckVuln: string | undefined = isValidVulnSeverity(TestVuln);

    expect(CheckVuln).toBe("This value must be between 0 and 1000000000");
  });

  it("Should be the same value", (): void => {
    expect.hasAssertions();

    const IsSame = sameValue("TestGroup")("TestGroup");

    expect(IsSame).toBeUndefined();
  });

  it("Should't be the same value", (): void => {
    expect.hasAssertions();

    const IsSame = sameValue("TestGroup")("TestGroup1");

    expect(IsSame).toBe("Required field");
  });

  it("Should path include the host", (): void => {
    expect.hasAssertions();

    const HosthPathTest = validPath("https://test.com")("https://test.com");

    expect(HosthPathTest).toBe("The path should not include the host");
  });

  it("Should path starts with: /", (): void => {
    expect.hasAssertions();

    const HosthPathTest = validPath("https://test_host_")(
      "/path_with_bad_char"
    );

    expect(HosthPathTest).toBe(
      "Field cannot begin with the following character: /"
    );
  });

  it("Should has good path", (): void => {
    expect.hasAssertions();

    const HosthPathTest = validPath("https://test_host_")("this_is_the_path");

    expect(HosthPathTest).toBeUndefined();
  });

  it("Should have valid environment", (): void => {
    expect.hasAssertions();

    const EnvUrl = isValidEnvironmentUrl(["Test1", "Test2"])("Test1");

    expect(EnvUrl).toBeUndefined();
  });

  it("Should not have environment url", (): void => {
    expect.hasAssertions();

    const EnvUrl = isValidEnvironmentUrl(["Test1", "Test2"])("Test");

    expect(EnvUrl).toBe("The environment URL is invalid");
  });

  it("Should be defined group values", (): void => {
    expect.hasAssertions();

    const helperList: Record<string, unknown> = {
      grouptest1: 1,
      grouptest2: 2,
    };
    const values: Record<string, Record<string, unknown>> = {
      grouptest1: helperList,
    };
    const name: string = "grouptest1.grouptest2.grouptest3";
    const someGroupValues = someRequired(true, values, helperList, name);

    expect(someGroupValues).toBeUndefined();
  });

  it("Should be undefined group values", (): void => {
    expect.hasAssertions();

    const helperList: Record<string, unknown> = {
      grouptest1: 1,
      grouptest2: 2,
    };
    const values: Record<string, Record<string, unknown>> = {
      grouptest1: helperList,
    };
    const name: string = "group1";
    const someGroupValues = someRequired(true, values, helperList, name);

    expect(someGroupValues).toBe("Select at least one value");
  });

  it("Should check the evidence", (): void => {
    expect.hasAssertions();

    const validEvidenceDescription: FieldValidator = isValidEvidenceDescription(
      "test.png",
      undefined
    );
    const evidenceDescription = validEvidenceDescription("");

    expect(evidenceDescription).toBeUndefined();
  });

  it("Should check the evidence description", (): void => {
    expect.hasAssertions();

    const file = new File([""], "image.png", { type: "image/png" });

    const validEvidenceDescription: FieldValidator = isValidEvidenceDescription(
      "",
      file
    );
    const evidenceDescription = validEvidenceDescription("test description");

    expect(evidenceDescription).toBeUndefined();
  });

  it("Should be a big size file", (): void => {
    expect.hasAssertions();

    const file = {
      ...new File([], ""),
      name: "test.yml",
      size: 1048577,
    };
    const vulnsFile = isValidVulnsFile([file]);

    expect(vulnsFile).toBe("The file size must be less than 1MB");
  });

  it("Should be a empty filelist", (): void => {
    expect.hasAssertions();

    const vulnsFile = isValidVulnsFile([]);

    expect(vulnsFile).toBe("No file selected");
  });

  it("Should be a file without .yml or .yaml extension", (): void => {
    expect.hasAssertions();

    const file = {
      ...new File([], ""),
      name: "test.txt",
      size: 1048575,
    };
    const vulnsFile = isValidVulnsFile([file]);

    expect(vulnsFile).toBe("The file must be .yaml or .yml type");
  });

  it("Should be a valid vulns file", (): void => {
    expect.hasAssertions();

    const file = {
      ...new File([], ""),
      name: "test.yml",
      size: 1048575,
    };
    const vulnsFile = isValidVulnsFile([file]);

    expect(vulnsFile).toBeUndefined();
  });

  it("Should ve a valid ssh format", (): void => {
    expect.hasAssertions();

    const value =
      "-----BEGIN OPENSSH PRIVATE KEY-----\ntestssh\n-----END OPENSSH PRIVATE KEY-----";
    const sshCheck = hasSshFormat(value);

    expect(sshCheck).toBeUndefined();
  });

  it("Should ve a invalid ssh format", (): void => {
    expect.hasAssertions();

    const value = "BEGIN OPENSSH PRIVATE KEY\ntest\nEND OPENSSH PRIVATE KEY";
    const sshCheck = hasSshFormat(value);

    expect(sshCheck).toBe("Invalid or malformed SSH private key");
  });

  it("Should include name in format", (): void => {
    expect.hasAssertions();

    const helperList: Record<string, string> = {
      url: "testDomain.com/testOrg/testRepo.git",
    };
    const value = "testRepo/testOrg/test";
    const formatCheck = excludeFormat(value, helperList);

    expect(formatCheck).toBe(
      "Root name should not be included in the exception pattern"
    );
  });

  it("Should't include name in format", (): void => {
    expect.hasAssertions();

    const helperList: Record<string, string> = {
      url: "testDomain.com/testOrg/testRepo.git",
    };
    const value = "testOrg/testRepo/test";
    const formatCheck = excludeFormat(value, helperList);

    expect(formatCheck).toBeUndefined();
  });

  it("Should't be an undefined name", (): void => {
    expect.hasAssertions();

    const helperList: Record<string, string> = {};
    const formatCheck = excludeFormat(undefined, helperList);

    expect(formatCheck).toBeUndefined();
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

describe("Window mock to undefined", (): void => {
  jest.spyOn(global, "window", "get").mockRestore();

  it("Should be undefined window", (): void => {
    expect.hasAssertions();

    jest
      .spyOn(global as unknown as { window: undefined }, "window", "get")
      .mockReturnValue(undefined);

    const expectedEnv = "development";
    const result = getEnvironment();
    jest.spyOn(global, "window", "get").mockRestore();

    expect(result).toBe(expectedEnv);
  });
});

describe("Window mock to production", (): void => {
  const { location } = window;
  jest.spyOn(window, "location", "get").mockRestore();

  it("Should be in production environment", (): void => {
    expect.hasAssertions();

    const mockedLocation = {
      ...location,
      hostname: "test.com",
    };
    jest.spyOn(window, "location", "get").mockReturnValue(mockedLocation);
    const expectedEnv = "production";
    const result = getEnvironment();
    jest.spyOn(window, "location", "get").mockRestore();

    expect(result).toBe(expectedEnv);
  });
});

describe("Window mock to ephemeral", (): void => {
  const { location } = window;
  jest.spyOn(window, "location", "get").mockRestore();

  it("Should be in ephemeral environment", (): void => {
    expect.hasAssertions();

    const mockedLocation = {
      ...location,
      hostname: "testatfluid.app.fluidattacks.com",
    };
    jest.spyOn(window, "location", "get").mockReturnValue(mockedLocation);
    const expectedEnv = "ephemeral";
    const result = getEnvironment();
    jest.spyOn(window, "location", "get").mockRestore();

    expect(result).toBe(expectedEnv);
  });
});

describe("Window mock to development", (): void => {
  const { location } = window;
  jest.spyOn(window, "location", "get").mockRestore();

  it("Should be in development environment", (): void => {
    expect.hasAssertions();

    const mockedLocation = {
      ...location,
      hostname: "localhost",
    };
    jest.spyOn(window, "location", "get").mockReturnValue(mockedLocation);
    const expectedEnv = "development";
    const result = getEnvironment();
    jest.spyOn(window, "location", "get").mockRestore();

    expect(result).toBe(expectedEnv);
  });
});

describe("formatHelpers", (): void => {
  it("Should return incorrect date value", (): void => {
    expect.hasAssertions();

    const value = -1;
    const checkFormat = formatDate(value);

    expect(checkFormat).toBe("-");
  });

  it("Should return correct duration", (): void => {
    expect.hasAssertions();

    const value = 123000;
    const checkFormat = formatDuration(value);

    expect(checkFormat).toBe("00:02:03");
  });

  it("Should return incorrect duration", (): void => {
    expect.hasAssertions();

    const value = -1;
    const checkFormat = formatDuration(value);

    expect(checkFormat).toBe("-");
  });
});

describe("date", (): void => {
  it("Should return correct remaining days", (): void => {
    expect.hasAssertions();

    const value = new Date(new Date().getTime() + 864001000).toISOString();
    const checkRemainingDays = getRemainingDays(value);

    expect(checkRemainingDays).toBe(10);
  });

  it("Should return correct formatted iso date", (): void => {
    expect.hasAssertions();

    const value = "2022-12-01T00:00:00";
    const checkRemainingDays = formatIsoDate(value);

    expect(checkRemainingDays).toBe("2022-12-01 12:00:00");
  });

  it("Should return correct date plus delta days", (): void => {
    expect.hasAssertions();

    const date = "2022-12-01T00:00:00";
    const days = 7;
    const checkDatePlusDeltaDays = getDatePlusDeltaDays(date, days);

    expect(checkDatePlusDeltaDays).toBe("2022-12-08 12:00:00");
  });

  it("Should return true if date is whitin a week", (): void => {
    expect.hasAssertions();

    const date = dayjs(new Date(new Date().getTime() - 6 * 86400000));
    const checkDatePlusDeltaDays = isWithInAWeek(date);

    expect(checkDatePlusDeltaDays).toBe(true);
  });

  it("Should return false if date is out of a week", (): void => {
    expect.hasAssertions();

    const date = dayjs(new Date(new Date().getTime() - 8 * 86400000));
    const checkDatePlusDeltaDays = isWithInAWeek(date);

    expect(checkDatePlusDeltaDays).toBe(false);
  });
});
