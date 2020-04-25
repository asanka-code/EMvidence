
$(document).ready( function() {
    // fill the default directory field
    fillDefaultDirectory();
    // set the EM data format
    setEMdataFormat();
    // set the modules selection menu
    setModuleSelectionList();
    // set the IoT devices selection menu
    setIoTDeviceSelectionList();
    // set the datasets selection menu
    setDatasetSelectionList();
} );
  
$( function() {
    $( "#em-data-format" ).selectmenu(
        {
            width: 200
        }
    );
} );
  
$( function() {
    $( "#select-module-to-delete" ).selectmenu(
        {
            width: 400
        }
    );
} );
  
$( function() {
    $( "#select-dataset-to-delete" ).selectmenu(
        {
            width: 400
        }
    );
} );
  
$( function() {
    $( "#select-iot-device-to-delete" ).selectmenu(
        {
            width: 400
        }
    );
} );        
  
$( function() {
    $( ".save-button button" ).button();
    $( ".save-button button" ).click( function( event ) {
        event.preventDefault();
        // submit the data to the backend
        saveSettings();
    } );
} );
  
$( function() {
    $( ".cancel-button button" ).button();
    $( ".cancel-button button" ).click( function( event ) {
        event.preventDefault();
            window.location.href = "/settings";
    } );
} );
  
$( function() {
    $( ".widget input[type=submit]" ).button();
    $( ".widget input[type=file]" ).button();
    $( ".widget input[type=button]" ).button();
  
    $( "#upload-zip" ).click( function( event ) {
        event.preventDefault();
        // submit the selected ZIP file            
        addModule()
        //document.getElementById("add-module-form").submit();
    } );
  
    $( "#cancel-upload" ).click( function( event ) {
        event.preventDefault();
        window.location.href = "/settings";
    } );
} );

function addModule() {                                                  
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
  
$( function() {          
    $( ".module-delete-widget input[type=button]" ).button();

    $( "#delete-module" ).click( function( event ) {
        event.preventDefault();
        // send the module deletion AJAX request
        deleteModule();
    } );
  
    $( "#cancel-delete" ).click( function( event ) {
        event.preventDefault();
        window.location.href = "/settings";            
    } );
} );
  
function deleteModule() {            
    // a form data object
    var formData = new FormData();
  
    // take the selected em data format index
    var module_to_delete = document.getElementById("select-module-to-delete");
    module_to_delete = module_to_delete.options[module_to_delete.selectedIndex].value;
    // append sampling rate choice to the form data object
    formData.append("module_to_delete", module_to_delete);
  
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "done") {                                          
                alert("Module deleted!");
                // refresh the settings page
                window.location.href = "/settings";
            } else {
                alert("Error occured while deleting!");
            }
        }
    };
  
    // send the AJAX request
    xhttp.open("POST", "/delete_module", true);
    xhttp.send(formData);
}
  
$( function() {          
    $( ".dataset-delete-widget input[type=button]" ).button();
        $( "#delete-dataset" ).click( function( event ) {
            event.preventDefault();
            // send the module deletion AJAX request
            deleteDataset();
        } );
  
        $( "#cancel-delete-dataset" ).click( function( event ) {
            event.preventDefault();
            window.location.href = "/settings";            
        } );
} );
  
function deleteDataset() {            
    // a form data object
    var formData = new FormData();
  
    // take the selected em data format index
    var dataset_to_delete = document.getElementById("select-dataset-to-delete");
    dataset_to_delete = dataset_to_delete.options[dataset_to_delete.selectedIndex].value;
    // append sampling rate choice to the form data object
    formData.append("dataset_to_delete", dataset_to_delete);
  
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "done") {                                          
                alert("Dataset deleted!");
                // refresh the settings page
                window.location.href = "/settings";
            } else {
                alert("Error occured while deleting!");
            }
        }
    };
  
    // send the AJAX request
    xhttp.open("POST", "/delete_dataset", true);
    xhttp.send(formData);
}
          
function fillDefaultDirectory() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            $("#default-capture-directory").val(this.responseText);              
        }
    };
    
    // send the AJAX request
    xhttp.open("POST", "/get_default_directory", true);
    xhttp.send();
}
    
function setEMdataFormat() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {              
            $("#em-data-format").val(this.responseText);
            $( "#em-data-format" ).selectmenu("refresh", true);
        }
    };

    // send the AJAX request
    xhttp.open("POST", "/get_em_data_format", true);
    xhttp.send();
}
          
function saveSettings() {            
    // a form data object
    var formData = new FormData();
  
    // take the default capture directory
    var capture_directory = document.getElementById("default-capture-directory").value;          
    // append the default capture directory to form data object
    formData.append("capture_directory", capture_directory);
  
    // take the selected em data format index
    var em_data_format = document.getElementById("em-data-format");
    em_data_format = em_data_format.options[em_data_format.selectedIndex].value;
    // append sampling rate choice to the form data object
    formData.append("em_data_format", em_data_format);
  
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "done") {                          
                // set the figures visible
                //document.getElementById("visualize-data").style.visibility = "visible";
                alert("Settings saved");
            } else {
                alert("Error occured while saving");
            }
        }
    };
  
    // send the AJAX request
    xhttp.open("POST", "/save_settings", true);
    xhttp.send(formData);
}  
  
