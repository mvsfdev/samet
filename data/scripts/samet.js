$(document).ready(function(){    
    /**
     *   Initialize zone
     *
     */
    initialize();
    
    var poll = setTimeout(function() {
        //refresh();
        setTimeout(arguments.callee,1000);
    },1000);
    
});

var system_state = 0;
var map = new Object();
//paper = Raphael("canvas",100,100);

function initialize(){
    /// Canvas variable
    map.width = $('#canvas').width();
    map.height = $('#canvas').height();
    map.paper = Raphael("canvas",map.width,map.height);
    map.paper.clear();
    map.background = map.paper.image("media/map.png",0,0,map.width,map.height);
    map.scale_x = map.width / 1912;   
    map.scale_y = map.height / 1022;  

    set_system_state('Ready');
    
    return false; 
};

function move(dx, dy) {
    this.update(dx - (this.dx || 0), dy - (this.dy || 0));
    this.dx = dx;
    this.dy = dy;
};

function up() {
    this.dx = this.dy = 0;
};

function clear_path(setx) {
    var il = setx.length;
    for(var i= 0;i < il;i+=1) {
        setx[i].removeData();
        setx[i].remove();
    }
};

function message(mesg) {
    $('#message_box').text(mesg);
    $('#write').val(mesg);
}

var dispatch = {
    'Ready'       :    {'LT': '设置',   'L' : handle_install,
                        'MT': '摆放',     'M' : handle_set,
                        'RT': '参数',     'R' : handle_parament,
                        'MSG': '系统工作中......'},
};    

function set_system_state(state) {
    if (system_state == state) {
        return false;
    }
    system_state = state;
    if(system_state in dispatch) {
        var Handler = dispatch[system_state];
        
        $('#left_btn').text(Handler['LT']);
        $('#left_btn').unbind();
        $('#left_btn').bind('click',{},Handler['L']);
        
        $('#mid_btn').text(Handler['MT']);
        $('#mid_btn').unbind();
        $('#mid_btn').bind('click',{},Handler['M']);
        
        $('#right_btn').text(Handler['RT']);
        $('#right_btn').unbind();
        $('#right_btn').bind('click',{},Handler['R']);
        
	message(Handler['MSG']);
    };
};

function handle_install(event) {
    set_system_state('Install');
    return false;
};

function handle_set(event) {
    set_system_state('Movement');
    return false;
};

function handle_parament(event) {
    set_system_state('parament');
    // $('#message_box').text(" " + map.width + " x "+ map.height +" " + map.scale_x +  " x " + map.scale_y);
    return false;
};


/***********************************************************************************************
 *
 *   Install
 * 
 ***********************************************************************************************/
var drag_point = { "fill" : "yellow",
		   "stroke" : "red",
		   "stroke-width": 2,
		 }; 
var drag_point_end = { "fill" : "blue",
		       "stroke" : "red",
		       "stroke-width": 2,
		     }; 

dispatch['Install'] = {'LT': '地图',      'L' : handle_install_from_map,
                       'MT': '读PM',     'M' : handle_install_readPM,
                       'RT': '返回',     'R' : handle_install_back,
                       'MSG': '参数设置模式......'};

function handle_install_from_map(event) {
    message('map');
    return false;
};

function handle_install_readPM(event) {
    return false;
};


function handle_install_back(event) {
    set_system_state('Ready');
    return false;
};


/***********************************************************************************************
 *
 *   Movement
 * 
 ***********************************************************************************************/

function put_sda(url,argx){
    var arg = JSON.stringify(argx);
    console.log(arg);
    $.ajax({url:url,
            data: arg,
            type: 'POST',
            contentType: 'application/json',
            processData: false,
            dataType: "json",
            success: function(data) {console.log(data["result"]);},
           });

};


dispatch['Movement'] = {'LT': '电缆',      'L' : handle_move_cable,
			'MT': '设备',      'M' : handle_move_module,
			'RT': '传感器',    'R' : handle_move_aux,
			'MSG': '参数设置模式......'};

