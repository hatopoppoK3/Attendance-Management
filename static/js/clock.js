function setNumber(number) {
    if (number < 10) {
        return "0" + number;
    }
    return number;
}

function setScreenday() {
    const today = new Date();

    year = today.getFullYear();
    months = setNumber(today.getMonth() + 1);
    days = setNumber(today.getDate());
    screenDay = `${year}/${months}/${days}`;

    document.getElementById("screenDay").innerHTML = screenDay;
}
setTimeout(setScreenday, 0);

function setScreenTime() {
    const nowTime = new Date();

    const hours = setNumber(nowTime.getHours());
    const minutes = setNumber(nowTime.getMinutes());
    const seconds = setNumber(nowTime.getSeconds());
    const screenTime = `${hours}:${minutes}:${seconds}`;
    document.getElementById("screenTime").innerHTML = screenTime;
}
setInterval(setScreenTime, 1000);

function setParameter() {
    screenDay = document.getElementById("screenDay").textContent;
    screenTime = document.getElementById("screenTime").textContent;
    document.getElementById("submitTime").value = `${screenDay}/${screenTime}`;
}