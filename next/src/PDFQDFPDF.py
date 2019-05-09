import os
import tempfile
from functools import reduce

import cv2
import numpy
import scipy.misc
import scipy as scipy
from PIL import Image
from matplotlib.patches import Circle
from pdf2image import convert_from_path
import matplotlib.pyplot as plt
import numpy as np
from scipy._lib.six import xrange


def scan_line(arr):
    result = []
    oldfield = 0
    i = 0
    temp = [arr[0]]
    width = 1
    for i in xrange(1, len(arr)):
        if arr[i]-arr[i-1] > 8:
            temp.append(width)
            if width > 20:
                result.append(temp)
            width = 1
            temp = [arr[i]]
        else:
            width += 1
    temp.append(width)
    if width > 20:
        result.append(temp)
    return result


def reduce_fields(fields):
    i = 0
    n = len(fields)
    fields = sorted(fields)
    new_fields = []
    for i in xrange(0,n-1):
        field_one = fields[i]
        if all((abs(field_one[0]-field_two[0]) + abs(field_one[1]-field_two[1])) > 6 for field_two in fields[i+1:]):
            new_fields.append(field_one)
    return new_fields










def main():

    path = "/home/jakob/Desktop/testImages/82+I_new-page-001.jpg"

    form = cv2.imread(path)

    mask = cv2.inRange(form, (160, 160, 160), (210, 210, 210))

    n = len(mask)
    m = len(mask[0])







    fields = []
    left = []
    segments = []

    for y in xrange(0,n):
        cur_row = mask[y]
        if max(cur_row) > 0:
            field_pixels = numpy.where(cur_row == max(cur_row))
            result = scan_line(field_pixels[0])
            for segment in result:
                segments.append([y, segment[0], segment[1], 1])
    fields = find_fields(segments)






def find_fields(rows):

    temp_fields = []
    fields = []
    append_flag = False
    if len(rows) > 0:
        current_fields = [rows.pop(0)]
        for row in rows:
            if len(current_fields) == 0:
                current_fields.append(row)
            #if row[]
            add_flag = True
            for field in current_fields:
                #[y,x,width,height]
                if abs(row[0]-(field[0] + field[3])) < 8:
                    if field[1] < row[1] < field[1] + field[2] or row[1] < field[1] < row[1] + row[2] \
                            or abs(field[1] - row[1]) < 8 or abs(field[1] + field[2] - row[1] + row[2]) < 8:
                        field[1] = min(field[1], row[1])
                        field[2] = max(row[1] + row[2], field[1] + field[2]) - min(field[1], row[1])
                        field[3] = row[0] - field[0]
                        add_flag = False
                elif field[3] > 8:
                    fields.append(field)
                    current_fields.remove(field)
                else:
                    current_fields.remove(field)
            if add_flag:
                current_fields.append(row)

    fields = reduce_fields(fields)

    print(fields)
    return fields



def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list


if __name__ == "__main__":
    main()

class Segment:
    def __init__(self,top,left,height,width):
        self.top = top
        self.left = left
        self.height = height
        self.width = width

