 // SideNav Button Initialization
        $(".button-collapse").sideNav({
            breakpoint: 1200
        });
        // SideNav Scrollbar Initialization
        var sideNavScrollbar = document.querySelector('.custom-scrollbar');
        Ps.initialize(sideNavScrollbar);


        // Material Select Initialization
        $(document).ready(function() {
            $('.mdb-select').materialSelect();
        });

    $('.dropdown-toggle').dropdown()


 // SideNav Button Initialization
    $(".button-collapse").sideNav({
        breakpoint: 1200
    });
    // SideNav Scrollbar Initialization
    var sideNavScrollbar = document.querySelector('.custom-scrollbar');
    Ps.initialize(sideNavScrollbar);


$(document).ready(function(){
 $(":checkbox").on("change", function() {
        if (this.id === "dataset1" && this.checked) {
             function verifyInput(){
            $.ajax({
                url: 'https://127.0.0.1:8000/filter_data',
                method: 'GET',
                data: {'email': email},
                success: function (data) {
                    console.log(data)
                }
            })
            .done(function() {
                $('span.rv-orange-color').append(email);
                $('.second')
                        .modal({closable: false})
                        .modal('setting', 'transition', 'horizontal flip')
                        .modal('show');
                return false;
            })
            .fail(function() {
                $('.first .ten').html('<h2>Sorry, there is some problem. Please Try again Later!</h2>');
                setTimeout(function(){
                    window.location.reload();
                },5000);
            })
        }
        }
        else{

            /* invalid input*/
            $('.red').text('Please provide Valid Email Address OR 10 digit Mobile No.').css("display","inline-block");
            setTimeout(function(){
                $('.red').css("display","none");
            },5000);

            return false;
        }

    });

});

$('.collapse').collapse()

