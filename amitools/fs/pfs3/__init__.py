"""Professional File System 3 (PFS3) volumes, as written by pfs3aio."""

import struct

from .Const import DISK_TYPES, is_pfs_dos_type


def is_pfs3_blkdev(blkdev):
    """does the block device hold a PFS3 volume? Looks at its boot block,
    where PFS3 has it: at the start of the partition aligned to its block
    size"""
    from .BlockIO import PFS3BlockIO

    try:
        data = PFS3BlockIO(blkdev).read(0)
    except (IOError, ValueError, AttributeError):
        return False
    if data is None or len(data) < 4:
        return False
    return struct.unpack_from(">I", data, 0)[0] in DISK_TYPES


def open_volume(blkdev):
    """open the volume of a block device: PFS3 or OFS/FFS"""
    if is_pfs3_blkdev(blkdev):
        from .PFS3Volume import PFS3Volume

        vol = PFS3Volume(blkdev)
    else:
        from amitools.fs.ADFSVolume import ADFSVolume

        vol = ADFSVolume(blkdev)
    vol.open()
    return vol


def create_volume(
    blkdev, name, meta_info=None, dos_type=None, boot_code=None, **pfs3_options
):
    """format a block device: with PFS3 if dos_type is one of its types,
    else with OFS/FFS. pfs3_options (fnsize, largefile, numreserved) are
    passed on to PFS3Volume.create()"""
    if dos_type is not None and is_pfs_dos_type(dos_type):
        from .PFS3Volume import PFS3Volume

        vol = PFS3Volume(blkdev)
        vol.create(
            name,
            meta_info=meta_info,
            dos_type=dos_type,
            boot_code=boot_code,
            **pfs3_options,
        )
        return vol
    from amitools.fs.ADFSVolume import ADFSVolume

    vol = ADFSVolume(blkdev)
    vol.create(name, meta_info=meta_info, dos_type=dos_type, boot_code=boot_code)
    return vol
