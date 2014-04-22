$(document).ready( function() {

// STATES:
// 0 = HOME
// 1 = RESUME
// 2 = LINKS
// 3 = CONTACT

var state = 0;

$('#menu_home').addClass('selected');
$('#general_container').css('width', Math.max($(window).outerWidth()-300, 600));
if($(window).outerWidth()-300 > 600)
    $('#general_container').css('margin-left', 200);
else if($(window).outerWidth()-100 > 600)
    $('#general_container').css('margin-left', 100 + ($(window).outerWidth() - 700)/2);
else
    $('#general_container').css('margin-left', 110);

$('#menu_items').find('a').on("click", function() {
    var id = this.id;
    var newstate = -1;
    
    switch(id) {
        case 'menu_home':
            newstate = 0;
            break;
        case 'menu_resume':
            newstate = 1;
            break;
        case 'menu_links':
            newstate = 2;
            break;
        case 'menu_contact':
            newstate = 3;
            break;
        default:
            break;
    }

    change_state(newstate);    
});


// Functions
function change_state(newstate) {
    // Do nothing if same or none
    if(newstate == state || newstate == -1)
        return;

    // Change highligting
    switch(state) {
        case 0:
            $('#menu_home').removeClass('selected');
            break;
        case 1:
            $('#menu_resume').removeClass('selected');
            break;
        case 2:
            $('#menu_links').removeClass('selected');
            break;
        case 3:
            $('#menu_contact').removeClass('selected');
            break;
        default:
            break;
    }

    // Add highlighting and animate
    switch(newstate) {
         case 0:
            $('#menu_home').addClass('selected');
            animate_home(state, newstate);
            break;
        case 1:
            $('#menu_resume').addClass('selected');
            animate_resume(state, newstate);
            break;
        case 2:
            $('#menu_links').addClass('selected');
            animate_links(state, newstate);
            break;
        case 3:
            $('#menu_contact').addClass('selected');
            animate_contact(state, newstate);
            break;
        default:
            break;
    }

    // Transition complete
    state = newstate;
}

function slide_menu_left() {
    $('#menu_container').animate({
        left: "0%",
        "margin-left": "5px"
        }, 1000, function() {
            // Animation complete
    });
}

function slide_menu_middle() {
    $('#menu_container').animate({
        left: "50%",
        "margin-left": "-53px"
        }, 1000, function() {
            // Animation complete
    });
}

function animate_home(oldstate, newstate) {
    slide_menu_middle();
    $('#general_container').fadeOut(1000);
}

function animate_resume(oldstate, newstate) {
    if(oldstate == 0)
        slide_menu_left();
    
    $('#general_container').load('/resume', function() {
    });
}

function animate_links(oldstate, newstate) {
    if(oldstate == 0)
        slide_menu_left();

    
}

function animate_contact(oldstate, newstate) {
    if(oldstate == 0)
        slide_menu_left();

    
}

});
