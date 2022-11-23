import type { ICredentialsAttr } from "./types";

const formatAuthCredentials = (value: ICredentialsAttr): "TOKEN" | "USER" => {
  if (value.isToken) {
    return "TOKEN";
  }

  return "USER";
};
const formatTypeCredentials = (
  value: ICredentialsAttr
): "SSH" | "TOKEN" | "USER" => {
  if (value.type === "HTTPS") {
    return formatAuthCredentials(value);
  }

  return "SSH";
};

export { formatTypeCredentials, formatAuthCredentials };
