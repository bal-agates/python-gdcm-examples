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
display a DICOM image with matPlotLib via numpy

Caveats:
- Does not support UINT12/INT12

Usage:

 python ConvertMPL.py DICOM_IMAGE_FILE

Thanks:
  plotting example - Ray Schumacher 2009
"""

import gdcm
import numpy
from matplotlib import pyplot as plt


def get_gdcm_to_numpy_typemap():
    """Returns the GDCM Pixel Format to numpy array type mapping."""
    _gdcm_np = {gdcm.PixelFormat.UINT8  :numpy.uint8,
                gdcm.PixelFormat.INT8   :numpy.int8,
                gdcm.PixelFormat.UINT16 :numpy.uint16,
                gdcm.PixelFormat.INT16  :numpy.int16,
                gdcm.PixelFormat.UINT32 :numpy.uint32,
                gdcm.PixelFormat.INT32  :numpy.int32,
                gdcm.PixelFormat.FLOAT32:numpy.float32,
                gdcm.PixelFormat.FLOAT64:numpy.float64 }
    return _gdcm_np

def get_numpy_array_type(gdcm_pixel_format):
    """Returns a numpy array typecode given a GDCM Pixel Format."""
    return get_gdcm_to_numpy_typemap()[gdcm_pixel_format]

def gdcm_to_numpy(image):
    """Converts a GDCM image to a numpy array.
    """
    pi = image.GetPhotometricInterpretation()
    samples_per_pixel = pi.GetSamplesPerPixel()
    pi_type = pi.GetType()
    print('PhotoInterp:', pi)
    if pi_type == 3:
        print("WARNING: Palette image not fully decoded")
    if pi_type == 1:
        cmap = "gray"
    elif pi_type == 2:
        cmap = "gray_r"
    else:
        cmap = None
   
    pf = image.GetPixelFormat().GetScalarType()
    print('pixelFormat', pf)
    print('pixelDataType', image.GetPixelFormat().GetScalarTypeAsString())
    assert pf in get_gdcm_to_numpy_typemap().keys(), \
           f"Unsupported array type {pf}"

    d = image.GetDimensions()   # (cols, rows[, frames]) = (x, y[, z])
    assert len(d) == 2, f"Must have 2D image dims={d}"
    print(f'Image Size: {d[0]} x {d[1]}')

    dtype = get_numpy_array_type(pf)
    image_buffer = image.GetBuffer()    # str
    buffer = image_buffer.encode("utf-8", errors="surrogateescape") # bytes
    buffer_len = len(buffer)
    print("len(buffer):", buffer_len)
    # If pi_type is PALETTE need to decode using lookup table.
    # Below is the general concept but it has type errors.
    # lut = image.GetLUT()
    # decoded_len = 3*buffer_len
    # decoded_buffer = bytearray(decoded_len)  # init to 0
    # lut.Decode(decoded_buffer, decoded_len, buffer, buffer_len)
    # samples_per_pixel *= 3

    # Use float for accurate scaling.
    # Valid range for imshow with RGB data ([0..1] for floats or [0..255] for integers).
    # result = numpy.frombuffer(gdcm_array, dtype=dtype).astype(float)/255.0
    result = numpy.frombuffer(buffer, dtype=dtype)
    ## optional gamma scaling
    #maxV = float(result[result.argmax()])
    #result = result + .5*(maxV-result)
    #result = numpy.log(result+50) ## apprx background level

    # Reverse the order of dims so (rows, cols)
    result.shape = (d[1], d[0], samples_per_pixel)
    print("numpy shape:", result.shape)

    fig, ax = plt.subplots()
    ax.set_title(filename)
    # Many possible colormaps (cmap).
    ax.imshow(result, cmap=cmap)
    plt.show()

    return result

if __name__ == "__main__":
    import sys
    r = gdcm.ImageReader()
    filename = sys.argv[1]
    r.SetFileName( filename )
    if not r.Read():  sys.exit(1)
    numpy_array = gdcm_to_numpy( r.GetImage() )

