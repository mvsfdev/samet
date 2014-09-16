function handle_move_segment_update(event) {
    $('#message_box').text('Segment Placement');
    put_segments(segment_datas);
    return false;
};


function put_segments(segments) {
    var arg = JSON.stringify(segments);
    console.log(arg);
    $.ajax({url:"putSegments",
            //data:{ segs : segments },
            data: arg,
            type: 'POST',
            contentType: 'application/json',
            processData: false,
            dataType: "json",
            success: function(data) {console.log(data["result"]);},
           });
}; 

