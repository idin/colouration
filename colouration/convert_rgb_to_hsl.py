def convert_rgb_to_hsl(red: float, green: float, blue: float, max_value: float = 1.0, min_value: float = 0.0) -> tuple:
    """
    Converts RGB values to HSL.

    Args:
        red: Red component.
        green: Green component.
        blue: Blue component.
        max_value: Maximum value for scaling.
        min_value: Minimum value for scaling.

    Returns:
        tuple: The HSL values (Hue in degrees, Saturation as percentage, Lightness as percentage).
    """
    red = (red - min_value) / max_value
    green = (green - min_value) / max_value
    blue = (blue - min_value) / max_value

    red = min(1.0, max(0.0, red))
    green = min(1.0, max(0.0, green))
    blue = min(1.0, max(0.0, blue))

    maximum = max(red, green, blue)
    minimum = min(red, green, blue)

    chroma = maximum - minimum

    # Compute Hue (H)
    if chroma == 0:
        hue = 0
    else:
        if red == maximum:
            segment = (green - blue) / chroma
            shift = 360 if segment < 0 else 0
            hue = segment * 60 + shift

        elif green == maximum:
            segment = (blue - red) / chroma
            hue = segment * 60 + 120

        else:
            segment = (red - green) / chroma
            hue = segment * 60 + 240

    # Compute Lightness (L)
    lightness = (maximum + minimum) / 2

    # Compute Saturation (S)
    if chroma == 0:
        saturation = 0
    else:
        saturation = chroma / (1 - abs(2 * lightness - 1))

    return hue, saturation, lightness  # Saturation and Lightness as percentages
