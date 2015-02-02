$(document).ready( function() {

var ROBOT_URL = '/robot/';
var UI_URL = '/userInterface/';
var MAP_URL = '/visualMap/';
var MAP_HTML_URL = '/visualMapImages/';

// Events

$('#robot-selector').on('change', function() {
    // Gets data for a particular robot and populates UI
    getAllRobotData();
    
});

$('#coordinates-clear').on('click', function() {
    // Clear real waypoints
    deleteField('realWaypoints');
});

$('#coordinates-refresh').on('click', function() {
    // Gets data for a particular robot and populates UI
    getAllRobotData();
});

$('#target-update').on('click', function() {
    // Update instructions for this robot
    var robotId = $('#robot-selector').val();
    if (robotId)
    {
        var x = parseInt($('#target').find('.xPos').val());
        var y = parseInt($('#target').find('.yPos').val());

        $.post(
            UI_URL + '?robotId=' + robotId,
            JSON.stringify({instruction: [x,y]}),
            function(data) {
                if (data.status == 'ok')
                {
                    alert(data.details);
                }
                else
                {
                    alert('Server error: ' + data.details);
                }
            },
            'json'
        ).fail(function() {
            alert('An unexpected error has occurred');
        });
    }
});

$('#target-clear').on('click', function() {
    // Clear instructions for this robot
    var jqxhr = deleteField('instruction');
    if (jqxhr)
    {
        jqxhr.done(function(data) {
            if (data.status == 'ok')
            {
                $('#target').find('.xPos').val(null);
                $('#target').find('.yPos').val(null);
            }
        });
    }
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
function getAllRobotData()
{
    var robotId = $('#robot-selector').val();
    if (robotId)
    {
        $.get(
            ROBOT_URL + '?robotId=' + robotId,
            function(data) {
                if (data.status == 'ok')
                {
                    // Set fields
                    $('#coordinates').find('.xPos').html(data.robot.position[0]);
                    $('#coordinates').find('.yPos').html(data.robot.position[1]);
                    $('#coordinates').find('.xExactPos').html(data.robot.exactPosition[0]);
                    $('#coordinates').find('.yExactPos').html(data.robot.exactPosition[1]);

                    if (data.robot.hasOwnProperty('instruction'))
                    {
                        $('#target').find('.xPos').val(data.robot.instruction[0]);
                        $('#target').find('.yPos').val(data.robot.instruction[1]);
                    }
                    else
                    {
                        $('#target').find('.xPos').val(null);
                        $('#target').find('.yPos').val(null);
                    }

                    // Grab map
                    generateRobotMap(robotId)
                }
                else
                {
                    alert('Server error: ' + data.details);
                }
            },
            'json'
        ).fail(function() {
            alert('An unexpected error has occurred');
        });
    }
    else
    {
        // Set fields
        $('#coordinates').find('.xPos').html('NONE');
        $('#coordinates').find('.yPos').html('NONE');
        $('#coordinates').find('.xExactPos').html('NONE');
        $('#coordinates').find('.yExactPos').html('NONE');
        $('#target').find('.xPos').val(null);
        $('#target').find('.yPos').val(null);
        $('#map-viewport').html('Please select a robot');
    }
}

function generateRobotMap(robotId)
{
    // Build a new map and display it
    $('#map-viewport').html('loading...');

    $.get(
        MAP_URL + '?robotId=' + robotId,
        function(data) {
            if (data.status == 'ok')
            {
                loadRobotMap(data.userId.toString());
            }
            else
            {
                alert('Server error: ' + data.details);
            }
        },
        'json'
    ).fail(function() {
        alert('An unexpected error has occurred in building the map');
    });
}

function loadRobotMap(userId)
{
   $.get(
    MAP_HTML_URL + '?userId=' + userId,
    function(data) {
        $('#map-viewport').html(data);
        $('#map-viewport').mapbox({mousewheel: true});
    },
    'html'
    ).fail(function() {
        alert('An unexpected error has occurred in loading the map');
    });
}

function deleteField(field)
{
    // Call Delete on a specified element
    var robotId = $('#robot-selector').val();
    if (robotId)
    {
        var jqxhr = $.ajax({
            type: 'DELETE',
            url: UI_URL + '?robotId=' + robotId,
            data: JSON.stringify({data: field.toString()}),
            success: function(data) {
                if (data.status == 'ok')
                {
                    alert(data.details);
                }
                else
                {
                    alert('Server error: ' + data.details);
                }
            },
            dataType: 'json'
        }).fail(function() {
            alert('An unexpected error has occurred');
        });
        return jqxhr;
    }
    return null;
}

});
