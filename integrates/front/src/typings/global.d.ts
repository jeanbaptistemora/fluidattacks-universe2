//Typings for img files
declare module "*.png" {
  const path: string;
  export = path;
}

declare module "*.svg" {
  const value: any;
  export = value;
}

declare module "*.gif" {
  const value: any;
  export = value;
}