function handle_move_cable(event) {
    set_system_state('Cable'); 
    get_display_segment();
    return false;
};

function handle_move_module(event) {
    set_system_state('Module'); 
    get_device();
    return false;
};

function handle_move_aux(event) {
    set_system_state('Aux');
    get_auxiliary();
    return false;
};


/***********************************************************************************************
 *
 *   Cable
 * 
 ***********************************************************************************************/
var drag_seg_point = { "fill" : "yellow",
		   "stroke" : "red",
		   "stroke-width": 2,
		   "title" : "起点",
		 }; 
var drag_seg_point_end = { "fill" : "blue",
		       "stroke" : "red",
		       "title" : "终点",
		       "stroke-width": 2,
		     }; 

dispatch['Cable'] = {'LT': '提交',      'L' : handle_move_segment_update,
		     'MT': '下一个',     'M' : handle_move_segment_next,
		     'RT': '返回',     'R' : handle_move_segment_back,
		     'MSG': '参数设置模式......'};


var segment_attr = { "stroke" : "green",
                     "stroke-width" : 5,
		     "fill" : "green",
		     "fill-opacity" : 1
		   };

var segment_selected_attr = { "stroke" : "red",
			      "stroke-width" : 5,
			      "fill" : "red",
			      "fill-opacity" : 1
			    };

var segment_datas = {
    "segment1" :{'x0' : 100,
		 'y0' : 100,
		 'x1' : 100,
		 'y1' : 200,
		 'id' : 1,
		 'name' : 'segment1',
		 'type' : "seg",
		 'comment' : 'Seg_1'
		},

    "segment2" :{'x0' : 200,
		 'y0' : 200,
		 'x1' : 200,
		 'y1' : 400,
		 'id' : 2,
		 'name' : 'segment2',
		 'type' : 'seg',
		 'comment' : 'Seg_2'
		},

};
var segment_set = 0;
var current_segment = 0;
var segment_set_length = 0;

function drawSegment(data){
    var path = "", line,x0,y0,x1,y1;
    if(segment_set) {
	clear_path(segment_set);
	segment_set.clear();
    }
    else {
	segment_set = map.paper.set();
    }
    segment_set_length = 0;


    $.each(data, function(name,value) {
        x0 = value['x0'] * map.scale_x;
        y0 = value['y0'] * map.scale_y;
        x1 = value['x1'] * map.scale_x;
        y1 = value['y1'] * map.scale_y;
        path  = "M" + x0 + "," + y0 ; 
        path += "L" + x1 + "," + y1 ; 

	line = map.paper.path(path);
	line.attr(segment_attr);

        line.data('key',name);
        line.data('id',value['id']);
        line.data('name',value['name']);
	line.data('index',segment_set_length);

        line.attr({'title': value['name']});
        segment_set.push(line);
        segment_set_length += 1;
    });
    if (segment_set_length == 0) {
        return false;
    }

    current_segment = 0;
    segment_set[current_segment].attr(segment_selected_attr);
    var msg = segment_set[current_segment].data('name');
    message(msg);

    var k = segment_set[current_segment].data("key");
    x0 = segment_datas[k]["x0"] * map.scale_x;
    y0 = segment_datas[k]["y0"] * map.scale_y;
    x1 = segment_datas[k]["x1"] * map.scale_x;
    y1 = segment_datas[k]["y1"] * map.scale_y;

    segment_controls = map.paper.set(
	map.paper.circle(x0, y0, 5).attr(drag_seg_point),
	map.paper.circle(x1, y1, 5).attr(drag_seg_point_end)
    );
    segment_controls[0].update = function (x, y){     
	var X = this.attr("cx") + x,
        Y = this.attr("cy") + y;
	var k = segment_set[current_segment].data("key");
	segment_datas[k]["x0"] = X /  map.scale_x;
	segment_datas[k]["y0"] = Y / map.scale_y;
        this.attr({cx: X, cy: Y});
	update_segment(k);
    };
    segment_controls[1].update = function (x, y){     
	var X = this.attr("cx") + x,
        Y = this.attr("cy") + y;
	var k = segment_set[current_segment].data("key");
	segment_datas[k]["x1"] = X /  map.scale_x;
	segment_datas[k]["y1"] = Y / map.scale_y;
        this.attr({cx: X, cy: Y});
	update_segment(k);
    };

    segment_controls.drag(move, up);
    segment_set.click(click_seg);    
    return true;
};

