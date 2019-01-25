#ifndef AXIS_LIST_H
#define AXIS_LIST_H
#include <Arduino.h>

#include "Axis.h"

class AxisList {
	private:
		int max_axes;
		int num_axes;
		Axis **axes;
	public:
		AxisList(int max_axes_num);
		bool add(Axis *new_axis);

		Axis **__get_axis_array_raw__() {
			return axes;
		}
		int __get_num_axes_raw__() {
			return num_axes;
		}
};

template <typename Func>

void iter_axes(AxisList *axis_list, Func const&callback) {
	Axis **axes = axis_list->__get_axis_array_raw__();
	int num_axes = axis_list->__get_num_axes_raw__();
	for(int i=0; i<num_axes; i++) {
		Axis *this_axis = axes[i];
		if(this_axis!=NULL) {
			callback(this_axis);
		}
	}
}
#endif