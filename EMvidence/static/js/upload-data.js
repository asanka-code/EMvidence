
$( function() {
    $( "#sdr-device" ).selectmenu(
        {
            width: 200
        }
    );
} );
  
$( function() {
    $( "#center-frequency-scale" ).selectmenu(
        {
            width: 200
        }
    );
} );
  
$( function() {
    $( "#sampling-rate" ).selectmenu(
        {
            width: 200
        }
    );
} );
  
$( function() {
    $( "#sampling-duration" ).selectmenu(
        {
            width: 200
        }
    );
} );
  
$( function() {
    $( "#hash-function" ).selectmenu(
        {
            width: 200
        }
    );
} );
  
$( function() {
    $( "#progressbar" ).progressbar({
        value: true
    });
  
    progressLabel = $( ".progress-label" );
    progressLabel.text("- Ready -");
} );
          
$( function() {
    $( ".widget input[type=submit]" ).button();
    $( ".widget input[type=file]" ).button();
    $( ".widget input[type=button]" ).button();
  
    $( "#upload-zip" ).click( function( event ) {
        event.preventDefault();
        // submit the selected EM trace file along with other information
        submitDataFile()
        //document.getElementById("add-module-form").submit();
    } );
  
    $( "#cancel-upload" ).click( function( event ) {
        event.preventDefault();
        window.location.href = "/settings";
    } );
} );
  
  
/*
function addData() {                                                  
    // a form data object
    var formData = new FormData();
  
    // take the selected file object
    formData.append("fileToUpload", $('input[type=file]')[0].files[0]);
            
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "done") {                                          
                alert("New module added successfully!");
                // refresh the settings page
                window.location.href = "/settings";
            } else {
                alert("Error occured while adding module!");
            }
        }
    };
  
    // send the AJAX request
    xhttp.open("POST", "/add_module", true);
    xhttp.send(formData);                    
}
*/
  
function submitDataFile() {
    // progress bar and its label objects
    progressbar = $( "#progressbar" );
    progressLabel = $( ".progress-label" );
  
    // update the progress bar status
    progressLabel.text("Uploading data...");
    progressbar.progressbar( "value", false);
  
    // a form data object
    var formData = new FormData();
  
    // take the selected SDR device index
    var sdr_choice = document.getElementById("sdr-device");
    var sdr = sdr_choice.options[sdr_choice.selectedIndex].value;
    // append sdr choice to the form data object
    formData.append("sdr", sdr);
  
    // take the center frequency for the SDR
    var center_frequency = document.getElementById("center-frequency").value;
    formData.append("center_frequency", center_frequency);
  
    // take the center frequency scale
    var center_frequency_scale = document.getElementById("center-frequency-scale");
    center_frequency_scale = center_frequency_scale.options[center_frequency_scale.selectedIndex].value;
    // append sampling rate choice to the form data object
    formData.append("center_frequency_scale", center_frequency_scale);
  
    // take the selected sampling rate index
    var sampling_rate = document.getElementById("sampling-rate");
    sampling_rate = sampling_rate.options[sampling_rate.selectedIndex].value;
    // append sampling rate choice to the form data object
    formData.append("sampling_rate", sampling_rate);
  
    // take the selected hash function index
    var hash_function = document.getElementById("hash-function");
    hash_function = hash_function.options[hash_function.selectedIndex].value;
    // append hash function choice to the form data object
    formData.append("hash_function", hash_function);
  
    // take the selected file object
    formData.append("fileToUpload", $('input[type=file]')[0].files[0]);
  
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
  
            // take the received JSON object
            var response = JSON.parse(this.response);
                
            // take the status
            var status = response["status"];
  
            if (status == "done") {
                // update progress bar status
                progressLabel.text("Done!");
                var val = progressbar.progressbar( "value" ) || 0;
                progressbar.progressbar( "value", true);
                  
                // set the figures visible
                document.getElementById("visualize-data").style.visibility = "visible";
  
                // realoading the iframe to show the graphs of the captured data
                var iframe = document.getElementById('captured-data-view');
                iframe.src = iframe.src;            
  
                // take and the file name
                var file_name = response["file_name"];                
                var message= "File name: ";
                message = message.concat(file_name);
                document.getElementById("file_name_info").innerText = message;
  
                // take the file size
                var file_size = response["file_size"];
                var message= "File size: ";
                message = message.concat(file_size);
                document.getElementById("file_size_info").innerText = message;
  
                // take the hash type
                var hash_type = response["hash_type"];
                var message= "Hash value ";
                message = message.concat("(", hash_type, "): ");
                // take the hash value
                var hash_value = response["hash_value"];
                message = message.concat(hash_value);                
                document.getElementById("hash_info").innerText = message;                               
  
            } else {
                // update progress bar status
                progressLabel.text("Something went wrong...");
                var val = progressbar.progressbar( "value" ) || 0;
                progressbar.progressbar( "value", true);  
            }
        }
    }
  
    // send the AJAX request
    xhttp.open("POST", "/upload-the-data-file", true);
    xhttp.send(formData);
}

