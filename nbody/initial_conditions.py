"""Saved systems and Bodies with initial conditions for testing."""

import numpy as np
from .n_body import Body, System

# earth and sun
earth = Body(m=1, r_0=(1, 0), v_0=(0, np.sqrt(333000)), name="earth")
sun = Body(m=333000, r_0=(0, 0), v_0=(0, 0), name="sun")
earth_sun_system = System(earth, sun)

# yin_yang_1a - beautiful non-chaotic 3 body system
# http://three-body.ipb.ac.rs/sol.php?id=1
v1 = 0.513938
v2 = 0.304736
yin_yang_1a = System(
    Body(m=1, r_0=(-1, 0), v_0=(v1 * 1.1, v2), name="b1"),
    Body(m=1, r_0=(1, 0), v_0=(v1, v2), name="b2"),
    Body(m=1, r_0=(0, 0), v_0=(-2 * v1, -2 * v2), name="b3"),
    name="Yin-Yang-1a",
)
