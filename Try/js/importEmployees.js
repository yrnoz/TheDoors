
function importEmployees() {

    var fileToLoad = document.getElementById("employees_input").files[0];
    $.ajax({
        type: "POST",
        url: "./import_employees_aux.py",
        data: { param: fileToLoad},
        success: callbackFunc

    });
    function callbackFunc(response) {
        // do something with the response
        alert("Great Success!");
    }

    /*
    var fileReader = new FileReader();
    fileReader.onload = function (fileLoadedEvent) {
        var textFromFileLoaded = fileLoadedEvent.target.result;
    };
    fileReader.readAsText(fileToLoad, "UTF-8");
    */
}