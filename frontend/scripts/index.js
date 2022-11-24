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
    return xmlHttp.responseText;
}

function getCalendarEvent() {
    logConsole("Getting Calendar Event");
    const Url = getRoute('/api/calendar');
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

function getSummary() {
    //const Url = 'http://192.168.2.103:5000/api/attendance';//swap IP for class
    const Url = getRoute('/api/attendance');
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    //alert(xmlHttp.responseText);
    return xmlHttp.responseText;
}

function getAttendance(attendanceID) {
    //const Url = 'http://192.168.2.103:5000/api/attendance/'+ attendanceID;//swap IP for class
    const Url = getRoute('/api/attendance/' + attendanceID);
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    //alert(xmlHttp.responseText);
    return xmlHttp.responseText;
}

function addAttendance(attendance_json) {
    logConsole("Sending Backend Attendance");
    /*const attendance_json = {   //placeholder attendance data
        "id": attendance_ID,
        "records": {
            "studentID": "ABC",
            "isPresent": true
        }
    } */
    //const Url = 'http://192.168.2.103:5000/api/attendance/' + attendance_json.id;
    const Url = getRoute('/api/attendance/' + attendance_json.id); //localhost ip, change for class
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", Url, false); // false for synchronous request

    console.log(attendance_json); //log json object for debugging

    xmlHttp.setRequestHeader("Content-Type", "application/json");
    xmlHttp.send(JSON.stringify(attendance_json));
}

function fillAttendanceDropdown() {
    const dropDown = document.getElementById("select-5c86");
    const attendance_json = JSON.parse(getSummary());
    console.log(attendance_json);
    for (let i = 0; i < attendance_json.ids.length; i++) {
        const newOption = document.createElement("option");
        newOption.innerText = "Attendance " + attendance_json.ids[i];
        newOption.value = attendance_json.ids[i];
        dropDown.appendChild(newOption);
    }
}

function fillStudentList() {
    const studentTable = document.getElementById("studentList");
    const students = JSON.parse(getClasslist());
    for (let i = 0; i < students.length; i++) {
        const newRow = document.createElement("tr");
        newRow.style = "height: 21px;";

        const newNameCell = document.createElement("td");
        newNameCell.classList.add("u-border-1", "u-border-grey-30", "u-first-column", "u-grey-5", "u-table-cell", "u-table-cell-39");
        newNameCell.innerText = students[i].firstname + " " + students[i].lastname;

        const newNumberCell = document.createElement("td");
        newNumberCell.classList.add("u-border-1", "u-border-grey-30", "u-table-cell");
        newNumberCell.innerText = students[i].studentNumber;

        newRow.appendChild(newNameCell);
        newRow.appendChild(newNumberCell);
        studentTable.appendChild(newRow);
    }
}

function fillNextAttendance() {
    const nextAttendance = JSON.parse(getCalendarEvent());
    const students = JSON.parse(getClasslist());
    const title = document.getElementById("nextAttendanceTitle");
    const time = document.getElementById("nextAttendanceTime");
    title.innerText = "Attendance for: " + nextAttendance.title;
    time.innerText = "(ends " + nextAttendance.dueDate + ")";

    const form = document.getElementById("attendanceForm");

    for (let i = 0; i < students.length; i++) {
        //input + label -> inputRows -> wrapper + label -> formGroups ->form
        const row = document.createElement("div");
        row.classList.add("u-form-group", "u-form-input-layout-horizontal", "u-form-radiobutton", "u-label-left", "u-form-group-4");

        const rowLabel = document.createElement("label");
        rowLabel.classList.add("u-label", "u-spacing-10", "u-label-2")
        rowLabel.innerText = students[i].firstname + " " + students[i].lastname + " - " + students[i].studentNumber;

        const buttonWrapper = document.createElement("div");
        buttonWrapper.classList.add("u-form-radio-button-wrapper");

        const rowPresent = document.createElement("div");
        rowPresent.classList.add("u-input-row");

        const presentRadio = document.createElement("input");
        presentRadio.type = "radio";
        presentRadio.value = "Present";
        presentRadio.required = "required";
        presentRadio.checked = "checked";
        presentRadio.id = students[i].studentNumber;
        presentRadio.name = "radio" + i;
        const presentLabel = document.createElement("label");
        presentLabel.htmlFor = "radio" + i;
        presentLabel.classList.add("u-label", "u-spacing-10", "u-label-4");
        presentLabel.innerText = "Present";


        const rowAbsent = document.createElement("div");
        rowAbsent.classList.add("u-input-row");

        const absentRadio = document.createElement("input");
        absentRadio.type = "radio";
        absentRadio.value = "Absent";
        absentRadio.required = "required";
        absentRadio.name = "radio" + i;
        const absentLabel = document.createElement("label");
        absentLabel.htmlFor = "radio" + i;
        absentLabel.classList.add("u-label", "u-spacing-10", "u-label-4");
        absentLabel.innerText = "Absent";

        rowPresent.appendChild(presentRadio);
        rowPresent.appendChild(presentLabel);

        rowAbsent.appendChild(absentRadio);
        rowAbsent.appendChild(absentLabel);

        buttonWrapper.appendChild(rowPresent);
        buttonWrapper.appendChild(rowAbsent);

        row.appendChild(rowLabel);
        row.appendChild(buttonWrapper);

        form.appendChild(row);
    }
    const buttonRow = document.createElement("div");
    buttonRow.classList.add("u-form-group", "u-form-submit", "u-label-left");

    const buttonSpacer = document.createElement("label");
    buttonSpacer.classList.add("u-label", "u-spacing-10", "u-label-17");

    const buttonContainer = document.createElement("div");
    buttonContainer.classList.add("u-align-left", "u-btn-submit-container");

    const buttonInput = document.createElement("input");
    buttonInput.type = "submit";
    buttonInput.value = "submit";
    buttonInput.classList.add("u-form-control-hidden");
    buttonInput.onclick = "addAttendance()";

    const buttonMessageSuccess = document.createElement("div");
    buttonMessageSuccess.classList.add("u-form-send-message", "u-form-send-message-success");
    buttonMessageSuccess.innerText = "New Attendance has been submitted, thank you!";

    const buttonMessageFailure = document.createElement("div");
    buttonMessageFailure.classList.add("u-form-send-message", "u-form-send-message-error");
    buttonMessageFailure.innerText = "Attendance was not submitted, please fix errors and try again.";

    const button = document.createElement("a");
    button.classList.add("u-btn", "u-btn-round", "u-btn-submit", "u-btn-style", "u-radius-50", "u-btn-2");
    button.onclick = function () { submitNextAttendance(); };
    button.innerText = "Submit";

    buttonContainer.appendChild(button);
    buttonContainer.appendChild(buttonInput);

    buttonRow.appendChild(buttonSpacer);
    buttonRow.appendChild(buttonContainer);

    form.appendChild(buttonRow);
    //form.appendChild(buttonMessageSuccess); commented out because messages were not hidden
    //form.appendChild(buttonMessageFailure); as intended, will fix later if messages are needed
}
function submitNextAttendance() {
    const nextAttendance = JSON.parse(getCalendarEvent());
    let attendanceString = '{"id": "' + nextAttendance.enterpriseID + '", "records": [';
    let formOptions = document.getElementsByClassName("u-form-radiobutton");
    let numOptions = formOptions.length;
    for (let i = 0; i < numOptions; i++) {
        if (i > 0) {
            attendanceString += ', ';
        }
        attendanceString += '{"studentID": ';
        let label = formOptions[i].lastChild.firstChild.firstChild.id;
        attendanceString += label;
        attendanceString += ', "isPresent": '
        if (formOptions[i].lastChild.firstChild.firstChild.checked) {
            attendanceString += 'true}';
        }
        else {
            attendanceString += 'false}';
        }
    }

    attendanceString += ']}'
    console.log(attendanceString);
    addAttendance(JSON.parse(attendanceString));
}

function fillPastAttendance() {
    const dropDown = document.getElementById("select-5c86");
    const selected = dropDown.value;
    const attendance = JSON.parse(getAttendance(selected));
    const table = document.getElementById("pastAttendanceTableBody");
    for (let i = 0; i < table.childElementCount; i++) {//clear table
        table.children[i].remove();
    }

    for (let i = 0; i < attendance.records.length; i++) {
        const row = document.createElement("tr");
        row.style = "height: 50px;";

        const nameBox = document.createElement("td");
        nameBox.classList.add("u-border-1", "u-border-black", "u-first-column", "u-grey-5", "u-table-cell", "u-table-cell-4");

        nameBox.innerText = attendance.records[i].studentID;

        const numberBox = document.createElement("td");
        numberBox.classList.add("u-border-1", "u-border-grey-30", "u-table-cell");

        numberBox.innerText = attendance.records[i].studentID;

        const presentBox = document.createElement("td");
        presentBox.classList.add("u-border-1", "u-border-grey-30", "u-table-cell");

        if (attendance.records[i].isPresent) {
            presentBox.innerText = "Present";
        }
        else {
            presentBox.innerText = "Absent";
        }

        row.appendChild(nameBox);
        row.appendChild(numberBox);
        row.appendChild(presentBox);

        table.appendChild(row);
    }
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