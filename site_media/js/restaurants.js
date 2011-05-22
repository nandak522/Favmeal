function retrieve_restaurantmenu(restaurant_alias){
	$.ajax({
		url:'/restaurants/'+restaurant_alias+'/',
		type:'GET',
		dataType:'json',
		beforeSend:function(){
			$('#restaurants_menu').html('<img alt="Please wait..." style="margin-top:4px;width:20px;height:20px;" src="/site_media/img/ajax-loader.gif"/>Retrieving Restaurant Menu');
		},
		error:function(response_data_xhr){
			if(response_data_xhr.status == '200'){
				$('selected_restaurant').value = restaurant_alias;
				$('#restaurants_menu').html(response_data_xhr.responseText);
				$('#restaurants > li').each(function(){$(this).attr('class','restaurant_nonselected');});
				$('#'+restaurant_alias).attr('class','restaurant_selected');
			}else{
				alert('There is a technical difficulty in preparing the Restaurant Menu. Please Try again. You can even place orders through phone. Its 040-32577666. Thankyou.');
			}
		},
		success:function(response_data){
			$('selected_restaurant').value = restaurant_alias;
			$('#restaurants_menu').html(""+response_data[0]);
			$('#restaurants > li').each(function(){$(this).attr('class','restaurant_nonselected');});
			$('#'+restaurant_alias).attr('class','restaurant_selected');
			$('#'+restaurant_alias).attr('style','color:#FFF;');
		}
	});
}
function show_restaurant_menu(restaurant_alias){
	if($('#cost').html() == '0'){
		retrieve_restaurantmenu(restaurant_alias);
	}else{
		var move_to_another_restaurant = confirm("Moving to another restaurant will cancel the existing Items Cart. You want to proceed?");
		if(move_to_another_restaurant){
			retrieve_restaurantmenu(restaurant_alias);
			$('#checkout_items').html('');
			$('#cost').html('0');
			closecart();
		}		
	}
}
function update_all_items(item_id,item_name,item_cost){
	old_items = $('#checkout_items').html();
	new_item = '<div class="cart_item" id="cart_item_'+item_id+'"><div class="item_name">'+item_name+'</div><div class="item_cost">'+item_cost+'<br/>Qty:<select id="item_quantity_'+item_id+'" onClick="javascript:update_cart_amount();return false;"><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option><option value="11">11</option><option value="12">12</option><option value="13">13</option><option value="14">14</option><option value="15">15</option><option value="16">16</option><option value="17">17</option><option value="18">18</option><option value="19">19</option><option value="20">20</option></select></div><div class="delete_link"><img style="cursor:pointer;" onClick="javascript:remove_from_cart(\''+item_id+'\');return false;" src="/site_media/img/icon_deletelink.gif"/></div><div style="clear:both;width:0%;height:0%;"></div></div>';
	$('#checkout_items').html(new_item + old_items);
}
function update_cart_amount(){
	total_cost = 0;
	$('#checkout_items .item_cost').each(function(){
												total_cost+=parseInt($(this).html())*(parseInt($(this).find('select').get(0).selectedIndex)+1);
										});
	$('#cost').html(''+total_cost);
}
function remove_item_from_cart(item_id){
	$('#cart_item_'+item_id).remove();
}
function remove_from_cart(item_id){
	remove_item_from_cart(item_id);
	update_cart_amount();
}
function add_to_cart(item_id, item_name,item_cost){
	update_all_items(item_id, item_name,item_cost);
	update_cart_amount();
}
function _calculate_totalitems_cost(){
	return parseInt($('#cost').html());
}
function confirm_cart(){
	if($('#id_selected_restaurant').length == 0){
		alert('Your checkout cart is empty. Please prepare the Items Cart and then click Checkout button');
	}
	total_cost = _calculate_totalitems_cost();
	if(total_cost>= 250){
		restaurant_alias = $('#id_selected_restaurant').get(0).value;
		if(restaurant_alias == ''){
			alert('Your checkout cart is empty. Please prepare the Items Cart and then click Checkout button');
		}else{
			item_ids = new Array();
			$('.cart_item').each(function(){
				item_id = this.id.substring(10);
				item_quantity = parseInt($('#item_quantity_'+item_id).get(0).selectedIndex)+1;
				for(i=0;i<item_quantity;i++){
					item_ids.push(this.id)	
				}
			});
			show_confirm_cart(restaurant_alias,item_ids);
		}
	}else{
		alert('You need to order atleast for Rs.250 to checkout')
	}
}
function show_confirm_cart(restaurant_alias,item_ids){
	item_ids = item_ids.join(',');
	$.ajax({
		url:'/orderconfirm/',
		type:'POST',
		data:{'item_ids':item_ids,'ralias':restaurant_alias},
		dataType:'json',
		beforeSend:function(){
		},
		error:function(response_data_xhr){
			if(response_data_xhr.status == '200'){
				$('#content').get(0).style.opacity='0.3';
				$('#confirm_cart').get(0).style.display='';
				$('#confirm_cart').center();
				build_order_table(response_data_xhr.responseText);
			}else{
				alert('There was a technical difficulty in preparing the Items Cart. Please click the Checkout button again. You can even place orders through phone. Its 040-32577666. Thankyou.');
			}
		},
		success:function(response_data){
			$('#content').get(0).style.opacity='0.3';
			$('#confirm_cart').get(0).style.display='';
			$('#confirm_cart').center();
			build_order_table(response_data[0]);
		}
	});
}
function build_items_list(response_content){
	old_content = $('#checkout_confirmationsummary').html();
	$('#checkout_confirmationsummary').html(old_content+response_content);
}
function build_order_table(response_content){
	build_items_list(response_content);
	$($("#confirm_cart").get(0)).height(54+$($('#checkout_confirmationsummary').get(0)).height())
}
function _debug_cart_response(response_data_xhr){//should only be used for testing, not for production use. Comment all the calls to this in production mode.
	//alert('Error:'+response_data_xhr.status+' Message:'+response_data_xhr.statusText);
	/* $.each(response_data, function(index, term) {
		alert(index+','+term);
	}); */
}
function closecart(){
	$('#content').get(0).style.opacity='1';
	$('#confirm_cart').get(0).style.display='none';
	clean_orderconfirmation_dialog();
}
function clean_orderconfirmation_dialog(){
	initial_ordercart_height = $($('#checkout_confirmationsummary').get(0)).height();
	$('.orderitem').remove();
	$('.orderitemcosts').remove();
	$('.buttons').remove();
	$('.ordertime').remove();
	$($("#confirm_cart").get(0)).height($($("#confirm_cart").get(0)).height() - initial_ordercart_height);
	
}
function post_order(){
	ordered_items_ids_quantity = new Array();
	$('.confirmeditem').each(function(){
		ordered_items_ids_quantity.push(this.value);
	});
	ordered_items_ids_quantity = ordered_items_ids_quantity.join(',');
	$.ajax({
		url:'/makeorder/',
		type:'POST',
		data:{'totalbill':$('#totalbill').get(0).innerHTML,'ordered_items_ids_quantity':ordered_items_ids_quantity, 'deliverytime':$('#deliverytime').get(0).innerHTML},
		dataType:'json',
		beforeSend:function(){
			$($('#confirmorder_button').get(0)).value = 'Please wait...';
			$($('#confirmorder_button').get(0)).disabled = true;
		},
		error:function(response_data_xhr){
			if(response_data_xhr.status != '200'){
				alert('There was a technical difficulty in preparing the Items Cart. Please click the Checkout button again. You can even place orders through phone. Its 040-32577666. Thankyou.');
			}
		},
		success:function(ordercreation_responsedict){
			if(ordercreation_responsedict["status"] == '500'){
				alert('There was a technical difficulty in preparing the Items Cart. Please click the Checkout button again. You can even place orders through phone. Its 040-32577666. Thankyou.');
			}else if(ordercreation_responsedict["status"] == '200'){
				document.location.href = '/ordersummary/?code='+ordercreation_responsedict["code"];
			}else{
				alert('There was a technical difficulty in Creating the Order. Please check back in a bit. You can even place orders through phone. Its 040-32577666. Thankyou.');
			}
		}
	});
}
function change_deliverytime(){
	hours = $('#available_hours').get(0).options[$('#available_hours').get(0).selectedIndex].value;
	$.ajax({
		url:'/computedeliverytime/',
		type:'POST',
		data:{'hours':hours},
		dataType:'json',
		beforeSend:function(){
			$($('#deliverytime').get(0)).html('Calculating Time. Please Wait...');
		},
		error:function(response_data_xhr){
			if(response_data_xhr.status == '200'){
				$($('#deliverytime').get(0)).html(response_data_xhr.responseText);
			}else{
				alert('There was a technical difficulty in preparing the Items Cart. Please click the Checkout button again. You can even place orders through phone. Its 040-32577666. Thankyou.');
			}
		},
		success:function(response_data){
			$($('#deliverytime').get(0)).html(response_data[0]);
		}
	});
}
$(document).ready(function() {
	$('li.restaurant_nonselected').click(function() {
			show_restaurant_menu(this.id);
	});
});