$( function() {
    $( ".save-iot-button button" ).button();
    $( ".save-iot-button button" ).click( function( event ) {
        event.preventDefault();
        // submit the data to the backend
        saveIoTDevice();
    } );
} );
  
$( function() {
    $( ".cancel-iot-button button" ).button();
    $( ".cancel-iot-button button" ).click( function( event ) {
        event.preventDefault();
        window.location.href = "/settings";
    } );
} );
  
function saveIoTDevice() {            
    // a form data object
    var formData = new FormData();
  
    // take the new IoT devife name
    var new_iot_device_name = document.getElementById("new-iot-device-name").value;          
    // append the new IoT device name to form data object
    formData.append("new_iot_device_name", new_iot_device_name);
  
    // take the new IoT devife description
    var new_iot_device_description = document.getElementById("new-iot-device-description").value;
    // append the new IoT device description to form data object
    formData.append("new_iot_device_description", new_iot_device_description);
  
  
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "done") {                          
                // set the figures visible
                //document.getElementById("visualize-data").style.visibility = "visible";
                alert("IoT device added");
                // clear the content of the fields
                document.getElementById("new-iot-device-name").value = "";
                document.getElementById("new-iot-device-description").value = "";
  
                // refresh the select menu to make the newly added options visible
                window.location.href = "/settings";
            } else {
                alert("Error occured while adding!");
            }
        }
    };
  
    // send the AJAX request
    xhttp.open("POST", "/add-iot-device", true);
    xhttp.send(formData);
}
          
function setDatasetSelectionList() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
  
            // take the received JSON object
            var response = JSON.parse(this.response);
                
            // take the number of IoT devices
            var len = parseInt(response["length"]);
  
            // process each IoT device
            for (var i=1; i<=len; i++) {          
                // add the option to the select menu
                $('#select-dataset-to-delete').append($('<option>', {
                    value: response[i.toString()]["value"],
                    text: response[i.toString()]["text"]
                }));
            }
                
            // refresh the select menu to make the newly added options visible
            $( "#select-dataset-to-delete" ).selectmenu("refresh", true);
        }
    };

    // send the AJAX request
    xhttp.open("POST", "/get_dataset_list", true);
    xhttp.send();
}
  
function setModuleSelectionList() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
  
            // take the received JSON object
            var response = JSON.parse(this.response);
                
            // take the number of IoT devices
            var len = parseInt(response["length"]);
  
            // process each IoT device
            for (var i=1; i<=len; i++) {          
                // add the option to the select menu
                $('#select-module-to-delete').append($('<option>', {
                    value: response[i.toString()]["module_id"],
                    text: response[i.toString()]["module_name"]
                }));
            }
                
            // refresh the select menu to make the newly added options visible
            $( "#select-module-to-delete" ).selectmenu("refresh", true);
        }
    };
            
    // send the AJAX request
    xhttp.open("POST", "/get_modules_list", true);
    xhttp.send();
}        
  
function setIoTDeviceSelectionList() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
  
        // take the received JSON object
        var response = JSON.parse(this.response);
                
        // take the number of IoT devices
        var len = parseInt(response["length"]);
  
        // process each IoT device
        for (var i=1; i<=len; i++) {          
            // add the option to the select menu
            $('#select-iot-device-to-delete').append($('<option>', {
                value: response[i.toString()]["value"],
                text: response[i.toString()]["text"]
            }));
        }
                
        // refresh the select menu to make the newly added options visible
        $( "#select-iot-device-to-delete" ).selectmenu("refresh", true);
        }
    };

    // send the AJAX request
    xhttp.open("POST", "/get_iot_device_list", true);
    xhttp.send();
}
  
$( function() {
    $( ".delete-iot-device button" ).button();
    $( ".delete-iot-device button" ).click( function( event ) {
        event.preventDefault();
        // submit the data to the backend
        deleteIoTDevice()
    } );
} );
  
$( function() {
    $( ".cancel-iot-delete button" ).button();
    $( ".cancel-iot-delete button" ).click( function( event ) {
        event.preventDefault();
        // refresh the settings page
        window.location.href = "/settings";
    } );
} );
          
function deleteIoTDevice() {            
    // a form data object
    var formData = new FormData();
  
    // take the selected em data format index
    var iot_device_to_delete = document.getElementById("select-iot-device-to-delete");
    iot_device_to_delete = iot_device_to_delete.options[iot_device_to_delete.selectedIndex].value;
    // append sampling rate choice to the form data object
    formData.append("iot_device_to_delete", iot_device_to_delete);
  
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (this.responseText == "done") {                                          
                alert("IoT device deleted!");
                // refresh the settings page
                window.location.href = "/settings";
            } else {
                alert("Error occured while deleting!");
            }
        }
    };
  
    // send the AJAX request
    xhttp.open("POST", "/delete_iot_device", true);
    xhttp.send(formData);
}
