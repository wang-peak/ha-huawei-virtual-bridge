"""Constants for the child-device editor."""

from __future__ import annotations

from ..const import DOMAIN, MAX_CHILD_DEVICES_PER_GATEWAY

# mapping.yaml lives next to the integration runtime data.
GATEWAY_ROOT = (".storage", DOMAIN, "gateways")
MAPPING_FILENAME = "mapping.yaml"
MAX_CHILDREN = MAX_CHILD_DEVICES_PER_GATEWAY

# Options-flow menu: the child-device editor plus the LAN interface setting.
MENU_OPTIONS = (
    "interface",
    "add_child",
    "edit_child",
    "delete_child",
    "raw_yaml",
    "settings",
)
