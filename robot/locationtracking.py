from math import sqrt


class LocationTracker:
    def __init__(self, imageSizeX, imageSizeY):
        self.dimensions = (imageSizeX, imageSizeY)

    def fractionalLocation(self, location):
        sx, sy = self.dimensions
        cx, cy = location
        return (cx / sx, cy / sy)

    def getCenter(self, box):
        boxCenterY = (box[1] + box[3]) // 2
        boxCenterX = (box[0] + box[2]) // 2
        return (boxCenterX, boxCenterY)

    def track(self, ballLocations, robotLocation):
        # Takes a list of xyxy ball locations (with the current and previous at the head of the list) and the xyxy robot location
        c_bal = self.getCenter(ballLocations[0])
        p_bal = self.getCenter(ballLocations[1])

        cbx, cby = c_bal
        pbx, pby = p_bal
        dist = sqrt((cbx - pbx) ** 2 + (cby - pby) ** 2)
        crx, cry = self.getCenter(robotLocation[0])

        if cbx - pbx == 0 or cby - pby == 0 or dist < 10:
            return (
                -(crx - cbx),
                (int(cbx), int(cry)),
                (int(cbx), int(cby)),
                (int(crx), int(cry)),
            )

        m = (c_bal[1] - p_bal[1]) / (c_bal[0] - p_bal[0])

        b = c_bal[1] - (c_bal[0] * m)

        xTarget = (cry - b) / m

        return (
            -(crx - xTarget),
            (int(xTarget), int(cry)),
            (int(cbx), int(cby)),
            (crx, cry),
        )  # Returns a fractional distance for the robot to travel
