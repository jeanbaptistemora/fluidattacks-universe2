/**
 * Note about security concerns
 *
 * All the following constants are just client ids.
 * They are not meant to be secret.
 * Their security relies on a list of allowed
 * origins and redirect urls
 */
const BUGSNAG_KEY: string = "c7b947a293ced0235cdd8edc8c09dad4";
const GOOGLE_CLIENT_ID_DEV: string =
  "335718398321-t2358fdl2nf0joiqsv41dobom3kon7nf.apps.googleusercontent.com";
const GOOGLE_CLIENT_ID_ANDROID: string =
  "335718398321-lkf186ev7fujqmfe59bb05oehn4l2g5c.apps.googleusercontent.com";
const GOOGLE_CLIENT_ID_IOS: string =
  "335718398321-s67kko7rj2cdf1a3jaj1vgdohjme2sna.apps.googleusercontent.com";
const MICROSOFT_CLIENT_ID: string = "4a9923e0-17f1-43b7-9b16-7892eed25f18";
const BITBUCKET_CLIENT_ID_DEV: string = "pYj72WzD7sGAXMvjFD";
const BITBUCKET_CLIENT_ID_PROD: string = "S3qM7quyfzGeemvnh2";

export {
  BUGSNAG_KEY,
  GOOGLE_CLIENT_ID_DEV,
  GOOGLE_CLIENT_ID_ANDROID,
  GOOGLE_CLIENT_ID_IOS,
  MICROSOFT_CLIENT_ID,
  BITBUCKET_CLIENT_ID_DEV,
  BITBUCKET_CLIENT_ID_PROD,
};
