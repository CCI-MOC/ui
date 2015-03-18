$( document ).ready(function() {
    $('.item').hide()
    $('.service').show()
    $('.market-nav').click(function() {
        $('.a').removeClass('a')
        $(this).addClass('a')
        var n = $(this).attr('name')
        $('.item').hide()
        $('.'+n).show()
    })

    $('.cart').click(function() {
        jQuery.noConflict()
        $('#myModal').modal('show')
    })

    function showModal(id) {
        $.get('modal', function (data) {
        });
    }

    $(function(){
// Population of dropdown values; marketplace and createVM
    $(".dropdown-menu").on('click', 'li a', function(){
        var menu = $(this).closest('ul').attr('class').split(' ')[1]
      $('.dd'+menu).text($(this).text())
      $('.dd'+menu).val($(this).text())
      $('.create-'+menu).text($(this).text())
      $('.create-'+menu).val($(this).text())
   });
// Population of dropdown values; editVM; project management page
    $(".edit-dropdown").on('click', 'li a', function(){
        var menu = $(this).closest('ul').attr('class').split(' ')[2]
      $('.edit-'+menu).text($(this).text())
      $('.edit-'+menu).val($(this).text())
   });
// Selection of VM; editVM; project management page
    $(".editVM").on('click', function(){
      $('.editVM-name').text($(this).text())
      $('.editVM-name').val($(this).text())
      $('.editVM-id').val($(this).val())
   });
// Selection of flavor; editVM; project management page
    $(".chosenFlavor").on('click', function(){
      $('.editFlavor-id').val($(this).data('id'))
   });
// Selection of tenant; projects page
    $(".chosenTenant").on('click', function(){
      $('.enterTenantName').val($(this).text())
      $('.enterTenantID').val($(this).val())
   });
// Selection of user; editUser; project settings page
    $(".chosenUser").on('click', function(){
      $('.editUserName').text($(this).text())
      $('.editUserName').val($(this).text())
   });
// Select user's role editing option; editUser; project settings page
    $(".editRoleAction").on('click', function(){
      $('.editAction').val($(this).val())
   });
});
});
