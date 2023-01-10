import React from "react";

import { Pill } from "components/Pill";

export function severityFormatter(severity: number): JSX.Element {
  const score = severity.toFixed(1);

  if (severity >= 0.1 && severity <= 3.9) {
    return <Pill textL={score} textR={"Low"} variant={"yellow"} />;
  } else if (severity >= 4.0 && severity <= 6.9) {
    return <Pill textL={score} textR={"Medium"} variant={"orange"} />;
  } else if (severity >= 7.0 && severity <= 8.9) {
    return <Pill textL={score} textR={"High"} variant={"red"} />;
  }

  return <Pill textL={score} textR={"Critical"} variant={"darkRed"} />;
}
