type Dictionary<T = {}> = { [key: string]: T };

//Typings for img files
declare module "*.png" {
    const value: any;
    export = value;
}

declare module "*.svg" { const value: any; export = value; }
