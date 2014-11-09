//MARKETPLACE JS
$( document ).ready(function() {
    $('.item').hide()
    $('.service').show()
    console.log("shishi")
    $('.market-nav').click(function() {
        $('.a').removeClass('a')
        $(this).addClass('a')
        var n = $(this).attr('name')
        console.log(n)
        $('.item').hide()
        $('.'+n).show()
    })

    $('.cart').click(function() {
        console.log($(this).siblings('td'))
        jQuery.noConflict()
        $('#myModal').modal('show')

    })
});