function click_seg(event){
    segment_set[current_segment].attr(segment_attr);
    current_segment = this.data("index");
    select_segment();
    return false;

};
function select_segment(){
    segment_set[current_segment].attr(segment_selected_attr);
    var msg = segment_set[current_segment].data('name');
    message(msg);
    var k = segment_set[current_segment].data("key");
    
    cx = segment_datas[k]["x0"] * map.scale_x;
    cy = segment_datas[k]["y0"] * map.scale_y;
    segment_controls[0].attr({"cx" : cx , "cy" : cy});

    cx = segment_datas[k]["x1"] * map.scale_x;
    cy = segment_datas[k]["y1"] * map.scale_y;
    segment_controls[1].attr({"cx" : cx , "cy" : cy});
};

function handle_move_segment_update(event) {

    var k = segment_set[current_segment].data("key");
    segment_datas[k]['name'] = $('#write').val();
    put_sda("putSegments",segment_datas);
    return false;
};

function handle_move_segment_next(event) {
    segment_set[current_segment].attr(segment_attr);
    current_segment++;
    if (current_segment >= segment_set_length) {
	current_segment = 0;
    }
    select_segment();
    return false;
};

function handle_move_segment_back(event) {
    segment_set.click(click_seg);    
    put_sda("putSegments",segment_datas);
    segment_set.attr(segment_attr);
    segment_controls[0].remove();
    segment_controls[1].remove();
    delete segment_controls;
    set_system_state('Ready');
    return false;
}  

function update_segment(k){
    var value = segment_datas[k];
    var x0 = value['x0'] * map.scale_x;
    var y0 = value['y0'] * map.scale_y;
    var x1 = value['x1'] * map.scale_x;
    var y1 = value['y1'] * map.scale_y;
    var path  = "M" + x0 + "," + y0 ; 
    path += "L" + x1 + "," + y1 ; 
    segment_set[current_segment].attr({path:path});
}


/*
*
*  Ajax function zone
*
*/
function get_display_segment() {
    $.get( "getDisplaySegment",
           { seg_no: 1},
           function(data) {
               segment_datas = data;
               drawSegment(data);
               //isAjaxFinished = true;
           }
         );
}; 


function put_segments(segments) {
    var arg = JSON.stringify(segments);
    console.log(arg);
    $.ajax({url:"putSegments",
            data: arg,
            type: 'POST',
            contentType: 'application/json',
            processData: false,
            dataType: "json",
            success: function(data) {console.log(data["result"]);},
           });
}; 

/***********************************************************************************************
 *
 *   Module
 * 
 ***********************************************************************************************/
dispatch['Module'] = {'LT': '提交',       'L' : handle_move_module_update,
		      'MT': '下一个',     'M' : handle_move_module_next,
		      'RT': '返回',       'R' : handle_move_module_back,
		      'MSG': '参数设置模式......'};


var icon_BOX = "M2,0h28c1.104,0,2,0.896,2,2v12c0,1.104-0.896,2-2,2H2c-1.104,0-2-0.896-2-2l0,0V2C0,0.896,0.896,0,2,0z";

