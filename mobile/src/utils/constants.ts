import { Constants } from "expo";

/* tslint:disable:no-inferrable-types
 * Disabling this rule is necessary due to a tslint 'type'
 * conflict that would force to reassign each variable,
 * compromising constants readability
 *
 * View: https://github.com/palantir/tslint/issues/711
 */

const GOOGLE_LOGIN_KEY_DEV: string = "335718398321-vv3cfdee0ng40tuhgm5g2mp42c2d2o9j.apps.googleusercontent.com";
const GOOGLE_LOGIN_KEY_PROD: string = "335718398321-lkf186ev7fujqmfe59bb05oehn4l2g5c.apps.googleusercontent.com";

export const GOOGLE_LOGIN_KEY: string = Constants.appOwnership === "expo"
    ? GOOGLE_LOGIN_KEY_DEV
    : GOOGLE_LOGIN_KEY_PROD;
