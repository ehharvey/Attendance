const { add, console_log, getCalendar } = require('../../frontend/scripts/index');

test('Tests placeholder function add', () => {
    expect(add(1, 2)).toBe(3);

});

test('Tests function consoleLog - empty', () => {
    const d = Date();
    expect(console_log()).toBe("[Page Load]" + " " + d);
});

test('Tests function consoleLog - empty', () => {
    const d = Date();
    expect(console_log("message123")).toBe("[message123] " + d);
});

test('Tests function getNextEvent', () => {
    const Url = 'http://192.168.2.101:27501/nextevent';
    var XMLHttpRequest = require('xhr2');
    var xmlHttp = new XMLHttpRequest();
    expect(getCalendar()).toBe(xmlHttp);
});