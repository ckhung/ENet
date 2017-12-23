#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage: python semseg.py -c semseg.conf -o ~/result/ *.jpg
"""
import os, sys, configargparse, warnings
import numpy as np
# from os.path import join
caffe_root = os.environ['CAFFE_PATH'] # Change this to the absolute directory to ENet Caffe

sys.path.insert(0, caffe_root + '/python')
import caffe
# sys.path.append('/usr/local/lib/python2.7/site-packages')
sys.path.append('/usr/local/lib/python3.5/site-packages/')
import cv2


__author__ = 'Timo Sämann'
__university__ = 'Aschaffenburg University of Applied Sciences'
__email__ = 'Timo.Saemann@gmx.de'
__data__ = '24th May, 2017'


def make_parser():
    parser = configargparse.ArgumentParser(default_config_files=['semseg.conf'])
    parser.add('-c', '--config', required=True, is_config_file=True,
        help='config file path')
    parser.add_argument('-m', '--model', type=str, required=True,
        help='.prototxt file for inference')
    parser.add_argument('-w', '--weights', type=str, required=True,
        help='.caffemodel file')
    parser.add_argument('-p', '--palette', type=str, required=True,
        help='label color palette')
    parser.add_argument('-o', '--out_dir', type=str, default='/tmp',
        help='output directory in which the segmented images should be stored')
    parser.add_argument('image_files', nargs='*',
        help='input images')
    return parser

if __name__ == '__main__':
    parser1 = make_parser()
    args = parser1.parse_args()

    if not os.access(args.out_dir, os.W_OK):
        sys.exit('Cannot write to output directory "'+ args.out_dir + '". Computation aborted.')
    net = caffe.Net(args.model, args.weights, caffe.TEST)

    input_shape = net.blobs['data'].data.shape
    output_shape = net.blobs['deconv6_0_0'].data.shape
    label_palette = cv2.imread(args.palette, 1).astype(np.uint8)

    for i in list(range(len(args.image_files))):
        image_filename = args.image_files[i]
        if not os.access(image_filename, os.R_OK):
            warnings.warn('Cannot read file: "' + image_filename + '". Skipping.')
            continue
        else:
            print('processing file "' + image_filename + '"')
        input_image = cv2.imread(args.image_files[i], 1).astype(np.float32)
        orig_shape = input_image.shape[1::-1]
        input_image = cv2.resize(input_image, (input_shape[3], input_shape[2]))
        input_image = np.asarray(input_image.transpose((2, 0, 1)))
        out = net.forward_all(**{net.inputs[0]: input_image})
        prediction = net.blobs['deconv6_0_0'].data[0].argmax(axis=0)
        prediction = np.squeeze(prediction)
        prediction = np.resize(prediction, (3, input_shape[2], input_shape[3]))
        prediction = prediction.transpose(1, 2, 0).astype(np.uint8)

        prediction_rgb = np.zeros(prediction.shape, dtype=np.uint8)
        label_palette_bgr = label_palette[..., ::-1]
        cv2.LUT(prediction, label_palette_bgr, prediction_rgb)
        prediction_rgb = cv2.resize(prediction_rgb, orig_shape)

        out_filename = args.out_dir + '/' + image_filename.split('/')[-1]
        cv2.imwrite(out_filename, prediction_rgb)

