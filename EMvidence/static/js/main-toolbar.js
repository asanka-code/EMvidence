$( function() {
    $( "#menu" ).menu();
} );

$( function() {
    $( ".toolbar" ).controlgroup();

    $( "#logout" ).click( function() {
      var answer = confirm("Do you want to logout?");
      if (answer == true){
        window.location.href = "/logout";
      } else {
        // do nothing.
      }
    });

    $( "#settings" ).click( function() {
      window.location.href = "/settings";        
    });

    $( "#dashboard" ).click( function() {
      window.location.href = "/dashboard";        
    });

    $( "#data" ).click( function() {
      window.location.href = "/upload-data";        
    });

    $( "#capture" ).click( function() {
      window.location.href = "/capture";        
    });
  
    $( "#analyse" ).click( function() {
      window.location.href = "/analyse";        
    });

    $( "#about" ).click( function() {
      window.location.href = "/about";        
    });

    $( "form" ).on( "submit", function( event ) {
      event.preventDefault();
    });
} );