$( window ).resize(function() {
if (window.innerWidth>900){
if (  $("#sidebar").attr("class").includes("opened")){
	$("#sidebar").css("width",70);
	$("#edit-sidebar").hide();
	$("body").css("width",window.innerWidth-70);
}
}
});
$(document).keypress(function(e) {
	if(e.ctrlKey && e.keyCode==11) {
		if (  $("#sidebar").attr("class").includes("opened")){
		var width=$("#sidebar").css("width");
		if(width=="70px"){
			open_sidebar();
		}
		if (width=="260px"){
			close_all_childs();
			close_sidebar();
		}
		}
	}
});


$(".llayout-side-section").css("display","none");
//action when module clicked from scroll bar
$(".carousel-cell").click(function(){
	clear_selected()
	$(this).addClass( "selected_module");
  });
//action when module clicked from scroll bar , except home
$(".normal-module").click(function(){
	clear_sidebar();
	 close_all_childs();
	if ( ! $("#sidebar").attr("class").includes("opened")){
	if (window.innerWidth>400){
	$("body").animate({"width":window.innerWidth-70});}}
	show_sidebar();
	$(".carousel-custom").slideUp();
	var id = $(this).attr('id');
	
	set_sidebar(id);
	//$("#sidebar").animate({width:70});
	//$("#closesidebar").hide();
	//$("#opensidebar").show();
	//$(".layout-side-section").css("display","none");
});
function gohome(){
	 close_all_childs();
	if (  $("#sidebar").attr("class").includes("opened")){
	$("#sidebar").css("width",70);
	hide_sidebar();
	$("body").animate({"width":"100%"});
		}
	$("#edit-sidebar").hide();
	$("#opensidebar").show();
	$("#closesidebar").hide();
	$(".carousel-custom").slideDown();
	clear_sidebar();
}
//action when home module clicked from scroll bar 
$(".home-module ,.app-logo").click(function(){
	gohome();
	//$(".layout-side-section").css("display","none");
});
function open_sidebar(){
	$("#sidebar").animate({width:260}, function(){ $("#edit-sidebar").show();});
	$("#opensidebar").hide();
	$("#closesidebar").show();
	if (window.innerWidth>900){
		$("body").animate({"width":window.innerWidth-260});
	}
	
}
$("#module-name-a").click(function(){
	close_all_childs();
	close_sidebar();

});
function close_sidebar(){
	$("#sidebar").animate({width:70});
	close_all_childs();
	if (window.innerWidth>900){
	$("body").animate({"width":window.innerWidth-70});}
	$("#closesidebar").hide();
	$("#opensidebar").show();
	$("#edit-sidebar").hide();
	//$('.sidebar-child').slideUp();
}
$("#opensidebar").click(function(){
	open_sidebar()
});
$("#closesidebar").click(function(){
	close_sidebar();
});
$("#logout-custom").click(function(){
frappe.app.logout();
window.location.href ="/login";
});
function clear_selected(){
	$(".carousel-cell").removeClass( "selected_module");
};

