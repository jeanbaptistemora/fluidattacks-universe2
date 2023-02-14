import _ from "lodash";

const validTextField = (value: string): string | undefined => {
  if (!_.isNil(value)) {
    const beginTextMatch: RegExpMatchArray | null = /^=/u.exec(value);
    if (!_.isNull(beginTextMatch)) {
      return `Invalid text begin '${beginTextMatch[0]}'`;
    }

    const textMatch: RegExpMatchArray | null =
      // We use them for control character pattern matching.
      // eslint-disable-next-line no-control-regex
      /[^a-zA-Z0-9ñáéíóúäëïöüÑÁÉÍÓÚÄËÏÖÜ\s(){}[\],./:;@&_$%'#*=¿?¡!+-]/u.exec(
        value
      );
    if (!_.isNull(textMatch)) {
      return `invalid text '${textMatch[0]}'`;
    }

    return undefined;
  }

  return undefined;
};

export { validTextField };
