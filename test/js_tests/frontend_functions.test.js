const { logConsole, addAttendance } = require('../../frontend/scripts/index');
global.XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

test('Tests function consoleLog - empty', () => {
    const d = Date();
    expect(logConsole()).toBe("[Page Load]" + " " + d);
});

test('Tests function consoleLog - with message', () => {
    const d = Date();
    expect(logConsole("TestMessage 123")).toBe("[TestMessage 123] " + d);
});

test('Sample test which accesses addAttendance', () => {
    const f = jest.spyOn(XMLHttpRequest, 'open');
    const testID = 55512;
    const attendance_json = {   //placeholder attendance data
        "id": testID,
        "records": {
            "studentID": "ABC",
            "isPresent": true
        }
    }
    const Url = '/api/attendance/' + testID; //localhost ip, change for class

    addAttendance(testID);

    expect(f).toHaveBeenCalledWith("POST", Url, false);
});

// test('Tests function getNextEvent', () => {
//     const Url = 'http://192.168.2.101:27501/nextevent';
//     var XMLHttpRequest = require('xhr2');
//     var xmlHttp = new XMLHttpRequest();
//     expect(getCalendar()).toBe(xmlHttp);
// });