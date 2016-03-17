$(document).ready(function() {
    "use-strict";

    // Highlight the top nav as scrolling occurs
    $('body').scrollspy({
        target: '.navbar-fixed-top'
    })

    /*Url jumping*/
    $(function() {
        $('a[href*=#]:not([href=#])').click(function() {
            if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
                var target = $(this.hash);
                target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
                if (target.length) {
                    $('html,body').animate({
                        scrollTop: target.offset().top
                    }, 1000);
                    return false;
                }
            }
        });
    });

    // Owl Carousel
    $(document).ready(function() {

        $("#owl-demo").owlCarousel({

            navigation: true, // Show next and prev buttons
            slideSpeed: 300,
            paginationSpeed: 400,
            singleItem: true

            // "singleItem:true" is a shortcut for:
            // items : 1, 
            // itemsDesktop : false,
            // itemsDesktopSmall : false,
            // itemsTablet: false,
            // itemsMobile : false

        });

    });

    // Animate and WOW Animation
    var wow = new WOW(
        {
            offset: 50,
            mobile: false,
            live: true
        }
    );
    wow.init();

    // Prettyphoto Installation
    $(document).ready(function(){
        $("a[class^='prettyPhoto']").prettyPhoto();
    });
    $('#myModal').modal({
                keyboard: true,
                backdrop: "static",
                show: false
            }).on('show.bs.modal', function (event) { //subscribe to show method
                var getId = $(event.relatedTarget).data('id'); //get the id from tr
                //make your ajax call populate items or what even you need
                $.post( "", { id: getId, csrfmiddlewaretoken : '{{ csrf_token  }}' }, function( data ) {
                    
                    $('h4.modal-title').html(data.title);
                    $('.item-desc').html(data.desc);
                });
                
            });
        // Menu scroll to.
    $('button#added').click(function(){
        target_element = $('#sectionadded');
        scroll_to = $(target_element).offset().top;
        if($(window).scrollTop() != scroll_to && target_element !== undefined){
            // Chrome scroll to calculation and other browser scroll to calculation is different.
                body_scroll_target = scroll_to;
            
            $('html,body').animate({scrollTop:body_scroll_target},1000);
        }
        return false;
    });
    $('button#about').click(function(){
        target_element = $('#sectionabout');
        scroll_to = $(target_element).offset().top;
        if($(window).scrollTop() != scroll_to && target_element !== undefined){
            // Chrome scroll to calculation and other browser scroll to calculation is different.
                body_scroll_target = scroll_to;
            
            $('html,body').animate({scrollTop:body_scroll_target},1000);
        }
        return false;
    });
    $('a.scroll_effect').on('click', function(e){
        target_element = $(this).attr('href');
        scroll_to = $(target_element).offset().top;
        if($(window).scrollTop() != scroll_to && target_element !== undefined){
            // Chrome scroll to calculation and other browser scroll to calculation is different.
            if($.templatemo_is_chrome){
                body_scroll_target = scroll_to;
            }else{
                body_scroll_target = $("body").scrollTop()+scroll_to;
            }
            $('html,body').animate({scrollTop:body_scroll_target},1000);
        }
        // If menu is visible hide the nav.
        $('nav:visible').templateMoMenuHide();
        return false;
    });
    $('span#delete').click(function(event){
        $('#myModal').find('.modal-title').html('Հաստատում');
        $('#myModal').find('.modal-body').html('Համոզվա՞ծ եք, որ ուզում եք ջնջել։');
        $('#myModal').find('.del').data('id',$(this).parent().find('img').attr('id'));
        $('#myModal').modal('show');
    });
    $('.del').click(function(){
        
        $.post('/del_prod', {'prod_id': $(this).data('id')}, function(datum){
            var id = $(this).data('id');
            $('#myModal').modal('hide');
            $('img#' + datum.id).parent().remove();
        });
    })
});
