#!/usr/bin/env python3
"""Calico utility script.

Calico utility script

"""

import os
import sys
import yaml
import tempfile

# Import project libraries. Use jm_dummy to test if we have a good path.
# Doing the test for all libraries could cause you to get a $PYTHONPATH
# error, when it could be a syntax error in one of the libraries.
try:
    import jm_dummy
except:
    print('Error: Please set your $PYTHONPATH variable')
    sys.exit(2)
import jm_cli
import jm_configuration
import jm_general
from snmp import snmp_manager
from snmp import snmp_info


def main():
    """Main Function.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    additional_help = """\
Utility script for the project.

"""

    # Process the CLI
    cli_object = jm_cli.Process(additional_help=additional_help)
    cli_args = cli_object.args()

    # Process the config
    config = jm_configuration.Read(cli_args.directory)

    # Show configuration data
    if cli_args.mode == 'config':
        do_config(cli_args, config)

    # Show interesting information
    if cli_args.mode == 'test':
        do_test(cli_args, config)

    # Process hosts
    if cli_args.mode == 'run':
        do_run(cli_args, config)


def do_config(cli_args, config):
    """Process 'config' CLI option.

    Args:
        connectivity_check: Set if testing for connectivity

    Returns:
        None

    """
    # Show hosts if required
    if cli_args.hosts is True:
        print('hosts:')
        print(yaml.dump(config.hosts(), default_flow_style=False))

    # Show hosts if required
    if cli_args.snmp_auth is True:
        print('snmp_auth:')
        print(yaml.dump(config.snmp_auth(), default_flow_style=False))


def do_test(cli_args, config):
    """Process 'test' CLI option.

    Args:
        connectivity_check: Set if testing for connectivity

    Returns:
        None

    """
    # Show host information
    validate = snmp_manager.Validate(cli_args.host, config.snmp_auth())
    snmp_params = validate.credentials()

    if bool(snmp_params) is True:
        print('\nValid credentials found:\n')
        print(yaml.dump(snmp_params, default_flow_style=False))
        print('\n')

        # Get SNMP data
        status = snmp_info.Query(snmp_params)
        data = status.everything()

        # Pring result as YAML
        yaml_string = jm_general.dict2yaml(data)
        print(yaml_string)
    else:
        # Error, host problems
        log_message = (
            'Uncontactable host %s or no valid SNMP '
            'credentials found for it.') % (cli_args.host)
        jm_general.logit(1006, log_message)


def do_run(cli_args, config):
    """Process 'run' CLI option.

    Args:
        connectivity_check: Set if testing for connectivity

    Returns:
        None

    """
    # Create directory if needed
    perm_dir = config.snmp_directory()
    temp_dir = tempfile.mkdtemp()

    # Delete all files in temporary directory
    jm_general.delete_files(temp_dir)

    # Get host data and write to file
    for host in config.hosts():
        # Show host information
        validate = snmp_manager.Validate(host, config.snmp_auth())
        snmp_params = validate.credentials()

        # Verbose output
        if cli_args.verbose is True:
            output = ('Processing on: host %s') % (host)
            print(output)

        # Skip invalid, and uncontactable hosts
        if bool(snmp_params) is False:
            if cli_args.verbose is True:
                output = (
                    'Uncontactable host %s or no valid SNMP '
                    'credentials found for it.') % (cli_args.host)
                print(output)
            continue

        # Process if valid
        if bool(snmp_params) is True:
            # Get data
            status = snmp_info.Query(snmp_params)
            data = status.everything()
            yaml_string = jm_general.dict2yaml(data)

            # Dump data
            temp_file = ('%s/%s.yaml') % (temp_dir, host)
            with open(temp_file, 'w') as file_handle:
                file_handle.write(yaml_string)

            # Verbose output
            if cli_args.verbose is True:
                output = ('Completed run: host %s') % (host)
                print(output)

    # Cleanup, move temporary files to clean permanent directory.
    # Delete temporary directory
    if os.path.isdir(perm_dir):
        jm_general.delete_files(perm_dir)
    else:
        os.makedirs(perm_dir, 0o755)
    jm_general.move_files(temp_dir, perm_dir)
    os.rmdir(temp_dir)


if __name__ == "__main__":
    main()