# AIOAlfacrm

[![PyPi Package Version](https://img.shields.io/pypi/v/aioalfacrm.svg?style=flat-square)](https://pypi.python.org/pypi/aioalfacrm)
[![Supported python versions](https://img.shields.io/pypi/pyversions/aioalfacrm.svg?style=flat-square)](https://pypi.python.org/pypi/aioalfacrm)
[![MIT License](https://img.shields.io/pypi/l/aioalfacrm.svg?style=flat-blue)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/pypi/dm/aioalfacrm.svg?style=flat-square)](https://pypi.python.org/pypi/aioalfacrm)
[![Tests](https://github.com/stas12312/aioalfacrm/actions/workflows/tests.yml/badge.svg)]( https://github.com/stas12312/aioalfacrm/actions)
**aioalfacrm** - is an asynchronous implementation for the [AlfaCRM API](https://alfacrm.pro/rest-api)

## Package is in development

## Installation using pip
```
$ pip install aioalfacrm
```

*Example:*

```python
import asyncio
from aioalfacrm import AlfaClient

HOSTNAME = 'demo.s20.online'
EMAIL = 'api-email@email.example'
API_KEY = 'user-api-token'
BRANCH_ID = 1


async def main():
    alfa_client = AlfaClient(
        hostname=HOSTNAME,
        email=EMAIL,
        api_key=API_KEY,
        branch_id=BRANCH_ID,
    )
    try:
        # Check auth (Optionaly)
        if not await alfa_client.check_auth():
            print("Authentification error")
            return
        # Get branches
        branches = await alfa_client.branch.list(page=0, count=20)
    finally:
        await alfa_client.close()


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # For Windows
asyncio.run(main())


```

## Available CRM objects

```python
alfa_client.branch  # Branch
alfa_client.customer  # Customer
alfa_client.location  # Location
alfa_client.study_status  # StudyStatus
alfa_client.subject  # Subject
alfa_client.lead_status  # LeadStatus
alfa_client.lead_source  # LeadSource
```

## Available CRM methods

```python
alfa_client.<object>.list(**filters)  # Get objects list
alfa_client.<object>.get(id)  # Get one object by id
alfa_client.<object>.create(fields)  # Create object
alfa_client.<object>.update(id, fields)  # Update object
```

## Paginator
```python
# Get all objects
for page in alfa_client.<object>.get_paginator():
    objects = page.items
```