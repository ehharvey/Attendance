module.exports.console_log = function logConsole(loggingValue) {
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

function getClasslist() {
    //this.logConsole("Getting Class List");
    const Url = 'http://192.168.2.104:27501/students';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    alert(xmlHttp.responseText);
}

module.exports.getCalendar = function getCalendarEvent() {
    //logConsole("Getting Calendar Event");
    const Url = 'http://192.168.2.101:27501/nextevent';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    alert(xmlHttp.responseText);
    return xmlHttp
}

function getBackend() {
    logConsole("Getting Backend");
    // 192.168.2.103
    const Url = 'http://192.168.2.103:5000';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", Url, false); // false for synchronous request
    xmlHttp.send(null);
    alert(xmlHttp.responseText);
}

/*------------------------------------------------------------------------------------------
* Function	        :	logConsole()
* Description	    :	This Function is used to log request and responses to the console.			
* Parameters	    :	String : the request or response to log to the console
* ------------------------------------------------------------------------------------------*/


module.exports.add = function add(a, b) {
    return a + b;
}


