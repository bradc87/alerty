document.addEventListener("DOMContentLoaded", function() {
    
    var statusUpdateButtons = document.querySelectorAll(".statusUpdateButton");
    statusUpdateButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            var newStatus = this.getAttribute("value");
            var alertID = this.getAttribute("alertid");
            alertID = alertID.replace("AL","");
            console.log(alertID);
            updateAlertStatusFetchCall(alertID, newStatus)
        });
    });   

    function updateAlertStatusFetchCall(alertID, newStatus) {
        console.log(JSON.stringify({ alertStatus: newStatus }));

        fetch(`/alert/${alertID}/status`, {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          method: "PUT",
          body: JSON.stringify({
            alertStatus: newStatus
          })
          
        })

        .then(updateCallSucceeded) // Separate success callback for updateAlertStatusFetchCall
        .catch(fetchCallFailed);
      }
    
      function updateCallSucceeded(res) {
        console.log("Alert update call succeeded:", res);
        // Handle the delete call response or do any other logic here if needed
        //location.reload(); // Reload the page once the delete call is successful
      }



function fetchCallFailed(err) {
  console.log(err)
}
});