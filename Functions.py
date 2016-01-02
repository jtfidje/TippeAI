#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Covey

# Standard libraries

# Third-party libraries
import numpy

# Own libraries

'''
Create an Numpy Array from a Pyhon list type
'''
def create_ndarray(lst):
	
	arr = numpy.array(lst, dtype=numpy.float32)

	return arr

'''
Create custom data tuple to be used as input to Neural Network
'''
def create_data_tuple(data_list):
	lvl_3_0 = list()
	lvl_3_1 = list()

	for f in data_list:
		lvl_3_0.append(create_ndarray(f[0]))
		lvl_3_1.append(f[1])

	lvl_2_0 = create_ndarray(lvl_3_0)
	lvl_2_1 = create_ndarray(lvl_3_1)

	lvl_1_0 = (lvl_2_0, lvl_2_1)

	return lvl_1_0

