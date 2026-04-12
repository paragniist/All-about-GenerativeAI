//base.js

function formsubmit(){
    const query = document.getElementById("query").value;
    const fileinput = document.getElementById("file").value;
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file before submitting!");
        return;
    }
    const formdata = new FormData();
    formdata.append("query", query);
    formdata.append("file", file);
    fetch("/upload", {
        method: "POST",
        body: formdata
    }).then(response => response.json()).then(data => {
        console.log(data);
    }).catch(error => {
        console.error("Error:", error);
    });

}