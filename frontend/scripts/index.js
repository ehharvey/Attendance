console.log("Hello World")

function getClasslist(){
    const Url = 'http://localhost:27501/students';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", Url, false ); // false for synchronous request
    xmlHttp.send( null );
    alert( xmlHttp.responseText);
}