var icon_PM ="M7.361,3.676h4.173c0.825,0,1.491,0.233,1.998,0.701s0.761,1.124,0.761,1.971c0,0.728-0.227,1.361-0.679,1.901c-0.453,0.539-1.146,0.81-2.078,0.81H8.624V13H7.361V3.676z M12.26,4.957c-0.277-0.131-0.658-0.196-1.141-0.196H8.624v3.231h2.496c0.563,0,1.02-0.121,1.371-0.362c0.351-0.241,0.526-0.667,0.526-1.276C13.017,5.668,12.765,5.203,12.26,4.957z";
icon_PM += "M15.879,3.676h1.81l2.681,7.883l2.663-7.883h1.797V13h-1.207V7.496c0-0.189,0.005-0.505,0.014-0.945c0.008-0.44,0.012-0.912,0.012-1.416L20.986,13h-1.252l-2.687-7.865v0.286c0,0.229,0.006,0.576,0.019,1.044s0.019,0.812,0.019,1.031V13h-1.206V3.676z";
var icon_LU ="M8.681,3.676h1.263v8.213h4.678V13H8.681V3.676z";
icon_LU += "M17.276,3.676v5.764c0,0.677,0.128,1.239,0.384,1.688c0.38,0.678,1.02,1.016,1.919,1.016c1.079,0,1.813-0.365,2.201-1.098c0.209-0.397,0.313-0.934,0.313-1.605V3.676h1.275v5.236c0,1.146-0.154,2.029-0.465,2.646c-0.568,1.126-1.643,1.689-3.223,1.689c-1.58,0-2.652-0.563-3.217-1.689C16.155,10.941,16,10.059,16,8.912V3.676H17.276z";

var icon_TU = "M15.46,3.676v1.11h-3.142V13h-1.276V4.786H7.9v-1.11H15.46z";
icon_TU += "M17.987,3.676v5.764c0,0.677,0.128,1.239,0.384,1.688c0.379,0.678,1.02,1.016,1.919,1.016c1.079,0,1.813-0.365,2.201-1.098c0.209-0.397,0.313-0.934,0.313-1.605V3.676h1.275v5.236c0,1.146-0.154,2.029-0.465,2.646c-0.568,1.126-1.643,1.689-3.223,1.689s-2.652-0.563-3.217-1.689c-0.31-0.617-0.465-1.5-0.465-2.646V3.676H17.987z";

var icon_RM="M7.393,3.676h4.239c0.698,0,1.273,0.104,1.727,0.311c0.86,0.397,1.29,1.132,1.29,2.203c0,0.559-0.115,1.016-0.346,1.371c-0.23,0.355-0.553,0.641-0.968,0.856c0.364,0.148,0.638,0.343,0.822,0.584c0.184,0.241,0.287,0.633,0.308,1.175l0.044,1.25c0.013,0.355,0.042,0.62,0.089,0.793c0.076,0.297,0.211,0.487,0.406,0.572V13h-1.549c-0.042-0.08-0.076-0.184-0.102-0.311s-0.046-0.373-0.063-0.736l-0.076-1.556c-0.029-0.609-0.249-1.018-0.66-1.226c-0.235-0.113-0.603-0.171-1.104-0.171H8.656V13H7.393V3.676z M11.495,7.947c0.576,0,1.032-0.118,1.368-0.355s0.503-0.664,0.503-1.282c0-0.664-0.234-1.117-0.704-1.358c-0.251-0.127-0.586-0.19-1.006-0.19h-3v3.187H11.495z";
icon_RM +="M16.597,3.676h1.81l2.682,7.883l2.662-7.883h1.797V13h-1.206V7.496c0-0.189,0.005-0.505,0.013-0.945s0.013-0.912,0.013-1.416L21.704,13h-1.252l-2.688-7.865v0.286c0,0.229,0.006,0.576,0.019,1.044s0.019,0.812,0.019,1.031V13h-1.206V3.676z";


var module_attr =  {"stroke" : "black",
		    "stroke-width" : 2,
		    "fill" : "#0F0",
		    "fill-opacity" : 1
		   };
