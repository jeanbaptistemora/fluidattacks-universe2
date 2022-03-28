import { faClipboard } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback } from "react";

import { Button } from "components/Button";

const SecretValue: React.FC<{ value: string }> = ({
  value,
}: {
  value: string;
}): JSX.Element => {
  return (
    <div>
      {"*********************"}
      <Button
        id={"copy-secret"}
        onClick={useCallback(async (): Promise<void> => {
          const { clipboard } = navigator;

          await clipboard.writeText(value);
          document.execCommand("copy");
        }, [value])}
        variant={"secondary"}
      >
        <FontAwesomeIcon icon={faClipboard} />
      </Button>
    </div>
  );
};

export { SecretValue };
