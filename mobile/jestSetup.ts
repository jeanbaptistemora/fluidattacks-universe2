/* tslint:disable-next-line: no-import-side-effect
 * Necessary to polyfill fetch in tests env (node)
 */
import fetch from "node-fetch";

Object.assign(global, { fetch });
