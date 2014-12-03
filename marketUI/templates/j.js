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
      $('.create-'+menu).text($(this).text())
      $('.create-'+menu).val($(this).text())
   });

    $(".edit-dropdown").on('click', 'li a', function(){
        var menu = $(this).closest('ul').attr('class').split(' ')[2]
      $('.edit-'+menu).text($(this).text())
      $('.edit-'+menu).val($(this).text())
   });

    $(".editVM").on('click', function(){
      $('.editVM-name').text($(this).text())
      $('.editVM-name').val($(this).text())
      $('.editVM-id').val($(this).val())
   });

    $(".chosenFlavor").on('click', function(){
      $('.editFlavor-id').val($(this).data('id'))
   });

    $(".chosenTenant").on('click', function(){
      $('.enterTenantName').val($(this).text())
      $('.enterTenantID').val($(this).val())
   });

// Poll the project management page every 1s
/*  var interval = setTimeout(pollProjManage, 1000)
  function pollProjManage() {
    window.location.location("/project_space/manage");
    interval = setTimeout(pollProjManage, 1000);
  }
*/

   $('.project-add').click(function() {
       //do stuff
       window.location.href = "/project_space/manage";
   })

});
});
