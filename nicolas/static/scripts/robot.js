$(document).ready( function() {

// Events

$('#map-zoom').on("input change", function() {
    $('#map-zoom-feedback').html($('#map-zoom').val().toString() + " %");
});

$('#target form').on("submit", function() {
    alert("Not implemented");
});


});
