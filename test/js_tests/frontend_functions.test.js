const { logConsole, addAttendance } = require('../../frontend/scripts/index');
//global.XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

test('Tests function consoleLog - empty', () => {
    const d = Date();
    expect(logConsole()).toBe("[Page Load]" + " " + d);
});

test('Tests function consoleLog - with message', () => {
    const d = Date();
    expect(logConsole("TestMessage 123")).toBe("[TestMessage 123] " + d);
});