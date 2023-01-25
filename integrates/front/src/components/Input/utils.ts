const createEvent = (type: string, name: string, value: unknown): Event => {
  const event = new Event(type);
  // eslint-disable-next-line fp/no-mutating-methods
  Object.defineProperty(event, "target", {
    value: { name, value },
  });

  return event;
};

export { createEvent };
