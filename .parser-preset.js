module.exports = {
    parserOpts: {
        headerPattern: /^(\w*)\((\w*)\):\s(#\d+(.\d+)?)\s(.*)$/,
        headerCorrespondence: ['type', 'scope', 'ticket', 'part', 'subject']
    }
};
