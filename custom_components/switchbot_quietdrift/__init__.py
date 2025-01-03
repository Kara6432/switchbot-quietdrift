"""QuietDrift support for SwitchBot Curtain devices by v6ak and Kara6432"""

import logging
from typing import Any

import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_ENTITY_ID
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import entity_registry

from .const import CONF_SPEED, CONF_POSITION, DOMAIN, SET_COVER_POSITION_SCHEMA

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    async def handle_set_cover_position(service_call: ServiceCall):
        data = service_call.data

        speed = data[CONF_SPEED]
        position = data[CONF_POSITION]

        entity_ids = data[CONF_ENTITY_ID]
        ent_reg = entity_registry.async_get(hass)
        registry_entities = list(map(ent_reg.async_get, entity_ids))
        entities = list(map(lambda re: hass.data['cover'].get_entity(re.entity_id), registry_entities))

        for entity in entities:
            # We rely on implementation details (._device etc.), which isn't nice, but I think it is good enough there.

            # set position
            res = await entity._device.set_position(position=position, speed=speed)
            (_LOGGER.info if res else _LOGGER.warning())('set position (%s, %d, %d) result: %s', entity.entity_id,
                                                         position, speed, res)

            # store result
            entity._last_run_success = bool(res)

            # refresh state
            entity._attr_is_opening = entity._device.is_opening()
            entity._attr_is_closing = entity._device.is_closing()
            entity.async_write_ha_state()

    hass.services.async_register(
        domain='switchbot_quietdrift',
        service='set_curtain_position',
        service_func=handle_set_cover_position,
        schema=SET_COVER_POSITION_SCHEMA,
    )

    return True
