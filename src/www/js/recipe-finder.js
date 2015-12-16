// Javascript file to dynamize the page

$('form.opinion').on('submit', function (e) {
    e.preventDefault();
})

$('a.go').on('click', function(e) {
    e.preventDefault();
    completeSearch(this.id);
    alert('good bye')
    window.location.href = this.href;
})

function completeSearch(id) {
    $.ajax({
        type: 'POST',
        url: '../cgi_bin/ajax_handler.py',
        data:
        {
            search: id
        },
        success: function() {
            // alert(id)
        }
    });
}

function fav(id) {
    $.ajax({
        type: 'POST',
        url: '../cgi_bin/ajax_handler.py',
        data:
        {
            fav: id
        },
        success: function() {
            $('button#'+id).hide();
        }
    });
}

function unfav(id) {
    $.ajax({
        type: 'POST',
        url: '../cgi_bin/ajax_handler.py',
        data:
        {
            unfav: id
        },
        success: function() {
            $('#well_'+id).hide();
        }
    });
}

function send_opinion(id) {
    $.ajax({
        type: 'POST',
        url: '../cgi_bin/ajax_handler.py',
        data: $('form#'+id+'_head').serialize(),
        success: function() {
            $('#'+id+'_head').hide();
        }
    });
}
