{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "sorts-training-and-tune";
  searchPaths = {
    bin = [
      outputs."/sorts/training"
      outputs."/sorts/tune"
    ];
  };
  entrypoint = ''
    : \
      && sorts-training \
      && sorts-tune
  '';
}
