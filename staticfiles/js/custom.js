/**
 * Created by yosef on 9/27/2016.
 * Don't use this page all js code is in html or jquery.js
 */




$(document).ready(function () {
    $(function () {
        // function of  image button
        var image;
        $(".image-link").click(function (event) {
            event.preventDefault();
            var pk = $(this).next(type = "hidden");
            if ($(this).next().hasClass("image-link") === true) {
                // meaning X button was pressed
                $(this).css("display", "none");
                image = $(this).siblings('.image-field').children('.image').detach();
                if (image) {
                }
                // $(this).siblings('.hidden-items').css("display", "none");
                $(this).siblings("#image-button").css("display", "inline");
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
                $(this).css("display", "none")
            }


        });
    });

    $(".submit-comment").click(function (event) {
        // submits comment
        event.preventDefault();
        var formData = $(this).parent(".comment-form").serializeArray();
        var image = $(this).siblings('.image-field').children("#image").val();
        var text = $(this).siblings("#text").val();
        // formData.append("image", $(this).siblings('.image-field').children("#image").val());
        //formData.append("text", $(this).siblings("#text").val());
        //formData.append("pk", $(this).siblings("#pk").val());
        //};
        console.log(formData);
        if (image) {
            alert("Need to reload to be able to save image");
            $(this).parent(".comment-form").submit();

        } else if (text === "") {
            alert("Post not posted. Add a picture or a post");
        } else {
            $.ajax({
                type: "POST",
                url: "{% url 'chat:post_comment' %}",
                data: formData,
                success: function (data) {
                    alert("Comment Added!");
                    var newPost = '<h3><img src="{{ user }}" class="profile_pic"/>{{ user }}';
                    newPost += '<small>{{ comment.time_posted|timesince }} ago</small></h3>';
                    newPost += '<p>' + data + '</p>';
                    $(this).parent("#new-post").html(newPost);

                },
                error: function (error) {
                    console.log(error.status + ": " + error.statusText);
                    $(this).parent(".comment-form").submit();
                }
            });
            $(this).parents(".comment-form").siblings("p").children(".reply").css("display", "inline");
            $(this).parents(".comment-form").css("display", "none");
        }
    });
    $(".name").css("font-weight", "bold");

    $(".reply").click(function () {
        $(this).parents().siblings(".comment-form").css("display", "inline");
        $(this).hide();
        console.log("Reply form revealed");
    });
});