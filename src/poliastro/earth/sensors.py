from astropy import units as u

from poliastro.core.sensors import (
    ground_range_diff_at_azimuth as ground_range_diff_at_azimuth_fast,
    min_and_max_ground_range as min_and_max_ground_range_fast,
)


@u.quantity_input(h=u.au, eta_fov=u.rad, eta_center=u.rad, R=u.au)
def min_and_max_ground_range(h, eta_fov, eta_center, R):
    """
    Calculates the minimum and maximum values of ground-range angles.

    Parameters
    ----------
    h: ~astropy.units.Quantity
        Altitude over surface.
    eta_fov: ~astropy.units.Quantity
        Angle of the total area that a sensor can observe.
    eta_center: ~astropy.units.Quantity
        Center boresight angle.
    R: ~astropy.units.Quantity
        Attractor equatorial radius.

    Returns
    -------
    lambda_min: ~astropy.units.Quantity
        Minimum value of latitude and longitude.
    lambda_max: ~astropy.units.Quantity
        Maximum value of latitude and longitude.

    """
    h = h.to(u.au).value
    eta_fov = eta_fov.to(u.rad).value
    eta_center = eta_center.to(u.rad).value
    R = R.to(u.au).value
    lambda_min, lambda_max = min_and_max_ground_range_fast(h, eta_fov, eta_center, R)

    return lambda_min * u.rad, lambda_max * u.rad


@u.quantity_input(
    h=u.au,
    eta_fov=u.rad,
    eta_center=u.rad,
    beta=u.rad,
    phi_nadir=u.rad,
    lambda_nadir=u.rad,
    R=u.au,
)
def ground_range_diff_at_azimuth(
    h, eta_fov, eta_center, beta, phi_nadir, lambda_nadir, R
):
    """
    Calculates the difference in ground-range angles from the eta_center angle and the latitude and longitude of the target
    for a desired phase angle, beta, used to specify where the sensor is looking.

    Parameters
    ----------
    h: ~astropy.units.Quantity
        Altitude over surface.
    eta_fov: ~astropy.units.Quantity
        Angle of the total area that a sensor can observe.
    eta_center: ~astropy.units.Quantity
        Center boresight angle.
    beta: ~astropy.units.Quantity
        Azimuth angle, used to specify where the sensor is looking.
    phi_nadir: ~astropy.units.Quantity
        Latitude angle of nadir point.
    lambda_nadir: ~astropy.units.Quantity
        Longitude angle of nadir point.
    R: ~astropy.units.Quantity
        Earth equatorial radius.

    Returns
    -------
    delta_lambda : ~astropy.units.Quantity
        The difference in ground-range angles from the eta_center angle.
    phi_tgt: ~astropy.units.Quantity
        Latitude angle of the target point.
    lambda_tgt: ~astropy.units.Quantity
        Longitude angle of the target point.

    Raises
    ------
    ValueError
        This formula always gives the answer for the short way to the target ot the acute angle, β,
        which must be greater than 0º and less than 180º.

    """
    h = h.to(u.au).value
    eta_fov = eta_fov.to(u.rad).value
    eta_center = eta_center.to(u.rad).value
    beta = beta.to(u.rad).value
    phi_nadir = phi_nadir.to(u.rad).value
    lambda_nadir = lambda_nadir.to(u.rad).value
    R = R.to(u.au).value

    (delta_lambda, phi_tgt, lambda_tgt,) = ground_range_diff_at_azimuth_fast(
        h, eta_fov, eta_center, beta, phi_nadir, lambda_nadir, R
    )

    return delta_lambda * u.rad, phi_tgt * u.rad, lambda_tgt * u.rad
