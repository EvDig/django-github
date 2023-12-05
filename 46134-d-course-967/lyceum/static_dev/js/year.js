var year = document.getElementById("year");

function getServerTime()
{
    return new Date();
}

var clientTime = new Date();
var serverTime = getServerTime();

if (Math.abs(serverTime - clientTime) > 1000 * 60 * 60 * 24)
{
    clientTime = serverTime;
}

year.innerText = clientTime.getFullYear();