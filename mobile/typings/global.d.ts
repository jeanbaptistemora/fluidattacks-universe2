type Dictionary<T = {}> = { [key: string]: T };

//Typings for img files
declare module "*.png" {
  const value: number;
  export = value;
}

declare module "*.gif" {
  const value: number;
  export = value;
}

declare module "*.svg" {
  const value: string;
  export = value;
}
