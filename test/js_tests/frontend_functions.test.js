const { logConsole, getRoute, addAttendance } = require('../../frontend/scripts/index');
//global.XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

test('Tests function consoleLog - empty', () => {
    const d = Date();
    expect(logConsole()).toBe("[Page Load]" + " " + d);
});

test('Tests function consoleLog - with message', () => {
    const d = Date();
    expect(logConsole("TestMessage 123")).toBe("[TestMessage 123] " + d);
});

test('Tests getRoute Proxied', () => {
    prepend = "/proxy/5000/";
    route = "/api/attendance";
    EXPECTED = "/proxy/5000/api/attendance"
    expect(getRoute(route, prepend)).toBe(EXPECTED);
});

test('Tests getRoute Unproxied', () => {
    prepend = "/";
    route = "/api/attendance";
    EXPECTED = "/api/attendance"
    expect(getRoute(route, prepend)).toBe(EXPECTED);
});
