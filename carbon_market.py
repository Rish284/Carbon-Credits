CARBON_PRICE = 1200  # INR per ton


def calculate_carbon_value(land_acres, irrigation, organic, soil_health):
    carbon_per_acre = (
        0.5 +
        (soil_health - 50) * 0.02 +
        (0.5 if organic == "Yes" else 0) +
        (0.2 if irrigation == "Yes" else 0)
    )

    total_carbon = carbon_per_acre * land_acres
    total_value = total_carbon * CARBON_PRICE

    return round(total_carbon, 2), round(total_value, 2)
