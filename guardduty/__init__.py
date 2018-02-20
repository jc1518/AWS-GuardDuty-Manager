"""
    AWS GuardDuty Python Client
    Reference: https://boto3.readthedocs.io/en/latest/reference/services/guardduty.html?highlight=guardduty
"""

import boto3
from botocore.exceptions import ClientError
import sys


class Client(object):

    def __init__(self, profile, region):
        """Authentication"""
        self.profile = profile
        self.region = region
        session = boto3.Session(profile_name=self.profile, region_name=self.region)
        self.client = session.client('guardduty')

    """
        Detectors managements
    """
    def list_detector(self):
        """Find detector ID, Max one"""
        try:
            response = self.client.list_detectors()
            print('detector id', response['DetectorIds'])
            return response['DetectorIds'][0] if len(response['DetectorIds']) == 1 else False
        except ClientError as e:
            print(e.response['Error']['Code'])
            sys.exit()

    def create_detector(self, status='enable'):
        """Create detector (enable/disable means resume/suspend GuardDuty)"""
        if not self.list_detector():
            try:
                response = self.client.create_detector(Enable=True) \
                           if status == 'enable' \
                           else self.client.create_detector(Enable=False)
                print(response['DetectorId'], 'has been created.')
                return response['DetectorId']
            except ClientError as e:
                print(e.response['Error']['Code'])
                return False
        else:
            print('detector already exists.')
            return False

    def get_detector(self):
        """Get detector status"""
        detector_id = self.list_detector()
        if detector_id:
            try:
                response = self.client.get_detector(DetectorId=detector_id)
                print('The status is', response['Status'])
                return response['Status']
            except ClientError as e:
                print(e.response['Error']['Code'])
                return False
        else:
            print('no detector has been found.')
            return False

    def enable_detector(self):
        """Enable detector (resume GuardDuty)"""
        detector_id = self.list_detector()
        if detector_id:
            try:
                response = self.client.update_detector(DetectorId=detector_id, Enable=True)
                print(detector_id, 'has been enabled')
                return True
            except ClientError as e:
                print(e.response['Error']['Code'])
                return False
        else:
            print('no detector has been found.')
            return False

    def disable_detector(self):
        """Disable detector (suspend GuardDuty)"""
        detector_id = self.list_detector()
        if detector_id:
            try:
                response = self.client.update_detector(DetectorId=detector_id, Enable=False)
                print(detector_id, 'has been disabled')
                return True
            except ClientError as e:
                print(e.response['Error']['Code'])
                return False
        else:
            print('no detector has been found.')
            return False

    def delete_detector(self):
        """Delete detector (disable GuardDuty)"""
        detector_id = self.list_detector()
        if detector_id:
            try:
                response = self.client.delete_detector(DetectorId=detector_id)
                print(detector_id, 'has been deleted')
                return True
            except ClientError as e:
                print(e.response['Error']['Code'])
                return False
        else:
            print('no detector has been found.')
            return False

    """
        Membership managements
    """
    def create_members(self, accounts_info):
        """Add members in master account"""
        detector_id = self.list_detector()
        if detector_id:
            try:
                response = self.client.create_members(
                    AccountDetails=accounts_info,
                    DetectorId=detector_id
                )
                for result in response['UnprocessedAccounts']:
                    print(result)
                return True
            except ClientError as e:
                print(e.response['Error']['Code'])
                return False

    def list_members(self):
        """Check associated members in master account"""
        detector_id = self.list_detector()
        if detector_id:
            try:
                response = self.client.list_members(
                    DetectorId=detector_id,
                    OnlyAssociated='FALSE'
                )
                return response['Members']
            except ClientError as e:
                print(e.response['Error']['Code'])
                return False

    def get_members(self, accounts_ids):
        """Check members info in master account"""
        detector_id = self.list_detector()
        if detector_id:
            try:
                response = self.client.get_members(
                    AccountIds=accounts_ids,
                    DetectorId=detector_id
                )
                return response['Members']
            except ClientError as e:
                print(e.response['Error']['Code'])
                return False

    def invite_members(self, accounts_ids):
        """Invite members in master account"""
        detector_id = self.list_detector()
        if detector_id:
            try:
                response = self.client.invite_members(
                    AccountIds=accounts_ids,
                    DetectorId=detector_id,
                    Message='This is for GuardDuty POC'
                )
                for result in response['UnprocessedAccounts']:
                    print(result)
                return True
            except ClientError as e:
                print(e.response['Error']['Code'])
                return False

    def disassociate_members(self, accounts_ids):
        """Disassociate members in master account"""
        detector_id = self.list_detector()
        if detector_id:
            try:
                response = self.client.disassociate_members(
                    AccountIds=accounts_ids,
                    DetectorId=detector_id
                )
                for result in response['UnprocessedAccounts']:
                    print(result)
                return True
            except ClientError as e:
                print(e.response['Error']['Code'])
                return False

    def delete_members(self, accounts_ids):
        """Delete members in master account"""
        detector_id = self.list_detector()
        if detector_id:
            try:
                response = self.client.delete_members(
                    AccountIds=accounts_ids,
                    DetectorId=detector_id
                )
                for result in response['UnprocessedAccounts']:
                    print(result)
                return True
            except ClientError as e:
                print(e.response['Error']['Code'])
                return False

    def list_invitation(self, master_id):
        """List pending invitations in member account"""
        try:
            response = self.client.list_invitations()
            for invitation in response['Invitations']:
                print(invitation['RelationshipStatus'])
                if invitation['AccountId'] == master_id and invitation['RelationshipStatus'] == 'Invited':
                    return invitation['InvitationId']
            return False
        except ClientError as e:
            print(e.response['Error']['Code'])
            return False

    def accept_invitation(self, master_id):
        """Accept master invitation in member account"""
        detector_id = self.list_detector()
        invitation_id = self.list_invitation(master_id)
        if detector_id and invitation_id:
            try:
                response = self.client.accept_invitation(
                    DetectorId=detector_id,
                    InvitationId=invitation_id,
                    MasterId=master_id
                )
                return True
            except ClientError as e:
                print(e.response['Error']['Code'])
                return False
        else:
            print('failed to accept invitation from', master_id)
            return False