var module_selected_attr =  {"stroke" : "red",
			     "stroke-width" : 2,
			     "fill" : "#0F0",
			     "fill-opacity" : 1
			    };

var module_text_attr =  {"stroke" : "black",
			 "stroke-width" : 1,
			 "fill" : "black",
			 "fill-opacity" : 1
			};


var module_datas = {
    'RM2': { 'x0' : 700,
	     'y0' : 100,
	     'x1' : 100,
	     'y1' : 100,
	     'id' : 2,
	     'name': "RM1",
	     'type' : "RM"
	   },	 

    'PM3': { 'x0' : 800,
	     'y0' : 100,
	     'x1' : 100,
	     'y1' : 100,
	     'id' : 3,
	     'name': "PM1",
	     'type' : "PM"
	   },	 

    'LU4': { 'x0' : 900,
	     'y0' : 100,
	     'x1' : 100,
	     'y1' : 100,
	     'id' : 4,
	     'name': "LU1",
	     'type' : "LU"
	   },	 
};


var device_set = 0;
var current_device = 0;
var device_set_length = 0;
var device_text = 0;
var device_controls;
var cx,cy;
function drawModule(data){
    var path = "", line,x0,y0,x1,y1,icon,dev_type;
    if(device_set) {
	clear_path(device_set);
	device_set.clear();
    }
    else {
	device_set = map.paper.set();
    }
    device_set_length = 0;

    if(device_text) {
	clear_path(device_text);
	device_text.clear();
    }
    else {
	device_text = map.paper.set();
    }

    $.each(data, function(name,value) {
        x0 = value['x0'] * map.scale_x;
        y0 = value['y0'] * map.scale_y;
        x1 = value['x1'] * map.scale_x;
        y1 = value['y1'] * map.scale_y;
        
	line = map.paper.path(icon_BOX);
	//line = map.paper.path(icon_seg);

	line.attr(module_attr);
        line.translate(x0,y0);
        line.data('key',name);
        line.data('id',value['id']);
        line.data('name',value['name']);
	line.data('index',device_set_length);

        line.attr({'title': value['name']});
        device_set.push(line);
        device_set_length += 1;

        dev_type = value['type'];
        switch(dev_type) {
        case "PM":
            icon = icon_PM;
            break;
        case "RM":
            icon = icon_RM;
            break;
        case "LU":
            icon = icon_LU;
            break;
        case "TU":
            icon = icon_TU;
            break;
        };

        line = map.paper.path(icon).attr(module_text_attr);
      	line.translate(x0,y0);
        device_text.push(line);
    });
    if (device_set_length == 0) {
        return false;
    }

    current_device = 0;
    device_set[current_device].attr(module_selected_attr);
    var msg = device_set[current_device].data('name');
    message(msg);

    var k = device_set[current_device].data("key");
    x0 = module_datas[k]["x0"] * map.scale_x;
    y0 = module_datas[k]["y0"] * map.scale_y;
    device_controls = map.paper.circle(x0, y0, 5).attr(drag_point);
    device_controls.update = function (x, y){     
	var X = this.attr("cx") + x,
        Y = this.attr("cy") + y;
	var k = device_set[current_device].data("key");
	module_datas[k]["x0"] = X /  map.scale_x;
	module_datas[k]["y0"] = Y / map.scale_y;
        this.attr({cx: X, cy: Y});
	device_set[current_device].transform('t'+ X + ','+ Y);
	device_text[current_device].transform('t'+ X + ','+ Y);   
    };

    device_controls.drag(move, up);
    device_set.click(click_dev);
    return true;
};

function click_dev(event){
    device_set[current_device].attr(module_attr);
    current_device = this.data("index");
    select_device();
    return false;

};
function select_device(){
    device_set[current_device].attr(module_selected_attr);
    var msg = device_set[current_device].data('name');
    message(msg);

    var k = device_set[current_device].data("key");
    
    cx = module_datas[k]["x0"] * map.scale_x;
    cy = module_datas[k]["y0"] * map.scale_y;
    device_controls.attr({"cx" : cx , "cy" : cy});

    return false;
};

