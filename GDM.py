#!/usr/bin/env python3
"""
    AWS GuardDuty Manager
    Author: Jackie Chen (support@jackiechen.org)
    Version: 20/02/2018
    Reference: https://docs.aws.amazon.com/guardduty/latest/ug/guardduty-ug.pdf
"""

import config
import guardduty
import sys


def enable_guardduty(profile, region):
    print('Enabling GuardDuty of AWS account', profile)
    gd_client = guardduty.Client(profile, region)
    gd_client.create_detector()


def disable_guardduty(profile, region):
    print('Disabling GuardDuty of AWS account', profile)
    gd_client = guardduty.Client(profile, region)
    gd_client.delete_detector()


def check_guardduty(profile, region):
    print('Checking GuardDuty of AWS account', profile)
    gd_client = guardduty.Client(profile, region)
    gd_client.get_detector()


def suspend_guardduty(profile, region):
    print('Suspend GuardDuty of AWS account', profile)
    gd_client = guardduty.Client(profile, region)
    gd_client.disable_detector()


def resume_guardduty(profile, region):
    print('Resume GuardDuty of AWS account', profile)
    gd_client = guardduty.Client(profile, region)
    gd_client.enable_detector()


def master_create_members(profile, region, members):
    print('Creating members in GuardDuty of AWS account', profile, ':', str(members))
    gd_client = guardduty.Client(profile, region)
    gd_client.create_members(members)


def master_invite_members(profile, region, members):
    print('Inviting members to join GuardDuty of AWS account', profile, ':', str(members))
    gd_client = guardduty.Client(profile, region)
    gd_client.invite_members(members)


def master_list_members(profile, region):
    print('Checking existing members of GuardDuty in AWS account', profile)
    gd_client = guardduty.Client(profile, region)
    return gd_client.list_members()


def master_dissociate_members(profile, region, members):
    print('Dissociate members from GuardDuty of AWS account', profile)
    gd_client = guardduty.Client(profile, region)
    gd_client.disassociate_members(members)


def master_delete_members(profile, region, members):
    print('Deleting members from GuardDuty of AWS account', profile)
    gd_client = guardduty.Client(profile, region)
    gd_client.delete_members(members)


def member_accept_invitation(profile, region, master_id, master_profile):
    print('Accepting invitation of GuardDuty from AWS account', master_profile, 'in account', profile)
    gd_client = guardduty.Client(profile, region)
    gd_client.accept_invitation(master_id)


def read_region_config(region):
    print("Reading config file...")
    # Enable GuardDuty for all accounts
    enable_guardduty(config.regions[region]['master']['profile'], region)
    members = []
    members_info = []
    for member in config.regions[region]['members']:
        enable_guardduty(member['profile'], region)
        members.append(member['id'])
        members_info.append(
            {
                'AccountId': member['id'],
                'Email': member['email']
            }
        )
    # Create members in master account
    master_create_members(config.regions[region]['master']['profile'], region, members_info)
    # Invite members to join master account
    master_invite_members(config.regions[region]['master']['profile'], region, members)
    # Accept invitation from master
    for member in config.regions[region]['members']:
        member_accept_invitation(member['profile'], region,config.regions[region]['master']['id'],
                                 config.regions[region]['master']['profile'])
        if member['desiredStatus'] == 'start':
            resume_guardduty(member['profile'], region)
        elif member['desiredStatus'] == 'stop':
            suspend_guardduty(member['profile'], region)
        elif member['desiredStatus'] == 'disable':
            disable_guardduty(member['profile'], region)
        else:
            print(member['desiredStatus'])
            print("Invalid desired status!")
            sys.exit()


if __name__ == '__main__':
    for region in config.regions.keys():
        print('Working on GuardDuty in region', region)
        read_region_config(region)







