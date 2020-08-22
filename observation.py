import datetime
from l10n import languages
from pyowm import OWM
from config import OWM_KEY


class ObservationHandler:

    def __init__(self, latitude, longitude, lang):
        owm = OWM(OWM_KEY)
        self.lang = lang
        owm.config['language'] = lang
        manager = owm.weather_manager()
        self.latitude = latitude
        self.longitude = longitude
        observation = manager.weather_at_coords(latitude, longitude)
        self.location = observation.location
        self.weather = observation.weather

    def location_info(self):
        return languages[self.lang]['geolocation'] + self.location.country + " - " + self.location.name

    def weather_image(self):
        return open("icons/" + self.weather.weather_icon_name + ".png", 'rb')

    def weather_status(self):
        temp = self.weather.temperature('celsius')
        return (self.weather.status +
                "\n" +
                languages[self.lang]['temperature'] +
                str(temp['temp']) +
                "\n" +
                languages[self.lang]['feels like'] +
                str(temp['feels_like']))

    def detailed_status(self):
        temp = self.weather.temperature('celsius')
        sun_rise = datetime.datetime.fromtimestamp(self.weather.srise_time)
        sun_set = datetime.datetime.fromtimestamp(self.weather.sset_time)
        return (self.weather.detailed_status +
                "\n\n" +
                languages[self.lang]['temperature'] +
                str(temp['temp']) +
                "\n" +
                languages[self.lang]['min'] +
                str(temp['temp_min']) +
                "\n" +
                languages[self.lang]['max'] +
                str(temp['temp_max']) +
                "\n" +
                languages[self.lang]['feels like'] +
                str(temp['feels_like']) +
                "\n\n" +
                languages[self.lang]['humidity'] +
                str(self.weather.humidity) +
                "\n\n" +
                languages[self.lang]['wind speed'] +
                str(self.weather.wind()['speed']) +
                "\n\n" +
                languages[self.lang]['pressure'] +
                str(self.weather.pressure['press']) +
                "\n\n" +
                sun_rise.strftime('%H:%M:%S') +
                languages[self.lang]['sun rise'] +
                "\n" +
                sun_set.strftime('%H:%M:%S') +
                languages[self.lang]['sun set'])

    def __str__(self):
        return "lat:" + str(self.latitude) + "&lon:" + str(self.longitude)
