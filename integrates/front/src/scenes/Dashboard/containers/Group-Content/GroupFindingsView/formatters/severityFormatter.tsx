import React from "react";

import { ScoreTag } from "components/ScoreTag";

export function severityFormatter(severity: number): JSX.Element {
  if (severity > 0.1 && severity <= 3.9) {
    return <ScoreTag score={severity} variant={"low"} />;
  } else if (severity > 4.0 && severity <= 6.9) {
    return <ScoreTag score={severity} variant={"medium"} />;
  } else if (severity > 7.0 && severity <= 8.9) {
    return <ScoreTag score={severity} variant={"high"} />;
  }

  return <ScoreTag score={severity} variant={"critical"} />;
}
