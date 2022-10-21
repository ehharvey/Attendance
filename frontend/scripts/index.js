function getClasslist(){
    const Url = 'http://192.168.2.104:27501/students';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", Url, false ); // false for synchronous request
    xmlHttp.send( null );
    alert( xmlHttp.responseText);
}

function getCalendarEvent(){
    const Url = 'http://192.168.2.101:27501/nextevent';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", Url, false ); // false for synchronous request
    xmlHttp.send( null );
    alert( xmlHttp.responseText);
}

function getBackend(){
    // 192.168.2.103
    const Url = 'http://192.168.2.103:5000';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", Url, false ); // false for synchronous request
    xmlHttp.send( null );
    alert( xmlHttp.responseText);
}
