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
        jQuery.noConflict()
        $('#myModal').modal('show')
    })

    function showModal(id) {
        $.get('modal', function (data) {
            console.log(data)
        });
    }

    $(function(){

    $(".dropdown-menu").on('click', 'li a', function(){
        var menu = $(this).closest('ul').attr('class').split(' ')[1]
      $('.dd'+menu).text($(this).text())
      $('.dd'+menu).val($(this).text())
   });

   $('.project-add').click(function() {
       //do stuff
       window.location.href = "/project_space/manage";
   })

});
});
