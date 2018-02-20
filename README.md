# AWS GuardDuty Manager

## Description
AWS GuardDuty Manager (GDM) is a tool that allows you to perform some common GuardDuty tasks (start, stop and disable) across multiple AWS accounts.

## Usage
1. Set up the config.py file
- id: AWS account number.
- profile: AWS credential profile name that is defined in ~/.aws/credentials.
- email: The member account contact Email address.
- desiredStatus: GuardDuty desired status [start|stop|disable].
	- start: Enable GuardDuty, join master, and sends findings to master account.
  - stop: Suspend GuardDuty but retain membership, so there will be no more new findings. The existing finding will be still available. Change to 'start' to resume.
  - disable: Disable GuardDuty, all existing findings will be lost.

Here is a sample config:
```bash
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
    },
    "us-east-1": {
        "master": {
            "id": "XXXXXXXXXXXXX",
            "profile": "account-A"
        },
        "members": [
            {
                "id": "XXXXXXXXXXXX",
                "profile": "account-B",
                "email": "account-B-owner@mydomain.com",
                "desiredStatus": "stop"
            },
            {
                "id": "XXXXXXXXXXXX",
                "profile": "account-C",
                "email": "account-C-owner@mydomain.com",
                "desiredStatus": "disable"
            }
        ]
    }
}
```
2. Run 
```bash
python GDM.py
```