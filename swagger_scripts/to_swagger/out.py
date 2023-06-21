schema = {
    "type": "object",
    "required": [
        "msg",
        "code",
        "data",
        "location"
    ],
    "properties": {
        "msg": {
            "type": "string",
            "example": "success"
        },
        "code": {
            "type": "integer",
            "example": 0
        },
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "detect_type",
                    "name",
                    "template_type",
                    "logo",
                    "desc",
                    "id",
                    "permissions"
                ],
                "properties": {
                    "detect_type": {
                        "type": "string"
                    },
                    "name": {
                        "type": "string"
                    },
                    "template_type": {
                        "type": "string"
                    },
                    "logo": {
                        "type": "string"
                    },
                    "desc": {
                        "type": "string"
                    },
                    "id": {
                        "type": "integer"
                    },
                    "permissions": {
                        "type": "boolean"
                    }
                }
            },
            "example": [
                {
                    "detect_type": "host_web",
                    "name": "Attack Surface Identification",
                    "template_type": "system",
                    "logo": "data:image/png;base64,iVBORw0KGg...",
                    "desc": "This test launches asset profili...",
                    "id": 6,
                    "permissions": False
                },
                {
                    "detect_type": "web",
                    "name": "Website Penetration",
                    "template_type": "system",
                    "logo": "data:image/png;base64,iVBORw0KGg...",
                    "desc": "This test launches cyber attacks...",
                    "id": 2,
                    "permissions": False
                },
                {
                    "detect_type": "host_web",
                    "name": "Intranet Penetration (IP + Defau...",
                    "template_type": "system",
                    "logo": "data:image/png;base64,iVBORw0KGg...",
                    "desc": "This scenario uses port scanning...",
                    "id": 1,
                    "permissions": False
                }
            ]
        },
        "location": {
            "type": "integer",
            "example": 6
        }
    }
}
