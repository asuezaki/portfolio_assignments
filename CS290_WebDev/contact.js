// post form 
document.addEventListener("DOMContentLoaded", bindPostButton)
//function for contact post form
function bindPostButton(){
    document.getElementById("submits").addEventListener("click", function(event){
        var req = new XMLHttpRequest();
        var payload = {name: null, email: null, message: null};
        payload.name = document.getElementById("names").value;
        payload.email = document.getElementById("emails").value;
        payload.message = document.getElementById("messages").value;
        var url = "http://httpbin.org/post";
        req.open("POST", url, true);
        req.setRequestHeader("Content-Type", "application/json");
        req.addEventListener("load", function(){
            if (req.status >= 200 && req.status < 400){
                var response = JSON.parse(req.responseText);
                document.getElementById("input").textContent = "Your message: " + response.data;
                document.getElementById("response").textContent = "Message submitted successfully. Thank you!";
            } else {
                console.log("Error in network request: " + req.statusText);
            }
        });
        req.send(JSON.stringify(payload));
        event.preventDefault();
    });
}