function handle_move_module_update(event) {
    var k = device_set[current_device].data("key");
    module_datas[k]['name'] = $('#write').val();
    put_sda("putDevices",module_datas);
    message('Module Placement');
    return false;
};

function handle_move_module_next(event) {
    device_set[current_device].attr(module_attr);
    current_device++;
    if (current_device >= device_set_length) {
	current_device = 0;
    }
    select_device();
    return false;
};

function handle_move_module_back(event) {
    put_sda("putDevices",module_datas);
    device_set.attr(module_attr);
    device_controls.remove();
    set_system_state('Ready');
    return false;
}  

/**
 *  AJAX Function zone
 *
 */
function get_device() {
    $.get("getDevices",
          {dev_no: 1},
          function(data) {
              module_datas = data;
              drawModule(data);
          }
         );
}; 





/***********************************************************************************************
 *
 *   Auxiliary
 * 
 ***********************************************************************************************/


dispatch['Aux'] = {'LT': '提交',       'L' : handle_move_aux_update,
		   'MT': '下一个',     'M' : handle_move_aux_next,
		   'RT': '返回',       'R' : handle_move_aux_back,
		   'MSG': 'aux设置模式......'};

var auxiliary_attr = { "stroke" : "blue",
                       "stroke-width" : 2,
		       "fill" : "blue",
		       "fill-opacity" : 0.6
		     };

var auxiliary_selected_attr = { "stroke" : "red",
				"stroke-width" : 2,
				"fill" : "blue",
				"fill-opacity" : 0.6
			      };

var auxiliary_datas = {
    "auxiliary1" :{'x0' : 130,
		   'y0' : 130,
		   'x1' : 130,
		   'y1' : 210,
		   'x2' : 210,
		   'y2' : 210,
		   'x3' : 210,
		   'y3' : 130,
		   'id' : 1,
		   'name' : 'auxiliary1',
		   'type' : "seg"
		  },
    
    "auxiliary2" :{'x0' : 260,
		   'y0' : 260,
		   'x1' : 260,
		   'y1' : 420,
		   'x2' : 420,
		   'y2' : 420,
		   'x3' : 420,
		   'y3' : 260,
		   'id' : 2,
		   'name' : 'auxiliary2',
		   'type' : 'seg'
		  },
    "auxiliary3" :{'x0' : 300,
		   'y0' : 300,
		   'x1' : 200,
		   'y1' : 450,
		   'x2' : 350,
		   'y2' : 450,
		   'x3' : 450,
		   'y3' : 300,
		   'id' : 3,
		   'name' : 'auxiliary3',
		   'type' : "seg"
		  },
    
    "auxiliary4" :{'x0' : 500,
		   'y0' : 500,
		   'x1' : 600,
		   'y1' : 650,
		   'x2' : 800,
		   'y2' : 650,
		   'x3' : 700,
		   'y3' : 500,
		   'id' : 4,
		   'name' : 'auxiliary4',
		   'type' : 'seg'
		  },

};


var auxiliary_set = 0;
var current_auxiliary = 0;
var auxiliary_set_length = 0;

