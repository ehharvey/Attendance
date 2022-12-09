function goHome() {
    fetch("/api/home_url")
        .then(res => res.json())
        .then((j) => {
            if ("url" in j) {
                console.log("Going to ", j.url)
                window.location = (j.url)
            } else {
                alert("Error trying to go home. Received: " + j.toString())
            }
        })
        .catch((error) => { alert(error) })
}

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
    const Url = getRoute('api/classlist');
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    localStorage.setItem('classlist', xmlHttp.responseText);
    return xmlHttp.responseText;
}

function getCalendarEvent() {
    const Url = getRoute('/api/calendar');
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    localStorage.setItem('calendar', xmlHttp.responseText);
    return xmlHttp.responseText;
}

function getSummary() {
    const Url = getRoute('/api/attendance');
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    localStorage.setItem('pastAttendances', xmlHttp.responseText);
    return JSON.parse(xmlHttp.responseText);
}

function getAttendance(attendanceID) {
    //const Url = 'http://192.168.2.103:5000/api/attendance/'+ attendanceID;//swap IP for class
    const Url = getRoute('/api/attendance/' + attendanceID);
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

function addAttendance(attendance_json) {
    const dropDown = document.getElementById("select-5c86");
    const oldDropDownValue = dropDown.value;

    logConsole("Sending Backend Attendance");
    const Url = getRoute('/api/attendance/' + attendance_json.id); //localhost ip, change for class

    fetch(Url,
        {
            method: "POST",
            body: JSON.stringify(attendance_json),
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then((response) => {
            if (response.status >= 200 && response.status < 300) {
                getSummary();
                getCalendarEvent();
                getClasslist();
                fillAttendanceDropdown();
                dropDown.value = oldDropDownValue;
                fillPastAttendance();
                alert("Attendance was sucessfully created! Any unset students have been marked ABSENT.")
                window.scrollTo(0, 0);
            } else {
                response.text().then(
                    (error_text) => {
                        alert("Attendance was not successfully updated. Received: " + response.status + ": " + error_text)
                    }
                )
            }
        })
        .catch((error) => {
            alert(error)
        })

    console.log("End of addAttendance")
}

function updateAttendance(attendance_json) {
    const dropDown = document.getElementById("select-5c86");
    const oldDropDownValue = dropDown.value;
    logConsole("Sending Backend Attendance");
    const Url = getRoute('/api/attendance/' + attendance_json.id); //localhost ip, change for class

    fetch(Url,
        {
            method: "PUT",
            body: JSON.stringify(attendance_json),
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then((response) => {
            if (response.status >= 200 && response.status < 300) {
                getSummary();
                getCalendarEvent();
                getClasslist();
                fillAttendanceDropdown();
                dropDown.value = oldDropDownValue;
                fillPastAttendance();
                alert("Attendance was sucessfully updated!")
                window.scrollTo(0, 0);
            } else {
                response.text().then(
                    (error_text) => {
                        alert("Attendance was not successfully updated. Received: " + response.status + ": " + error_text)
                    }
                )
            }
        })
        .catch((error) => {
            alert(error)
        })
}

function fillAttendanceDropdown(teacherMode = true) {
    const dropDown = document.getElementById("select-5c86");
    dropDown.innerText = '';
    const pastAttendances = localStorage.getItem('pastAttendances');
    const pastAttendance_json = JSON.parse(pastAttendances);

    let completed = Array();

    const futureAttendance_json = JSON.parse(localStorage.getItem("calendar"));
    for (let i = 0; i < futureAttendance_json.length; i++) { //future attendances
        const newOption = document.createElement("option");
        newOption.innerText = "Attendance " + futureAttendance_json[i].eID;
        let label = "(" + futureAttendance_json[i].eID + ") " + futureAttendance_json[i].title + " | " + futureAttendance_json[i].tag;
        let l = (80 - label.length) % 6;

        newOption.value = futureAttendance_json[i].eID;

        let isSavedAttendance = pastAttendance_json.ids.includes(futureAttendance_json[i].eID);

        if (isSavedAttendance) {
            newOption.innerHTML = label.padEnd(122 - l, "&emsp;") + " (Completed)";
        } else {
            newOption.innerHTML = label;
        }

        if (!(teacherMode)) {
            if (isSavedAttendance) {
                dropDown.appendChild(newOption);
            }
        } else {
            dropDown.appendChild(newOption);
        }
    }
}

function editOldAttendance() { //triggered by re-submit button
    const dropDown = document.getElementById("select-5c86");
    const selected = dropDown.value;

    let attendanceString = '{"id": "' + selected + '", "records": [';
    let formOptions = document.getElementsByClassName("u-form-radiobutton");
    let numOptions = formOptions.length;
    for (let i = 0; i < numOptions; i++) {
        if (i > 0) {
            attendanceString += ', ';
        }
        attendanceString += '{"studentID": "';
        let label = formOptions[i].lastChild.firstChild.firstChild.id;
        attendanceString += label;
        attendanceString += '", "isPresent": '
        if (formOptions[i].lastChild.firstChild.firstChild.checked) {
            attendanceString += 'true}';
        }
        else {
            attendanceString += 'false}';
        }
    }
    attendanceString += ']}'

    console.log(attendanceString);
    updateAttendance(JSON.parse(attendanceString));
}

function submitNewAttendance() {//triggered by submit button
    const dropDown = document.getElementById("select-5c86");
    const selected = dropDown.value;
    const futureEvents = JSON.parse(localStorage.getItem("calendar"));

    for (let i = 0; i < futureEvents.length; i++) {
        if (futureEvents[i].eID === selected) {
            var selectedEvent = futureEvents[i];
        }
    }


    let attendanceString = '{"id": "' + selectedEvent.eID + '", "records": [';
    let formOptions = document.getElementsByClassName("u-form-radiobutton");
    let numOptions = formOptions.length;
    for (let i = 0; i < numOptions; i++) {
        if (i > 0) {
            attendanceString += ', ';
        }
        attendanceString += '{"studentID": ';
        let label = formOptions[i].lastChild.firstChild.firstChild.id; //gets id of radio buttons
        attendanceString += label;                                      //which is set to studentNumber of student it reps.
        attendanceString += ', "isPresent": '
        if (formOptions[i].lastChild.firstChild.firstChild.checked) {
            attendanceString += 'true}';
        }
        else {
            attendanceString += 'false}';
        }
    }

    attendanceString += ']}'
    addAttendance(JSON.parse(attendanceString));
}

function fillPastAttendance(teacherMode = true) { //triggered by the retrieve attendance button
    const page = document.getElementById("page-base");
    const form = document.getElementById("form-students");
    form.innerHTML = "";

    const dropDown = document.getElementById("select-5c86");
    const selected = dropDown.value;

    if (selected) {
        const students = JSON.parse(localStorage.getItem('classlist'));
        const pastAttendances = localStorage.getItem('pastAttendances');
        const pastAttendance_json = JSON.parse(pastAttendances)

        const completedAttendance = pastAttendance_json.ids.includes(selected);

        if (completedAttendance) {
            const attendance = JSON.parse(getAttendance(selected));
            const classlist = JSON.parse(localStorage.getItem("classlist"));
            for (let i = 0; i < attendance.records.length; i++) {
                const name_label = document.createElement("p");
                name_label.classList.add("u-form-group", "u-form-partition-factor-3", "u-form-text", "u-text", "u-text-1");

                for (let j = 0; j < classlist.length; j++) {    //match studentID against studentNumbers from classlist to find name
                    if (String(classlist[j].studentNumber) === attendance.records[i].studentID) {
                        var studentName = classlist[j].firstname + " " + classlist[j].lastname;

                        classlist.splice(j, 1);//remove classlist student so it doesnt get matched again

                        break;
                    }

                }
                if (typeof studentName === 'undefined') { //reuse student number if no name could be found/matched
                    studentName = "UNKNOWN";
                }

                name_label.innerText = studentName;

                const number_label = document.createElement("p");
                number_label.classList.add("u-form-group", "u-form-partition-factor-3", "u-form-text", "u-text", "u-text-2");

                if (teacherMode) {
                    number_label.innerText = attendance.records[i].studentID;
                } else {
                    number_label.innerText = "";
                }


                const form_group = document.createElement("div");
                form_group.classList.add("u-form-group", "u-form-input-layout-horizontal", "u-form-partition-factor-3", "u-form-radiobutton", "u-form-group-5");

                const hidden_label = document.createElement("label");
                hidden_label.classList.add("u-form-control-hidden", "u-label");

                const buttonWrapper = document.createElement("div");
                buttonWrapper.classList.add("u-form-radio-button-wrapper");

                const rowPresent = document.createElement("div");
                rowPresent.classList.add("u-input-row");

                const presentRadio = document.createElement("input");
                presentRadio.type = "radio";
                presentRadio.value = "Present";
                presentRadio.required = "required"; {
                    if (attendance.records[i].isPresent)
                        presentRadio.checked = "checked";
                }
                presentRadio.id = attendance.records[i].studentID;
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
                if (!attendance.records[i].isPresent) {
                    absentRadio.checked = "checked";
                }
                absentRadio.name = "radio" + i;
                const absentLabel = document.createElement("label");
                absentLabel.htmlFor = "radio" + i;
                absentLabel.classList.add("u-label", "u-spacing-10", "u-label-4");
                absentLabel.innerText = "Absent";

                if (!teacherMode) {
                    presentRadio.disabled = true;
                    absentRadio.disabled = true;
                }

                rowPresent.appendChild(presentRadio);
                rowPresent.appendChild(presentLabel);

                rowAbsent.appendChild(absentRadio);
                rowAbsent.appendChild(absentLabel);

                buttonWrapper.appendChild(rowPresent);
                buttonWrapper.appendChild(rowAbsent);

                form_group.appendChild(hidden_label);
                form_group.appendChild(buttonWrapper);

                form.appendChild(name_label);
                form.appendChild(number_label);
                form.appendChild(form_group);

                var buttonText = "Re-Submit";
                var buttonFunction = function () { editOldAttendance(); };
            }
        }
        else { //non-completed attendance
            for (let i = 0; i < students.length; i++) {
                const name_label = document.createElement("p");
                name_label.classList.add("u-form-group", "u-form-partition-factor-3", "u-form-text", "u-text", "u-text-1");
                name_label.innerText = students[i].firstname + " " + students[i].lastname;

                const number_label = document.createElement("p");
                number_label.classList.add("u-form-group", "u-form-partition-factor-3", "u-form-text", "u-text", "u-text-2");
                number_label.innerText = students[i].studentNumber;

                const form_group = document.createElement("div");
                form_group.classList.add("u-form-group", "u-form-input-layout-horizontal", "u-form-partition-factor-3", "u-form-radiobutton", "u-form-group-5");

                const hidden_label = document.createElement("label");
                hidden_label.classList.add("u-form-control-hidden", "u-label");

                const buttonWrapper = document.createElement("div");
                buttonWrapper.classList.add("u-form-radio-button-wrapper");

                const rowPresent = document.createElement("div");
                rowPresent.classList.add("u-input-row");

                const presentRadio = document.createElement("input");
                presentRadio.type = "radio";
                presentRadio.value = "Present";
                presentRadio.required = "required";
                //presentRadio.checked = "checked";
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

                form_group.appendChild(hidden_label);
                form_group.appendChild(buttonWrapper);

                form.appendChild(name_label);
                form.appendChild(number_label);
                form.appendChild(form_group);

                var buttonText = "Submit";
                var buttonFunction = function () { submitNewAttendance(); };
            }
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

        const button = document.createElement("a");
        button.classList.add("u-btn", "u-btn-round", "u-btn-submit", "u-btn-style", "u-radius-50", "u-btn-2");
        button.onclick = buttonFunction;//button function and text dependant on 
        button.innerText = buttonText;//completed attendance or new attendance

        buttonContainer.appendChild(button);
        buttonContainer.appendChild(buttonInput);

        buttonRow.appendChild(buttonSpacer);
        buttonRow.appendChild(buttonContainer);

        form.appendChild(buttonRow);
        page.appendChild(form);
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
    logConsole, addAttendance, updateAttendance, getRoute
};
