function getClasslist() {
    //this.logConsole("Getting Class List");
    const Url = '/api/classlist';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    alert(xmlHttp.responseText);
    return xmlHttp;
}

function getCalendarEvent() {
    //logConsole("Getting Calendar Event");
    const Url = '/api/calendar';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    alert(xmlHttp.responseText);
    return xmlHttp;
}

function getSummary() {
    //const Url = 'http://192.168.2.103:5000/api/attendance';//swap IP for class
    const Url = '/api/attendance';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    alert(xmlHttp.responseText);
    return xmlHttp;
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
    return xmlHttp;
}

function fillAttendanceDropdown() {
    const dropDown = document.getElementById("select-5c86");
    const options = dropDown.getElementsByTagName("option");
    const attendance_json = JSON.parse(getSummary().responseText);
    console.log(attendance_json);
    for (let i = 0; i < attendance_json.ids.length; i++) {
        const newOption = document.createElement("option");
        newOption.innerText = "Attendance " + attendance_json.ids[i];
        dropDown.appendChild(newOption);
    }
    //options[0].innerText = "Attendance " + attendance_json.ids[0];
    //options[1].innerText = "Attendance " + attendance_json.ids[1];
    //options[2].innerText = "test";
    //console.log(options);
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


