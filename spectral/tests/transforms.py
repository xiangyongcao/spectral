#########################################################################
#
#   transforms.py - This file is part of the Spectral Python (SPy) package.
#
#   Copyright (C) 2013 Thomas Boggs
#
#   Spectral Python is free software; you can redistribute it and/
#   or modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 2
#   of the License, or (at your option) any later version.
#
#   Spectral Python is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this software; if not, write to
#
#               Free Software Foundation, Inc.
#               59 Temple Place, Suite 330
#               Boston, MA 02111-1307
#               USA
#
#########################################################################
#
# Send comments to:
# Thomas Boggs, tboggs@users.sourceforge.net
#

import numpy as np
from numpy.testing import assert_almost_equal
from spytest import SpyTest, test_method


class LinearTransformTest(SpyTest):
    '''Tests that LinearTransform objects produce correct values.'''
    def __init__(self, file, datum, value):
        '''
        Arguments:

            `file` (str or `SpyFile`):

                The SpyFile to be tested.  This can be either the name of the
                file or a SpyFile object that has already been opened.

            `datum` (3-tuple of ints):

                (i, j, k) are the row, column and band of the datum to be
                tested. 'i' and 'j' should be at least 10 pixels away from the
                edge of the associated image and `k` should have at least 10
                bands above and below it in the image.

            `value` (int or float):

                The scalar value associated with location (i, j, k) in
                the image.
        '''
        self.file = file
        self.datum = datum
        self.value = value

    def setup(self):
        import numpy as np
        import spectral
        if isinstance(self.file, spectral.SpyFile):
            self.image = self.file
        elif isinstance(self.file, np.ndarray):
            self.image = self.file
        else:
            self.image = spectral.open_image(self.file)

        self.scalar = 10.
        self.matrix = self.scalar * np.identity(self.image.shape[2],
                                                dtype='f8')
        self.pre = 37.
        self.post = 51.

    @test_method
    def test_scalar_multiply(self):
        from spectral.algorithms.transforms import LinearTransform
        (i, j, k) = self.datum
        transform = LinearTransform(self.scalar)
        result = transform(self.image[i, j])[k]
        assert_almost_equal(result,
                            self.scalar * self.value)

    @test_method
    def test_pre_scalar_multiply(self):
        from spectral.algorithms.transforms import LinearTransform
        (i, j, k) = self.datum
        transform = LinearTransform(self.scalar, pre=self.pre)
        result = transform(self.image[i, j])[k]
        assert_almost_equal(result,
                            self.scalar * (self.pre + self.value))

    @test_method
    def test_scalar_multiply_post(self):
        from spectral.algorithms.transforms import LinearTransform
        (i, j, k) = self.datum
        transform = LinearTransform(self.scalar, post=self.post)
        result = transform(self.image[i, j])[k]
        assert_almost_equal(result,
                            self.scalar * self.value + self.post)

    @test_method
    def test_pre_scalar_multiply_post(self):
        from spectral.algorithms.transforms import LinearTransform
        (i, j, k) = self.datum
        transform = LinearTransform(self.scalar, pre=self.pre,
                                    post=self.post)
        result = transform(self.image[i, j])[k]
        assert_almost_equal(result,
                            self.scalar * (self.pre + self.value)
                            + self.post)

    @test_method
    def test_matrix_multiply(self):
        from spectral.algorithms.transforms import LinearTransform
        (i, j, k) = self.datum
        transform = LinearTransform(self.matrix)
        result = transform(self.image[i, j])[k]
        assert_almost_equal(result,
                            self.scalar * self.value)

    @test_method
    def test_pre_matrix_multiply(self):
        from spectral.algorithms.transforms import LinearTransform
        (i, j, k) = self.datum
        transform = LinearTransform(self.matrix, pre=self.pre)
        result = transform(self.image[i, j])[k]
        assert_almost_equal(result,
                            self.scalar * (self.pre + self.value))

    @test_method
    def test_matrix_multiply_post(self):
        from spectral.algorithms.transforms import LinearTransform
        (i, j, k) = self.datum
        transform = LinearTransform(self.matrix, post=self.post)
        result = transform(self.image[i, j])[k]
        assert_almost_equal(result,
                            self.scalar * self.value + self.post)

    @test_method
    def test_pre_matrix_multiply_post(self):
        from spectral.algorithms.transforms import LinearTransform
        (i, j, k) = self.datum
        transform = LinearTransform(self.matrix, pre=self.pre,
                                    post=self.post)
        result = transform(self.image[i, j])[k]
        assert_almost_equal(result,
                            self.scalar * (self.pre + self.value)
                            + self.post)

    def run(self):
        '''Executes the test case.'''
        self.setup()
        self.test_scalar_multiply()
        self.test_pre_scalar_multiply()
        self.test_scalar_multiply_post()
        self.test_pre_scalar_multiply_post()
        self.test_matrix_multiply()
        self.test_pre_matrix_multiply()
        self.test_matrix_multiply_post()
        self.test_pre_matrix_multiply_post()
        self.finish()


def run():
    import spectral as spy
    (fname, datum, value) = ('92AV3C.lan', (99, 99, 99), 2057.0)
    image = spy.open_image(fname)
    test = LinearTransformTest(image, datum, value)
    test.run()
    data = image.load()
    test = LinearTransformTest(data, datum, value)
    test.run()
    image.scale_factor = 10000.0
    test = LinearTransformTest(image, datum, value / 10000.0)
    test.run()

if __name__ == '__main__':
    run()
