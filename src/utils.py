import configparser
import os
from PIL import Image as pil_image
from io import BytesIO
import base64


def read_config(config_path='./config/development.conf'):
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(config_path)

    # convert
    config = config._sections

    # scraping
    config['scraping']['years_range'] = (
        [int(x) for x in config['scraping']['years_range'].split('-')])
    config['scraping']['n_proc'] = int(config['scraping']['n_proc'])

    config['features']['pca_n_components'] = int(config['features']
                                                 ['pca_n_components'])
    return config


def create_folder(folder):
    """ Create folders to retrieve posters and thumbnails
    """
    print(folder)
    if not os.path.exists(folder):
        os.makedirs(folder)


def load_img(base64_img, grayscale=False, target_size=None,
             interpolation='nearest'):
    """Loads an image into PIL format from base64 encoded img
    # Arguments
        path: Path to image file
        grayscale: Boolean, whether to load the image as grayscale.
        target_size: Either `None` (default to original size)
            or tuple of ints `(img_height, img_width)`.
        interpolation: Interpolation method used to resample the image if the
            target size is different from that of the loaded image.
            Supported methods are "nearest", "bilinear", and "bicubic".
            If PIL version 1.1.3 or newer is installed, "lanczos" is also
            supported. If PIL version 3.4.0 or newer is installed, "box" and
            "hamming" are also supported. By default, "nearest" is used.
    # Returns
        A PIL Image instance.
    # Raises
        ImportError: if PIL is not available.
        ValueError: if interpolation method is not supported.
    """
    if pil_image is not None:
        _PIL_INTERPOLATION_METHODS = {
            'nearest': pil_image.NEAREST,
            'bilinear': pil_image.BILINEAR,
            'bicubic': pil_image.BICUBIC,
        }
        # These methods were only introduced in version 3.4.0 (2016).
        if hasattr(pil_image, 'HAMMING'):
            _PIL_INTERPOLATION_METHODS['hamming'] = pil_image.HAMMING
        if hasattr(pil_image, 'BOX'):
            _PIL_INTERPOLATION_METHODS['box'] = pil_image.BOX
        # This method is new in version 1.1.3 (2013).
        if hasattr(pil_image, 'LANCZOS'):
            _PIL_INTERPOLATION_METHODS['lanczos'] = pil_image.LANCZOS

    if pil_image is None:
        raise ImportError('Could not import PIL.Image. '
                          'The use of `array_to_img` requires PIL.')
    img = pil_image.open(BytesIO(base64.b64decode(base64_img)))
    if grayscale:
        if img.mode != 'L':
            img = img.convert('L')
    else:
        if img.mode != 'RGB':
            img = img.convert('RGB')
    if target_size is not None:
        width_height_tuple = (target_size[1], target_size[0])
        if img.size != width_height_tuple:
            if interpolation not in _PIL_INTERPOLATION_METHODS:
                raise ValueError(
                    'Invalid interpolation method {} specified. Supported '
                    'methods are {}'.format(
                        interpolation,
                        ", ".join(_PIL_INTERPOLATION_METHODS.keys())))
            resample = _PIL_INTERPOLATION_METHODS[interpolation]
            img = img.resize(width_height_tuple, resample)
    return img
