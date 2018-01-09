var myDate = new Date();
var greeting = "Hello World!";
/* hour is before noon */
if (myDate.getHours() < 12) {
    greeting = "Good Morning!";
}
else  /* Hour is from noon to 5pm (actually to 5:59 pm) */
if (myDate.getHours() >= 12 && myDate.getHours() <= 17) {
    greeting = "Good Afternoon!";
}
else  /* the hour is after 5pm, so it is between 6pm and midnight */
if (myDate.getHours() > 17 && myDate.getHours() <= 24) {
    greeting = "Good Evening!"
}
var result = greeting.fontsize(5).fontcolor("white");
document.getElementById("greeting").innerHTML = result;
