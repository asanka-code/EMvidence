
$( function() {
    $( ".widget input[type=submit]" ).button();
} );

/* returns the cookie with the given name or undefined if not found */
function getCookie(name) {
    let matches = document.cookie.match(new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}
  
  
$(document).ready( function() {
    var cookie = document.cookie;         
    
    //alert("Document ready!: " + getCookie('auth'));

    if(getCookie('auth') =='logged-out'){        
        document.getElementById("status").innerHTML = "<tr><td><p style='color:green;'> Logged out successfully! </p> </td></tr>";

    } else if (getCookie('auth') == 'wrong-credentials') {
        document.getElementById("status").innerHTML = "<tr><td><p style='color:red;'> Wrong username or password! </p> </td></tr>";
    }
});
          