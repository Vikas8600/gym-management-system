frappe.pages['gym-member-subscript'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Gym Member Subscription Plan',
		single_column: true
	});
	frappe.gym_subscription.make(page)
}

frappe.gym_subscription = {
	start: 0,
	make: function(page) {
		page.start = 0
		var me = frappe.gym_subscription;
		me.page = page;
		me.body = $('<div class="list-data"></div>').appendTo(me.page.main);
		me.page.gym_member_field = page.add_field({
			fieldname: 'gym_member',
			label: __('Member'),
			fieldtype: 'Link',
			options: 'Gym Member',
			change: function() {
				me.run();
			},
			get_query: function() {
				return {
					filters: {
						"enabled": 1
					}
				};
			},
		});
		page.set_secondary_action('Refresh', () => me.run(), 'refresh');
		me.run();
	},
	run: function() {
		var me = frappe.gym_subscription;
		let params = (new URL(document.location)).searchParams;
		var gym_member = me.page.gym_member_field.get_value();
		frappe.call({
			method: 'gym_management_system.gym_management_system.page.gym_member_subscript.gym_member_subscript.get_data',
			args:{
				'gym_member':gym_member
			},
			callback: function(r) {
				$('.list-data').html('')
				if (r.message) {
					var filters_data = {'active_sub': null, 'expired_sub': null}
					if (r.message[0] && r.message[0].length > 0){
						filters_data['active_sub'] = r.message[0]
					}
					if (r.message[1] && r.message[1].length > 0){
						filters_data['expired_sub'] = r.message[1]
					}

					if (filters_data){
						$(frappe.render_template('gym_member_subscript', filters_data)).appendTo(me.body);
					}
					
				} else {
					frappe.show_alert({message: __('No Data'), indicator: 'gray'});
				}
			}
		});
	},
}