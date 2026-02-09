import math

def calculate_area(shape, **kwargs):
    """
    Calculates the area of different shapes.

    Args:
        shape (str): The name of the shape (e.g., 'rectangle', 'circle', 'triangle').
        **kwargs: The dimensions of the shape.
            For 'rectangle', expects 'length' and 'width'.
            For 'circle', expects 'radius'.
            For 'triangle', expects 'base' and 'height'.

    Returns:
        float: The calculated area of the shape.
        str: An error message if the shape is not supported or dimensions are missing.
    """
    if shape == "rectangle":
        if "length" in kwargs and "width" in kwargs:
            return kwargs["length"] * kwargs["width"]
        else:
            return "Error: Missing length or width for rectangle."
    elif shape == "circle":
        if "radius" in kwargs:
            return math.pi * (kwargs["radius"] ** 2)
        else:
            return "Error: Missing radius for circle."
    elif shape == "triangle":
        if "base" in kwargs and "height" in kwargs:
            return 0.5 * kwargs["base"] * kwargs["height"]
        else:
            return "Error: Missing base or height for triangle."
    else:
        return "Error: Unsupported shape."

# Example Usage:
rectangle_area = calculate_area("rectangle", length=10, width=5)
print(f"The area of the rectangle is: {rectangle_area}")

circle_area = calculate_area("circle", radius=7)
print(f"The area of the circle is: {circle_area}")

triangle_area = calculate_area("triangle", base=8, height=4)
print(f"The area of the triangle is: {triangle_area}")

# Example of an error
square_area = calculate_area("square", side=5)
print(f"The area of the square is: {square_area}")
