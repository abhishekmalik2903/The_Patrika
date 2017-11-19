/**
 * Created by Yosef Fastow on 12/13/2016.
 */
$(document).ready(function () {

    // Not used. Function to show flash message
    function showFlashMessage(message) {
        // var template = "{% include 'alert.html' with message='" + message + "' %}";
        var template = "<div class='container container-alert-flash'>" +
            "<div class='col-sm-3 col-sm-offset-8'>" +
            "<div class='alert alert-success alert-dismissible' role='alert'>" +
            "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" +
            "<span aria-hidden='true'>&times;</span></button>" + message + "</div></div></div>";
        console.log(template);
        $("body").append(template);
        $(".container-alert-flash").fadeIn();
        setTimeout(function () {
            $(".container-alert-flash").fadeOut();
        }, 1800)
    }
    
    
    // layout nav bar
    $(".search-button").hover(function() {
        // not used anymore meant to "Find Friend" Button when you hover over the "Search" Button
        $(this).parent().siblings("#find-friends-form").children("#submit-find-friends").css("display", "inline");
        $(this).next().css("display", "inline");
    });
    
    $(".top-bar").mouseleave(function() {
        $(this).next().css("display", "none");
    });

    $(".submit-find-friends").click(function () {
        // goes to find_friends.html and uses the query filter out people
        $("#find-friends-form").submit();
    });
    
    
    // chat.html
     $(function () {
         // shows images
         var image;
         $(".image-link").click(function (event) {
             // reveals <input=file> to screen.
            event.preventDefault();
            var pk = $(this).next(type = "hidden");
            if ($(this).next().hasClass("image-link") === true) {
                // meaning X button was pressed
                $(this).css("display", "none");
                $(this).siblings(".image-link").css("display", "inline");
                image = $(this).siblings('.image-field').children('.image').detach();
                if (image) {
                }
            } else {
                // meaning camera button was pressed
                if (image) {
                    image.appendTo($(this).siblings(".image-field"));
                    image = null;
                } else {
                    $(this).siblings(".image-field").append("<input type='file' name='image' id='image' placeholder='image' class='image' />");
                }
                $(this).siblings('.hidden-items').css("display", "inline");
                $(this).next(type = "hidden").submit();
                $(this).css("display", "none");
            }
         });
    });
    
    $("#share").click(function() {
        var share = $(this).children().val();
        if (share == "Private Message") {
            $("#only-me").css("display", "block");
        } else {
            $("#only-me").css("display", "none");
        }
    });

    
    // comment_loop.html
     $(".like-button").click(function() {
         console.log("like button pressed");
         $(this).parent().siblings('.like-unlike-form').submit();
     });

    $(".like").hover(function() {
        var likes = $(this).siblings(".like-amount").val();
        if ($(this).parent().siblings(".likes").css("display", "hidden") && likes > 0) {
            $(this).parent().siblings(".likes").css("display", "inline");
        }
    });
    

    $(".reply").click(function () {
        // reveals form to reply to post
        $(this).parents().siblings(".comment-form").css("display", "inline");
        $(this).hide();
        $(this).parents(".post").siblings(".show_replies").hide();
        $(this).parents(".post").siblings(".hidden-items").show();
        console.log("Reply form revealed");
    });

    $(".show_replies").click(function () {
        var comment = $(this).next().val();
        $(this).next().css("display", "block");
        $(this).css("display", "none");
        console.log("Went through");
    });

    $(".hide-replies").click(function () {
        $(this).parent().css("display", "none");
        $(this).parent().prev().css("display", "block");
        console.log("replies hidden");
    });
});


// messages
$(".respond").click(function() {
        $respondForm =  $(this).siblings(".respond-form");
        if ($respondForm.css("display") == "none") {
            $(this).html("Hide Form");
            $respondForm.show();
        } else {
            $(this).html("Respond");
            $respondForm.hide();
        }
});

