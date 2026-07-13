"""Central logger configuration.

This module sets up a basic logger that can be imported by other
modules. It follows the rules defined in the constitution: a single
module that configures the root logger.
"""

from __future__ import annotations

import logging

def configure_logging(level: int = logging.INFO) -> None:
    """Configure the root logger.

    Parameters
    ----------
    level:
        Logging level to set for the root logger.
    """

    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
