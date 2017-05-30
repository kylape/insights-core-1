"""
DumpE2FS - Command ``dumpe2fs -h``
==================================

This mapper handles ``dumpe2fs`` output.

The object provides access to this data using a dictionary.  Particular keys
are stored as lists:

* Filesystem features
* Filesystem flags
* Default mount options

Other keys are stored as strings.  The name of the device is stored in the
``dev_name`` property.

Typical contents of the ``/sbin/dumpe2fs -h /dev/device`` command::

    dumpe2fs 1.41.12 (17-May-2010)
    Filesystem volume name:   <none>
    Last mounted on:          /usr
    Filesystem UUID:          1b332c5d-2410-4934-9118-466f8a14841f
    Filesystem magic number:  0xEF53
    Filesystem revision #:    1 (dynamic)
    Filesystem features:      has_journal ext_attr resize_inode dir_index filetype needs_recovery extent flex_bg sparse_super large_file huge_file uninit_bg dir_nlink extra_isize
    Filesystem flags:         signed_directory_hash
    Default mount options:    user_xattr acl

Examples:

    >>> e2fs = shared[DumpE2fs]
    >>> e2fs.dev_name
    '/dev/device'
    >>> e2fs.data['Filesystem volume name']
    '<none>'
    >>> e2fs.data['Last mounted on']
    '/usr'
    >>> e2fs.data['Filesystem UUID']
    '1b332c5d-2410-4934-9118-466f8a14841f'
    >>> e2fs.data['Filesystem magic number']
    '0xEF53'
    >>> e2fs.data['Filesystem revision #']
    '1 (dynamic)'
    >>> e2fs.data['Filesystem features']
    ['has_journal', 'ext_attr', 'resize_inode', 'dir_index', 'filetype',
     'needs_recovery', 'extent', 'flex_bg', 'sparse_super', 'large_file',
     'huge_file', 'uninit_bg', 'dir_nlink', 'extra_isize'],
    >>> e2fs.data['Filesystem flags']
    ['signed_directory_hash']
    >>> e2fs.data['Default mount options']
    ['user_xattr', 'acl']


"""

from .. import mapper, Mapper

COMPOUND_FIELDS = ['Filesystem features', 'Filesystem flags', 'Default mount options']


@mapper('dumpe2fs-h')
class DumpE2fs(Mapper):
    """
    Parse each line in the output of the ``dumpe2fs`` command.
    """
    def parse_content(self, content):
        dumpe2fs_values_dict = {}
        for line in content:
            if ":" in line:
                key, value = line.split(":", 1)
                if key in COMPOUND_FIELDS:
                    dumpe2fs_values_dict[key] = list(value.strip().split())
                else:
                    dumpe2fs_values_dict[key] = value.strip()
        self.dev_name = self.file_name.split('dumpe2fs_-h_')[-1].replace('.', '/')
        self.data = dumpe2fs_values_dict


@mapper('dumpe2fs-h')
def get_dumpe2fs_output(context):
    """
    Deprecated, use DumpE2fs instead.

    Also provides the data in the old device: data dictionary format.
    """
    obj = DumpE2fs(context)
    return {obj.dev_name: obj.data}