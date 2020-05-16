$(document).ready(function () {
    var price_range = parseInt($("#price_range").val());

    //location autocompete
    $(function () {
        $("#location").on('keyup', function () {
            var value = $(this).val();
            $.ajax({
                url: '/autocomplete_location',
                data: {
                    'search': value
                },
                dataType: 'json',
                success: function (data) {
                    list = data.list;
                    $("#location").autocomplete({
                        source: list,
                        minLength: 2
                    });
                }
            });
        });
    });

    //price slider
    $(function () {
        $("#slider").slider({
            max: 10000,
            min: 0,
            step: 500,
            value: price_range,
            animate: "fast",
            range: "min",
            slide: function (event, ui) {
                $("#price").html("$" + ui.value);
                $("#price_range").val(ui.value);
            },
        });
    });


    //submit filter form
    function submit_filter_form() {
        document.querySelector('#filterForm').submit();
    }

    //sort functions
    $('#most_recent').click(function () {
        $("#sort").val("MR");
        submit_filter_form()
    });
    $('#alphabetical_order').click(function () {
        $("#sort").val("AO");
        submit_filter_form()
    });
    $('#most_expensive').click(function () {
        $("#sort").val("ME");
        submit_filter_form()
    });
    $('#cheapest').click(function () {
        $("#sort").val("C");
        submit_filter_form()
    });


    //clear filter selections
    $('#clear_selections').click(function () {
        $('#state').val("ALL");
        $('#distance').val("25");
        $('#location').val("");
        $('#breed').val("ALL");
        $('#age').val("ALL");
        $('#gender').val("ALL");
        $('#price_range').val(10000);
        submit_filter_form()
    });

    //send message to seller
    $('#send_message').click(function () {
        $('#overlay_message').show();
    });
    $('#cancel_message').click(function () {
        $("#return_message").hide();
        $("#message").val("");
        $('#overlay_message').hide();
    });

    $(".custom-file-input").on("change", function () {
        var fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    });

    $("#form_send_message").submit(function () {
        $(".spinner").removeClass("d-none");
        $.ajax({
            type: "POST",
            url: '/send_message',
            data: {
                'ad_id': $("#ad_id").val(),
                'message': $("#message").val(),
            },
            headers: {
                'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')
            },
            dataType: 'json',
            success: function (data) {
                if (data.result == 'SUCCESS') {
                    $(".spinner").addClass("d-none");
                    $("#return_message").removeClass("d-none");
                    $("#return_message").html("Message sent!");
                    $("#message").val("");

                } else {
                    $(".spinner").addClass("d-none");
                    $("#return_message").removeClass("d-none");
                    $("#return_message").html("Error sending message!");
                    $("#message").val("");
                }

            }
        });
        event.preventDefault();
    });
});
