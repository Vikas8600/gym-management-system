// Copyright (c) 2023, Milan Pethani and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gym Assign Workout Plan', {
	gym_workout_plan: function(frm) {
		if(frm.doc.gym_workout_plan){
			frm.clear_table("workout_plan_exercise");
			frm.refresh_fields();
			// frm.set_value('workout_plan_exercise', []);
			frappe.db.get_doc("Gym Workout Plan", frm.doc.gym_workout_plan)
			.then(({ workout_plan_exercise }) => {
				workout_plan_exercise.forEach(detail => {
					frm.add_child("workout_plan_exercise", {
						workout_exercise: detail.workout_exercise,
						equipment: detail.equipment,
						counts_duration: detail.counts_duration,
						week_day: detail.week_day
					});
				})
				frm.refresh_field('workout_plan_exercise')
			});
		}
	},
});
