interface ILicenseItem {
  repository: string;
  licenseUrl: string;
  parents: string;
  key: string;
  name: string;
  licenses: string;
  version: string;
}

interface ILicenses {
  licenses: ILicenseItem[];
}

export { ILicenseItem, ILicenses };
