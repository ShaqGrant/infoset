#!/usr/bin/env python3
"""Module for ETHERLIKE-MIB."""


from collections import defaultdict


class Query(object):
    """Class interacts with ETHERLIKE-MIB.

    Args:
        None

    Returns:
        None

    Key Methods:

        supported: Queries the device to determine whether the MIB is
            supported using a known OID defined in the MIB. Returns True
            if the device returns a response to the OID, False if not.

        layer1: Returns all needed layer 1 MIB information from the device.
            Keyed by OID's MIB name (primary key), ifIndex (secondary key)

    """

    def __init__(self, snmp_object):
        """Function for intializing the class.

        Args:
            snmp_object: SNMP Interact class object from snmp_manager.py

        Returns:
            None

        """
        # Define query object
        self.snmp_object = snmp_object

    def supported(self):
        """Return device's support for the MIB.

        Args:
            None

        Returns:
            validity: True if supported

        """
        # Support OID
        validity = False

        # Get one OID entry in MIB (dot3StatsDuplexStatus)
        oid = '.1.3.6.1.2.1.10.7.2.1.19'

        # Return nothing if oid doesn't exist
        if self.snmp_object.oid_exists(oid) is True:
            validity = True

        # Return
        return validity

    def layer1(self):
        """Get layer 1 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface dot3StatsDuplexStatus data
        values = self.dot3statsduplexstatus()
        for key, value in values.items():
            final[key]['dot3StatsDuplexStatus'] = value

        # Return
        return final

    def dot3statsduplexstatus(self):
        """Return dict of ETHERLIKE-MIB dot3StatsDuplexStatus for each port.

        Args:
            None

        Returns:
            data_dict: Dict of dot3StatsDuplexStatus using ifIndex as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.2.1.10.7.2.1.19'
        results = self.snmp_object.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict
