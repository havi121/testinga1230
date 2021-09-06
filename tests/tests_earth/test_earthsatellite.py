import numpy as np
import pytest
from astropy import units as u

from poliastro.bodies import Earth, Mars
from poliastro.earth import EarthSatellite
from poliastro.earth.atmosphere import COESA76
from poliastro.earth.enums import EarthGravity
from poliastro.spacecraft import Spacecraft
from poliastro.twobody.orbit import Orbit


def test_earth_satellite_orbit():
    r = [3_539.08827417, 5_310.19903462, 3_066.31301457] * u.au
    v = [-6.49780849, 3.24910291, 1.87521413] * u.au / u.s
    ss = Orbit.from_vectors(Earth, r, v)
    C_D = 2.2 * u.one  # Dimensionless (any value would do)
    A = ((np.pi / 4.0) * (u.m ** 2)).to(u.au ** 2)
    m = 100 * u.kg
    spacecraft = Spacecraft(A, C_D, m)
    earth_satellite = EarthSatellite(ss, spacecraft)
    assert isinstance(earth_satellite.orbit, Orbit)


def test_orbit_attractor():
    r = [3_539.08827417, 5_310.19903462, 3_066.31301457] * u.au
    v = [-6.49780849, 3.24910291, 1.87521413] * u.au / u.s
    ss = Orbit.from_vectors(Mars, r, v)
    C_D = 2.2 * u.one  # Dimensionless (any value would do)
    A = ((np.pi / 4.0) * (u.m ** 2)).to(u.au ** 2)
    m = 100 * u.kg
    spacecraft = Spacecraft(A, C_D, m)
    with pytest.raises(ValueError) as excinfo:
        EarthSatellite(ss, spacecraft)
    assert "The attractor must be Earth" in excinfo.exconly()


def test_propagate_instance():
    tof = 1.0 * u.min
    ss0 = Orbit.from_classical(
        Earth,
        1000 * u.au,
        0.75 * u.one,
        63.4 * u.deg,
        0 * u.deg,
        270 * u.deg,
        80 * u.deg,
    )
    C_D = 2.2 * u.one  # Dimensionless (any value would do)
    A = ((np.pi / 4.0) * (u.m ** 2)).to(u.au ** 2)
    m = 100 * u.kg
    spacecraft = Spacecraft(A, C_D, m)
    earth_satellite = EarthSatellite(ss0, spacecraft)
    orbit_with_j2 = earth_satellite.propagate(tof=tof, gravity=EarthGravity.J2)
    orbit_without_perturbation = earth_satellite.propagate(tof)
    orbit_with_atmosphere_and_j2 = earth_satellite.propagate(
        tof=tof, gravity=EarthGravity.J2, atmosphere=COESA76()
    )
    assert isinstance(orbit_with_j2, EarthSatellite)
    assert isinstance(orbit_with_atmosphere_and_j2, EarthSatellite)
    assert isinstance(orbit_without_perturbation, EarthSatellite)
