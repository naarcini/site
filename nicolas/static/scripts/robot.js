$(document).ready( function() {

// Prepare panning/zooming map

$('#map-viewport').mapbox({mousewheel: true});

// Events

$('#robot-selector').on('change', function() {
    // TODO
});

$('#coordinates-clear').on('click', function() {
    // TODO
});

$('#coordinates-refresh').on('click', function() {
    // TODO
});

$('#target-update').on('click', function() {
    // TODO
});

$('#target-clear').on('click', function() {
    // TODO
});

$('#show-legend').on('click', function() {
    if ($('#legend').is(':visible'))
    {
        $('#show-legend').html('[+] Show Legend');
    }
    else
    {
        $('#show-legend').html('[-] Hide Legend');
    }

    $('#legend').toggle();
});

// Functions

});
