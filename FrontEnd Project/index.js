/**
 * Created by yosef on 1/24/2017.
 */

    var root = 'https://jsonplaceholder.typicode.com';
    var allAlbums = "NUzz";


     function allowDrop(ev) {
                ev.preventDefault();
            }

            function drag(ev) {
                ev.dataTransfer.setData("text", ev.target.id);
                // console.log("HERE id" + ev.target.id);
            }

            function drop(ev) {
                ev.preventDefault();
                console.log(ev.target);
                dropTo = ev.target;
                d = $(dropTo).parents(".main");

                var data = ev.dataTransfer.getData("text");
                console.log("DATA: " + data);
                originalChart = $("#" + data).parents(".main");
                if (originalChart.attr("id") != d.attr("id")) {
                    console.log(d.attr("id"));
                    if (d.attr("id") ==  "main-1") {
                        $(dropTo).parents(".main").append(document.getElementById(data));
                    } else {
                        $(dropTo).parents(".main").prepend(document.getElementById(data));
                    }
                    box = document.getElementById(data);
                    $.ajax({
                        url: root + '/albums?id=' + data,
                        method: 'POST',
                        success: function (box) {
                            // alert("Success");
                            // console.log(box.id);

                        },
                        error: function (error) {
                            alert("Error")
                        }
                    });
                    $("#main-1").children().each(function (index, value) {
                        if (index % 2 == 0) {
                            $(this).removeClass('odd');
                        } else if (index % 2 == 1) {
                            $(this).addClass('odd');
                        }
                    });
                    $("#main-2").children().each(function (index, value) {
                        console.log(index);
                        if (index % 2 == 0) {
                            $(this).removeClass('odd');
                        } else if (index % 2 == 1) {
                            $(this).addClass('odd');
                        }
                    });
                }

            }


    $.ajax({
        url: root + '/users?id=1',
        method: 'GET'
    }).then(function (data) {
        // console.log(data);
        console.log(data[0].name);
        $("#title-one").html(data[0].name);
    });


    $.ajax({
        url: root + '/albums?userId=1',
        method: 'GET'
    }).then(function (data) {
        // console.log(data);
        allAlbums = data;
        console.log("allAlbums works in the ajax request" + allAlbums);
        for (album in allAlbums) {
            id = allAlbums[album].id;
            var row = '<section class="draggable section-1';
            if (album % 2 == 1) {
                row += ' odd';
            }
            row += '" draggable="true" ondragstart="drag(event)" id="' + id + '">';
            row += '<span class="avail">' + allAlbums[album].id + '</span>';
            row += '<span class="list">' + allAlbums[album].title + '</span>';
            row += '</section>';
            $("#main-1").append(row);
        }
    });


    $.ajax({
        url: root + '/users?id=2',
        method: 'GET'
    }).then(function (data) {
        // console.log(data);
        console.log(data[0].name);
        $("#title-two").html(data[0].name);
    });

    function init() {
        $(".draggable").draggable();
    }


    $.ajax({
        url: root + '/albums?userId=2',
        method: 'GET'
    }).then(function (data) {
        // console.log(data);
        allAlbums = data;
        console.log("allAlbums works in the ajax request" + allAlbums);
        for (album in allAlbums) {
            id = allAlbums[album].id;
            var row = '<section class="draggable section-2';
            if (album % 2 == 1) {
                row += ' odd';
            }
            row += '" draggable="true" ondragstart="drag(event)" id="' + id +'">';
            row += '<span class="avail">' + allAlbums[album].id + '</span>';
            row += '<span class="list">' + allAlbums[album].title + '</span>';
            row += '</section>';
            console.log(album);
            $("#main-2").append(row);

        }
    });