function drawAuxiliary(data){
    var path = "", line,x0,y0,x1,y1,x2,y2,x3,y3;
    if(auxiliary_set) {
	clear_path(auxiliary_set);
	auxiliary_set.clear();
    }
    else {
	auxiliary_set = map.paper.set();
    }
    auxiliary_set_length = 0;

    $.each(data, function(name,value) {
        x0 = value['x0'] * map.scale_x;
        y0 = value['y0'] * map.scale_y;
        x1 = value['x1'] * map.scale_x;
        y1 = value['y1'] * map.scale_y;
        x2 = value['x2'] * map.scale_x;
        y2 = value['y2'] * map.scale_y;
        x3 = value['x3'] * map.scale_x;
        y3 = value['y3'] * map.scale_y;

        path  = "M" + x0 + "," + y0 ; 
        path += "L" + x1 + "," + y1 ; 
        path += "L" + x2 + "," + y2 ; 
        path += "L" + x3 + "," + y3 ; 
	path += "Z";

	line = map.paper.path(path);
	line.attr(auxiliary_attr);

        line.data('key',name);
        line.data('id',value['id']);
        line.data('name',value['name']);
	line.data('index',auxiliary_set_length);
        line.attr({'title': value['name']});
        auxiliary_set.push(line);
        auxiliary_set_length += 1;
    });
    if (auxiliary_set_length == 0) {
        return false;
    }

    current_auxiliary = 0;
    auxiliary_set[current_auxiliary].attr(auxiliary_selected_attr);
    var msg = auxiliary_set[current_auxiliary].data('name');
    message(msg);
    var k = auxiliary_set[current_auxiliary].data("key");
    x0 = auxiliary_datas[k]["x0"] * map.scale_x;
    y0 = auxiliary_datas[k]["y0"] * map.scale_y;
    x1 = auxiliary_datas[k]["x1"] * map.scale_x;
    y1 = auxiliary_datas[k]["y1"] * map.scale_y;
    x2 = auxiliary_datas[k]["x2"] * map.scale_x;
    y2 = auxiliary_datas[k]["y2"] * map.scale_y;
    x3 = auxiliary_datas[k]["x3"] * map.scale_x;
    y3 = auxiliary_datas[k]["y3"] * map.scale_y;

    auxiliary_controls = map.paper.set(
	map.paper.circle(x0, y0, 5).attr(drag_point),
	map.paper.circle(x1, y1, 5).attr(drag_point),
	map.paper.circle(x2, y2, 5).attr(drag_point),
	map.paper.circle(x3, y3, 5).attr(drag_point)
    );
    auxiliary_controls[0].update = function (x, y){     
	var X = this.attr("cx") + x,
        Y = this.attr("cy") + y;
	var k = auxiliary_set[current_auxiliary].data("key");
	auxiliary_datas[k]["x0"] = X /  map.scale_x;
	auxiliary_datas[k]["y0"] = Y / map.scale_y;
        this.attr({cx: X, cy: Y});
	update_auxiliary(k);
    };
    auxiliary_controls[1].update = function (x, y){     
	var X = this.attr("cx") + x,
        Y = this.attr("cy") + y;
	var k = auxiliary_set[current_auxiliary].data("key");
	auxiliary_datas[k]["x1"] = X /  map.scale_x;
	auxiliary_datas[k]["y1"] = Y / map.scale_y;
        this.attr({cx: X, cy: Y});
	update_auxiliary(k);
    };

    auxiliary_controls[2].update = function (x, y){     
	var X = this.attr("cx") + x,
        Y = this.attr("cy") + y;
	var k = auxiliary_set[current_auxiliary].data("key");
	auxiliary_datas[k]["x2"] = X /  map.scale_x;
	auxiliary_datas[k]["y2"] = Y / map.scale_y;
        this.attr({cx: X, cy: Y});
	update_auxiliary(k);
    };
    auxiliary_controls[3].update = function (x, y){     
	var X = this.attr("cx") + x,
        Y = this.attr("cy") + y;
	var k = auxiliary_set[current_auxiliary].data("key");
	auxiliary_datas[k]["x3"] = X /  map.scale_x;
	auxiliary_datas[k]["y3"] = Y / map.scale_y;
        this.attr({cx: X, cy: Y});
	update_auxiliary(k);
    };

    auxiliary_controls.drag(move, up);
    auxiliary_set.click(click_aux);
    return true;
};

function click_aux(event){
    auxiliary_set[current_auxiliary].attr(auxiliary_attr);
    current_auxiliary = this.data("index");
    select_auxiliary();
    return false;

};

