const functionA = require('../../frontend/scripts/index');

test('Tests function consoleLog - empty', () => {
    const d = Date();
    expect(functionA()).toBe("[Page Load]" + " " + d);
});

// test('Tests function consoleLog - empty', () => {
//     const d = Date();
//     expect(logConsole("message123")).toBe("[message123] " + d);
// });

// test('Tests function getNextEvent', () => {
//     const Url = 'http://192.168.2.101:27501/nextevent';
//     var XMLHttpRequest = require('xhr2');
//     var xmlHttp = new XMLHttpRequest();
//     expect(getCalendar()).toBe(xmlHttp);
// });