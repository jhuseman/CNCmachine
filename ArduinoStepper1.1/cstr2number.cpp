#include "cstr2number.h"
long cstr2number(char *num) {
	switch(num[0]) {
		case '-':
			return -1*cstr2number(&num[1]);
		case '+':
			return cstr2number(&num[1]);
		default:
			return String(num).toInt();
	}
}