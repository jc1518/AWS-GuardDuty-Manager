#!/usr/bin/env python3
"""
    AWS GuardDuty Manager Configuration File
    id: AWS account number
    profile: AWS credential profile
    email: The GuardDuty invitation will be sent to the Email address (no need to click to approve)
    desiredStatus: GuardDuty desired status [start|stop]
        start: Enable GuardDuty, join master, and sends findings to master account.
        stop: Suspend GuardDuty and retain membership, so there will be no more new findings.
              The existing finding will be still available. Change to 'start' to resume.
        disable: Disable GuardDuty, all existing findings will be lost
"""

regions = {
    "us-west-2": {
        "master": {
            "id": "XXXXXXXXXXXXX",
            "profile": "account-A"
        },
        "members": [
            {
                "id": "XXXXXXXXXXXX",
                "profile": "account-B",
                "email": "account-B-owner@mydomain.com",
                "desiredStatus": "start"
            },
            {
                "id": "XXXXXXXXXXXX",
                "profile": "account-C",
                "email": "account-C-owner@mydomain.com",
                "desiredStatus": "start"
            }
        ]
    }
}