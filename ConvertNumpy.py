############################################################################
#
#  Program: GDCM (Grassroots DICOM). A DICOM library
#
#  Copyright (c) 2006-2011 Mathieu Malaterre
#  All rights reserved.
#  See Copyright.txt or http://gdcm.sourceforge.net/Copyright.html for details.
#
#     This software is distributed WITHOUT ANY WARRANTY; without even
#     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#     PURPOSE.  See the above copyright notice for more information.
#
############################################################################

"""
This module add support for converting a gdcm.Image to a numpy array.

Caveats:
- Does not support UINT12/INT12

Removed:
- float16 is defined in GDCM API but no implementation exist for it
  in numpy.
"""

import gdcm
import numpy

def get_gdcm_to_numpy_typemap():
    """Returns the GDCM Pixel Format to numpy array type mapping."""
    _gdcm_np = {gdcm.PixelFormat.UINT8  :numpy.uint8,
                gdcm.PixelFormat.INT8   :numpy.int8,
                #gdcm.PixelFormat.UINT12 :numpy.uint12,
                #gdcm.PixelFormat.INT12  :numpy.int12,
                gdcm.PixelFormat.UINT16 :numpy.uint16,
                gdcm.PixelFormat.INT16  :numpy.int16,
                gdcm.PixelFormat.UINT32 :numpy.uint32,
                gdcm.PixelFormat.INT32  :numpy.int32,
                #gdcm.PixelFormat.FLOAT16:numpy.float16,
                gdcm.PixelFormat.FLOAT32:numpy.float32,
                gdcm.PixelFormat.FLOAT64:numpy.float64 }
    return _gdcm_np

def get_numpy_array_type(gdcm_pixel_format):
    """Returns a numpy array typecode given a GDCM Pixel Format."""
    return get_gdcm_to_numpy_typemap()[gdcm_pixel_format]

def gdcm_to_numpy(image):
    """Converts a GDCM image to a numpy array.
    """
    pf = image.GetPixelFormat()
    samples_per_pixel = pf.GetSamplesPerPixel()

    assert pf.GetScalarType() in get_gdcm_to_numpy_typemap().keys(), \
           f"Unsupported array type {pf}"

    shape = image.GetDimensions() # (x, y, z) = (cols, rows, frames)
    shape.reverse()
    shape.append(samples_per_pixel)

    dtype = get_numpy_array_type(pf.GetScalarType())
    image_buffer = image.GetBuffer()
    gdcm_array = image_buffer.encode("utf-8", errors="surrogateescape") # bytes
    result = numpy.frombuffer(gdcm_array, dtype=dtype)
    result.shape = shape
    return result

if __name__ == "__main__":
  import sys
  r = gdcm.ImageReader()
  filename = sys.argv[1]
  r.SetFileName( filename )
  if not r.Read():
    sys.exit(1)

  numpy_array = gdcm_to_numpy( r.GetImage() )
  print("For single-frame shape is (rows, cols, samplesPerPixel)")
  print("For multi-frame shape is (frames, rows, cols, samplesPerPixel)")
  print("numpy_array.shape:", numpy_array.shape)
  print("numpy_array:")
  print(numpy_array)