function select_auxiliary(){
    auxiliary_set[current_auxiliary].attr(auxiliary_selected_attr);
    var msg = auxiliary_set[current_auxiliary].data('name');
    message(msg);

    var k = auxiliary_set[current_auxiliary].data("key");
    
    cx = auxiliary_datas[k]["x0"] * map.scale_x;
    cy = auxiliary_datas[k]["y0"] * map.scale_y;
    auxiliary_controls[0].attr({"cx" : cx , "cy" : cy});

    cx = auxiliary_datas[k]["x1"] * map.scale_x;
    cy = auxiliary_datas[k]["y1"] * map.scale_y;
    auxiliary_controls[1].attr({"cx" : cx , "cy" : cy});

    cx = auxiliary_datas[k]["x2"] * map.scale_x;
    cy = auxiliary_datas[k]["y2"] * map.scale_y;
    auxiliary_controls[2].attr({"cx" : cx , "cy" : cy});

    cx = auxiliary_datas[k]["x3"] * map.scale_x;
    cy = auxiliary_datas[k]["y3"] * map.scale_y;
    auxiliary_controls[3].attr({"cx" : cx , "cy" : cy});

    return false;
};

function handle_move_aux_update(event) {
    var k = auxiliary_set[current_auxiliary].data("key");
    auxiliary_datas[k]['name'] = $('#write').val();
    put_sda("putAuxiliaries",auxiliary_datas);
    message('Auxiliary Placement');
    return false;
};

function handle_move_aux_next(event) {
    auxiliary_set[current_auxiliary].attr(auxiliary_attr);
    current_auxiliary++;
    if (current_auxiliary >= auxiliary_set_length) {
	current_auxiliary = 0;
    }
    select_auxiliary();
    return false;
};

function handle_move_aux_back(event) {
    put_sda("putAuxiliaries",auxiliary_datas);
    auxiliary_set.attr(auxiliary_attr);
    set_system_state('Ready');
    auxiliary_controls[0].remove();
    auxiliary_controls[1].remove();
    auxiliary_controls[2].remove();
    auxiliary_controls[3].remove();
    
    delete auxiliary_controls;
    return false;
}  

function update_auxiliary(k){
    var value = auxiliary_datas[k];
    var x0 = value['x0'] * map.scale_x;
    var y0 = value['y0'] * map.scale_y;
    var x1 = value['x1'] * map.scale_x;
    var y1 = value['y1'] * map.scale_y;
    var x2 = value['x2'] * map.scale_x;
    var y2 = value['y2'] * map.scale_y;
    var x3 = value['x3'] * map.scale_x;
    var y3 = value['y3'] * map.scale_y;

    var path  = "M" + x0 + "," + y0 ; 
    path += "L" + x1 + "," + y1 ; 
    path += "L" + x2 + "," + y2 ; 
    path += "L" + x3 + "," + y3 ; 
    path += "Z";
    auxiliary_set[current_auxiliary].attr({path:path});
}


/**
 *  AJAX Function zone
 *
 */
function get_auxiliary() {
    $.get("getAuxiliaries",
          {aux_no: 1},
          function(data) {
              auxiliary_datas = data;
              drawAuxiliary(data);
          }
         );
}; 

/***********************************************************************************************
 *
 *   Parament
 * 
 ***********************************************************************************************/

dispatch['parament'] = {'LT': '导入',      'L' : handle_parament_import,
			'MT': '导出',     'M' : handle_parament_export,
			'RT': '返回',     'R' : handle_parament_back,
			'MSG': '参数设置模式......'};

function handle_parament_import(event) {
    message('导入');
    return false;
};

function handle_parament_export(event) {
    message('导出');
    return false;
};

function handle_parament_back(Event) {
    set_system_state('Ready');
    return false;
};

///////////////////////////////////////////////////// Only Test !!!!!!!!!!!!!!






















