#include "axis_list.h"

AxisList::AxisList(int max_axes_num) {
	max_axes = max_axes_num;
	num_axes = 0;
	axes = (Axis**)malloc(max_axes*sizeof(Axis *));
}

bool AxisList::add(Axis *new_axis) {
	if(num_axes<max_axes) {
		axes[num_axes] = new_axis;
		num_axes++;
		return true;
	}
	return false;
}