//remove all items from sidebar
function clear_sidebar(){
	$('.sidebar-item-custom').slideUp(function(){ $(this).remove()});
	//$('.sidebar-item-custom').remove();
};
//set menu to sidebar according to menu selected
function set_sidebar(module){
//	if {!module) return [];
	$("#module-name").html(__(module));
	$("#module-name-a").attr("href","/app/"+module.toLowerCase().replaceAll(" ","-"));
	$("#module-name-edit").val(__(module));
	frappe.call({
		method:"slnee_theme.desktop.sidebar.get_sidebar",
		args: {
			"module":module
		},
		async:true,
		callback(r){
			if(r.message){
				clear_sidebar();
				var items=r.message["items"];
				console.log(items);
				$("head").append(r.message["font_css"]);
				$("#sidebar").css("background-image", "linear-gradient("+r.message["direction"]+", "+r.message['color1']+", "+r.message['color2']+")");
				for (var i=0; i<items.length ;i++){
					 insert_element_sidebar(items[i],r.message["font"]);
				}
				//$(".child-items").css("background-image", "linear-gradient("+r.message["direction"]+", "+r.message['color1']+", "+r.message['color2']+")");
				slidedown_sidebar();
				$(".child-items").click(function(){
					close_all_childs();
				});
				$(".sidebar-title").css("color",r.message["color2"]);
			}
		}
	});
};
function show_sidebar(){
	$("#sidebar").addClass("opened-custom");
};
function hide_sidebar(){
	$("#sidebar").removeClass("opened-custom");
};
function slidedown_sidebar(){
	$('.sidebar-parent').slideDown();
}
function close_all_childs(){
	$(".child-items").slideUp("fast");
	$(".sidebar-parent").css("border","")
}
function click_parent(parent){
	var p="#"+parent.replaceAll(" ","-")+"-childs";
	var d=$(p).css("display");
	close_all_childs();
	//$("[item-name='"+parent+"']").css("border","solid 1px gray")
	//if (  $("#sidebar").width()<70){open_sidebar();}
	//var position = $("[item-parent='"+parent+"']").position();
	//console.log(parent);
	if (d=="none"){
	$("[item-name='"+parent+"']").css("border","solid 1px gray");
	$(p).slideDown("fast");}
};
function insert_element_sidebar(item,font="",type="parent",parent="",insert_into=""){
	var sidebar=$("#sidebar-custom");
	if (insert_into){
		var sidebar=$("#"+insert_into.replaceAll(" ","-"));
	}
	if (type=="parent"){
		var element="<div onclick='click_parent(`"+item["label"]+"`)' style='display:none;' class='sidebar-item-custom sidebar-parent sidebar-item-container is-draggable' item-parent='' item-name='"+item["label"]+"' item-public='1'>";
		element+="<div class='desk-sidebar-item standard-sidebar-item-custom desk-sidebar-item-custom'>";
		element+="<span class='item-anchor align-custom' title='"+item["label"]+"'>";
		element+="<span class='item-anchor align-custom' title='"+item["label"]+"'>";
		
		if (item["image"]){
			element+="<img class='icon-size image-custom' src='"+item["image"]+"' style='' alt=''>";
		}else{
		element+="<span class='sidebar-item-icon sidebar-item-icon-custom' item-icon='"+item["icon"]+"'><svg class='sidebar-icon icon  icon-md' style=''>";
		element+="<use class='' href='#icon-"+item["icon"]+"'></use>";
		element+="</svg></span>"
		}
		element+="<span class='sidebar-item-label' style='font-family:"+font+"'>"+item["label"]+"<span></span></span></span>";
	}else{
		var element="<div style='' class='sidebar-item-custom sidebar-child sidebar-item-container is-draggable' item-parent='"+parent+"' item-$name='"+item["label"]+"' item-public='1'>";
		element+="<div class='desk-sidebar-item standard-sidebar-item-custom desk-sidebar-item-custom sidebar-item-child' style='padding-top:0px !important;padding-bottom:0px !important;'>";
		element+="<a href='"+item["url"]+"' class='item-anchor align-customm' title='"+item["label"]+"'>";
	element+="<span class='item-anchor align-customm' title='"+item["label"]+"'>";
	//element+="<span class='sidebar-item-icon sidebar-item-icon-custom' item-icon='"+item["icon"]+"'><svg class='sidebar-icon icon  icon-md' style=''>";
	//element+="<use class='' href='#icon-"+item["icon"]+"'></use>";
	element+="<span class='sidebar-item-label' style='font-family:"+font+"'>&#x2022; "+item["label"]+"<span></span></span></a>";}
	element+="</div></div>";
	sidebar.append(element);
	if (type=="parent"){
		if (item.childs.length >0){
			var div ="<div id='"+item["label"].replaceAll(" ","-")+"-childs' class='child-items'  style='position:absolute;z-index:9998;display:none;'>";
			div+="<div class='sidebar-title'><span  style='font-family:"+font+";font-weight:bold;'>"+item["label"]+"</span></div>"
			div+="</div>"
			$("#top-sidebar").append(div);
}}
	//element+="</div>";
	//sidebar.append(element);

	for (var i=0;i<item.childs.length;i++){
		insert_element_sidebar(item.childs[i],font,"child",item["label"],item["label"]+"-childs")
	}}

$("#edit-sidebar").click(function(){
	$(".item-original").toggle();
	$(".item-editing").toggle();
	$(this).toggle();
	$("#save-sidebar").toggle();
});

$("#save-sidebar").click(function(){
	var module_name=$("#module-name-edit").val();
	frappe.call({
		method:"slnee_theme.desktop.sidebar.update_sidebar",
		args:{
			module:$("#module-name").html(),
			new_name:module_name,
			childs:[]
		}
	});

});
