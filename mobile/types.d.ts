type Dictionary<T = {}> = { [key: string]: T };

//Typings for img files
declare module "*.png" {
  const value: number;
  export = value;
}
