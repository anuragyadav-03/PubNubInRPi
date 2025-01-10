var myChannel = "RSPY";
var alive_second = 0;
var heartbeat_rate = 5000;

function keep_alive() {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                if (this.responseText !== null) {
                    console.log("Client Response : ", this.responseText);
                    var date = new Date();
                    alive_second = date.getTime();
                    var json_obj = JSON.parse(this.responseText);

                    // Check motion and update UI
                    if (json_obj.motion == 1) {
                        document.getElementById("motion_id").innerHTML = "Yes";
                    } else {
                        document.getElementById("motion_id").innerHTML = "No";
                    }
                }
            } else {
                console.error("Error: Failed to get response from the server.");
            }
        }
    };
    
    request.onerror = function() {
        console.error("Error: Network request failed.");
    };

    request.open("GET", "keep_alive", true);
    request.send(null);

    setTimeout(keep_alive, heartbeat_rate);
}

function time() {
    var d = new Date();
    var current_sec = d.getTime();
    var connectionStatusElement = document.getElementById("Connection_id");

    if (current_sec - alive_second > heartbeat_rate + 1000) {
        connectionStatusElement.innerHTML = "<b>Dead</b>";
        connectionStatusElement.style.color = "red"; 
    } else {
        connectionStatusElement.innerHTML = "<b>Alive</b>";
        connectionStatusElement.style.color = "#4cd137"; 
    }

    setTimeout(time, 1000);
}

// LED state change listener
document.getElementById("led").addEventListener("change", function() {
    var ledState = this.checked ? 1 : 0;
    var ledStatusText = document.getElementById("led-status");

    if (this.checked) {
        ledStatusText.innerText = "LED: ON";
        console.log("LED state set: ON"); 
    } else {
        ledStatusText.innerText = "LED: OFF";
        console.log("LED state set: OFF"); 
    }

    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            console.log("LED state updated.");
        }
    };

    request.onerror = function() {
        console.error("Error: Failed to send LED state update.");
    };

    request.open("POST", "/status", true);
    request.setRequestHeader("Content-Type", "application/json");
    console.log("DataSentPost: ",JSON.stringify({ state: ledState }));
    request.send(JSON.stringify({ state: ledState }));
});

// Start the keep_alive and time functions
setTimeout(keep_alive, heartbeat_rate);
setTimeout(time, 1000);

pubnub = new PubNub({
    subscribe_key : 'sub-c-f3d64305-2b22-4b82-b72d-74fb6093fe74' ,
    publish_key : 'pub-c-fa518d5d-8837-4617-b351-101b4eca59e0' 

});

pubnub.addListener({
    status: function(statusEvent) {
        if(statusEvent.category === "PNConnectedCategory" ){    
            // Publish Message
        }
    },
    message: function(message){
        var msg = message.message;
    },

    presence: function(presenceEvent){
        // handle presence
    }

})

pubnub.subscribe({
    channels: [Iot_Channel]
})