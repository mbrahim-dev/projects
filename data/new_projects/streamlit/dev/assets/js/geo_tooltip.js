function(params) {
    const d = params.data;

    if (!d || d.actualValue === undefined) {
        return params.name || '';
    }

    const value = Number(d.actualValue);

    const formattedValue = value.toLocaleString(
        undefined,
        {
            minimumFractionDigits: 0,
            maximumFractionDigits: 2
        }
    );

    const displayValue =
        d.format === 'currency'
            ? '$' + formattedValue
            : formattedValue;

    return '<b>' + d.city + '</b><br/>' +
        d.country + '<br/>' +
        '<span style="color:' +
        params.color + '">●</span> ' +
        d.name + ': ' + displayValue;
}