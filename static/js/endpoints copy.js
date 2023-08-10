document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("createNewEndpointForm");
    console.log(form);
    form.addEventListener('submit', e => {
        // stop regular form submission process (form-data, syncronus)
        //e.preventDefault();
        console.log(e); 
        // build your input
        const formData = {
            endpointDisplayName: form.elements.endpointDisplayNameInput.value
        }
        // make your fetch call
        doYourFetchCall(formData);
    }); 

    var deleteButtons = document.querySelectorAll(".endpointDelete");
    deleteButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            var endpointID = this.value;
            endpointDeleteFetchCall(endpointID)
        });
    });   


function endpointDeleteFetchCall(endpointID) {
    fetch("/endpoint/modify",
    {
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
    .then(fetchCallSucceeded)
    .catch(fetchCallFailed)
    
}

function doYourFetchCall(formData) {
  // do your fetch implementation
  fetch("/endpoint/create",
  {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      method: "POST",
      //body: JSON.stringify({a: 1, b: 2})
      body:JSON.stringify(formData)
  })
  .then(fetchCallSucceeded)
  .catch(fetchCallFailed)
  
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