// This function corrects route
// requests to account for proxies
// (e.g., when running in the web VM)
function getRoute(route, route_prepend = window.location.pathname) {
    if (route.startsWith("/")) {
        return route_prepend + route.substring(1);
    }
    else {
        return route_prepend + route;
    }
}

function getClasslist() {
    logConsole("Getting Class List");
    const Url = getRoute('api/classlist');
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    alert(xmlHttp.responseText);
}

function getCalendarEvent() {
    logConsole("Getting Calendar Event");
    const Url = getRoute('/api/calendar');
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    alert(xmlHttp.responseText);
    return xmlHttp
}

function getSummary() {
    //const Url = 'http://192.168.2.103:5000/api/attendance';//swap IP for class
    const Url = getRoute('/api/attendance');
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    alert(xmlHttp.responseText);
}

function addAttendance(attendance_ID) {
    logConsole("Sending Backend Attendance");
    const attendance_json = {   //placeholder attendance data
        "id": attendance_ID,
        "records": [{
            "studentID": "ABC",
            "isPresent": true,
            "startDate": "someDate"
        }]
    }
    //const Url = 'http://192.168.2.103:5000/api/attendance/' + attendance_json.id;
    const Url = getRoute('/api/attendance/' + attendance_json.id); //localhost ip, change for class
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", Url, false); // false for synchronous request

    logConsole(attendance_json); //log json object for debugging
    console.log(attendance_json);
    xmlHttp.setRequestHeader("Content-Type", "application/json");
    xmlHttp.send(JSON.stringify(attendance_json));
    alert(xmlHttp.responseText);
}


/*------------------------------------------------------------------------------------------
* Function	        :	logConsole()
* Description	    :	This Function is used to log request and responses to the console.			
* Parameters	    :	String : the request or response to log to the console
* ------------------------------------------------------------------------------------------*/
function logConsole(loggingValue) {
    //Gets the date time
    if (loggingValue) {
        const d = Date();
        console.log("[" + loggingValue + "] " + d);
        return ("[" + loggingValue + "] " + d);
    }
    else {
        //logging page load
        const d = Date();
        console.log("[Page Load]" + " " + d);
        return ("[Page Load]" + " " + d);
    }
}

module.exports = {
    logConsole, addAttendance, getRoute
};