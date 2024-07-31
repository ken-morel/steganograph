from PIL import Image
from pyoload import *


ENDTOKEN = b"<endtoken-staganograph>"


@annotate
def destruct(data: bytes | int):
    if isinstance(data, int):
        data = data.to_bytes()
    return ''.join([format(i, "08b") for i in data])


@annotate
def construct(data: str):
    return int(data, 2)


@annotate
def steganograph(file, inimage, outimage, endtoken=ENDTOKEN, channels=(1,)):
    with open(file, "rb") as f:
        file_data = f.read()

    image = Image.open(inimage).convert("RGBA")
    indata = image.tobytes()
    if (len(indata) // 8 * len(channels)) < len(file_data):
        raise ValueError(
            f"input image too small, has "
            f"{(len(indata) // 8 * len(channels))}b needed {len(file_data)}b"
        )

    outdata = insert_bytes_in_bytes(indata, file_data, endtoken)

    Image.frombytes("RGBA", image.size, outdata).save(outimage)


@annotate
def insert_bytes_in_bytes(base_data, data, endtoken, channels, skip=True):
    bits = destruct(data + endtoken)
    base = bytearray(base_data)
    read_idx = 0
    # data_size = len(data)

    for channel in channels:
        write_idx = 0
        while write_idx < len(base_data):
            if skip and (write_idx + 1) % 4 == 0:
                write_idx += 1
                continue
            if read_idx < len(bits):
                out = destruct(base[write_idx])
                out = out[:channel] + bits[read_idx] + out[channel + 1:]
                base[write_idx] = construct(out)
            write_idx += 1
            read_idx += 1
    return bytes(base)


@annotate
def unsteganograph(inimage, file, endtoken=ENDTOKEN):
    image = Image.open(inimage).convert("RGBA")
    indata = image.tobytes()

    outdata = extract_bytes_from_bytes(indata, endtoken)

    with open(file, "wb") as f:
        f.write(outdata)


@annotate
def extract_bytes_from_bytes(indata, endtoken, channels, skip=True):
    data = bytearray()
    cache = ""
    for channel in channels:
        for idx, byte in enumerate(indata):
            if skip and (idx + 1) % 4 == 0:
                continue
            cache += destruct(byte)[channel]
            if len(cache) == 8:
                data.append(construct(cache))
                cache = ""
                if data.endswith(endtoken):
                    return data[:-len(endtoken)]
    raise ValueError("end token not found")
