document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("createNewEndpointForm");
    console.log(form);
    form.addEventListener('submit', e => {
        // stop regular form submission process (form-data, syncronus)
        e.preventDefault();
        console.log(e); 
        // build your input
        const formData = {
            endpointDisplayName: form.elements.endpointDisplayNameInput.value
        }
        // make your fetch call
        endpointCreateFetchCall(formData);
    }); 

    var deleteButtons = document.querySelectorAll(".endpointDelete");
    deleteButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            var endpointID = this.value;
            const confirmed = window.confirm("Are you sure you want to delete this endpoint? This cannot be undone.");
            if (confirmed) {
                endpointDeleteFetchCall(endpointID)
            }
        });
    });   


    function endpointDeleteFetchCall(endpointID) {
        fetch("/endpoint/modify", {
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
        .then(deleteCallSucceeded) // Separate success callback for endpointDeleteFetchCall
        .catch(fetchCallFailed);
      }
    
      function deleteCallSucceeded(res) {
        console.log("Delete call succeeded:", res);
        // Handle the delete call response or do any other logic here if needed
        location.reload(); // Reload the page once the delete call is successful
      }

function endpointCreateFetchCall(formData) {
    // do your fetch implementation
    fetch("/endpoint/create", {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      method: "POST",
      body: JSON.stringify(formData)
    })
    .then(createCallSucceeded) // Separate success callback for doYourFetchCall
    .catch(fetchCallFailed);
  }
  
  function createCallSucceeded(res) {
    console.log("Create call succeeded:", res);
    // Handle the create call response or do any other logic here if needed
    location.reload(); // Reload the page once the create call is successful
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