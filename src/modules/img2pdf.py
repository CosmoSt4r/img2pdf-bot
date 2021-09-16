"""Module for converting images to PDF."""

from PIL import Image, UnidentifiedImageError


def checksum(string: str) -> int:
    """
    Get CRC for string.

    Warning: simple algorithm, many collisions.

    Args:
        string: string to calculate checksum

    Returns:
        calculated checksum
        (sum of utf-8 values mod first char's utf-8 value)
    """
    return sum(bytearray(string, 'utf-8')) % ord(string[0])


def convert_names_to_images(filenames: list) -> list:
    """
    Convert filenames to PIL images.

    Args:
        filenames: list of images' file names

    Returns:
        list of PIL images
    """
    images: list = []

    for filename in filenames:
        try:
            images.append(Image.open(filename).convert('RGB'))
        except FileNotFoundError:
            ...
        except UnidentifiedImageError:
            ...

    return images


def generate_pdf(filenames: list, output_name: str = '') -> str:
    """
    Generate PDF file from list of images.

    Args:
        filenames: tuple with images' filenames
        output_name: optional, name of output PDF file

    Returns:
        name of generated PDF file

    Raises:
        ValueError: no images found or they are invalid
    """
    images = convert_names_to_images(filenames)

    if not output_name:
        files_crc = checksum(''.join(filenames))
        output_name = '{name}.pdf'.format(name=str(files_crc))
    if not output_name.endswith('.pdf'):
        output_name = '{name}.pdf'.format(name=output_name)

    if len(images) > 1:
        images[0].save(output_name, save_all=True, append_images=images[1:])
    elif len(images) == 1:
        images[0].save(output_name, save_all=True)
    else:
        raise ValueError('No images found')

    return output_name
