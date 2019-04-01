from __future__ import absolute_import

import sys
import os

sys.path.append(os.path.abspath('../gryds'))

from unittest import TestCase
import numpy as np
import gryds
import gryds.interpolators.bspline_cuda
DTYPE = gryds.DTYPE


class TestLinearInterpolator(TestCase):
    """Tests grid initialization and scaling."""
    
    def test_2d_bspline_cuda_interpolator_90_deg_rotation(self):
        image = np.array([
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0]
        ], dtype=DTYPE)
        expected = np.array([
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ], dtype=DTYPE) # Borders will be zero due to being outside of image domain
        intp = gryds.interpolators.BSplineInterpolatorCUDA(image)
        trf = gryds.AffineTransformation(ndim=2, angles=[np.pi/2.], center=[0.4, 0.4])
        new_image = intp.transform(trf).astype(DTYPE)
        np.testing.assert_almost_equal(expected, new_image, decimal=4)

    def test_2d_bspline_cuda_interpolator_45_deg_rotation(self):
        image = np.array([
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0]
        ], dtype=DTYPE)
        expected = np.array([
            [0, 0, 0., 0, 0],
            [0., 1., 0.5, 1., 0.],
            [0., 0.5, 1., 0.5, 0.],
            [0., 1., 0.5, 1., 0.],
            [0., 0., 0., 0., 0.]
        ], dtype=DTYPE) # Borders will be zero due to being outside of image domain
        intp = gryds.interpolators.BSplineInterpolatorCUDA(image, mode='mirror')
        trf = gryds.AffineTransformation(ndim=2, angles=[np.pi/4.], center=[0.4, 0.4])
        new_image = intp.transform(trf).astype(DTYPE)
        np.testing.assert_almost_equal(expected, new_image, decimal=4)

    def test_3d_bspline_cuda_interpolator_90_deg_rotation(self):
        image = np.zeros((2, 5, 5))
        image[1] = np.array([[
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0]
        ]], dtype=DTYPE)
        image[0] = image[1]
        expected = np.zeros((2, 5, 5))
        expected[0] = np.array([
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0]
        ], dtype=DTYPE) # Borders will be zero due to being outside of image domain
        intp = gryds.interpolators.BSplineInterpolatorCUDA(image)
        trf = gryds.AffineTransformation(ndim=3, angles=[np.pi/2., 0, 0], center=[0.4, 0.4, 0.4])
        new_image = intp.transform(trf).astype(DTYPE)
        np.testing.assert_almost_equal(expected, new_image, decimal=4)

    def test_3d_bspline_cuda_interpolator_45_deg_rotation(self):
        image = np.array([
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0]
        ], dtype=DTYPE)
        expected = np.array([
            [0, 0, 0., 0, 0],
            [0., 1., 0.5, 1., 0.],
            [0., 0.5, 1., 0.5, 0.],
            [0., 1., 0.5, 1., 0.],
            [0., 0., 0., 0., 0.]
        ], dtype=DTYPE) # Borders will be zero due to being outside of image domain
        intp = gryds.interpolators.BSplineInterpolatorCUDA(image)
        trf = gryds.AffineTransformation(ndim=2, angles=[np.pi/4.], center=[0.4, 0.4])
        new_image = intp.transform(trf, mode='nope').astype(DTYPE)
        np.testing.assert_almost_equal(expected, new_image, decimal=4)

    def test_bspline_cuda_interpolator_sampling(self):

        image = np.array([
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0]
        ], dtype=DTYPE)
        intp = gryds.interpolators.BSplineInterpolatorCUDA(image)

        np.testing.assert_equal(intp.sample([0, 2.5], mode='NOPE'), 0.5)


    def test_bspline_cuda_interpolator_error(self):

        image = np.random.rand(3, 3, 3, 3)
        self.assertRaises(ValueError, gryds.interpolators.bspline_cuda, image)

