#!/usr/bin/env python3
"""Class interacts with CISCO-VTP-MIB."""

import sys
import binascii
from collections import defaultdict

# Import project libraries
from snmp import snmp_manager


class Query(object):

    """Class interacts with CISCO-VTP-MIB.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, snmp_params):
        """Function for intializing the class.

        Args:
            snmp_params: SNMP parameters for querying the host

        Returns:
            None

        """
        # Define query object
        self.snmp_query = snmp_manager.Interact(snmp_params)

    def supported(self):
        """Return device's support for the MIB.

        Args:
            None

        Returns:
            validity: True if supported

        """
        # Support OID
        validity = False

        # Get one OID entry in MIB
        oid = '.1.3.6.1.4.1.9.9.46.1.3.1.1.2'

        # Return nothing if oid doesn't exist
        if self.snmp_query.oid_exists(oid) is True:
            validity = True

        # Return
        return validity

    def layer2(self):
        """Get layer 2 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface vtpVlanName data
        values = self.vtpvlanname()
        for key, value in values.items():
            final[key]['vtpVlanName'] = value

        # Get interface vtpVlanType data
        values = self.vtpvlantype()
        for key, value in values.items():
            final[key]['vtpVlanType'] = value

        # Get interface vtpVlanState data
        values = self.vtpvlanstate()
        for key, value in values.items():
            final[key]['vtpVlanState'] = value

        # Return
        return final

    def layer1(self):
        """Get layer 1 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Get interface vlanTrunkPortDynamicState data
        values = self.vlantrunkportdynamicstate()
        for key, value in values.items():
            final[key]['vlanTrunkPortDynamicState'] = value

        # Get interface vlanTrunkPortDynamicStatus data
        values = self.vlantrunkportdynamicstatus()
        for key, value in values.items():
            final[key]['vlanTrunkPortDynamicStatus'] = value

        # Get interface vlanTrunkPortDynamicStatus data
        values = self.vlantrunkportnativevlan()
        for key, value in values.items():
            final[key]['vlanTrunkPortNativeVlan'] = value

        # Return
        return final

    def vlantrunkportnativevlan(self):
        """Return dict of CISCO-VTP-MIB vlanTrunkPortNativeVlan per ifIndex.

        Args:
            None

        Returns:
            data_dict: Dict of vlanTrunkPortNativeVlan
                using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.46.1.6.1.1.5'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def vlantrunkportdynamicstatus(self):
        """Return dict of CISCO-VTP-MIB vlanTrunkPortDynamicStatus per ifIndex.

        Args:
            None

        Returns:
            data_dict: Dict of vlanTrunkPortDynamicStatus
                using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.46.1.6.1.1.14'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def vlantrunkportdynamicstate(self):
        """Return dict of CISCO-VTP-MIB vlanTrunkPortDynamicState per ifIndex.

        Args:
            None

        Returns:
            data_dict: Dict of vlanTrunkPortDynamicState
                using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.46.1.6.1.1.13'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def vtpvlanname(self):
        """Return dict of CISCO-VTP-MIB vtpVlanName for each VLAN.

        Args:
            None

        Returns:
            data_dict: Dict of vtpVlanName using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.46.1.3.1.1.4'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = str(bytes(value), encoding='utf-8')

        # Return the interface descriptions
        return data_dict

    def vtpvlantype(self):
        """Return dict of CISCO-VTP-MIB vtpVlanType for each VLAN.

        Args:
            None

        Returns:
            data_dict: Dict of vtpVlanType using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.46.1.3.1.1.3'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def vtpvlanstate(self):
        """Return dict of CISCO-VTP-MIB vtpVlanState for each VLAN.

        Args:
            None

        Returns:
            data_dict: Dict of vtpVlanState using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = '.1.3.6.1.4.1.9.9.46.1.3.1.1.2'
        results = self.snmp_query.walk(oid, normalized=True)
        for key, value in sorted(results.items()):
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict
