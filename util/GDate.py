from datetime import datetime, timedelta

dateFormat = "%d/%m/%Y %H:%M:%S"


class GDate:
    @staticmethod
    def getTimeWithFormat():
        return datetime.now().strftime(dateFormat)

    @staticmethod
    def getTimeDifference(generation_time):
        return int((datetime.strptime(GDate.getTimeWithFormat(), dateFormat) - datetime.strptime(
            (generation_time + timedelta(hours=3)).strftime(dateFormat), dateFormat)).total_seconds() / 60)
