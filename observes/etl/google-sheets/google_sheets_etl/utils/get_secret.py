from fa_purity import (
    Cmd,
    JsonObj,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
)
from fa_purity.json.factory import (
    loads,
)
from google_sheets_etl.utils.process import (
    RunningSubprocess,
    Subprocess,
)
from google_sheets_etl.utils.temp_file import (
    TempFile,
)
from pathlib import (
    Path,
)


def get_secret(file_path: Path) -> Cmd[JsonObj]:
    out = TempFile.new()

    def save(file: TempFile) -> Cmd[None]:
        def _action(unwrapper: CmdUnwrapper) -> None:
            with file.path.open("w") as f:
                process = RunningSubprocess.run_universal_newlines(
                    Subprocess(
                        (
                            "sops",
                            "--aws-profile",
                            "default",
                            "--decrypt",
                            "--output-type",
                            "json",
                            file_path.as_posix(),
                        ),
                        None,
                        f,
                        None,
                    )
                )
                result = unwrapper.act(process.bind(lambda p: p.wait(None)))
                if result == 0:
                    return
                raise Exception(
                    f"Sops call return code error != 0 i.e. code {result}"
                )

        return Cmd.new_cmd(_action)

    return (
        out.bind(lambda f: save(f).map(lambda _: f))
        .bind(lambda f: f.read_lines().to_list().map("".join))
        .map(loads)
        .map(lambda r: r.alt(Exception).unwrap())
    )
