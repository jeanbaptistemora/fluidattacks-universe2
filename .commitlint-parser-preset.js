module.exports = {
  parserOpts: {
    headerPattern: /^(all|asserts|forces|integrates|observes|reviews|serves|skims|sorts|tools)\\(\w*)\((\w*)\):\s(#[1-9]\d*)(.\d+)?\s(.*)$/,
    headerCorrespondence: [ 'product', 'type', 'scope', 'ticket', 'part', 'subject' ],
  },
};
