/**
 * react-native-rollbar requires native code so we adapted the web JS
 * version instead. This type definition is a merge between the two
 * @see https://github.com/rollbar/rollbar-react-native/blob/master/index.d.ts
 * @see https://github.com/rollbar/rollbar.js/blob/master/index.d.ts
 */
declare module "rollbar/src/react-native/rollbar" {
  import { default as RollbarBase } from "rollbar";

  class Rollbar extends RollbarBase {
    public setPerson(person: { id: string, name?: string, email?: string }): void;
    public clearPerson(): void;
  };
  namespace Rollbar {
    export class Rollbar { };

    export interface Configuration extends RollbarBase.Configuration {
      platform: string;
    }
  }

  export = Rollbar;
}
