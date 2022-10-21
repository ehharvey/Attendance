function getClasslist(){
    const Url = 'http://192.168.2.104:27501/students';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", Url, false ); // false for synchronous request
    xmlHttp.send( null );
    alert( xmlHttp.responseText);
}

function getCalendarEvent(){
    const Url = 'http://localhost:27501/students';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", Url, false ); // false for synchronous request
    xmlHttp.send( null );
    alert( xmlHttp.responseText);
}

function getBackend(){
    // 192.168.2.102
    const Url = 'http://192.168.46.9:5000';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", Url, false ); // false for synchronous request
    xmlHttp.send( null );
    alert( xmlHttp.responseText);
}
