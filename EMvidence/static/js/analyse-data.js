$( function() {
    $( "#iot-device-type" ).selectmenu(
      {
        width: 200
      }
    );
} );

$( function() {
    $( "#dataset" ).selectmenu(
      {
        width: 500
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
    $( ".analyze-button button" ).button();
    $( ".analyze-button button" ).click( function( event ) {
      event.preventDefault();
      submitAnalysis();
    } );
} );

$( function() {
    $( ".cancel-analyze-button button" ).button();
    $( ".cancel-analyze-button button" ).click( function( event ) {
      event.preventDefault();
      cancelAnalysis();
    } );
} );

$( function() {
  $( ".save-report-button button" ).button();
  $( ".save-report-button button" ).click( function( event ) {
    event.preventDefault();
    saveReport();
  } );
} );

function submitAnalysis() {
    // a form data object
    var formData = new FormData();

    // take the selection of dataset
    var dataset_choice = document.getElementById("dataset");
    dataset_choice = dataset_choice.options[dataset_choice.selectedIndex].value;
    // append the choice of dataset to the form data object
    formData.append("dataset_choice", dataset_choice);

    // take the selection of IoT device
    var iot_device_type = document.getElementById("iot-device-type");
    iot_device_type = iot_device_type.options[iot_device_type.selectedIndex].value;
    // append the choice of IoT device to the form data object
    formData.append("iot_device_type", iot_device_type);                    

    // append the choice of modules to the form data object
    formData.append("selected_modules", checked_elements);

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {

        // clear any results from a previous analysis
        document.getElementById("classification-results").innerHTML = "";

        // take the received JSON object
        var response = JSON.parse(this.response);
        
        // take the number of IoT devices
        var len = parseInt(response["length"]);                        

        //if (this.responseText == "done") {
        if (len>0) {

          // add the result of each module to the table
          for (var i=1; i<=len; i++) {                          
            content = response[i.toString()]['module_name'];
            content = content.concat(": ", response[i.toString()]['result']);                                
            row = document.getElementById("classification-results").insertRow(0);
            row.insertCell(0).innerHTML = response[i.toString()]['module_name'];
            row.insertCell(1).innerHTML = response[i.toString()]['result'];                
          }
          
          // update progress bar status
          progressLabel.text("Done!");
          var val = progressbar.progressbar( "value" ) || 0;
          progressbar.progressbar( "value", true);
          
          // set the figures visible
          document.getElementById("visualize-data").style.visibility = "visible";

          // realoading the iframe to show the results of the analysis
         // var iframe = document.getElementById('captured-data-view');
          //iframe.src = iframe.src;

        } else {
          // update progress bar status
          progressLabel.text("Something went wrong...");
          var val = progressbar.progressbar( "value" ) || 0;
          progressbar.progressbar( "value", true);  
        }
      }
    };

    if(checked_elements.length < 1){
      alert("Please select the modules to apply.");
    } else {

      // progress bar and its label objects
      progressbar = $( "#progressbar" );
      progressLabel = $( ".progress-label" );

      // update the progress bar status
      progressLabel.text("Data analysis in progress...");
      progressbar.progressbar( "value", false);

      // send the AJAX request
      xhttp.open("POST", "/analyze-data", true);
      xhttp.send(formData);
    }
}

function cancelAnalysis() {
    // progress bar and its label objects
    progressbar = $( "#progressbar" );
    progressLabel = $( ".progress-label" );

    // a form data object
    var formData = new FormData();

    var temp = 'temp';
    formData.append("temp", temp);

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {

        if (this.responseText == "done") {
          // update progress bar status
          progressLabel.text("Analysis canceled!");
          var val = progressbar.progressbar( "value" ) || 0;
          progressbar.progressbar( "value", true);
          
          // set the figures visible
          document.getElementById("visualize-data").style.visibility = "hidden";

          // realoading the iframe to show the results of the analysis
          //var iframe = document.getElementById('captured-data-view');
          //iframe.src = iframe.src;

        } else {
          // update progress bar status
          progressLabel.text("Something went wrong...");
          var val = progressbar.progressbar( "value" ) || 0;
          progressbar.progressbar( "value", true);  
        }
      }
    };

    // send the AJAX request
    xhttp.open("POST", "/cancel-analysis", true);
    xhttp.send(formData);
  }

