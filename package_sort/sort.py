STANDARD = "STANDARD"
SPECIAL = "SPECIAL"
REJECTED = "REJECTED"

def sort(width: int, height: int, length: int, mass: int) -> str:

    if width < 1 or height < 1 or length < 1 or mass < 1:
        raise Exception("invalid input")

    bulkThresh = 10**6
    dimThresh = 150
    weightThresh = 20

    heavy = weightThresh <= mass
    volume = width * height * length

    bulky = bulkThresh <= volume or dimThresh <= width or dimThresh <= height or dimThresh <= length

    if bulky and heavy:
        return REJECTED
    
    if bulky or heavy:
        return SPECIAL

    return STANDARD
