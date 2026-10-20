"""Config flow for TickTick Integration."""

from collections.abc import Mapping
import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    SOURCE_REAUTH,
    ConfigEntry,
    ConfigFlowResult,
    OptionsFlowWithReload,
)
from homeassistant.core import callback
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig

from .const import CONF_ASSIGNEE_NAMES, DOMAIN


class OAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """Config flow to handle TickTick Integration OAuth2 authentication."""

    DOMAIN = DOMAIN

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return logging.getLogger(__name__)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> "TickTickOptionsFlow":
        """Return the options flow."""
        return TickTickOptionsFlow()

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Start a new sign-in when the access token has expired."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Ask the user to sign in to TickTick again."""
        if user_input is None:
            return self.async_show_form(step_id="reauth_confirm")
        return await self.async_step_user()

    async def async_oauth_create_entry(self, data: dict) -> ConfigFlowResult:
        """Create the entry, or update the existing one after a re-auth."""
        if self.source == SOURCE_REAUTH:
            return self.async_update_reload_and_abort(
                self._get_reauth_entry(), data=data
            )
        return await super().async_oauth_create_entry(data)


def _parse_assignee_names(text: str) -> dict[str, str]:
    """Parse lines of `user@example.com = Name`."""
    names = {}
    for line in text.splitlines():
        username, sep, name = line.partition("=")
        if sep and username.strip() and name.strip():
            names[username.strip()] = name.strip()
    return names


class TickTickOptionsFlow(OptionsFlowWithReload):
    """Options for the TickTick integration."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Edit how assignees are named."""
        if user_input is not None:
            return self.async_create_entry(
                data={
                    CONF_ASSIGNEE_NAMES: _parse_assignee_names(
                        user_input.get(CONF_ASSIGNEE_NAMES, "")
                    )
                }
            )
        current = self.config_entry.options.get(CONF_ASSIGNEE_NAMES, {})
        text = "\n".join(f"{username} = {name}" for username, name in current.items())
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_ASSIGNEE_NAMES, default=text): TextSelector(
                        TextSelectorConfig(multiline=True)
                    )
                }
            ),
        )