function saveReport() {

  // report file name
  var date_object = new Date();
  var number = date_object.getTime();
  var report_name = "EMvidence-Report-" + number;

  // progress bar and its label objects
  progressbar = $( "#progressbar" );
  progressLabel = $( ".progress-label" );

  // a form data object
  var formData = new FormData();

  var temp = 'temp';
  formData.append("temp", temp);

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

      if (this.responseText == "done") {
        // update progress bar status
        progressLabel.text("Report ready!");
        var val = progressbar.progressbar( "value" ) || 0;
        progressbar.progressbar( "value", true);
    
        // download the report file
        fetch('/send-report')
        .then(resp => resp.blob())
        .then(blob => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.style.display = 'none';
          a.href = url;
          // the filename you want
          //a.download = 'report.pdf';
          a.download = report_name;
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          //alert('your file has downloaded!'); // or you know, something with better UX...
        })
        .catch(() => alert('error occurred!'));


      } else {
        // update progress bar status
        progressLabel.text("Something went wrong...");
        var val = progressbar.progressbar( "value" ) || 0;
        progressbar.progressbar( "value", true);  
      }
    }
  };

  // send the AJAX request
  xhttp.open("POST", "/create-report", true);
  xhttp.send(formData);
}


$( function() {
    $( ".widget input[type=submit]" ).button();
    $( ".widget input[type=file]" ).button();
    $( ".widget input[type=button]" ).button();
} );

// things to do once the document is loaded
$(document).ready( function() {          
    // set the dataset selection menu
    setDatasetSelectionList();

    // set the IoT devices selection menu
    setIoTDeviceSelectionList();

    // set the modules as checkbox elements
    setModulesCheckboxList();

} );              

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
          $('#dataset').append($('<option>', {
            value: response[i.toString()]["value"],
            text: response[i.toString()]["text"]
          }));
        }
        
        // refresh the select menu to make the newly added options visible
        $( "#dataset" ).selectmenu("refresh", true);
      }
    };
    // send the AJAX request
    xhttp.open("POST", "/get_dataset_list", true);
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
          $('#iot-device-type').append($('<option>', {
            value: response[i.toString()]["value"],
            text: response[i.toString()]["text"]
          }));
        }
        
        // refresh the select menu to make the newly added options visible
        $( "#iot-device-type" ).selectmenu("refresh", true);
      }
    };
    // send the AJAX request
    xhttp.open("POST", "/get_iot_device_list", true);
    xhttp.send();
}
  
function setModulesCheckboxList() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        
        // take the received JSON object
        var response = JSON.parse(this.response);
        
        // take the number of modules
        var len = parseInt(response["length"]);

        // process each module
        for (var i=1; i<=len; i++) {        

          // take the module ID
          var module_id = response[i.toString()]["module_id"]
          // set the new module label
          $('#modules-to-apply').append($('<label>', {
            for: module_id,
            text: response[i.toString()]["module_name"]            
          }));
          // set the input checkbox for this module
          $('#modules-to-apply').append($('<input>', {
            type: "checkbox",
            name: module_id,
            id: module_id,
            onclick: "recordCheckBox(this)"
          }));
          $( "#" + module_id ).checkboxradio(
          {
            icon: false
          });
        }                            
      }
    };
    // send the AJAX request
    xhttp.open("POST", "/get_modules_list", true);
    xhttp.send();
}

// the array that holds the module ids of checked checkerboxes
var checked_elements = [];


function recordCheckBox(element) {
    var checkBox = element;
    if (checkBox.checked == true){
        checked_elements.push(checkBox.id);
    } else {
      var filteredAry = checked_elements.filter(function(e) { return e !== checkBox.id });
      checked_elements = filteredAry;
    }          
}
