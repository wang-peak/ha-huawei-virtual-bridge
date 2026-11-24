"""Apply a saved mapping by reloading the gateway config entry."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ReloadError(RuntimeError):
    """Reloading the gateway after a mapping change failed."""


async def async_apply_mapping(
    hass: HomeAssistant, entry_id: str, serial: str
) -> str:
    """Reload the gateway entry so the new mapping takes effect.

    Returns ``"callback"`` when the entry's reload callback was used, or
    ``"entry"`` when the config entry itself had to be reloaded.
    """

    callbacks = hass.data.get(DOMAIN, {}).get("reload_callbacks", {})
    callback = callbacks.get(entry_id)
    if callback is not None:
        try:
            await callback()
        except HomeAssistantError as error:
            _LOGGER.warning(
                "Reload callback failed for gateway %s, falling back to entry reload: %s",
                serial,
                error,
            )
        else:
            return "callback"

    entry = hass.config_entries.async_get_entry(entry_id)
    if entry is None:
        raise ReloadError("找不到对应的网关配置，请重新打开配置")
    if not await hass.config_entries.async_reload(entry_id):
        raise ReloadError(
            "重新加载网关配置失败，请到「设置 -> 设备与服务」手动重载"
        )
    return "entry"
