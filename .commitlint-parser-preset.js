module.exports = {
  parserOpts: {
    headerPattern: /^(all|forces|integrates|reviews|skims|sorts)\\(\w*)\((\w*)\):\s(#[1-9]\d*)(.\d+)?\s(.*)$/,
    headerCorrespondence: [ 'product', 'type', 'scope', 'ticket', 'part', 'subject' ],
  },
};
