document.addEventListener("DOMContentLoaded", function() {
    
    var deleteButtons = document.querySelectorAll(".statusUpdateButton");
    statusUpdateButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            var newStatus = this.value;
            var alertID = this.alertID;
            updateAlertStatusFetchCall(alertID, newStatus)
        });
    });   

    function updateAlertStatusFetchCall(alertID, newStatus) {
        fetch("/endpoint/alert/<alertID>/status", {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          method: "POST",
          body: JSON.stringify({
            "endpointID": endpointID,
            "modifyAction": "delete"
          })
        })
        .then(deleteCallSucceeded) // Separate success callback for updateAlertStatusFetchCall
        .catch(fetchCallFailed);
      }
    
      function deleteCallSucceeded(res) {
        console.log("Delete call succeeded:", res);
        // Handle the delete call response or do any other logic here if needed
        location.reload(); // Reload the page once the delete call is successful
      }


function fetchCallSucceeded(res) {
  console.log(res)
  location.reload()
  window.reload()
}
function fetchCallFailed(err) {
  console.log(err)
}
});