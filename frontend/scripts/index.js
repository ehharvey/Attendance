function getClasslist() {
    //this.logConsole("Getting Class List");
    const Url = '/api/classlist';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    alert(xmlHttp.responseText);
}

function getCalendarEvent() {
    //logConsole("Getting Calendar Event");
    const Url = '/api/calendar';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    alert(xmlHttp.responseText);
    return xmlHttp
}

function getSummary() {
    //const Url = 'http://192.168.2.103:5000/api/attendance';//swap IP for class
    const Url = '/api/attendance';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    alert(xmlHttp.responseText);
}

function addAttendance(attendance_ID) {
    //exports.console_log("Sending Backend Attendance");
    const attendance_json = {   //placeholder attendance data
        "id": attendance_ID,
        "records": {
            "studentID": "ABC",
            "isPresent": true
        }
    }
    //const Url = 'http://192.168.2.103:5000/api/attendance/' + attendance_json.id;
    const Url = '/api/attendance/' + attendance_json.id; //localhost ip, change for class
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", Url, false); // false for synchronous request

    console.log(attendance_json); //log json object for debugging

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


